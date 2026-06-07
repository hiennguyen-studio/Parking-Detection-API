<<<<<<< HEAD
"""
Stream processor for video analysis
"""
import cv2
import logging
import asyncio
from typing import Optional, Callable, List
from datetime import datetime

logger = logging.getLogger(__name__)


class StreamProcessor:
    """Process video streams in real-time with detection and notification"""

    def __init__(self, camera_handler, detector=None, notification_manager=None):
        """
        Initialize stream processor
        
        Args:
            camera_handler: CameraHandler instance
            detector: AI detector for violations
            notification_manager: Manager for sending notifications
        """
        self.camera_handler = camera_handler
        self.detector = detector
        self.notification_manager = notification_manager
        self.is_running = False
        self.frame_skip = 5  # Process every 5th frame for performance
        self.frame_count = 0
        self.processed_count = 0
        self.violation_count = 0
        self.callbacks: List[Callable] = []

    def add_callback(self, callback: Callable):
        """Add callback for violations"""
        self.callbacks.append(callback)

    def start(self):
        """Start processing stream"""
        if not self.camera_handler.is_connected:
            logger.error("Camera not connected")
            return False
        
        self.is_running = True
        logger.info(f"Stream processor started for {self.camera_handler.name}")
        return True

    def stop(self):
        """Stop processing stream"""
        self.is_running = False
        logger.info(f"Stream processor stopped")

    def process_frame(self, frame: cv2.Mat) -> Optional[dict]:
        """
        Process a single frame
        
        Returns:
            Detection result dict with violations, or None
        """
        if frame is None:
            return None
        
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % self.frame_skip != 0:
            return None
        
        self.processed_count += 1
        result = None
        
        try:
            # Run detection if available
            if self.detector:
                detections = self.detector.detect(frame)
                if detections and len(detections) > 0:
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "frame_number": self.frame_count,
                        "camera": self.camera_handler.name,
                        "detections": detections,
                        "frame_shape": frame.shape
                    }
                    self.violation_count += len(detections)
                    self._trigger_callbacks(result)
                    logger.info(f"Violations detected: {len(detections)}")
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
        
        return result

    def process_stream(self, max_frames: int = None) -> dict:
        """
        Process entire stream
        
        Args:
            max_frames: Maximum frames to process (None for unlimited)
            
        Returns:
            Statistics dict
        """
        if not self.start():
            return {"error": "Failed to start stream processing"}
        
        frame_limit = max_frames
        
        try:
            while self.is_running and (frame_limit is None or self.frame_count < frame_limit):
                frame_data = self.camera_handler.get_frame()
                if frame_data is None:
                    break
                
                ret, frame = frame_data
                if not ret:
                    break
                
                self.process_frame(frame)
        except KeyboardInterrupt:
            logger.info("Stream processing interrupted")
        finally:
            self.stop()
        
        return self.get_statistics()

    async def process_stream_async(self, max_frames: int = None) -> dict:
        """
        Async stream processing
        
        Args:
            max_frames: Maximum frames to process
            
        Returns:
            Statistics dict
        """
        if not self.start():
            return {"error": "Failed to start stream processing"}
        
        frame_limit = max_frames
        
        try:
            while self.is_running and (frame_limit is None or self.frame_count < frame_limit):
                frame_data = self.camera_handler.get_frame()
                if frame_data is None:
                    break
                
                ret, frame = frame_data
                if not ret:
                    break
                
                self.process_frame(frame)
                await asyncio.sleep(0.01)  # Yield to event loop
        except Exception as e:
            logger.error(f"Error in async stream processing: {e}")
        finally:
            self.stop()
        
        return self.get_statistics()

    def _trigger_callbacks(self, result: dict):
        """Trigger registered callbacks"""
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(result))
                else:
                    callback(result)
            except Exception as e:
                logger.error(f"Error in callback: {e}")

    def get_statistics(self) -> dict:
        """Get processing statistics"""
        return {
            "is_running": self.is_running,
            "total_frames": self.frame_count,
            "processed_frames": self.processed_count,
            "violations_found": self.violation_count,
            "skip_rate": self.frame_skip
        }
