"""
Scene change detection module.
"""

import cv2
import numpy as np
from scipy.spatial.distance import euclidean
from scipy import stats


class SceneDetector:
    """Detects scene changes and transitions in video."""
    
    def __init__(self, threshold=0.5, method='ssim'):
        """
        Initialize scene detector.
        
        Args:
            threshold (float): Detection threshold (0-1)
            method (str): Detection method ('ssim', 'histogram', 'pixeldiff', 'all')
        """
        self.threshold = threshold
        self.method = method
        self.scene_changes = []
        self.frame_differences = []
    
    def detect_scenes(self, frames):
        """
        Detect scene changes across frames.
        
        Args:
            frames (list): List of frames as numpy arrays
            
        Returns:
            list: Frame indices where scene changes occur
        """
        self.scene_changes = [0]  # First frame is always a scene change
        self.frame_differences = []
        
        if len(frames) < 2:
            return self.scene_changes
        
        # Preprocessing: resize frames for faster processing
        preprocessed = [self._preprocess_frame(f) for f in frames]
        
        # Calculate differences between consecutive frames
        for i in range(1, len(preprocessed)):
            if self.method == 'all':
                diff = self._calculate_combined_difference(
                    preprocessed[i-1], preprocessed[i]
                )
            elif self.method == 'histogram':
                diff = self._histogram_difference(
                    preprocessed[i-1], preprocessed[i]
                )
            elif self.method == 'pixeldiff':
                diff = self._pixel_difference(
                    preprocessed[i-1], preprocessed[i]
                )
            else:  # SSIM
                diff = self._ssim_difference(
                    preprocessed[i-1], preprocessed[i]
                )
            
            self.frame_differences.append(diff)
            
            # Scene change if difference exceeds threshold
            if diff > self.threshold:
                self.scene_changes.append(i)
        
        return self.scene_changes
    
    def _preprocess_frame(self, frame, scale=0.25):
        """
        Preprocess frame for faster comparison.
        
        Args:
            frame (np.ndarray): Input frame
            scale (float): Scaling factor
            
        Returns:
            np.ndarray: Preprocessed frame
        """
        # Resize for faster processing
        height, width = frame.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(frame, (new_width, new_height))
        
        # Convert to grayscale
        if len(resized.shape) == 3:
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        else:
            gray = resized
        
        return gray
    
    def _histogram_difference(self, frame1, frame2, bins=256):
        """
        Calculate histogram-based difference between frames.
        
        Args:
            frame1 (np.ndarray): First frame (grayscale)
            frame2 (np.ndarray): Second frame (grayscale)
            bins (int): Number of histogram bins
            
        Returns:
            float: Normalized difference (0-1)
        """
        hist1 = cv2.calcHist([frame1], [0], None, [bins], [0, 256])
        hist2 = cv2.calcHist([frame2], [0], None, [bins], [0, 256])
        
        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        # Calculate difference using Bhattacharyya distance
        diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        
        return min(diff, 1.0)
    
    def _pixel_difference(self, frame1, frame2):
        """
        Calculate pixel-level difference between frames.
        
        Args:
            frame1 (np.ndarray): First frame (grayscale)
            frame2 (np.ndarray): Second frame (grayscale)
            
        Returns:
            float: Normalized difference (0-1)
        """
        # Calculate absolute difference
        diff = cv2.absdiff(frame1, frame2)
        
        # Calculate mean absolute difference
        mean_diff = np.mean(diff)
        
        # Normalize to 0-1 range
        normalized_diff = mean_diff / 255.0
        
        return normalized_diff
    
    def _ssim_difference(self, frame1, frame2):
        """
        Calculate Structural Similarity Index (SSIM) difference.
        
        Args:
            frame1 (np.ndarray): First frame (grayscale)
            frame2 (np.ndarray): Second frame (grayscale)
            
        Returns:
            float: Difference (high = very different, low = similar)
        """
        # Ensure same size
        if frame1.shape != frame2.shape:
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
        
        # Calculate SSIM
        ssim = self._calculate_ssim(frame1, frame2)
        
        # Convert SSIM (-1 to 1) to difference (0 to 1)
        difference = (1.0 - ssim) / 2.0
        
        return max(0.0, min(1.0, difference))
    
    def _calculate_ssim(self, frame1, frame2):
        """
        Calculate SSIM between two frames.
        
        Args:
            frame1 (np.ndarray): First frame
            frame2 (np.ndarray): Second frame
            
        Returns:
            float: SSIM value (-1 to 1)
        """
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        
        frame1 = frame1.astype(np.float64)
        frame2 = frame2.astype(np.float64)
        
        # Mean
        mu1 = cv2.blur(frame1, (11, 11))
        mu2 = cv2.blur(frame2, (11, 11))
        
        # Variance
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        
        sigma1_sq = cv2.blur(frame1 ** 2, (11, 11)) - mu1_sq
        sigma2_sq = cv2.blur(frame2 ** 2, (11, 11)) - mu2_sq
        sigma12 = cv2.blur(frame1 * frame2, (11, 11)) - mu1_mu2
        
        # SSIM calculation
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / (
            (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
        )
        
        return np.mean(ssim_map)
    
    def _calculate_combined_difference(self, frame1, frame2):
        """
        Calculate combined difference using multiple methods.
        
        Args:
            frame1 (np.ndarray): First frame
            frame2 (np.ndarray): Second frame
            
        Returns:
            float: Combined normalized difference
        """
        hist_diff = self._histogram_difference(frame1, frame2)
        pixel_diff = self._pixel_difference(frame1, frame2)
        ssim_diff = self._ssim_difference(frame1, frame2)
        
        # Weighted average
        combined = (hist_diff * 0.3 + pixel_diff * 0.4 + ssim_diff * 0.3)
        
        return min(combined, 1.0)
    
    def get_scene_statistics(self):
        """
        Get statistics about detected scenes.
        
        Returns:
            dict: Scene statistics
        """
        if not self.scene_changes or len(self.scene_changes) < 2:
            return {
                'total_scenes': len(self.scene_changes),
                'scene_changes': len(self.scene_changes) - 1,
                'avg_scene_length': 0,
                'min_scene_length': 0,
                'max_scene_length': 0
            }
        
        scene_lengths = []
        for i in range(1, len(self.scene_changes)):
            length = self.scene_changes[i] - self.scene_changes[i-1]
            scene_lengths.append(length)
        
        return {
            'total_scenes': len(self.scene_changes),
            'scene_changes': len(self.scene_changes) - 1,
            'avg_scene_length': int(np.mean(scene_lengths)),
            'min_scene_length': int(np.min(scene_lengths)),
            'max_scene_length': int(np.max(scene_lengths))
        }
