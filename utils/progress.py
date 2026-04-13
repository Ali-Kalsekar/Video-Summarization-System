"""
Progress tracking and display utilities for video processing.
"""

import time
from datetime import timedelta


class ProgressTracker:
    """Tracks and displays progress with ETA calculation."""
    
    def __init__(self, total_frames, description="Processing"):
        """
        Initialize progress tracker.
        
        Args:
            total_frames (int): Total number of frames to process
            description (str): Description of the task
        """
        self.total_frames = total_frames
        self.description = description
        self.processed_frames = 0
        self.start_time = time.time()
        self.last_update = self.start_time
        
    def update(self, frames=1, force=False):
        """
        Update progress.
        
        Args:
            frames (int): Number of frames processed
            force (bool): Force display regardless of update interval
        """
        self.processed_frames += frames
        current_time = time.time()
        
        # Display every 1 second or when forced
        if force or (current_time - self.last_update) >= 1.0:
            self._display()
            self.last_update = current_time
    
    def _display(self):
        """Display current progress."""
        elapsed = time.time() - self.start_time
        progress_percent = (self.processed_frames / self.total_frames) * 100
        
        # Calculate ETA
        if self.processed_frames > 0:
            time_per_frame = elapsed / self.processed_frames
            remaining_frames = self.total_frames - self.processed_frames
            eta_seconds = time_per_frame * remaining_frames
            eta = timedelta(seconds=int(eta_seconds))
        else:
            eta = "N/A"
        
        # Create progress bar
        bar_length = 40
        filled = int(bar_length * self.processed_frames / self.total_frames)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(
            f"\r{self.description}: [{bar}] "
            f"{progress_percent:.1f}% ({self.processed_frames}/{self.total_frames}) "
            f"ETA: {eta}",
            end="", flush=True
        )
    
    def finish(self):
        """Mark progress as complete."""
        self.processed_frames = self.total_frames
        self._display()
        elapsed = time.time() - self.start_time
        print(
            f"\n✓ Completed in {timedelta(seconds=int(elapsed))}\n"
        )


class ProgressBar:
    """Simple percentage-based progress bar."""
    
    def __init__(self, max_value, label="Progress"):
        """
        Initialize progress bar.
        
        Args:
            max_value (int): Maximum value
            label (str): Progress label
        """
        self.max_value = max_value
        self.label = label
        self.current_value = 0
    
    def update(self, value):
        """Update progress bar."""
        self.current_value = value
        self._display()
    
    def _display(self):
        """Display progress bar."""
        if self.max_value == 0:
            percentage = 0
        else:
            percentage = (self.current_value / self.max_value) * 100
        
        bar_length = 50
        filled = int(bar_length * percentage / 100)
        bar = "#" * filled + "-" * (bar_length - filled)
        
        print(
            f"\r{self.label}: |{bar}| {percentage:.1f}%",
            end="", flush=True
        )
    
    def finish(self):
        """Mark as finished."""
        self.current_value = self.max_value
        self._display()
        print()
