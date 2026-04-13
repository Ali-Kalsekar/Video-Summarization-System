"""
Video loading and reading utilities.
"""

import cv2
import os
from pathlib import Path


class VideoReader:
    """Handles video file loading and frame reading."""
    
    def __init__(self, video_path):
        """
        Initialize video reader.
        
        Args:
            video_path (str): Path to video file
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file is invalid
        """
        self.video_path = video_path
        self.cap = None  # Initialize early for safe cleanup
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        # Get video properties
        self._total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._fps = self.cap.get(cv2.CAP_PROP_FPS)
        self._width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._frame_index = 0
    
    @property
    def total_frames(self):
        """Get total number of frames."""
        return self._total_frames
    
    @property
    def fps(self):
        """Get frames per second."""
        return self._fps
    
    @property
    def width(self):
        """Get frame width."""
        return self._width
    
    @property
    def height(self):
        """Get frame height."""
        return self._height
    
    @property
    def frame_index(self):
        """Get current frame index."""
        return self._frame_index
    
    @property
    def duration_seconds(self):
        """Get video duration in seconds."""
        if self._fps > 0:
            return self._total_frames / self._fps
        return 0
    
    @property
    def resolution(self):
        """Get video resolution as tuple."""
        return (self._width, self._height)
    
    def read_frame(self):
        """
        Read next frame from video.
        
        Returns:
            tuple: (success, frame) where frame is numpy array or None
        """
        if not self.cap.isOpened():
            return False, None
        
        success, frame = self.cap.read()
        if success:
            self._frame_index += 1
        
        return success, frame
    
    def read_frame_at(self, frame_number):
        """
        Read specific frame from video.
        
        Args:
            frame_number (int): Frame number to read
            
        Returns:
            tuple: (success, frame)
        """
        if frame_number < 0 or frame_number >= self._total_frames:
            return False, None
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = self.cap.read()
        
        if success:
            self._frame_index = frame_number + 1
        
        return success, frame
    
    def read_frames_in_range(self, start_frame, end_frame):
        """
        Read frames in specified range.
        
        Args:
            start_frame (int): Starting frame number
            end_frame (int): Ending frame number
            
        Yields:
            tuple: (frame_number, frame)
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for frame_num in range(start_frame, end_frame):
            success, frame = self.cap.read()
            if success:
                self._frame_index = frame_num + 1
                yield frame_num, frame
            else:
                break
    
    def read_all_frames(self):
        """
        Read all frames from video.
        
        Yields:
            tuple: (frame_number, frame)
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_num = 0
        
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            
            self._frame_index = frame_num + 1
            yield frame_num, frame
            frame_num += 1
    
    def get_info_string(self):
        """Get formatted video information string."""
        info = (
            f"Video: {os.path.basename(self.video_path)}\n"
            f"Resolution: {self.width}x{self.height}\n"
            f"FPS: {self.fps:.2f}\n"
            f"Total Frames: {self.total_frames}\n"
            f"Duration: {self.duration_seconds:.2f} seconds"
        )
        return info
    
    def close(self):
        """Close video file."""
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
    
    def __del__(self):
        """Destructor to ensure video is closed."""
        self.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
