"""
Example usage of camera module
"""

from src.camera import CameraManager


def example_single_camera():
    """Example: Process single camera stream"""
    from src.camera import CameraHandler, StreamProcessor
    
    # Create camera handler
    camera = CameraHandler(camera_source=0, name="Front Parking")
    
    # Connect to camera
    if camera.connect():
        print(f"✓ Camera connected: {camera.get_info()}")
        
        # Create processor
        processor = StreamProcessor(camera)
        
        # Add violation callback
        def on_violation(result):
            print(f"🚗 Violation detected: {result['detections']}")
        
        processor.add_callback(on_violation)
        processor.start()
        
        # Process frames
        for _ in range(100):
            frame_data = camera.get_frame()
            if frame_data:
                ret, frame = frame_data
                if ret:
                    processor.process_frame(frame)
        
        processor.stop()
        stats = processor.get_statistics()
        print(f"Statistics: {stats}")
        
        camera.disconnect()
    else:
        print("✗ Failed to connect to camera")


def example_multiple_cameras():
    """Example: Manage multiple cameras"""
    
    manager = CameraManager()
    
    # Add cameras
    manager.add_camera("camera_1", 0, "Entrance")
    manager.add_camera("camera_2", "rtsp://192.168.1.100:554/stream", "Exit Gate")
    
    # Get all cameras
    cameras = manager.get_all_cameras()
    for cam_id, info in cameras.items():
        print(f"Camera {cam_id}: {info}")
    
    # Add violation callback for specific camera
    def on_violation(result):
        print(f"🚗 Violation on {result['camera']}: {result['detections']}")
    
    manager.register_violation_callback("camera_1", on_violation)
    
    # Start processing
    manager.start_all()
    
    # Process frames from first camera
    for _ in range(50):
        manager.process_frame("camera_1")
    
    # Get statistics
    stats = manager.get_statistics()
    for cam_id, cam_stats in stats.items():
        print(f"{cam_id} statistics: {cam_stats}")
    
    # Cleanup
    manager.stop_all()
    manager.disconnect_all()


def example_with_detector():
    """Example: Use with AI detector"""
    from src.camera import CameraManager
    from src.AI.detector import ViolationDetector
    
    # Initialize detector (when ready)
    # detector = ViolationDetector(model_path="models/best.pt")
    
    # Create manager with detector
    manager = CameraManager(detector=None)  # Pass detector when available
    
    manager.add_camera("cam1", 0, "Main Camera")
    
    # Define callback
    def on_violation(result):
        print(f"⚠️ Parking violation detected!")
        print(f"   Time: {result['timestamp']}")
        print(f"   Camera: {result['camera']}")
        print(f"   Detections: {result['detections']}")
        # Here you can send Telegram notification, save to database, etc.
    
    manager.register_violation_callback("cam1", on_violation)
    
    print("Camera system ready! Waiting for violations...")
    # System will now detect violations and trigger callbacks


def example_context_manager():
    """Example: Use camera manager as context manager"""
    
    with CameraManager() as manager:
        manager.add_camera("cam1", 0, "Camera 1")
        manager.add_camera("cam2", "rtsp://stream.url", "Camera 2")
        
        print("Cameras added")
        
        # Process frames
        for _ in range(100):
            manager.process_frame("cam1")
    
    print("✓ All cameras properly disconnected")


if __name__ == "__main__":
    print("=" * 50)
    print("Camera Module Examples")
    print("=" * 50)
    
    print("\n1. Single Camera Example")
    print("-" * 50)
    # example_single_camera()
    
    print("\n2. Multiple Cameras Example")
    print("-" * 50)
    # example_multiple_cameras()
    
    print("\n3. Context Manager Example")
    print("-" * 50)
    example_context_manager()
    
    print("\n✓ Examples completed!")
