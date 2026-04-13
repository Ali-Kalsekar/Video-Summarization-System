"""
Test script to verify the Video Summarization System installation and functionality.
"""

import sys
import os


def test_imports():
    """Test if all required modules can be imported."""
    print("\n" + "="*60)
    print("TEST 1: Checking Imports")
    print("="*60 + "\n")
    
    modules_to_test = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("yaml", "PyYAML"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib"),
    ]
    
    failed = []
    
    for module, name in modules_to_test:
        try:
            __import__(module)
            print(f"✓ {name:<20} installed")
        except ImportError:
            print(f"✗ {name:<20} NOT installed")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing modules: {', '.join(failed)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All external modules installed")
        return True


def test_local_modules():
    """Test if local modules can be imported."""
    print("\n" + "="*60)
    print("TEST 2: Checking Local Modules")
    print("="*60 + "\n")
    
    modules_to_test = [
        ("video_loader", "VideoReader"),
        ("scene_detection", "SceneDetector"),
        ("keyframe_extraction", "KeyframeSelector"),
        ("video_writer", "SummaryWriter"),
        ("utils", "ProgressTracker"),
        ("utils", "VideoLogger"),
        ("utils", "ProcessingMetrics"),
    ]
    
    failed = []
    
    for module, class_name in modules_to_test:
        try:
            mod = __import__(module)
            getattr(mod, class_name)
            print(f"✓ {module}.{class_name:<30} OK")
        except (ImportError, AttributeError) as e:
            print(f"✗ {module}.{class_name:<30} FAILED - {e}")
            failed.append(f"{module}.{class_name}")
    
    if failed:
        print(f"\n❌ Import errors: {', '.join(failed)}")
        return False
    else:
        print("\n✓ All local modules importable")
        return True


def test_folder_structure():
    """Test if required folders exist."""
    print("\n" + "="*60)
    print("TEST 3: Checking Folder Structure")
    print("="*60 + "\n")
    
    required_folders = [
        "video_loader",
        "scene_detection",
        "keyframe_extraction",
        "video_writer",
        "utils",
        "config",
        "input",
        "output",
    ]
    
    failed = []
    
    for folder in required_folders:
        if os.path.isdir(folder):
            print(f"✓ {folder:<30} exists")
        else:
            print(f"✗ {folder:<30} MISSING")
            failed.append(folder)
    
    if failed:
        print(f"\n⚠️  Missing folders: {', '.join(failed)}")
        print("   The system will create missing folders automatically.")
        return True  # Not a critical error
    else:
        print("\n✓ All required folders present")
        return True


def test_config_file():
    """Test if configuration file exists and is valid."""
    print("\n" + "="*60)
    print("TEST 4: Checking Configuration File")
    print("="*60 + "\n")
    
    config_path = "config/config.yaml"
    
    if not os.path.exists(config_path):
        print(f"✗ Configuration file not found: {config_path}")
        return False
    
    print(f"✓ Configuration file found: {config_path}")
    
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✓ Configuration file is valid YAML")
        
        # Check required keys
        required_keys = ['input_video', 'output_summary_video', 'scene_detection']
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"⚠️  Missing config keys: {', '.join(missing_keys)}")
        else:
            print(f"✓ All required configuration keys present")
        
        return True
    
    except Exception as e:
        print(f"✗ Error reading configuration: {e}")
        return False


def test_opencv_functionality():
    """Test OpenCV basic functionality."""
    print("\n" + "="*60)
    print("TEST 5: Testing OpenCV Functionality")
    print("="*60 + "\n")
    
    try:
        import cv2
        import numpy as np
        
        # Test frame creation and processing
        test_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        print("✓ Created test frame (480x640)")
        
        # Test color conversion
        gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
        print("✓ Color space conversion working")
        
        # Test histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        print("✓ Histogram calculation working")
        
        # Test resizing
        resized = cv2.resize(test_frame, (320, 240))
        print("✓ Frame resizing working")
        
        print("\n✓ OpenCV functionality OK")
        return True
    
    except Exception as e:
        print(f"✗ OpenCV test failed: {e}")
        return False


def test_system_instantiation():
    """Test if system components can be instantiated."""
    print("\n" + "="*60)
    print("TEST 6: Testing System Components")
    print("="*60 + "\n")
    
    try:
        from scene_detection import SceneDetector
        from keyframe_extraction import KeyframeSelector
        from video_writer import SummaryWriter
        from utils import ProgressTracker, VideoLogger, ProcessingMetrics
        
        # Test SceneDetector
        detector = SceneDetector(threshold=0.5)
        print("✓ SceneDetector instantiated")
        
        # Test KeyframeSelector
        selector = KeyframeSelector(interval=30)
        print("✓ KeyframeSelector instantiated")
        
        # Test SummaryWriter
        writer = SummaryWriter("test_output.mp4")
        print("✓ SummaryWriter instantiated")
        
        # Test utilities
        progress = ProgressTracker(100)
        print("✓ ProgressTracker instantiated")
        
        logger = VideoLogger()
        print("✓ VideoLogger instantiated")
        
        metrics = ProcessingMetrics()
        print("✓ ProcessingMetrics instantiated")
        
        print("\n✓ All components instantiated successfully")
        return True
    
    except Exception as e:
        print(f"✗ Component instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_output_permissions():
    """Test if we have write permissions to output directory."""
    print("\n" + "="*60)
    print("TEST 7: Checking Output Permissions")
    print("="*60 + "\n")
    
    try:
        test_file = "output/test_write.txt"
        
        os.makedirs("output", exist_ok=True)
        
        with open(test_file, 'w') as f:
            f.write("test")
        
        if os.path.exists(test_file):
            os.remove(test_file)
            print("✓ Write permissions to output/ OK")
            return True
        else:
            print("✗ Could not write to output directory")
            return False
    
    except Exception as e:
        print(f"✗ Permission test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print(" "*15 + "VIDEO SUMMARIZATION SYSTEM - INSTALLATION TEST")
    print("="*70)
    
    tests = [
        ("Imports", test_imports),
        ("Local Modules", test_local_modules),
        ("Folder Structure", test_folder_structure),
        ("Configuration File", test_config_file),
        ("OpenCV Functionality", test_opencv_functionality),
        ("System Components", test_system_instantiation),
        ("Output Permissions", test_output_permissions),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:<10} {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Place a video in input/sample_video.mp4")
        print("  2. Run: python main.py")
        print("  3. Results will be in output/")
        return True
    else:
        print("\n❌ Some tests failed. Please fix issues before proceeding.")
        print("\nFor help:")
        print("  1. Check README.md for troubleshooting")
        print("  2. Verify all dependencies are installed")
        print("  3. Ensure file permissions are correct")
        return False


def main():
    """Main entry point."""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)


if __name__ == '__main__':
    main()
