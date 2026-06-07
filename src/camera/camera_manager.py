<<<<<<< HEAD
"""
Camera manager for handling multiple cameras
"""
import logging
from typing import Dict, Optional, List
from .camera_handler import CameraHandler
from .stream_processor import StreamProcessor

logger = logging.getLogger(__name__)


class CameraManager:
    """Manage multiple cameras and their streams"""

    def __init__(self, detector=None, notification_manager=None):
        """
        Initialize camera manager
        
        Args:
            detector: AI detector for violations
            notification_manager: Manager for sending notifications
        """
        self.cameras: Dict[str, CameraHandler] = {}
        self.processors: Dict[str, StreamProcessor] = {}
        self.detector = detector
        self.notification_manager = notification_manager

    def add_camera(self, camera_id: str, source: int | str, name: str = None) -> bool:
        """
        Add a new camera
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source (int for webcam, str for RTSP URL)
            name: Camera display name
            
        Returns:
            True if successful, False otherwise
        """
        if camera_id in self.cameras:
            logger.warning(f"Camera {camera_id} already exists")
            return False
        
        try:
            camera = CameraHandler(camera_source=source, name=name or camera_id)
            if camera.connect():
                self.cameras[camera_id] = camera
                # Create processor for this camera
                processor = StreamProcessor(
                    camera,
                    detector=self.detector,
                    notification_manager=self.notification_manager
                )
                self.processors[camera_id] = processor
                logger.info(f"Camera added: {camera_id}")
                return True
            else:
                logger.error(f"Failed to connect to camera: {camera_id}")
                return False
        except Exception as e:
            logger.error(f"Error adding camera: {e}")
            return False

    def remove_camera(self, camera_id: str) -> bool:
        """Remove a camera"""
        if camera_id not in self.cameras:
            logger.warning(f"Camera {camera_id} not found")
            return False
        
        try:
            # Stop processor
            if camera_id in self.processors:
                self.processors[camera_id].stop()
                del self.processors[camera_id]
            
            # Disconnect camera
            self.cameras[camera_id].disconnect()
            del self.cameras[camera_id]
            logger.info(f"Camera removed: {camera_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing camera: {e}")
            return False

    def get_camera(self, camera_id: str) -> Optional[CameraHandler]:
        """Get camera by ID"""
        return self.cameras.get(camera_id)

    def get_processor(self, camera_id: str) -> Optional[StreamProcessor]:
        """Get processor by camera ID"""
        return self.processors.get(camera_id)

    def get_all_cameras(self) -> Dict[str, dict]:
        """Get all cameras with their info"""
        return {
            cam_id: camera.get_info()
            for cam_id, camera in self.cameras.items()
        }

    def start_camera(self, camera_id: str) -> bool:
        """Start processing for a camera"""
        if camera_id not in self.processors:
            logger.error(f"Processor not found for camera: {camera_id}")
            return False
        
        return self.processors[camera_id].start()

    def stop_camera(self, camera_id: str):
        """Stop processing for a camera"""
        if camera_id in self.processors:
            self.processors[camera_id].stop()

    def start_all(self) -> bool:
        """Start all cameras"""
        success = True
        for camera_id in self.cameras.keys():
            if not self.start_camera(camera_id):
                success = False
        return success

    def stop_all(self):
        """Stop all cameras"""
        for camera_id in self.cameras.keys():
            self.stop_camera(camera_id)

    def process_frame(self, camera_id: str) -> Optional[dict]:
        """Process next frame from camera"""
        if camera_id not in self.cameras:
            logger.error(f"Camera {camera_id} not found")
            return None
        
        frame_data = self.cameras[camera_id].get_frame()
        if frame_data is None:
            return None
        
        ret, frame = frame_data
        if ret:
            return self.processors[camera_id].process_frame(frame)
        return None

    def register_violation_callback(self, camera_id: str, callback):
        """Register callback for violations from specific camera"""
        if camera_id in self.processors:
            self.processors[camera_id].add_callback(callback)

    def get_statistics(self) -> Dict[str, dict]:
        """Get statistics for all cameras"""
        return {
            cam_id: self.processors[cam_id].get_statistics()
            for cam_id in self.cameras.keys()
        }

    def disconnect_all(self):
        """Disconnect all cameras"""
        for camera_id in list(self.cameras.keys()):
            self.remove_camera(camera_id)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect_all()
