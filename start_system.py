<<<<<<< HEAD
"""
Full Parking Detection System Startup
Khởi động hệ thống đầy đủ với camera, AI, Telegram
"""
import sys
import logging
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '.')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from src.parking_system import ParkingDetectionSystem
from src.config.settings import settings


def print_banner():
    """Print system banner"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  🚗 HỆ THỐNG PHÁT HIỆN VÀ CẢNH BÁO ĐỖ XE TRÁI PHÉP           ║
║     Illegal Parking Detection & Alert System v1.0             ║
║                                                                ║
║  📹 Real-time Camera Monitoring                               ║
║  🤖 AI/ML Vehicle Detection (YOLOv8)                          ║
║  💬 Telegram Bot Notifications                                ║
║  📊 Web Dashboard & API                                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_config():
    """Print system configuration"""
    print("\n⚙️  SYSTEM CONFIGURATION")
    print("=" * 60)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗄️  Database: {settings.DATABASE_URL}")
    print(f"🌐 API: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📹 Evidence Path: {settings.EVIDENCE_PATH}")
    print(f"🤖 AI Model: {settings.MODEL_NAME}")
    print(f"📊 Confidence Threshold: {settings.CONFIDENCE_THRESHOLD*100:.0f}%")
    print(f"💬 Telegram: {'✓ Enabled' if settings.TELEGRAM_BOT_TOKEN else '✗ Disabled'}")
    print("=" * 60 + "\n")


def initialize_system(detector_model: str = None):
    """
    Initialize parking detection system
    
    Args:
        detector_model: Path to AI detector model
    """
    print("\n🔧 INITIALIZING SYSTEM...")
    print("-" * 60)
    
    try:
        # Create necessary directories
        Path(settings.EVIDENCE_PATH).mkdir(parents=True, exist_ok=True)
        Path(settings.MODEL_PATH).mkdir(parents=True, exist_ok=True)
        Path("./logs").mkdir(parents=True, exist_ok=True)
        print("✓ Directories created")
        
        # Initialize system
        system = ParkingDetectionSystem(
            detector_model=detector_model,
            enable_telegram=True
        )
        print("✓ System initialized")
        
        return system
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        return None


def setup_cameras(system):
    """
    Setup cameras for the system
    
    Args:
        system: ParkingDetectionSystem instance
    """
    print("\n📹 SETTING UP CAMERAS")
    print("-" * 60)
    
    # Configure cameras
    camera_configs = [
        {
            "id": "entrance",
            "source": 0,
            "name": "Parking Entrance"
        },
        # Uncomment to add more cameras:
        # {
        #     "id": "exit",
        #     "source": "rtsp://192.168.1.100:554/stream",
        #     "name": "Exit Gate"
        # },
        # {
        #     "id": "side",
        #     "source": 1,
        #     "name": "Side View"
        # }
    ]
    
    connected = system.connect_to_all_cameras(camera_configs)
    print(f"✓ Connected to {connected}/{len(camera_configs)} cameras")
    
    if connected == 0:
        print("\n⚠️  WARNING: No cameras connected!")
        print("To add cameras, modify the camera_configs list:")
        print("  - Webcam: 0")
        print("  - RTSP: 'rtsp://192.168.1.100:554/stream'")
        return False
    
    return True


def print_statistics(stats):
    """Print system statistics"""
    print("\n📊 SYSTEM STATISTICS")
    print("-" * 60)
    print(f"Total Violations Detected: {stats['total_violations']}")
    print(f"Active Cameras: {stats['active_cameras']}")
    print(f"System Running: {'✓ Yes' if stats['running'] else '✗ No'}")
    print(f"Detector Loaded: {'✓ Yes' if stats['detector_loaded'] else '✗ No'}")
    print(f"Telegram Connected: {'✓ Yes' if stats['telegram_connected'] else '✗ No'}")
    
    if stats.get('cameras'):
        print("\nCamera Details:")
        for cam_id, cam_stats in stats['cameras'].items():
            print(f"  • {cam_id}:")
            print(f"    - Total Frames: {cam_stats.get('total_frames', 0)}")
            print(f"    - Processed: {cam_stats.get('processed_frames', 0)}")
            print(f"    - Violations: {cam_stats.get('violations_found', 0)}")


def print_menu():
    """Print control menu"""
    print("\n🎮 SYSTEM CONTROLS")
    print("-" * 60)
    print("Commands:")
    print("  P - Pause detection")
    print("  R - Resume detection")
    print("  S - Show statistics")
    print("  Q - Quit system")
    print("-" * 60)


def run_system(system, duration: int = None):
    """
    Run the parking detection system
    
    Args:
        system: ParkingDetectionSystem instance
        duration: Runtime duration in seconds (None = indefinite)
    """
    print("\n🚀 STARTING SYSTEM")
    print("-" * 60)
    
    # Send startup alert
    if system.telegram:
        system.send_status_report()
    
    print("✓ System started")
    print("Press Ctrl+C to stop")
    print("\n" + "=" * 60)
    
    try:
        # Run detection
        stats = system.start(duration=duration)
        
        print("\n" + "=" * 60)
        print_statistics(stats)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  STOPPING SYSTEM")
        print("-" * 60)
        stats = system.stop()
        print_statistics(stats)
    
    except Exception as e:
        logger.error(f"System error: {e}")
        system.stop()


def print_next_steps():
    """Print next steps and tips"""
    print("\n📝 NEXT STEPS & TIPS")
    print("=" * 60)
    print("""
