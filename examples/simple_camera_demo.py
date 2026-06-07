<<<<<<< HEAD
"""
Simple camera demo script
"""
import sys
sys.path.insert(0, '.')

from src.camera import CameraManager

# Demo 1: Initialize manager
print("=" * 50)
print("Camera Module Demo")
print("=" * 50)

manager = CameraManager()
print("\n✓ Camera manager initialized")

# Demo 2: Mock add camera
print("\n📹 Adding cameras...")
# Note: These require actual cameras/streams to connect
# We'll just test the structure here

print("""
Example usage:
  
  # Add webcam
  manager.add_camera("cam1", 0, "Entrance Camera")
  
  # Add RTSP stream
  manager.add_camera("cam2", "rtsp://192.168.1.100/stream", "Exit Gate")
  
  # Get all cameras
  cameras = manager.get_all_cameras()
  print(cameras)
  
  # Start processing
  manager.start_all()
  
  # Process frames
  for _ in range(100):
    manager.process_frame("cam1")
    manager.process_frame("cam2")
  
  # Cleanup
  manager.stop_all()
  manager.disconnect_all()
""")

print("\n✓ Demo completed")
print("=" * 50)
=======
"""
Simple camera demo script
"""
import sys
sys.path.insert(0, '.')

from src.camera import CameraManager

# Demo 1: Initialize manager
print("=" * 50)
print("Camera Module Demo")
print("=" * 50)

manager = CameraManager()
print("\n✓ Camera manager initialized")

# Demo 2: Mock add camera
print("\n📹 Adding cameras...")
# Note: These require actual cameras/streams to connect
# We'll just test the structure here

print("""
Example usage:
  
  # Add webcam
  manager.add_camera("cam1", 0, "Entrance Camera")
  
  # Add RTSP stream
  manager.add_camera("cam2", "rtsp://192.168.1.100/stream", "Exit Gate")
  
  # Get all cameras
  cameras = manager.get_all_cameras()
  print(cameras)
  
  # Start processing
  manager.start_all()
  
  # Process frames
  for _ in range(100):
    manager.process_frame("cam1")
    manager.process_frame("cam2")
  
  # Cleanup
  manager.stop_all()
  manager.disconnect_all()
""")

print("\n✓ Demo completed")
print("=" * 50)
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
