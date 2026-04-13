"""
Video Summarization System - Main Entry Point

This is a complete production-ready video summarization system that:
- Loads video files
- Detects scene changes
- Extracts keyframes
- Generates summarized video
- Saves results and statistics
"""

import os
import sys
import yaml
import time
import argparse
from pathlib import Path

# Import custom modules
from video_loader import VideoReader
from scene_detection import SceneDetector
from keyframe_extraction import KeyframeSelector
from video_writer import SummaryWriter
from utils import logger, ProgressTracker, ProcessingMetrics


class VideoSummarizationSystem:
    """Main video summarization system coordinator."""
    
    def __init__(self, config_path='config/config.yaml'):
        """
        Initialize the video summarization system.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.metrics = ProcessingMetrics()
        self.video_reader = None
        self.frames = []
        self.scene_indices = []
        self.keyframe_indices = []
        self.keyframes = []
    
    def _load_config(self, config_path):
        """
        Load configuration from YAML file.
        
        Args:
            config_path (str): Path to config file
            
        Returns:
            dict: Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.success(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the complete video summarization pipeline."""
        self.metrics.start()
        
        try:
            logger.section("VIDEO SUMMARIZATION SYSTEM")
            
            # Step 1: Load video
            if not self._load_video():
                return False
            
            # Step 2: Detect scenes
            if not self._detect_scenes():
                return False
            
            # Step 3: Extract keyframes
            if not self._extract_keyframes():
                return False
            
            # Step 4: Generate summary video
            if not self._generate_summary():
                return False
            
            # Step 5: Save keyframes as images
            if not self._save_keyframes():
                return False
            
            # Step 6: Display statistics
            self._display_statistics()
            
            self.metrics.end()
            return True
        
        except Exception as e:
            logger.error(f"Error in summarization pipeline: {e}")
            return False
        finally:
            self._cleanup()
    
    def _load_video(self):
        """Load video file."""
        logger.section("STEP 1: LOADING VIDEO")
        
        video_path = self.config.get('input_video', 'input/sample_video.mp4')
        
        try:
            self.video_reader = VideoReader(video_path)
            logger.info(self.video_reader.get_info_string())
            
            self.metrics.total_frames = self.video_reader.total_frames
            
            # Load all frames
            logger.info("\nLoading frames...")
            progress = ProgressTracker(
                self.video_reader.total_frames,
                "Loading frames"
            )
            
            for frame_num, frame in self.video_reader.read_all_frames():
                self.frames.append(frame)
                progress.update()
            
            progress.finish()
            
            start_time = time.time()
            self.metrics.record_timing("video_loading", time.time() - start_time)
            
            return True
        
        except FileNotFoundError:
            logger.error(f"Video file not found: {video_path}")
            return False
        except Exception as e:
            logger.error(f"Error loading video: {e}")
            return False
    
    def _detect_scenes(self):
        """Detect scene changes."""
        logger.section("STEP 2: DETECTING SCENES")
        
        try:
            # Get scene detection config
            scene_config = self.config.get('scene_detection', {})
            method = scene_config.get('method', 'ssim')
            threshold = scene_config.get('threshold', 0.5)
            
            logger.info(f"Scene detection method: {method}")
            logger.info(f"Threshold: {threshold}")
            
            # Perform scene detection
            detector = SceneDetector(threshold=threshold, method=method)
            
            start_time = time.time()
            self.scene_indices = detector.detect_scenes(self.frames)
            detection_time = time.time() - start_time
            
            self.metrics.scene_changes_detected = len(self.scene_indices) - 1
            self.metrics.record_timing("scene_detection", detection_time)
            
            # Display statistics
            stats = detector.get_scene_statistics()
            logger.success(f"Scene detection completed")
            logger.info(f"Total scenes: {stats['total_scenes']}")
            logger.info(f"Scene changes: {stats['scene_changes']}")
            logger.info(f"Avg scene length: {stats['avg_scene_length']} frames")
            logger.info(f"Time taken: {detection_time:.2f}s")
            
            return True
        
        except Exception as e:
            logger.error(f"Error detecting scenes: {e}")
            return False
    
    def _extract_keyframes(self):
        """Extract keyframes."""
        logger.section("STEP 3: EXTRACTING KEYFRAMES")
        
        try:
            # Get keyframe extraction config
            kf_config = self.config.get('keyframe_extraction', {})
            method = kf_config.get('method', 'adaptive')
            
            logger.info(f"Keyframe extraction method: {method}")
            
            selector = KeyframeSelector(
                interval=kf_config.get('interval', 30),
                similarity_threshold=kf_config.get('similarity_threshold', 0.9)
            )
            
            start_time = time.time()
            
            # Select keyframes based on method
            if method == 'interval':
                self.keyframe_indices = selector.select_keyframes_by_interval(self.frames)
            elif method == 'scenes':
                self.keyframe_indices = selector.select_keyframes_from_scenes(
                    self.frames, self.scene_indices
                )
            elif method == 'adaptive':
                self.keyframe_indices = selector.select_keyframes_adaptive(self.frames)
            elif method == 'importance':
                self.keyframe_indices = selector.select_keyframes_importance(
                    self.frames, self.scene_indices
                )
            else:
                logger.warning(f"Unknown method {method}, using adaptive")
                self.keyframe_indices = selector.select_keyframes_adaptive(self.frames)
            
            # Filter duplicates
            self.keyframe_indices = selector.filter_duplicates()
            
            extraction_time = time.time() - start_time
            
            # Get keyframe frames
            self.keyframes = [self.frames[i] for i in self.keyframe_indices]
            
            self.metrics.keyframes_extracted = len(self.keyframes)
            self.metrics.record_timing("keyframe_extraction", extraction_time)
            
            # Display statistics
            stats = selector.get_statistics()
            logger.success(f"Keyframe extraction completed")
            logger.info(f"Keyframes extracted: {stats['total_keyframes']}")
            logger.info(f"Avg interval: {stats['avg_interval']} frames")
            logger.info(f"Time taken: {extraction_time:.2f}s")
            
            # Calculate compression ratio
            if len(self.frames) > 0 and len(self.keyframes) > 0:
                self.metrics.compression_ratio = len(self.frames) / len(self.keyframes)
                logger.info(f"Compression ratio: {self.metrics.compression_ratio:.2f}x")
            
            return True
        
        except Exception as e:
            logger.error(f"Error extracting keyframes: {e}")
            return False
    
    def _generate_summary(self):
        """Generate summarized video."""
        logger.section("STEP 4: GENERATING SUMMARY VIDEO")
        
        try:
            # Get summary generation config
            summary_config = self.config.get('summary_generation', {})
            output_path = self.config.get('output_summary_video', 'output/summary_video.mp4')
            fps = self.config.get('output_fps', 15)
            
            logger.info(f"Output path: {output_path}")
            logger.info(f"Output FPS: {fps}")
            logger.info(f"Duration per frame: {summary_config.get('duration_per_frame', 0.5)}s")
            
            writer = SummaryWriter(
                output_path=output_path,
                fps=fps,
                codec=summary_config.get('codec', 'mp4v')
            )
            
            start_time = time.time()
            
            success = writer.create_summary_video(
                self.keyframe_indices,
                self.video_reader,
                duration_per_frame=summary_config.get('duration_per_frame', 0.5),
                interpolate=summary_config.get('interpolate', False)
            )
            
            generation_time = time.time() - start_time
            
            if success:
                self.metrics.output_video_frames = writer.frame_count
                self.metrics.record_timing("summary_generation", generation_time)
                
                info = writer.get_video_info()
                logger.success(f"Summary video generated")
                logger.info(f"Output frames: {info['frame_count']}")
                logger.info(f"Duration: {info['duration_seconds']:.2f}s")
                logger.info(f"Time taken: {generation_time:.2f}s")
                
                return True
            else:
                return False
        
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return False
    
    def _save_keyframes(self):
        """Save keyframes as images."""
        logger.section("STEP 5: SAVING KEYFRAMES")
        
        try:
            output_dir = self.config.get('output_keyframes_dir', 'output/keyframes')
            
            logger.info(f"Saving keyframes to: {output_dir}")
            
            writer = SummaryWriter(output_dir)
            saved_paths = writer.save_keyframes_as_images(self.keyframes, output_dir)
            
            # Create thumbnail if configured
            advanced_config = self.config.get('advanced', {})
            if advanced_config.get('save_thumbnails', False) and len(self.keyframes) > 0:
                thumbnail_path = os.path.join(output_dir, 'thumbnail.jpg')
                thumbnail_size = tuple(advanced_config.get('thumbnail_size', [320, 180]))
                writer.create_thumbnail(self.keyframes[0], thumbnail_path, thumbnail_size)
                logger.success(f"Thumbnail saved: {thumbnail_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving keyframes: {e}")
            return False
    
    def _display_statistics(self):
        """Display processing statistics."""
        self.metrics.end()
        self.metrics.print_summary()
    
    def _cleanup(self):
        """Clean up resources."""
        if self.video_reader:
            self.video_reader.close()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Video Summarization System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Use default config
  python main.py -c config/custom_config.yaml      # Use custom config
  python main.py -i input/video.mp4 -o output/summary.mp4  # Override input/output
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config/config.yaml',
        help='Configuration file path'
    )
    parser.add_argument(
        '-i', '--input',
        help='Input video file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output summary video path'
    )
    parser.add_argument(
        '-m', '--method',
        choices=['ssim', 'histogram', 'pixeldiff', 'all'],
        help='Scene detection method'
    )
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        help='Scene detection threshold'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Create system instance
    system = VideoSummarizationSystem(config_path=args.config)
    
    # Override config with command line arguments if provided
    if args.input:
        system.config['input_video'] = args.input
    if args.output:
        system.config['output_summary_video'] = args.output
    if args.method:
        system.config['scene_detection']['method'] = args.method
    if args.threshold:
        system.config['scene_detection']['threshold'] = args.threshold
    
    # Run the system
    success = system.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
