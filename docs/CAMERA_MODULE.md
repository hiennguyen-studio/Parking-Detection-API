# 📹 Camera Module Documentation

## Overview
Complete camera management system for handling webcam and RTSP streams with real-time frame processing and violation detection.

## Components

### 1. **CameraHandler** - Low-level camera control
```python
from src.camera import CameraHandler

# Webcam (ID 0)
camera = CameraHandler(camera_source=0, name="Front Camera")

# RTSP Stream
camera = CameraHandler(
    camera_source="rtsp://192.168.1.100:554/stream",
    name="Gate Camera"
)

# Connect
if camera.connect():
    # Get frame
    frame_data = camera.get_frame()
    if frame_data:
        ret, frame = frame_data
        
        # Save frame
        camera.save_frame(frame, "./evidence/frame.jpg")
        
        # Get resized frame
        ret, resized = camera.get_frame_resized(640, 480)
    
    # Get info
    info = camera.get_info()
    print(info)
    
    camera.disconnect()
```

**Methods:**
- `connect()` → bool: Connect to camera source
- `get_frame()` → (ret, frame) or None: Get current frame
- `get_frame_resized(width, height)` → (ret, frame) or None: Get resized frame
- `save_frame(frame, path)` → bool: Save frame to file
- `disconnect()`: Close camera connection
- `get_info()` → dict: Camera information

---

### 2. **StreamProcessor** - Real-time stream processing
```python
from src.camera import StreamProcessor

processor = StreamProcessor(
    camera_handler=camera,
    detector=detector,  # AI detector (optional)
    notification_manager=notifier  # Notification service (optional)
)

# Add violation callback
def on_violation_detected(result):
    print(f"Violation found: {result['detections']}")
    # Send Telegram notification
    # Save to database
    # Log evidence

processor.add_callback(on_violation_detected)

# Start processing
processor.start()

# Process frames
while processor.is_running:
    frame_data = camera.get_frame()
    if frame_data:
        ret, frame = frame_data
        detection_result = processor.process_frame(frame)

# Stop processing
processor.stop()

# Get statistics
stats = processor.get_statistics()
print(f"Total frames: {stats['total_frames']}")
print(f"Violations found: {stats['violations_found']}")
```

**Methods:**
- `start()` → bool: Start stream processing
- `stop()`: Stop stream processing
- `process_frame(frame)` → dict or None: Process single frame
- `add_callback(callback)`: Register violation callback
- `process_stream(max_frames)` → dict: Process entire stream (blocking)
- `process_stream_async(max_frames)` → dict: Process stream asynchronously
- `get_statistics()` → dict: Processing statistics

---

### 3. **CameraManager** - Multi-camera management
```python
from src.camera import CameraManager

manager = CameraManager(
    detector=detector,
    notification_manager=notifier
)

# Add cameras
manager.add_camera("parking_entrance", 0, "Entrance Camera")
manager.add_camera("parking_exit", "rtsp://gate-camera/stream", "Exit Gate")

# Get camera information
cameras = manager.get_all_cameras()
for cam_id, info in cameras.items():
    print(f"{cam_id}: {info}")

# Register callbacks per camera
def on_entrance_violation(result):
    print(f"Entrance violation: {result['detections']}")

manager.register_violation_callback("parking_entrance", on_entrance_violation)

# Start all cameras
manager.start_all()

# Process frames
for _ in range(100):
    manager.process_frame("parking_entrance")
    manager.process_frame("parking_exit")

# Get statistics
stats = manager.get_statistics()

# Cleanup
manager.stop_all()
manager.disconnect_all()
```

**Methods:**
- `add_camera(cam_id, source, name)` → bool: Add camera
- `remove_camera(cam_id)` → bool: Remove camera
- `get_camera(cam_id)` → CameraHandler: Get camera object
- `get_processor(cam_id)` → StreamProcessor: Get processor
- `get_all_cameras()` → dict: All cameras info
- `start_camera(cam_id)` → bool: Start specific camera
- `stop_camera(cam_id)`: Stop specific camera
- `start_all()` → bool: Start all cameras
- `stop_all()`: Stop all cameras
- `process_frame(cam_id)` → dict or None: Process one frame
- `register_violation_callback(cam_id, callback)`: Register callback
- `get_statistics()` → dict: All cameras statistics
- `disconnect_all()`: Disconnect all cameras

---

## Usage Patterns

