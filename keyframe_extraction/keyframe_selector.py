"""
Keyframe extraction and selection module.
"""

import cv2
import numpy as np
from scipy.spatial.distance import cosine


class KeyframeSelector:
    """Selects representative keyframes from video."""
    
    def __init__(self, interval=30, similarity_threshold=0.9):
        """
        Initialize keyframe selector.
        
        Args:
            interval (int): Minimum frame interval between keyframes
            similarity_threshold (float): Similarity threshold for filtering (0-1)
        """
        self.interval = interval
        self.similarity_threshold = similarity_threshold
        self.keyframes = []
        self.keyframe_indices = []
    
    def select_keyframes_by_interval(self, frames):
        """
        Select keyframes at fixed intervals.
        
        Args:
            frames (list): List of frames as numpy arrays
            
        Returns:
            list: Selected keyframe indices
        """
        self.keyframe_indices = list(range(0, len(frames), self.interval))
        self.keyframes = [frames[i] for i in self.keyframe_indices]
        
        return self.keyframe_indices
    
    def select_keyframes_from_scenes(self, frames, scene_indices):
        """
        Select one keyframe from each scene.
        
        Args:
            frames (list): List of frames
            scene_indices (list): Scene change frame indices
            
        Returns:
            list: Selected keyframe indices
        """
        self.keyframe_indices = []
        self.keyframes = []
        
        for i in range(len(scene_indices)):
            if i < len(scene_indices) - 1:
                start = scene_indices[i]
                end = scene_indices[i + 1]
            else:
                start = scene_indices[i]
                end = len(frames)
            
            # Select frame in the middle of the scene
            mid_frame = (start + end) // 2
            
            if mid_frame < len(frames):
                self.keyframe_indices.append(mid_frame)
                self.keyframes.append(frames[mid_frame])
        
        return self.keyframe_indices
    
    def select_keyframes_adaptive(self, frames, similarity_threshold=None):
        """
        Select keyframes adaptively based on frame similarity.
        
        Args:
            frames (list): List of frames
            similarity_threshold (float): Override default threshold
            
        Returns:
            list: Selected keyframe indices
        """
        if similarity_threshold is None:
            similarity_threshold = self.similarity_threshold
        
        if len(frames) == 0:
            return []
        
        self.keyframe_indices = [0]  # Always include first frame
        self.keyframes = [frames[0]]
        
        # Preprocess frames to histograms for comparison
        histograms = [self._get_histogram(f) for f in frames]
        
        for i in range(1, len(frames)):
            # Check similarity with last selected keyframe
            last_keyframe_idx = self.keyframe_indices[-1]
            similarity = self._calculate_histogram_similarity(
                histograms[i],
                histograms[last_keyframe_idx]
            )
            
            # Select frame if sufficiently different
            if similarity < similarity_threshold:
                self.keyframe_indices.append(i)
                self.keyframes.append(frames[i])
        
        # Always include last frame
        if len(frames) > 1 and self.keyframe_indices[-1] != len(frames) - 1:
            self.keyframe_indices.append(len(frames) - 1)
            self.keyframes.append(frames[-1])
        
        return self.keyframe_indices
    
    def select_keyframes_importance(self, frames, scene_indices=None):
        """
        Select keyframes based on importance scoring.
        
        Args:
            frames (list): List of frames
            scene_indices (list): Optional scene indices
            
        Returns:
            list: Selected keyframe indices
        """
        if len(frames) < 2:
            return [0]
        
        # Calculate importance scores
        scores = self._calculate_frame_importance(frames, scene_indices)
        
        # Get frames with highest importance
        self.keyframe_indices = []
        self.keyframes = []
        
        # Always include first frame
        self.keyframe_indices.append(0)
        self.keyframes.append(frames[0])
        
        # Sort by importance and select high-scoring frames
        sorted_indices = np.argsort(scores)[::-1]
        
        for idx in sorted_indices:
            if idx == 0 or idx == len(frames) - 1:
                continue
            
            # Check minimum interval
            if all(abs(idx - k) >= self.interval // 2 for k in self.keyframe_indices):
                self.keyframe_indices.append(idx)
                self.keyframes.append(frames[idx])
                
                if len(self.keyframe_indices) >= max(3, len(frames) // self.interval):
                    break
        
        # Always include last frame
        if self.keyframe_indices[-1] != len(frames) - 1:
            self.keyframe_indices.append(len(frames) - 1)
            self.keyframes.append(frames[-1])
        
        # Sort by frame index
        sorted_pairs = sorted(
            zip(self.keyframe_indices, self.keyframes),
            key=lambda x: x[0]
        )
        self.keyframe_indices = [idx for idx, _ in sorted_pairs]
        self.keyframes = [frame for _, frame in sorted_pairs]
        
        return self.keyframe_indices
    
    def _calculate_frame_importance(self, frames, scene_indices=None):
        """
        Calculate importance score for each frame.
        
        Args:
            frames (list): List of frames
            scene_indices (list): Optional scene indices
            
        Returns:
            np.ndarray: Importance scores
        """
        scores = np.zeros(len(frames))
        
        # Scene boundary frames are more important
        if scene_indices:
            for idx in scene_indices:
                if idx < len(scores):
                    scores[idx] += 2.0
        
        # Frames with high content variation
        histograms = [self._get_histogram(f) for f in frames]
        
        for i in range(1, len(frames) - 1):
            # Calculate variance from neighbors
            sim_prev = self._calculate_histogram_similarity(
                histograms[i], histograms[i-1]
            )
            sim_next = self._calculate_histogram_similarity(
                histograms[i], histograms[i+1]
            )
            
            variation = 2.0 - (sim_prev + sim_next)  # High variation = low similarity
            scores[i] += max(0, variation)
        
        return scores
    
    def _get_histogram(self, frame):
        """
        Get histogram of frame.
        
        Args:
            frame (np.ndarray): Input frame
            
        Returns:
            np.ndarray: Histogram
        """
        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        return hist
    
    def _calculate_histogram_similarity(self, hist1, hist2):
        """
        Calculate similarity between histograms.
        
        Args:
            hist1 (np.ndarray): First histogram
            hist2 (np.ndarray): Second histogram
            
        Returns:
            float: Similarity (0-1, higher = more similar)
        """
        # Using cosine similarity
        if len(hist1) == 0 or len(hist2) == 0:
            return 0.0
        
        try:
            similarity = 1.0 - cosine(hist1, hist2)
        except:
            similarity = 0.0
        
        return max(0.0, min(1.0, similarity))
    
    def filter_duplicates(self, max_similarity=0.95):
        """
        Filter out duplicate frames from keyframes.
        
        Args:
            max_similarity (float): Maximum allowed similarity
            
        Returns:
            list: Filtered keyframe indices
        """
        if len(self.keyframes) < 2:
            return self.keyframe_indices
        
        original_keyframes = self.keyframes
        original_indices = self.keyframe_indices
        histograms = [self._get_histogram(f) for f in self.keyframes]
        
        kept_positions = [0]
        filtered_indices = [original_indices[0]]
        filtered_histograms = [histograms[0]]
        
        for i in range(1, len(original_keyframes)):
            # Check similarity with all kept keyframes
            is_duplicate = False
            
            for hist in filtered_histograms:
                similarity = self._calculate_histogram_similarity(
                    histograms[i], hist
                )
                
                if similarity > max_similarity:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                kept_positions.append(i)
                filtered_indices.append(original_indices[i])
                filtered_histograms.append(histograms[i])
        
        self.keyframe_indices = filtered_indices
        self.keyframes = [original_keyframes[i] for i in kept_positions]
        
        return self.keyframe_indices
    
    def get_statistics(self):
        """
        Get keyframe selection statistics.
        
        Returns:
            dict: Statistics
        """
        return {
            'total_keyframes': len(self.keyframe_indices),
            'keyframe_indices': self.keyframe_indices.copy(),
            'avg_interval': int(
                np.mean(np.diff(self.keyframe_indices))
            ) if len(self.keyframe_indices) > 1 else 0
        }