1. MONITORING:
   • Open web dashboard: http://localhost:8000
   • Check logs: ./logs/system.log
   • Monitor statistics in real-time

2. ADDING MORE CAMERAS:
   Edit this script and add to camera_configs:
   {
       "id": "camera_name",
       "source": "rtsp://camera_url",
       "name": "Display Name"
   }

3. TELEGRAM SETUP:
   • Set TELEGRAM_BOT_TOKEN in .env
   • Set TELEGRAM_CHAT_ID in .env
   • Test with: system.send_status_report()

4. CUSTOMIZATION:
   • Adjust CONFIDENCE_THRESHOLD in .env (0.0-1.0)
   • Modify NMS_THRESHOLD for detection filtering
   • Change violation callback in parking_system.py

5. DATABASE:
   • Check violations: SELECT * FROM violation;
   • View cameras: SELECT * FROM camera;
   • Analyze statistics: analytics queries

6. PERFORMANCE:
   • Process every N-th frame: processor.frame_skip = 10
   • Resize frames: camera.get_frame_resized(640, 480)
   • Use multiple threads for multiple cameras

7. API ENDPOINTS:
   • List violations: GET /api/v1/violations
   • Get statistics: GET /api/v1/statistics/summary
   • Create violation: POST /api/v1/violations
   • Docs: http://localhost:8000/docs

8. TROUBLESHOOTING:
   • Camera not found: Check device permissions
   • Telegram not sending: Verify token and chat_id
   • High CPU usage: Increase frame skip or reduce resolution
   • Database locked: Restart system

For more info, see docs/:
  • CAMERA_MODULE.md
  • API.md
  • ARCHITECTURE.md
  • SETUP.md
""")
    print("=" * 60)


def main():
    """Main system startup"""
    print_banner()
    
    # Configuration
    print_config()
    
    # Initialize
    system = initialize_system(detector_model=None)  # Set to "yolov8n.pt" when ready
    if system is None:
        print("❌ Failed to initialize system")
        return
    
    # Setup cameras
    if not setup_cameras(system):
        print("❌ Failed to setup cameras")
        system.stop()
        return
    
    # Show menu
    print_menu()
    
    # Run system
    run_system(system, duration=None)  # None = run indefinitely
    
    # Cleanup
    print("\n🧹 CLEANING UP")
    print("-" * 60)
    system.camera_manager.disconnect_all()
    print("✓ Cleanup complete")
    
    # Show next steps
    print_next_steps()
    
    print("\n✅ System stopped successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal Error: {e}")
        print("Check ./logs/system.log for details")
=======
"""
Full Parking Detection System Startup
Khởi động hệ thống đầy đủ với camera, AI, Telegram
"""
import sys
import logging
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '.')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from src.parking_system import ParkingDetectionSystem
from src.config.settings import settings


def print_banner():
    """Print system banner"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  🚗 HỆ THỐNG PHÁT HIỆN VÀ CẢNH BÁO ĐỖ XE TRÁI PHÉP           ║
