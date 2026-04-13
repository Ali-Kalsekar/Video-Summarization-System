"""
Logging utilities for video processing system.
"""

import logging
import sys
from datetime import datetime


class VideoLogger:
    """Logger for video processing operations."""
    
    def __init__(self, name="VideoSummarization"):
        """
        Initialize logger.
        
        Args:
            name (str): Logger name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def success(self, message):
        """Log success message."""
        self.logger.info(f"✓ {message}")
    
    def section(self, title):
        """Log section header."""
        padding = "=" * (60 - len(title) - 2)
        self.logger.info(f"\n{title} {padding}")


# Global logger instance
logger = VideoLogger()
