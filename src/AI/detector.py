"""
AI/ML Model for parking violation detection
"""
from typing import Optional, Tuple, List
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import YOLOv8, but don't fail if not available
try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False
    logger.warning("YOLOv8 not installed. Install with: pip install ultralytics")


class ParkingDetector:
    """Main detector for parking violations using YOLOv8"""

    # Class IDs for common objects
    CAR_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    PARKING_SIGN_ID = 75  # Parking sign in COCO

    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        """
        Initialize the detector with a model
        
        Args:
            model_path: Path to YOLOv8 model (.pt file)
            confidence_threshold: Confidence threshold for detections
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.device = "cpu"  # Can be changed to "cuda" if GPU available
        self._load_model()

    def _load_model(self):
        """Load the pre-trained YOLOv8 model"""
        if not HAS_YOLO:
            logger.error("YOLOv8 not available. Cannot load model.")
            return
        
        try:
            if Path(self.model_path).exists():
                self.model = YOLO(self.model_path)
                logger.info(f"Model loaded: {self.model_path}")
            else:
                # Try to download model
                logger.info(f"Downloading YOLOv8 model: {self.model_path}")
                self.model = YOLO(self.model_path)  # Downloads from Ultralytics
                logger.info(f"Model downloaded and loaded")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def detect(self, frame: np.ndarray) -> List[dict]:
        """
        Detect vehicles in a frame

        Args:
            frame: Input frame (numpy array)

        Returns:
            List of detections with bounding boxes and confidence scores
        """
        if self.model is None:
            logger.warning("Model not loaded. Cannot perform detection.")
            return []
        
        try:
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        # Extract box information
                        xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        cls_name = result.names[cls_id]
                        
                        # Only keep vehicle detections
                        if cls_id in self.CAR_CLASSES:
                            detection = {
                                "class_id": cls_id,
                                "class_name": cls_name,
                                "confidence": conf,
                                "bbox": {
                                    "x1": int(xyxy[0]),
                                    "y1": int(xyxy[1]),
                                    "x2": int(xyxy[2]),
                                    "y2": int(xyxy[3]),
                                    "width": int(xyxy[2] - xyxy[0]),
                                    "height": int(xyxy[3] - xyxy[1])
                                }
                            }
                            detections.append(detection)
            
            return detections
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []

    def detect_with_plate(self, frame: np.ndarray) -> List[dict]:
        """
        Detect vehicles and try to recognize license plates
        
        Args:
            frame: Input frame
            
        Returns:
            List of detections with plate info
        """
        detections = self.detect(frame)
        
        # TODO: Integrate with ALPR (Automatic License Plate Recognition)
        # For now, just return vehicle detections
        return detections

    def is_violation(self, detection: dict, frame: np.ndarray = None) -> bool:
        """
        Check if a detection is a parking violation
        
        Simple heuristics:
        - If vehicle is detected near "No Parking" sign → violation
        - If vehicle is in restricted zone → violation
        
        Args:
            detection: Detection dict from detect()
            frame: Original frame (for advanced analysis)
            
        Returns:
            True if violation detected
        """
        # Basic checks
        if detection["confidence"] < self.confidence_threshold:
            return False
        
        # Could add more sophisticated logic here
        # For now, consider all parked vehicles as potential violations
        # You would implement zone-based or sign-based detection
        return True

    def get_info(self) -> dict:
        """Get detector information"""
        return {
            "model_path": self.model_path,
            "loaded": self.model is not None,
            "confidence_threshold": self.confidence_threshold,
            "device": self.device
        }

    def __del__(self):
        """Cleanup"""
        if self.model is not None:
            self.model = None
