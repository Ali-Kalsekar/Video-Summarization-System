"""
Video writing and summarization module.
"""

import cv2
import os
import numpy as np
from pathlib import Path


class SummaryWriter:
    """Creates summarized videos from keyframes."""
    
    def __init__(self, output_path, fps=15, codec='mp4v'):
        """
        Initialize summary writer.
        
        Args:
            output_path (str): Path to output video file
            fps (int): Frames per second for output video
            codec (str): Video codec ('mp4v', 'XVID', 'MJPG')
        """
        self.output_path = output_path
        self.fps = fps
        self.codec = codec
        self.video_writer = None
        self.frame_width = None
        self.frame_height = None
        self.frame_count = 0
    
    def create_summary_video(self, keyframe_indices, video_reader, 
                           duration_per_frame=0.5, interpolate=False):
        """
        Create summarized video from keyframes.
        
        Args:
            keyframe_indices (list): Indices of keyframes to include
            video_reader: VideoReader object
            duration_per_frame (float): Duration to display each frame (seconds)
            interpolate (bool): Whether to interpolate between frames
            
        Returns:
            bool: Success status
        """
        try:
            # Create output directory if needed
            os.makedirs(os.path.dirname(self.output_path) or '.', exist_ok=True)
            
            # Read first keyframe to get dimensions
            success, first_frame = video_reader.read_frame_at(keyframe_indices[0])
            if not success:
                print("Error: Could not read first keyframe")
                return False
            
            self.frame_height, self.frame_width = first_frame.shape[:2]
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            self.video_writer = cv2.VideoWriter(
                self.output_path,
                fourcc,
                self.fps,
                (self.frame_width, self.frame_height)
            )
            
            if not self.video_writer.isOpened():
                print(f"Error: Could not open video writer for {self.output_path}")
                return False
            
            # Frames to write per keyframe
            frames_per_keyframe = int(self.fps * duration_per_frame)
            
            # Process each keyframe
            for i, frame_idx in enumerate(keyframe_indices):
                success, frame = video_reader.read_frame_at(frame_idx)
                
                if not success:
                    print(f"Warning: Could not read frame {frame_idx}")
                    continue
                
                # Ensure correct dimensions
                if frame.shape[:2] != (self.frame_height, self.frame_width):
                    frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                
                # Write keyframe multiple times for duration
                for _ in range(frames_per_keyframe):
                    self.video_writer.write(frame)
                    self.frame_count += 1
                
                # Interpolate between keyframes if requested
                if interpolate and i < len(keyframe_indices) - 1:
                    next_frame_idx = keyframe_indices[i + 1]
                    success, next_frame = video_reader.read_frame_at(next_frame_idx)
                    
                    if success:
                        if next_frame.shape[:2] != (self.frame_height, self.frame_width):
                            next_frame = cv2.resize(
                                next_frame,
                                (self.frame_width, self.frame_height)
                            )
                        
                        # Create transition frames
                        transition_frames = 10
                        for j in range(1, transition_frames):
                            alpha = j / transition_frames
                            blended = cv2.addWeighted(
                                frame, 1 - alpha,
                                next_frame, alpha,
                                0
                            )
                            self.video_writer.write(blended)
                            self.frame_count += 1
            
            self.video_writer.release()
            print(f"✓ Summary video created: {self.output_path}")
            print(f"  Frames written: {self.frame_count}")
            
            return True
        
        except Exception as e:
            print(f"Error creating summary video: {e}")
            if self.video_writer:
                self.video_writer.release()
            return False
    
    def create_video_from_frames(self, frames, frame_duration=0.5):
        """
        Create video from a list of frames.
        
        Args:
            frames (list): List of frames as numpy arrays
            frame_duration (float): Duration to display each frame (seconds)
            
        Returns:
            bool: Success status
        """
        try:
            if len(frames) == 0:
                print("Error: No frames provided")
                return False
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(self.output_path) or '.', exist_ok=True)
            
            # Get dimensions from first frame
            self.frame_height, self.frame_width = frames[0].shape[:2]
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            self.video_writer = cv2.VideoWriter(
                self.output_path,
                fourcc,
                self.fps,
                (self.frame_width, self.frame_height)
            )
            
            if not self.video_writer.isOpened():
                print(f"Error: Could not open video writer")
                return False
            
            # Frames to write per input frame
            frames_per_input = int(self.fps * frame_duration)
            
            # Write each frame
            for frame in frames:
                # Ensure correct dimensions
                if frame.shape[:2] != (self.frame_height, self.frame_width):
                    frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                
                # Write frame multiple times for duration
                for _ in range(frames_per_input):
                    self.video_writer.write(frame)
                    self.frame_count += 1
            
            self.video_writer.release()
            print(f"✓ Video created: {self.output_path}")
            print(f"  Frames written: {self.frame_count}")
            
            return True
        
        except Exception as e:
            print(f"Error creating video: {e}")
            if self.video_writer:
                self.video_writer.release()
            return False
    
    def save_keyframes_as_images(self, keyframe_frames, output_dir):
        """
        Save keyframes as individual images.
        
        Args:
            keyframe_frames (list): List of keyframes as numpy arrays
            output_dir (str): Output directory for images
            
        Returns:
            list: List of saved image paths
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            saved_paths = []
            
            for i, frame in enumerate(keyframe_frames):
                filename = f"keyframe_{i:04d}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                success = cv2.imwrite(filepath, frame)
                if success:
                    saved_paths.append(filepath)
                else:
                    print(f"Warning: Could not save {filename}")
            
            print(f"✓ Saved {len(saved_paths)} keyframes to {output_dir}")
            return saved_paths
        
        except Exception as e:
            print(f"Error saving keyframes: {e}")
            return []
    
    def create_thumbnail(self, frame, output_path, size=(320, 180)):
        """
        Create thumbnail from frame.
        
        Args:
            frame (np.ndarray): Input frame
            output_path (str): Path to save thumbnail
            size (tuple): Thumbnail size (width, height)
            
        Returns:
            bool: Success status
        """
        try:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            # Resize frame
            thumbnail = cv2.resize(frame, size)
            
            # Save thumbnail
            success = cv2.imwrite(output_path, thumbnail)
            return success
        
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
    
    def get_video_info(self):
        """
        Get information about created video.
        
        Returns:
            dict: Video information
        """
        return {
            'output_path': self.output_path,
            'fps': self.fps,
            'frame_width': self.frame_width,
            'frame_height': self.frame_height,
            'frame_count': self.frame_count,
            'duration_seconds': (self.frame_count / self.fps) if self.fps > 0 else 0,
            'codec': self.codec
        }
