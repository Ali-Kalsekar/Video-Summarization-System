"""
Metrics and statistics tracking for video processing.
"""

import time
from datetime import timedelta
import json


class ProcessingMetrics:
    """Tracks processing metrics and statistics."""
    
    def __init__(self):
        """Initialize metrics tracker."""
        self.start_time = None
        self.end_time = None
        self.total_frames = 0
        self.scene_changes_detected = 0
        self.keyframes_extracted = 0
        self.output_video_frames = 0
        self.compression_ratio = 0
        self.peak_memory_mb = 0
        self.timings = {}
        self.frame_sizes = []
    
    def start(self):
        """Mark processing start time."""
        self.start_time = time.time()
    
    def end(self):
        """Mark processing end time."""
        self.end_time = time.time()
    
    def record_timing(self, operation, duration):
        """
        Record operation timing.
        
        Args:
            operation (str): Operation name
            duration (float): Duration in seconds
        """
        self.timings[operation] = duration
    
    def record_frame_size(self, size_bytes):
        """Record frame size."""
        self.frame_sizes.append(size_bytes)
    
    def get_total_duration(self):
        """Get total processing duration."""
        if self.start_time and self.end_time:
            return timedelta(seconds=int(self.end_time - self.start_time))
        return timedelta(0)
    
    def get_summary(self):
        """Get metrics summary."""
        duration = self.get_total_duration()
        
        summary = {
            "total_frames": self.total_frames,
            "scene_changes": self.scene_changes_detected,
            "keyframes_extracted": self.keyframes_extracted,
            "output_video_frames": self.output_video_frames,
            "compression_ratio": f"{self.compression_ratio:.2f}x",
            "total_processing_time": str(duration),
            "fps_processed": round(self.total_frames / max((self.end_time - self.start_time), 0.001), 2)
                if self.start_time and self.end_time else 0,
            "timings": {k: f"{v:.2f}s" for k, v in self.timings.items()}
        }
        
        return summary
    
    def print_summary(self):
        """Print formatted metrics summary."""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("PROCESSING STATISTICS")
        print("=" * 60)
        print(f"Total Frames Processed: {summary['total_frames']}")
        print(f"Scene Changes Detected: {summary['scene_changes']}")
        print(f"Keyframes Extracted: {summary['keyframes_extracted']}")
        print(f"Output Video Frames: {summary['output_video_frames']}")
        print(f"Compression Ratio: {summary['compression_ratio']}")
        print(f"Total Processing Time: {summary['total_processing_time']}")
        print(f"Average FPS: {summary['fps_processed']}")
        
        if summary['timings']:
            print("\nTiming Breakdown:")
            for operation, time_str in summary['timings'].items():
                print(f"  {operation}: {time_str}")
        
        print("=" * 60 + "\n")
    
    def to_json(self):
        """Convert metrics to JSON."""
        return json.dumps(self.get_summary(), indent=2)


class MemoryTracker:
    """Tracks memory usage."""
    
    def __init__(self):
        """Initialize memory tracker."""
        self.peak_memory = 0
        self.memory_samples = []
    
    def record_sample(self, memory_mb):
        """Record memory sample."""
        self.memory_samples.append(memory_mb)
        if memory_mb > self.peak_memory:
            self.peak_memory = memory_mb
    
    def get_peak_memory(self):
        """Get peak memory usage in MB."""
        return self.peak_memory
    
    def get_average_memory(self):
        """Get average memory usage in MB."""
        if not self.memory_samples:
            return 0
        return sum(self.memory_samples) / len(self.memory_samples)