║     Illegal Parking Detection & Alert System v1.0             ║
║                                                                ║
║  📹 Real-time Camera Monitoring                               ║
║  🤖 AI/ML Vehicle Detection (YOLOv8)                          ║
║  💬 Telegram Bot Notifications                                ║
║  📊 Web Dashboard & API                                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_config():
    """Print system configuration"""
    print("\n⚙️  SYSTEM CONFIGURATION")
    print("=" * 60)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗄️  Database: {settings.DATABASE_URL}")
    print(f"🌐 API: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📹 Evidence Path: {settings.EVIDENCE_PATH}")
    print(f"🤖 AI Model: {settings.MODEL_NAME}")
    print(f"📊 Confidence Threshold: {settings.CONFIDENCE_THRESHOLD*100:.0f}%")
    print(f"💬 Telegram: {'✓ Enabled' if settings.TELEGRAM_BOT_TOKEN else '✗ Disabled'}")
    print("=" * 60 + "\n")


def initialize_system(detector_model: str = None):
    """
    Initialize parking detection system
    
    Args:
        detector_model: Path to AI detector model
    """
    print("\n🔧 INITIALIZING SYSTEM...")
    print("-" * 60)
    
    try:
        # Create necessary directories
        Path(settings.EVIDENCE_PATH).mkdir(parents=True, exist_ok=True)
        Path(settings.MODEL_PATH).mkdir(parents=True, exist_ok=True)
        Path("./logs").mkdir(parents=True, exist_ok=True)
        print("✓ Directories created")
        
        # Initialize system
        system = ParkingDetectionSystem(
            detector_model=detector_model,
            enable_telegram=True
        )
        print("✓ System initialized")
        
        return system
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        return None


def setup_cameras(system):
    """
    Setup cameras for the system
    
    Args:
        system: ParkingDetectionSystem instance
    """
    print("\n📹 SETTING UP CAMERAS")
    print("-" * 60)
    
    # Configure cameras
    camera_configs = [
        {
            "id": "entrance",
            "source": 0,
            "name": "Parking Entrance"
        },
        # Uncomment to add more cameras:
        # {
        #     "id": "exit",
        #     "source": "rtsp://192.168.1.100:554/stream",
        #     "name": "Exit Gate"
        # },
        # {
        #     "id": "side",
        #     "source": 1,
        #     "name": "Side View"
        # }
    ]
    
    connected = system.connect_to_all_cameras(camera_configs)
    print(f"✓ Connected to {connected}/{len(camera_configs)} cameras")
    
    if connected == 0:
        print("\n⚠️  WARNING: No cameras connected!")
        print("To add cameras, modify the camera_configs list:")
        print("  - Webcam: 0")
        print("  - RTSP: 'rtsp://192.168.1.100:554/stream'")
        return False
    
    return True


def print_statistics(stats):
    """Print system statistics"""
    print("\n📊 SYSTEM STATISTICS")
    print("-" * 60)
    print(f"Total Violations Detected: {stats['total_violations']}")
    print(f"Active Cameras: {stats['active_cameras']}")
    print(f"System Running: {'✓ Yes' if stats['running'] else '✗ No'}")
    print(f"Detector Loaded: {'✓ Yes' if stats['detector_loaded'] else '✗ No'}")
    print(f"Telegram Connected: {'✓ Yes' if stats['telegram_connected'] else '✗ No'}")
    
    if stats.get('cameras'):
        print("\nCamera Details:")
        for cam_id, cam_stats in stats['cameras'].items():
            print(f"  • {cam_id}:")
            print(f"    - Total Frames: {cam_stats.get('total_frames', 0)}")
            print(f"    - Processed: {cam_stats.get('processed_frames', 0)}")
            print(f"    - Violations: {cam_stats.get('violations_found', 0)}")


