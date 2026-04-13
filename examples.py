"""
Example usage script demonstrating various features of the Video Summarization System.
"""

from video_loader import VideoReader
from scene_detection import SceneDetector
from keyframe_extraction import KeyframeSelector
from video_writer import SummaryWriter
from utils import logger, ProgressTracker
import cv2
import os


def example_basic_usage():
    """Basic usage example: load video, detect scenes, extract keyframes, generate summary."""
    print("\n" + "="*60)
    print("EXAMPLE 1: BASIC USAGE")
    print("="*60 + "\n")
    
    video_path = "input/sample_video.mp4"
    
    # Check if video exists
    if not os.path.exists(video_path):
        logger.warning(f"Video file not found: {video_path}")
        logger.info("Please place a video file in input/sample_video.mp4")
        return
    
    # Load video
    try:
        reader = VideoReader(video_path)
        print(reader.get_info_string())
    except Exception as e:
        print(f"Error loading video: {e}")
        return


def example_scene_detection():
    """Example: Perform scene detection with different methods."""
    print("\n" + "="*60)
    print("EXAMPLE 2: SCENE DETECTION METHODS")
    print("="*60 + "\n")
    
    # Create sample frames (for demonstration)
    print("Creating sample frames...")
    
    # You would normally load real frames from video
    # frames = load_frames_from_video()
    
    print("\nSupported Scene Detection Methods:")
    print("1. SSIM (Structural Similarity Index) - Most accurate")
    print("2. Histogram - Fast, color-based")
    print("3. Pixel Difference - Simple, direct comparison")
    print("4. Combined - Weighted combination of all methods")
    
    print("\nExample configuration:")
    print("""
    detector = SceneDetector(threshold=0.5, method='ssim')
    scene_indices = detector.detect_scenes(frames)
    stats = detector.get_scene_statistics()
    """)


def example_keyframe_extraction():
    """Example: Demonstrate keyframe extraction methods."""
    print("\n" + "="*60)
    print("EXAMPLE 3: KEYFRAME EXTRACTION METHODS")
    print("="*60 + "\n")
    
    print("Supported Keyframe Extraction Methods:")
    print("\n1. INTERVAL:")
    print("   - Extract every N frames")
    print("   - Usage: selector.select_keyframes_by_interval(frames)")
    
    print("\n2. SCENES:")
    print("   - Extract one keyframe per detected scene")
    print("   - Usage: selector.select_keyframes_from_scenes(frames, scene_indices)")
    
    print("\n3. ADAPTIVE:")
    print("   - Smart extraction based on frame similarity")
    print("   - Usage: selector.select_keyframes_adaptive(frames)")
    
    print("\n4. IMPORTANCE:")
    print("   - Score-based selection (content importance)")
    print("   - Usage: selector.select_keyframes_importance(frames, scene_indices)")


def example_configuration():
    """Show configuration examples."""
    print("\n" + "="*60)
    print("EXAMPLE 4: CONFIGURATION")
    print("="*60 + "\n")
    
    print("Common Configuration Patterns:")
    
    print("\n1. Fast Processing:")
    print("""
    scene_detection:
      method: histogram
      threshold: 0.3
    keyframe_extraction:
      method: interval
      interval: 50
    """)
    
    print("\n2. High Quality:")
    print("""
    scene_detection:
      method: ssim
      threshold: 0.7
    keyframe_extraction:
      method: adaptive
      similarity_threshold: 0.95
    """)
    
    print("\n3. Scene-Based Summarization:")
    print("""
    scene_detection:
      method: ssim
      threshold: 0.5
    keyframe_extraction:
      method: scenes
    """)


def example_custom_processing():
    """Example: Custom processing pipeline."""
    print("\n" + "="*60)
    print("EXAMPLE 5: CUSTOM PROCESSING")
    print("="*60 + "\n")
    
    print("Custom Pipeline Example:")
    print("""
from video_loader import VideoReader
from scene_detection import SceneDetector
from keyframe_extraction import KeyframeSelector

# Load video
reader = VideoReader('input/video.mp4')
frames = []
for idx, frame in reader.read_all_frames():
    frames.append(frame)

# Detect scenes
detector = SceneDetector(threshold=0.5, method='ssim')
scenes = detector.detect_scenes(frames)

# Extract keyframes
selector = KeyframeSelector()
keyframes = selector.select_keyframes_from_scenes(frames, scenes)

# Generate summary
writer = SummaryWriter('output/summary.mp4', fps=15)
writer.create_summary_video(keyframes, reader)
    """)


def example_advanced_features():
    """Example: Advanced features."""
    print("\n" + "="*60)
    print("EXAMPLE 6: ADVANCED FEATURES")
    print("="*60 + "\n")
    
    print("Advanced Features Available:")
    
    print("\n1. Duplicate Frame Filtering:")
    print("   selector.filter_duplicates(max_similarity=0.95)")
    
    print("\n2. Keyframe Statistics:")
    print("   stats = selector.get_statistics()")
    
    print("\n3. Save Individual Keyframes:")
    print("   writer.save_keyframes_as_images(keyframes, 'output/keyframes')")
    
    print("\n4. Create Thumbnail:")
    print("   writer.create_thumbnail(frame, 'output/thumbnail.jpg')")
    
    print("\n5. Interpolated Transitions:")
    print("""
    writer.create_summary_video(
        keyframe_indices,
        reader,
        interpolate=True
    )
    """)


