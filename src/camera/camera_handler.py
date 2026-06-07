"""
Camera handler for video stream processing
"""
import cv2
import logging
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class CameraHandler:
    """Handle camera input and stream management (webcam or RTSP)"""

    def __init__(self, camera_source: int | str = 0, name: str = "Camera"):
        """
        Initialize camera handler
        
        Args:
            camera_source: Webcam ID (int) or RTSP URL (str)
            name: Camera name for logging
        """
        self.camera_source = camera_source
        self.name = name
        self.cap = None
        self.is_connected = False
        self.frame_count = 0
        self.fps = 30
        self.frame_width = 0
        self.frame_height = 0

    def connect(self) -> bool:
        """Connect to camera (webcam or RTSP stream)"""
        try:
            self.cap = cv2.VideoCapture(self.camera_source)
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera: {self.camera_source}")
                return False
            
            # Get camera properties
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 30
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            self.is_connected = True
            logger.info(f"Camera connected: {self.name} ({self.frame_width}x{self.frame_height}@{self.fps}fps)")
            return True
        except Exception as e:
            logger.error(f"Error connecting to camera: {e}")
            return False

    def get_frame(self) -> Optional[Tuple[bool, cv2.Mat]]:
        """Get a frame from the camera"""
        if not self.is_connected or self.cap is None:
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
            return (ret, frame) if ret else None
        except Exception as e:
            logger.error(f"Error reading frame: {e}")
            return None

    def get_frame_resized(self, width: int = 640, height: int = 480) -> Optional[Tuple[bool, cv2.Mat]]:
        """Get and resize frame"""
        frame_data = self.get_frame()
        if frame_data is None:
            return None
        
        ret, frame = frame_data
        if ret and frame is not None:
            resized = cv2.resize(frame, (width, height))
            return (True, resized)
        return None

    def save_frame(self, frame: cv2.Mat, output_path: str) -> bool:
        """Save frame to file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(output_path, frame)
            logger.info(f"Frame saved: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return False

    def disconnect(self):
        """Disconnect from camera"""
        if self.cap:
            self.cap.release()
            self.is_connected = False
            logger.info(f"Camera disconnected: {self.name}")

    def get_info(self) -> dict:
        """Get camera information"""
        return {
            "name": self.name,
            "source": self.camera_source,
            "is_connected": self.is_connected,
            "frame_width": self.frame_width,
            "frame_height": self.frame_height,
            "fps": self.fps,
            "frame_count": self.frame_count
        }

    def __del__(self):
        """Ensure camera is released on cleanup"""
        self.disconnect()