def print_menu():
    """Print control menu"""
    print("\n🎮 SYSTEM CONTROLS")
    print("-" * 60)
    print("Commands:")
    print("  P - Pause detection")
    print("  R - Resume detection")
    print("  S - Show statistics")
    print("  Q - Quit system")
    print("-" * 60)


def run_system(system, duration: int = None):
    """
    Run the parking detection system
    
    Args:
        system: ParkingDetectionSystem instance
        duration: Runtime duration in seconds (None = indefinite)
    """
    print("\n🚀 STARTING SYSTEM")
    print("-" * 60)
    
    # Send startup alert
    if system.telegram:
        system.send_status_report()
    
    print("✓ System started")
    print("Press Ctrl+C to stop")
    print("\n" + "=" * 60)
    
    try:
        # Run detection
        stats = system.start(duration=duration)
        
        print("\n" + "=" * 60)
        print_statistics(stats)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  STOPPING SYSTEM")
        print("-" * 60)
        stats = system.stop()
        print_statistics(stats)
    
    except Exception as e:
        logger.error(f"System error: {e}")
        system.stop()


def print_next_steps():
    """Print next steps and tips"""
    print("\n📝 NEXT STEPS & TIPS")
    print("=" * 60)
    print("""
1. MONITORING:
   • Open web dashboard: http://localhost:8000
   • Check logs: ./logs/system.log
   • Monitor statistics in real-time

2. ADDING MORE CAMERAS:
   Edit this script and add to camera_configs:
   {
       "id": "camera_name",
       "source": "rtsp://camera_url",
       "name": "Display Name"
   }

3. TELEGRAM SETUP:
   • Set TELEGRAM_BOT_TOKEN in .env
   • Set TELEGRAM_CHAT_ID in .env
   • Test with: system.send_status_report()

4. CUSTOMIZATION:
   • Adjust CONFIDENCE_THRESHOLD in .env (0.0-1.0)
   • Modify NMS_THRESHOLD for detection filtering
   • Change violation callback in parking_system.py

5. DATABASE:
   • Check violations: SELECT * FROM violation;
   • View cameras: SELECT * FROM camera;
   • Analyze statistics: analytics queries

6. PERFORMANCE:
   • Process every N-th frame: processor.frame_skip = 10
   • Resize frames: camera.get_frame_resized(640, 480)
   • Use multiple threads for multiple cameras

7. API ENDPOINTS:
   • List violations: GET /api/v1/violations
   • Get statistics: GET /api/v1/statistics/summary
   • Create violation: POST /api/v1/violations
   • Docs: http://localhost:8000/docs

8. TROUBLESHOOTING:
   • Camera not found: Check device permissions
   • Telegram not sending: Verify token and chat_id
   • High CPU usage: Increase frame skip or reduce resolution
   • Database locked: Restart system

For more info, see docs/:
  • CAMERA_MODULE.md
  • API.md
  • ARCHITECTURE.md
  • SETUP.md
""")
    print("=" * 60)


def main():
    """Main system startup"""
    print_banner()
    
    # Configuration
    print_config()
    
    # Initialize
    system = initialize_system(detector_model=None)  # Set to "yolov8n.pt" when ready
    if system is None:
        print("❌ Failed to initialize system")
        return
    
    # Setup cameras
    if not setup_cameras(system):
        print("❌ Failed to setup cameras")
        system.stop()
        return
    
    # Show menu
    print_menu()
    
    # Run system
    run_system(system, duration=None)  # None = run indefinitely
    
    # Cleanup
    print("\n🧹 CLEANING UP")
    print("-" * 60)
    system.camera_manager.disconnect_all()
    print("✓ Cleanup complete")
    
    # Show next steps
    print_next_steps()
    
    print("\n✅ System stopped successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal Error: {e}")
        print("Check ./logs/system.log for details")
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
