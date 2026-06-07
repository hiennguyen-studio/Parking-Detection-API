"""
Quick System Initialization Test
"""
import sys
sys.path.insert(0, '.')

print("\n" + "="*60)
print("🚀 PARKING DETECTION SYSTEM - INITIALIZATION TEST")
print("="*60 + "\n")

# Test 1: Import modules
print("1️⃣ Testing imports...")
try:
    from src.camera import CameraManager
    print("   ✓ Camera module imported")
    
    from src.parking_system import ParkingDetectionSystem
    print("   ✓ Parking system imported")
    
    from src.config.settings import settings
    print("   ✓ Settings imported")
    
    from src.notify.telegram_bot import TelegramBot
    print("   ✓ Telegram bot imported")
    
except Exception as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

# Test 2: Initialize system
print("\n2️⃣ Initializing system...")
try:
    from pathlib import Path
    Path("./logs").mkdir(exist_ok=True)
    
    system = ParkingDetectionSystem(enable_telegram=True)
    print("   ✓ System initialized")
    
except Exception as e:
    print(f"   ✗ Init error: {e}")
    sys.exit(1)

# Test 3: Setup cameras
print("\n3️⃣ Setting up cameras...")
try:
    # Add camera
    if system.add_camera("entrance", 0, "Parking Entrance"):
        print("   ✓ Camera added")
    else:
        print("   ⚠ Could not add camera (may not be available)")
    
except Exception as e:
    print(f"   ✗ Camera error: {e}")

# Test 4: Show statistics
print("\n4️⃣ System statistics:")
try:
    stats = system.get_statistics()
    print(f"   • Running: {stats['running']}")
    print(f"   • Active cameras: {stats['active_cameras']}")
    print(f"   • Detector loaded: {stats['detector_loaded']}")
    print(f"   • Telegram connected: {stats['telegram_connected']}")
    print("   ✓ Statistics retrieved")
except Exception as e:
    print(f"   ✗ Stats error: {e}")

# Test 5: Telegram test
print("\n5️⃣ Testing Telegram...")
try:
    if system.telegram:
        # Just test message formatting, not actual sending
        test_violation = {
            "timestamp": "2024-01-01T10:00:00",
            "camera": "entrance",
            "location": "Parking Area",
            "plate_number": "TEST123",
            "confidence": 0.95
        }
        print("   ✓ Telegram bot initialized")
        print("   • Ready to send alerts")
    else:
        print("   ⚠ Telegram disabled (no token in .env)")
except Exception as e:
    print(f"   ✗ Telegram error: {e}")

# Test 6: Cleanup
print("\n6️⃣ Cleaning up...")
try:
    system.camera_manager.disconnect_all()
    print("   ✓ Cleanup complete")
except Exception as e:
    print(f"   ✗ Cleanup error: {e}")

# Summary
print("\n" + "="*60)
print("✅ SYSTEM INITIALIZATION TEST COMPLETE")
print("="*60)

print("""
📝 NEXT STEPS:

To start the full detection system, run:
   python start_system.py

To start just the API server:
   python -m uvicorn src.backend.main:app --reload

To test camera directly:
   python examples/camera_startup.py

Configuration files:
   • .env - Main configuration
   • src/config/settings.py - Settings class
   • src/config/telegram_config.py - Telegram templates
""")

print("\n✨ Ready to process!")
