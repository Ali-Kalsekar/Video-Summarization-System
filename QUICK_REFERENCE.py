"""
Quick Reference Guide for Video Summarization System

This script provides quick reference commands and configurations.
"""


def print_quick_commands():
    """Print quick reference commands."""
    guide = """
╔══════════════════════════════════════════════════════════════════════════════╗
║          VIDEO SUMMARIZATION SYSTEM - QUICK REFERENCE GUIDE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

📖 QUICK START COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Basic Usage (uses default config)
   $ python main.py

2. Test Installation
   $ python test_installation.py

3. View Examples & Documentation
   $ python examples.py

4. Custom Input/Output
   $ python main.py -i input/my_video.mp4 -o output/my_summary.mp4

5. Change Scene Detection Mode
   $ python main.py -m histogram          # Fast
   $ python main.py -m ssim              # Accurate (slower)
   $ python main.py -m pixeldiff         # Simple

6. Adjust Sensitivity
   $ python main.py -t 0.3               # More sensitive
   $ python main.py -t 0.7               # Less sensitive


⚙️  CONFIGURATION EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAST PROCESSING (Large videos, quick results):
  scene_detection:
    method: histogram
    threshold: 0.3
  keyframe_extraction:
    method: interval
    interval: 50
  processing:
    frame_resize_scale: 0.5


HIGH QUALITY (Small/important videos, best results):
  scene_detection:
    method: ssim
    threshold: 0.7
  keyframe_extraction:
    method: adaptive
    similarity_threshold: 0.95
  summary_generation:
    interpolate: true


BALANCED (Good speed + quality):
  scene_detection:
    method: ssim
    threshold: 0.5
  keyframe_extraction:
    method: adaptive
  processing:
    frame_resize_scale: 0.75


📊 SCENE DETECTION METHODS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method          Speed    Accuracy    Use Case
─────────────────────────────────────────────────────────────────────────────
SSIM            Slow     Excellent   Production, important content
Histogram       Fast     Good        Quick prototyping, large videos
Pixeldiff       Very Fast Fair       Testing, simple scenes
Combined        Medium   Excellent   Best overall (slower)

Threshold Guidance:
  0.2-0.3 = Very sensitive (many scenes detected)
  0.5     = Balanced (default)
  0.7-0.8 = Less sensitive (fewer scenes detected)


🖼️  KEYFRAME EXTRACTION METHODS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method          Speed    Quality     Use Case
─────────────────────────────────────────────────────────────────────────────
Interval        Fastest  Fair        Regular sampling, quick results
Scenes          Fast     Good        Scene-based summaries
Adaptive        Medium   Excellent   Content-aware selection
Importance      Slow     Excellent   Quality-focused summaries


🚀 PERFORMANCE TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPEED OPTIMIZATION:
  ✓ frame_resize_scale: 0.25-0.5      (Reduce resolution)
  ✓ method: histogram                 (Fast detection)
  ✓ interval: 60-100                  (Fewer keyframes)
  ✓ use_threading: true               (Parallel processing)
  ✓ batch_size: 10-20                 (Smaller batches)

MEMORY OPTIMIZATION:
  ✓ frame_resize_scale: 0.5           (Reduce memory per frame)
  ✓ batch_size: 5-10                  (Process fewer frames at once)
  ✓ interval: 50+                     (Fewer total frames to hold)

QUALITY OPTIMIZATION:
  ✓ frame_resize_scale: 1.0           (Full resolution)
  ✓ method: ssim or all               (More accurate detection)
  ✓ similarity_threshold: 0.95+       (Keep more unique frames)
  ✓ interpolate: true                 (Smooth transitions)


🐛 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: "Cannot open video file"
  ✓ Install FFmpeg: pip install ffmpeg-python
  ✓ Verify video format (mp4, avi, mov, etc.)
  ✓ Check file path is correct
  ✓ Ensure video file is not corrupted

Problem: "No scenes detected"
  ✓ Lower threshold: -t 0.3 (or threshold: 0.3 in config)
  ✓ Try different method: -m histogram
  ✓ Video may legitimately have no scene cuts

Problem: "Out of memory"
  ✓ Reduce resolution: frame_resize_scale: 0.25
  ✓ Lower batch_size: 5 or 10
  ✓ Use interval method for keyframes
  ✓ Process video in smaller chunks

Problem: "Poor keyframe quality"
  ✓ Use similarity_threshold: 0.95 (keep more frames)
  ✓ Use importance method for selection
  ✓ Enable interpolation: interpolate: true
  ✓ Increase keyframe count: interval: 20

Problem: "Output video plays too fast/slow"
  ✓ Check duration_per_frame in summary_generation
  ✓ Verify output_fps setting
  ✓ Test video player compatibility


📁 FILE ORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

input/                      # Place videos here
  sample_video.mp4
  
output/                     # Results generated here
  summary_video.mp4         # Main output
  keyframes/                # Individual keyframe images
    keyframe_0000.jpg
    keyframe_0001.jpg
    ...
    thumbnail.jpg

config/
  config.yaml               # Main configuration file


📊 EXPECTED PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Video Length    Resolution    Typical Time    Compression
────────────────────────────────────────────────────────────────────────────
1 minute        1080p         2-5 seconds     10-20x
5 minutes       720p          5-15 seconds    8-15x
30 minutes      480p          20-40 seconds   6-12x

Times vary based on:
  - Scene complexity
  - Detection method used
  - Hardware specifications
  - Frame resolution


🎯 RECOMMENDED WORKFLOWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For LONG VIDEOS (>30 min):
  $ python main.py -m histogram -t 0.3
  Edit config: frame_resize_scale: 0.5

For IMPORTANT CONTENT:
  $ python main.py -m ssim -t 0.6
  Edit config: interpolate: true

For SOCIAL MEDIA:
  $ python main.py -m ssim
  Edit config: output_fps: 24, duration_per_frame: 0.3

For QUICK PREVIEW:
  $ python main.py -m histogram -t 0.4
  Edit config: interval: 100


🔧 PYTHON API USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from video_loader import VideoReader
from scene_detection import SceneDetector
from keyframe_extraction import KeyframeSelector
from video_writer import SummaryWriter

# Load video
reader = VideoReader('input/video.mp4')

# Load frames
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


📈 ADJUSTING SENSITIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Too many scenes detected?  → Increase threshold (0.6, 0.7, 0.8)
Too few scenes detected?   → Decrease threshold (0.3, 0.4, 0.5)
Poor keyframe selection?   → Adjust similarity_threshold (0.85, 0.90, 0.95)
Jittery output?            → Enable interpolation: true


═══════════════════════════════════════════════════════════════════════════════

For more information, see:
  - README.md for full documentation
  - examples.py for detailed examples
  - config/config.yaml for all configuration options

═══════════════════════════════════════════════════════════════════════════════
"""
    print(guide)


if __name__ == '__main__':
    print_quick_commands()