=======
"""
Camera manager for handling multiple cameras
"""
import logging
from typing import Dict, Optional, List
from .camera_handler import CameraHandler
from .stream_processor import StreamProcessor

logger = logging.getLogger(__name__)


class CameraManager:
    """Manage multiple cameras and their streams"""

    def __init__(self, detector=None, notification_manager=None):
        """
        Initialize camera manager
        
        Args:
            detector: AI detector for violations
            notification_manager: Manager for sending notifications
        """
        self.cameras: Dict[str, CameraHandler] = {}
        self.processors: Dict[str, StreamProcessor] = {}
        self.detector = detector
        self.notification_manager = notification_manager

    def add_camera(self, camera_id: str, source: int | str, name: str = None) -> bool:
        """
        Add a new camera
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source (int for webcam, str for RTSP URL)
            name: Camera display name
            
        Returns:
            True if successful, False otherwise
        """
        if camera_id in self.cameras:
            logger.warning(f"Camera {camera_id} already exists")
            return False
        
        try:
            camera = CameraHandler(camera_source=source, name=name or camera_id)
            if camera.connect():
                self.cameras[camera_id] = camera
                # Create processor for this camera
                processor = StreamProcessor(
                    camera,
                    detector=self.detector,
                    notification_manager=self.notification_manager
                )
                self.processors[camera_id] = processor
                logger.info(f"Camera added: {camera_id}")
                return True
            else:
                logger.error(f"Failed to connect to camera: {camera_id}")
                return False
        except Exception as e:
            logger.error(f"Error adding camera: {e}")
            return False

    def remove_camera(self, camera_id: str) -> bool:
        """Remove a camera"""
        if camera_id not in self.cameras:
            logger.warning(f"Camera {camera_id} not found")
            return False
        
        try:
            # Stop processor
            if camera_id in self.processors:
                self.processors[camera_id].stop()
                del self.processors[camera_id]
            
            # Disconnect camera
            self.cameras[camera_id].disconnect()
            del self.cameras[camera_id]
            logger.info(f"Camera removed: {camera_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing camera: {e}")
            return False

    def get_camera(self, camera_id: str) -> Optional[CameraHandler]:
        """Get camera by ID"""
        return self.cameras.get(camera_id)

    def get_processor(self, camera_id: str) -> Optional[StreamProcessor]:
        """Get processor by camera ID"""
        return self.processors.get(camera_id)

    def get_all_cameras(self) -> Dict[str, dict]:
        """Get all cameras with their info"""
        return {
            cam_id: camera.get_info()
            for cam_id, camera in self.cameras.items()
        }

    def start_camera(self, camera_id: str) -> bool:
        """Start processing for a camera"""
        if camera_id not in self.processors:
            logger.error(f"Processor not found for camera: {camera_id}")
            return False
        
        return self.processors[camera_id].start()

    def stop_camera(self, camera_id: str):
        """Stop processing for a camera"""
        if camera_id in self.processors:
            self.processors[camera_id].stop()

    def start_all(self) -> bool:
        """Start all cameras"""
        success = True
        for camera_id in self.cameras.keys():
            if not self.start_camera(camera_id):
                success = False
        return success

    def stop_all(self):
        """Stop all cameras"""
        for camera_id in self.cameras.keys():
            self.stop_camera(camera_id)

    def process_frame(self, camera_id: str) -> Optional[dict]:
        """Process next frame from camera"""
        if camera_id not in self.cameras:
            logger.error(f"Camera {camera_id} not found")
            return None
        
        frame_data = self.cameras[camera_id].get_frame()
        if frame_data is None:
            return None
        
        ret, frame = frame_data
        if ret:
            return self.processors[camera_id].process_frame(frame)
        return None

    def register_violation_callback(self, camera_id: str, callback):
        """Register callback for violations from specific camera"""
        if camera_id in self.processors:
            self.processors[camera_id].add_callback(callback)

    def get_statistics(self) -> Dict[str, dict]:
        """Get statistics for all cameras"""
        return {
            cam_id: self.processors[cam_id].get_statistics()
            for cam_id in self.cameras.keys()
        }

    def disconnect_all(self):
        """Disconnect all cameras"""
        for camera_id in list(self.cameras.keys()):
            self.remove_camera(camera_id)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect_all()
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