def example_performance_tips():
    """Example: Performance optimization tips."""
    print("\n" + "="*60)
    print("EXAMPLE 7: PERFORMANCE OPTIMIZATION")
    print("="*60 + "\n")
    
    print("Speed vs Quality Trade-offs:")
    
    print("\n📊 For Speed (Large Videos):")
    print("   - Use histogram scene detection")
    print("   - Use interval keyframe selection")
    print("   - Reduce frame resolution (frame_resize_scale: 0.5)")
    print("   - Increase batch size")
    print("   - Example: 30-minute video → 5-10 seconds")
    
    print("\n⭐ For Quality (Important Content):")
    print("   - Use SSIM scene detection")
    print("   - Use adaptive/importance keyframe selection")
    print("   - Keep full resolution")
    print("   - Filter duplicates (max_similarity: 0.95)")
    print("   - Enable interpolation")
    print("   - Example: 5-minute video → 30-60 seconds")
    
    print("\n⚙️ Memory Optimization:")
    print("   - Process videos in batches")
    print("   - Use frame resizing for large videos")
    print("   - Monitor memory usage")
    print("   - Adjust batch_size based on available RAM")


def example_error_handling():
    """Example: Error handling."""
    print("\n" + "="*60)
    print("EXAMPLE 8: ERROR HANDLING")
    print("="*60 + "\n")
    
    print("Common Issues and Solutions:")
    
    print("\n❌ 'Video file not found'")
    print("   ✓ Ensure input_video path in config.yaml is correct")
    print("   ✓ Use absolute paths if relative paths don't work")
    
    print("\n❌ 'Cannot open video file'")
    print("   ✓ Install FFmpeg")
    print("   ✓ Verify video format is supported (.mp4, .avi, .mov)")
    print("   ✓ Check if video file is corrupt")
    
    print("\n❌ 'Out of memory'")
    print("   ✓ Reduce frame_resize_scale in config")
    print("   ✓ Lower batch_size")
    print("   ✓ Use interval method for keyframes")
    
    print("\n❌ 'No scenes detected'")
    print("   ✓ Lower scene_detection.threshold")
    print("   ✓ Video might not have scene changes")
    print("   ✓ Try different detection method")


def print_usage_guide():
    """Print complete usage guide."""
    print("\n" + "="*70)
    print(" "*15 + "VIDEO SUMMARIZATION SYSTEM - USAGE GUIDE")
    print("="*70 + "\n")
    
    print("QUICK START:")
    print("   1. Place video in input/sample_video.mp4")
    print("   2. Run: python main.py")
    print("   3. Find results in output/")
    
    print("\nCOMMAND LINE OPTIONS:")
    print("   python main.py                    # Default config")
    print("   python main.py -c config.yaml     # Custom config")
    print("   python main.py -i input.mp4       # Override input")
    print("   python main.py -m ssim -t 0.5     # Override method/threshold")
    
    print("\nCONFIGURATION:")
    print("   Edit config/config.yaml to customize:")
    print("   - Input/output paths")
    print("   - Scene detection method and threshold")
    print("   - Keyframe extraction method")
    print("   - Output video FPS")
    print("   - Processing options")
    
    print("\nOUTPUT:")
    print("   - output/summary_video.mp4        # Summarized video")
    print("   - output/keyframes/               # Individual keyframes")
    print("   - output/keyframes/thumbnail.jpg  # Preview thumbnail")
    
    print("\nSUPPORTED VIDEO FORMATS:")
    print("   .mp4, .avi, .mov, .mkv, .flv, .wmv, .webm, .3gp, .m4v")
    
    print("\nDOCUMENTATION:")
    print("   See README.md for comprehensive documentation")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" "*20 + "VIDEO SUMMARIZATION SYSTEM")
    print(" "*15 + "EXAMPLES AND DOCUMENTATION")
    print("="*70)
    
    examples = [
        ("Basic Usage", example_basic_usage),
        ("Scene Detection Methods", example_scene_detection),
        ("Keyframe Extraction Methods", example_keyframe_extraction),
        ("Configuration", example_configuration),
        ("Custom Processing", example_custom_processing),
        ("Advanced Features", example_advanced_features),
        ("Performance Optimization", example_performance_tips),
        ("Error Handling", example_error_handling),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print(f"  {len(examples) + 1}. Usage Guide")
    print(f"  0. Exit")
    
    while True:
        try:
            choice = input("\nSelect an example (0-{}): ".format(len(examples) + 1))
            choice = int(choice)
            
            if choice == 0:
                print("\nExiting...")
                break
            elif 1 <= choice <= len(examples):
                _, func = examples[choice - 1]
                func()
            elif choice == len(examples) + 1:
                print_usage_guide()
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break


if __name__ == '__main__':
    main()