=======
"""
Stream processor for video analysis
"""
import cv2
import logging
import asyncio
from typing import Optional, Callable, List
from datetime import datetime

logger = logging.getLogger(__name__)


class StreamProcessor:
    """Process video streams in real-time with detection and notification"""

    def __init__(self, camera_handler, detector=None, notification_manager=None):
        """
        Initialize stream processor
        
        Args:
            camera_handler: CameraHandler instance
            detector: AI detector for violations
            notification_manager: Manager for sending notifications
        """
        self.camera_handler = camera_handler
        self.detector = detector
        self.notification_manager = notification_manager
        self.is_running = False
        self.frame_skip = 5  # Process every 5th frame for performance
        self.frame_count = 0
        self.processed_count = 0
        self.violation_count = 0
        self.callbacks: List[Callable] = []

    def add_callback(self, callback: Callable):
        """Add callback for violations"""
        self.callbacks.append(callback)

    def start(self):
        """Start processing stream"""
        if not self.camera_handler.is_connected:
            logger.error("Camera not connected")
            return False
        
        self.is_running = True
        logger.info(f"Stream processor started for {self.camera_handler.name}")
        return True

    def stop(self):
        """Stop processing stream"""
        self.is_running = False
        logger.info(f"Stream processor stopped")

    def process_frame(self, frame: cv2.Mat) -> Optional[dict]:
        """
        Process a single frame
        
        Returns:
            Detection result dict with violations, or None
        """
        if frame is None:
            return None
        
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % self.frame_skip != 0:
            return None
        
        self.processed_count += 1
        result = None
        
        try:
            # Run detection if available
            if self.detector:
                detections = self.detector.detect(frame)
                if detections and len(detections) > 0:
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "frame_number": self.frame_count,
                        "camera": self.camera_handler.name,
                        "detections": detections,
                        "frame_shape": frame.shape
                    }
                    self.violation_count += len(detections)
                    self._trigger_callbacks(result)
                    logger.info(f"Violations detected: {len(detections)}")
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
        
        return result

    def process_stream(self, max_frames: int = None) -> dict:
        """
        Process entire stream
        
        Args:
            max_frames: Maximum frames to process (None for unlimited)
            
        Returns:
            Statistics dict
        """
        if not self.start():
            return {"error": "Failed to start stream processing"}
        
        frame_limit = max_frames
        
        try:
            while self.is_running and (frame_limit is None or self.frame_count < frame_limit):
                frame_data = self.camera_handler.get_frame()
                if frame_data is None:
                    break
                
                ret, frame = frame_data
                if not ret:
                    break
                
                self.process_frame(frame)
        except KeyboardInterrupt:
            logger.info("Stream processing interrupted")
        finally:
            self.stop()
        
        return self.get_statistics()

    async def process_stream_async(self, max_frames: int = None) -> dict:
        """
        Async stream processing
        
        Args:
            max_frames: Maximum frames to process
            
        Returns:
            Statistics dict
        """
        if not self.start():
            return {"error": "Failed to start stream processing"}
        
        frame_limit = max_frames
        
        try:
            while self.is_running and (frame_limit is None or self.frame_count < frame_limit):
                frame_data = self.camera_handler.get_frame()
                if frame_data is None:
                    break
                
                ret, frame = frame_data
                if not ret:
                    break
                
                self.process_frame(frame)
                await asyncio.sleep(0.01)  # Yield to event loop
        except Exception as e:
            logger.error(f"Error in async stream processing: {e}")
        finally:
            self.stop()
        
        return self.get_statistics()

    def _trigger_callbacks(self, result: dict):
        """Trigger registered callbacks"""
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(result))
                else:
                    callback(result)
            except Exception as e:
                logger.error(f"Error in callback: {e}")

    def get_statistics(self) -> dict:
        """Get processing statistics"""
        return {
            "is_running": self.is_running,
            "total_frames": self.frame_count,
            "processed_frames": self.processed_count,
            "violations_found": self.violation_count,
            "skip_rate": self.frame_skip
        }
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
