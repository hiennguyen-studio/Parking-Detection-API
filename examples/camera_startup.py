"""
Parking Detection System - Camera Startup
Khởi động hệ thống phát hiện vi phạm đỗ xe
"""
import sys
import logging
from pathlib import Path

# Setup path
sys.path.insert(0, '.')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from src.camera import CameraManager, CameraHandler
from src.config.settings import settings

def startup_camera():
    """Khởi động camera và hệ thống phát hiện"""
    
    print("\n" + "="*60)
    print("🚗 HỆ THỐNG PHÁT HIỆN VÀ CẢNH BÁO ĐỖ XE TRÁI PHÉP")
    print("   Parking Violation Detection System")
    print("="*60 + "\n")
    
    # Test camera connection
    print("📹 Testing Camera Connection...")
    print("-" * 60)
    
    try:
        # Try to connect to default camera (0 = built-in webcam)
        test_camera = CameraHandler(0, "Test Camera")
        
        if test_camera.connect():
            print("✓ Camera connected successfully!")
            info = test_camera.get_info()
            print(f"  • Resolution: {info['frame_width']}x{info['frame_height']}")
            print(f"  • FPS: {info['fps']}")
            print(f"  • Status: Connected")
            
            # Try to get a frame
            frame_data = test_camera.get_frame()
            if frame_data:
                ret, frame = frame_data
                if ret:
                    print(f"  • Frame captured successfully")
                    # Save test frame
                    Path("./data/test").mkdir(parents=True, exist_ok=True)
                    test_camera.save_frame(frame, "./data/test/test_frame.jpg")
                    print(f"  • Test frame saved: ./data/test/test_frame.jpg")
            
            test_camera.disconnect()
        else:
            print("✗ Camera not found!")
            print("\nTroubleshooting:")
            print("  1. Check if camera is connected")
            print("  2. Try camera ID: 0 (built-in), 1, 2, etc.")
            print("  3. Or use RTSP URL for network camera")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nTips:")
        print("  • For RTSP streams: rtsp://192.168.1.100:554/stream")
        print("  • For USB cameras: 0, 1, 2 (webcam index)")
        return False
    
    # Initialize camera manager
    print("\n📋 Initializing Camera Manager...")
    print("-" * 60)
    
    manager = CameraManager()
    print("✓ Camera manager initialized")
    
    # Configure cameras
    print("\n🎥 Adding Cameras to System...")
    print("-" * 60)
    
    # Add default webcam
    if manager.add_camera("webcam", 0, "Built-in Camera"):
        print("✓ Added: webcam (Built-in Camera)")
    else:
        print("⚠ Could not add webcam")
    
    # Show available cameras
    cameras = manager.get_all_cameras()
    print(f"\n📊 Active Cameras: {len(cameras)}")
    for cam_id, info in cameras.items():
        print(f"  • {cam_id}: {info.get('name', 'Unknown')}")
        if info.get('is_connected'):
            print(f"    - Resolution: {info.get('frame_width')}x{info.get('frame_height')}")
            print(f"    - FPS: {info.get('fps')}")
    
    # Configuration summary
    print("\n⚙️  SYSTEM CONFIGURATION")
    print("-" * 60)
    print(f"Database: {settings.DATABASE_URL}")
    print(f"API: {settings.API_HOST}:{settings.API_PORT}")
    print(f"Telegram: {'Enabled' if settings.TELEGRAM_BOT_TOKEN else 'Disabled'}")
    print(f"AI Model: {settings.MODEL_NAME}")
    print(f"Confidence: {settings.CONFIDENCE_THRESHOLD*100:.0f}%")
    
    # Show next steps
    print("\n📝 NEXT STEPS")
    print("-" * 60)
    print("""
1. Test API Server:
   python -m uvicorn src.backend.main:app --reload
   
2. Open Dashboard:
   http://localhost:8000/dashboard
   
3. Test AI Detection:
   python -m pytest tests/test_integration.py -v
   
4. Start Full System:
   from src.parking_system import ParkingDetectionSystem
   system = ParkingDetectionSystem(detector_model="yolov8n.pt")
   system.add_camera("entrance", 0, "Parking Entrance")
   system.start(duration=300)  # Run for 5 minutes
""")
    
    print("\n✅ Camera System Ready!")
    print("="*60 + "\n")
    
    return True


def show_camera_options():
    """Hiển thị các tuỳ chọn camera"""
    print("\n📸 CAMERA OPTIONS")
    print("-" * 60)
    print("""
Choose camera source:

1. Built-in Webcam (ID 0):
   camera = CameraHandler(0, "Webcam")
   
2. USB Camera (ID 1, 2, 3...):
   camera = CameraHandler(1, "USB Camera")
   
3. RTSP Network Stream:
   camera = CameraHandler("rtsp://192.168.1.100:554/stream", "Network Camera")
   
4. RTSP Examples:
   - Hikvision: rtsp://user:pass@192.168.1.100/stream/ch1
   - Dahua: rtsp://user:pass@192.168.1.100/stream/profile2
   - Generic: rtsp://host:port/path/to/stream
""")


def create_startup_script():
    """Tạo script khởi động"""
    startup_content = '''#!/usr/bin/env python
"""Auto-startup script for parking detection system"""
import sys
sys.path.insert(0, '.')

from examples.camera_startup import startup_camera

if __name__ == "__main__":
    startup_camera()
    show_camera_options()
'''
    
    Path("start.py").write_text(startup_content)
    print("✓ Created: start.py")


if __name__ == "__main__":
    success = startup_camera()
    show_camera_options()
    
    if success:
        print("🎉 System ready to process!")
    else:
        print("❌ Camera not available")
        print("\nDo one of the following:")
        print("  1. Connect a camera/webcam")
        print("  2. Configure RTSP stream URL")
        print("  3. Use IP camera address")
