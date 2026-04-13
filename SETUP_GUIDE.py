"""
INSTALLATION AND SETUP GUIDE

Step-by-step guide to set up and run the Video Summarization System
"""


def print_setup_guide():
    """Print complete setup guide."""
    guide = """

╔══════════════════════════════════════════════════════════════════════════════╗
║     VIDEO SUMMARIZATION SYSTEM - INSTALLATION & SETUP GUIDE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝


SYSTEM REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

Hardware Minimum:
  • CPU: Intel i5 / AMD Ryzen 5 (or equivalent)
  • RAM: 4 GB (8 GB recommended for large videos)
  • Storage: 1 GB free space for videos
  • GPU: Optional (system works on CPU)

Software Requirements:
  • Python 3.7 or higher
  • pip (Python package manager)
  • FFmpeg (for video codec support)


STEP 1: INSTALL PYTHON & PIP
═══════════════════════════════════════════════════════════════════════════════

Windows:
  1. Download from https://www.python.org/downloads/
  2. Install with "Add Python to PATH" checked
  3. Verify: python --version

Mac:
  1. brew install python3
  2. Verify: python3 --version

Linux:
  1. sudo apt-get install python3 python3-pip
  2. Verify: python3 --version


STEP 2: INSTALL FFMPEG (Required for video codec support)
═══════════════════════════════════════════════════════════════════════════════

Windows:
  1. Download from https://ffmpeg.org/download.html
  2. Extract to folder (e.g., C:\\ffmpeg)
  3. Add to PATH environment variable
  4. Verify: ffmpeg -version

Mac:
  1. brew install ffmpeg
  2. Verify: ffmpeg -version

Linux:
  1. sudo apt-get install ffmpeg
  2. Verify: ffmpeg -version


STEP 3: INSTALL PROJECT DEPENDENCIES
═══════════════════════════════════════════════════════════════════════════════

Navigate to project directory:
  $ cd video_summarization_system

Install dependencies:
  $ pip install -r requirements.txt

This will install:
  ✓ opencv-python (4.8.1.78)
  ✓ numpy (1.24.3)
  ✓ scipy (1.11.2)
  ✓ matplotlib (3.7.2)
  ✓ ffmpeg-python (0.2.1)
  ✓ pyyaml (6.0)
  ✓ pandas (2.0.3)

Installation should take 2-5 minutes depending on internet speed.


STEP 4: VERIFY INSTALLATION
═══════════════════════════════════════════════════════════════════════════════

Run the test script:
  $ python test_installation.py

This will check:
  ✓ All Python modules are installed
  ✓ Local modules are importable
  ✓ Folder structure is correct
  ✓ Configuration file is valid
  ✓ OpenCV functionality works
  ✓ System components are functional
  ✓ Output permissions are correct

Expected output:
  TEST SUMMARY
  ✓ PASS  Imports
  ✓ PASS  Local Modules
  ✓ PASS  Folder Structure
  ✓ PASS  Configuration File
  ✓ PASS  OpenCV Functionality
  ✓ PASS  System Components
  ✓ PASS  Output Permissions
  
  7/7 tests passed! System is ready to use.


STEP 5: PREPARE INPUT VIDEO
═══════════════════════════════════════════════════════════════════════════════

1. Place your video file in the input/ directory:
   input/sample_video.mp4

2. Supported formats:
   ✓ MP4 (.mp4)
   ✓ AVI (.avi)
   ✓ MOV (.mov)
   ✓ MKV (.mkv)
   ✓ FLV (.flv)
   ✓ WMV (.wmv)
   ✓ WebM (.webm)
   ✓ 3GP (.3gp)
   ✓ M4V (.m4v)

3. For testing with a sample video:
   - Use a short video (1-5 minutes) first
   - This lets you test the system quickly


STEP 6: CONFIGURE (Optional)
═══════════════════════════════════════════════════════════════════════════════

Edit config/config.yaml to customize:

Basic settings:
  input_video: input/sample_video.mp4
  output_summary_video: output/summary_video.mp4
  output_fps: 15

Scene detection:
  - method: ssim (accurate) or histogram (fast)
  - threshold: 0.5 (0-1, lower = more sensitive)

Keyframe extraction:
  - method: adaptive, interval, scenes, importance
  - similarity_threshold: 0.9

For first run, use defaults (no changes needed!)


STEP 7: RUN THE SYSTEM
═══════════════════════════════════════════════════════════════════════════════

Basic usage (uses default configuration):
  $ python main.py

Output should show:
  ✓ Configuration loaded
  ✓ STEP 1: LOADING VIDEO
  ✓ STEP 2: DETECTING SCENES
  ✓ STEP 3: EXTRACTING KEYFRAMES
  ✓ STEP 4: GENERATING SUMMARY VIDEO
  ✓ STEP 5: SAVING KEYFRAMES
  ✓ Processing Statistics

Processing time depends on video length and your computer.


STEP 8: CHECK RESULTS
═══════════════════════════════════════════════════════════════════════════════

After processing completes, check:

1. Summary video:
   output/summary_video.mp4
   - Compressed version of original video
   - Much shorter than original

2. Keyframe images:
   output/keyframes/keyframe_0000.jpg
   output/keyframes/keyframe_0001.jpg
   ...
   - Individual representative frames
   - Can be used for thumbnails/previews

3. Thumbnail preview:
   output/keyframes/thumbnail.jpg
   - Quick visual preview of the video


TROUBLESHOOTING INSTALLATION
═══════════════════════════════════════════════════════════════════════════════

Problem: "python: command not found"
  ✓ Python not installed or not in PATH
  ✓ Try: python3 main.py (Mac/Linux)
  ✓ Reinstall Python with PATH checked

Problem: "ModuleNotFoundError: No module named 'cv2'"
  ✓ Dependencies not installed
  ✓ Run: pip install -r requirements.txt
  ✓ Or: pip install opencv-python

Problem: "ffmpeg not found or not in PATH"
  ✓ FFmpeg not installed or not in PATH
  ✓ Install FFmpeg (see Step 2)
  ✓ Add FFmpeg bin folder to PATH

Problem: "Permission denied" on output/
  ✓ Insufficient write permissions
  ✓ Run as administrator / with sudo
  ✓ Check folder permissions

Problem: Tests pass but main.py fails
  ✓ Try with a different video file
  ✓ Check video file is not corrupted
  ✓ Try a simpler video format (MP4)


FIRST TIME USE TIPS
═══════════════════════════════════════════════════════════════════════════════

✓ Start with a SHORT video (1-3 minutes)
  - Faster processing for testing
  - Identify any issues quickly

✓ Use DEFAULT configuration first
  - No changes needed initially
  - Adjust after understanding output

✓ View the README.md
  - Complete documentation
  - Configuration details
  - Advanced features

✓ Check QUICK_REFERENCE.py
  - Quick tips and tricks
  - Common use cases
  - Performance optimization

✓ View examples.py
  - Usage examples
  - Different configurations
  - Advanced techniques


PERFORMANCE EXPECTATIONS
═══════════════════════════════════════════════════════════════════════════════

Video Length    First Run Time    Typical Size Reduction
────────────────────────────────────────────────────────────
30 seconds      5-10 seconds      5-15x smaller
1 minute        10-20 seconds     8-20x smaller
5 minutes       30-60 seconds     10-25x smaller
30 minutes      2-5 minutes       15-30x smaller

Factors affecting speed:
  - Video resolution (higher = slower)
  - Scene complexity (complex = slower)
  - Computer specifications
  - Selected detection method
  - Frame resize settings


NEXT STEPS
═══════════════════════════════════════════════════════════════════════════════

1. Process several test videos
2. Adjust configuration for your use case:
   - SPEED: Lower resolution, simpler methods
   - QUALITY: Keep resolution, complex methods
3. Integrate into your workflow
4. Read README.md for advanced features


COMMON CONFIGURATIONS
═══════════════════════════════════════════════════════════════════════════════

For SPEED (process quickly):
  └─ Edit config/config.yaml:
     scene_detection:
       method: histogram
       threshold: 0.3
     processing:
       frame_resize_scale: 0.5

For QUALITY (best results):
  └─ Edit config/config.yaml:
     scene_detection:
       method: ssim
       threshold: 0.6
     keyframe_extraction:
       similarity_threshold: 0.95

For BALANCED (good speed + quality):
  └─ Keep defaults (no changes needed!)


GETTING HELP
═══════════════════════════════════════════════════════════════════════════════

1. Run test suite:
   $ python test_installation.py

2. View documentation:
   $ cat README.md

3. Check quick reference:
   $ python QUICK_REFERENCE.py

4. View examples:
   $ python examples.py

5. Check config file:
   $ cat config/config.yaml


WHAT TO DO AFTER SETUP
═══════════════════════════════════════════════════════════════════════════════

✓ Process your first video:
  $ python main.py

✓ Try different configurations:
  $ python main.py -m ssim -t 0.5

✓ Use custom input/output:
  $ python main.py -i input/video.mp4 -o output/summary.mp4

✓ Explore advanced features:
  - Edit config.yaml
  - Try different keyframe methods
  - Enable interpolation
  - Adjust output FPS


═══════════════════════════════════════════════════════════════════════════════
✓ Installation Complete! You're ready to summarize videos!
═══════════════════════════════════════════════════════════════════════════════

Commands to remember:
  $ python main.py              # Run system
  $ python test_installation.py # Verify setup
  $ python examples.py          # View examples
  $ python QUICK_REFERENCE.py   # Quick tips

For full documentation:
  See README.md in project directory
"""
    print(guide)


if __name__ == '__main__':
    print_setup_guide()