### Pattern 1: Simple Single Camera
```python
from src.camera import CameraHandler

camera = CameraHandler(0, "My Camera")
camera.connect()

ret, frame = camera.get_frame() or (False, None)
if ret:
    camera.save_frame(frame, "./photo.jpg")

camera.disconnect()
```

### Pattern 2: Real-time Processing
```python
from src.camera import CameraHandler, StreamProcessor

camera = CameraHandler("rtsp://camera/stream")
camera.connect()

processor = StreamProcessor(camera)
processor.add_callback(lambda r: print(f"Detection: {r}"))
processor.start()

# Auto process loop
stats = processor.process_stream(max_frames=1000)
print(stats)
```

### Pattern 3: Multiple Cameras with Manager
```python
from src.camera import CameraManager

with CameraManager() as manager:
    manager.add_camera("cam1", 0)
    manager.add_camera("cam2", "rtsp://camera2")
    manager.add_camera("cam3", "rtsp://camera3")
    
    manager.start_all()
    
    for _ in range(1000):
        manager.process_frame("cam1")
        manager.process_frame("cam2")
        manager.process_frame("cam3")
    
    print(manager.get_statistics())
```

### Pattern 4: With AI Detector and Notifications
```python
from src.camera import CameraManager
from src.AI.detector import ViolationDetector
from src.notify import TelegramNotifier

detector = ViolationDetector("models/best.pt")
notifier = TelegramNotifier(token="...", chat_id="...")

manager = CameraManager(detector=detector, notification_manager=notifier)

def on_violation(result):
    # Send Telegram alert
    notifier.send_alert(result)
    # Save evidence
    # Log to database

manager.add_camera("entrance", 0, "Parking Entrance")
manager.register_violation_callback("entrance", on_violation)
manager.start_camera("entrance")

# Process indefinitely
manager.process_stream("entrance")
```

---

## Configuration

### Environment Variables (.env)
```bash
# Camera settings
CAMERA_ID=0                          # Default camera ID
CAMERA_SKIP_FRAMES=5                # Process every N-th frame
STREAM_RESIZE_WIDTH=640              # Resize width
STREAM_RESIZE_HEIGHT=480             # Resize height
EVIDENCE_PATH=./data/evidence/       # Where to save evidence
```

---

## Performance Tips

1. **Frame Skipping**: Skip frames to reduce processing load
   ```python
   processor.frame_skip = 10  # Process every 10th frame
   ```

2. **Resizing**: Resize frames before detection
   ```python
   ret, frame = camera.get_frame_resized(640, 480)
   ```

3. **Multiple Cameras**: Use manager to efficiently handle multiple streams

4. **Threading**: Use async processing for long-running operations
   ```python
   stats = await processor.process_stream_async(max_frames=5000)
   ```

---

## Error Handling

```python
from src.camera import CameraHandler

camera = CameraHandler(0)

try:
    if camera.connect():
        frame_data = camera.get_frame()
        if frame_data:
            ret, frame = frame_data
            print("✓ Frame captured")
        else:
            print("✗ Could not read frame")
    else:
        print("✗ Could not connect to camera")
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    camera.disconnect()
```

---

## Testing

Run tests:
```bash
pytest tests/test_camera.py -v
```

All tests passing ✓

---

## Integration with Other Modules

### With AI Detector
```python
from src.camera import CameraManager
from src.AI.detector import ViolationDetector

detector = ViolationDetector("models/best.pt")
manager = CameraManager(detector=detector)
```

### With Telegram Notifications
```python
from src.notify.telegram_bot import TelegramBot

telegram = TelegramBot(token="YOUR_TOKEN")

def on_violation(result):
    telegram.send_alert(result)

processor.add_callback(on_violation)
```

### With Database
```python
from src.database import db_manager

def on_violation(result):
    # Save to database
    db_manager.save_violation(result)

processor.add_callback(on_violation)
```

---

## Troubleshooting

**Camera not connecting:**
- Check if camera is not already in use
- Verify camera ID (0 = default webcam)
- For RTSP, verify URL and network connectivity

**Low frame rate:**
- Reduce frame size with `get_frame_resized()`
- Increase frame skip: `processor.frame_skip = 10`
- Check camera/network bandwidth

**Memory leaks:**
- Always call `disconnect()` or use context manager
- Use `with CameraManager() as manager:` pattern

---

**Status**: ✅ Fully implemented and tested
