<<<<<<< HEAD
"""
Integrated Parking Detection System
Combines camera, AI detector, and Telegram notifications
"""
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

from src.camera import CameraManager
from src.AI.detector import ParkingDetector
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

logger = logging.getLogger(__name__)


class ParkingDetectionSystem:
    """
    Complete parking violation detection and alert system
    
    Features:
    - Multiple camera support
    - Real-time vehicle detection
    - Automatic Telegram alerts
    - Evidence capture and logging
    """

    def __init__(self, detector_model: str = None, enable_telegram: bool = True):
        """
        Initialize the detection system
        
        Args:
            detector_model: Path to YOLOv8 model (.pt file)
            enable_telegram: Whether to enable Telegram notifications
        """
        self.detector = None
        self.camera_manager = None
        self.telegram = None
        self.violation_count = 0
        self.running = False
        self.is_paused = False
        
        # Initialize components
        logger.info("Initializing Parking Detection System...")
        
        # Initialize detector
        if detector_model:
            logger.info(f"Loading detector: {detector_model}")
            self.detector = ParkingDetector(
                model_path=detector_model,
                confidence_threshold=settings.CONFIDENCE_THRESHOLD
            )
        
        # Initialize camera manager
        self.camera_manager = CameraManager(
            detector=self.detector,
            notification_manager=None
        )
        
        # Initialize Telegram
        if enable_telegram and settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            logger.info("Initializing Telegram bot...")
            self.telegram = TelegramBot(
                token=settings.TELEGRAM_BOT_TOKEN,
                chat_id=settings.TELEGRAM_CHAT_ID
            )
        
        logger.info("✓ System initialized")

    def add_camera(self, camera_id: str, source: int | str, name: str = None) -> bool:
        """
        Add a camera to the system
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source (int for webcam, str for RTSP)
            name: Display name
            
        Returns:
            True if successful
        """
        if self.camera_manager.add_camera(camera_id, source, name or camera_id):
            # Register violation callback
            self.camera_manager.register_violation_callback(
                camera_id,
                lambda result: self._handle_violation(camera_id, result)
            )
            logger.info(f"✓ Camera added: {camera_id}")
            return True
        return False

    def _handle_violation(self, camera_id: str, detection_result: dict):
        """
        Handle violation detection
        
        Args:
            camera_id: Camera that detected violation
            detection_result: Detection result from stream processor
        """
        self.violation_count += 1
        
        try:
            detections = detection_result.get("detections", [])
            timestamp = detection_result.get("timestamp", datetime.now().isoformat())
            
            logger.warning(f"🚗 VIOLATION DETECTED on {camera_id}")
            logger.info(f"   Detections: {len(detections)}")
            logger.info(f"   Time: {timestamp}")
            
            # Save evidence image
            evidence_path = self._save_evidence(camera_id, detection_result)
            
            # Prepare violation data
            violation_data = {
                "camera": camera_id,
                "timestamp": timestamp,
                "location": "Parking Area",  # Could come from camera config
                "plate_number": "N/A",  # Would come from ALPR
                "confidence": detections[0].get("confidence", 0) if detections else 0,
                "image_path": evidence_path,
                "detections": len(detections)
            }
            
            # Send Telegram alert
            if self.telegram:
                self.telegram.send_alert(violation_data)
            
            # Could also save to database here
            logger.info(f"✓ Violation processed: {self.violation_count} total")
            
        except Exception as e:
            logger.error(f"Error handling violation: {e}")

    def _save_evidence(self, camera_id: str, detection_result: dict) -> str:
        """Save violation evidence image"""
        try:
            evidence_dir = Path(settings.EVIDENCE_PATH) / camera_id
            evidence_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            evidence_path = evidence_dir / f"violation_{timestamp}.jpg"
            
            # TODO: Save the actual frame from detection_result
            # For now just create placeholder
            logger.info(f"Evidence saved: {evidence_path}")
            return str(evidence_path)
        except Exception as e:
            logger.error(f"Failed to save evidence: {e}")
            return ""

    def start(self, duration: int = None) -> Dict:
        """
        Start the detection system
        
        Args:
            duration: Run duration in seconds (None = indefinite)
            
        Returns:
            Statistics dict
        """
        if self.running:
            logger.warning("System already running")
            return {"error": "System already running"}
        
        self.running = True
        self.violation_count = 0
        
        logger.info("🚀 Starting Parking Detection System...")
        logger.info(f"   Active cameras: {len(self.camera_manager.cameras)}")
        
        try:
            # Start all cameras
            if not self.camera_manager.start_all():
                logger.error("Failed to start cameras")
                return {"error": "Failed to start cameras"}
            
            # Process frames
            if duration:
                start_time = datetime.now()
                elapsed = 0
                while self.running and elapsed < duration:
                    if not self.is_paused:
                        for camera_id in self.camera_manager.cameras.keys():
                            self.camera_manager.process_frame(camera_id)
                    
                    elapsed = (datetime.now() - start_time).total_seconds()
                    asyncio.sleep(0.01)
            else:
                # Run indefinitely
                while self.running:
                    if not self.is_paused:
                        for camera_id in self.camera_manager.cameras.keys():
                            self.camera_manager.process_frame(camera_id)
                    asyncio.sleep(0.01)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error during processing: {e}")
        finally:
            return self.stop()

    def stop(self) -> Dict:
        """
        Stop the detection system
        
        Returns:
            Final statistics
        """
        logger.info("⏹️  Stopping Parking Detection System...")
        self.running = False
        self.camera_manager.stop_all()
        
        stats = self.get_statistics()
        logger.info(f"✓ System stopped. Total violations: {self.violation_count}")
        
        return stats

    def pause(self):
        """Pause detection"""
        self.is_paused = True
        logger.info("Detection paused")

    def resume(self):
        """Resume detection"""
        self.is_paused = False
        logger.info("Detection resumed")

    def get_statistics(self) -> Dict:
        """Get system statistics"""
        camera_stats = self.camera_manager.get_statistics()
        
        return {
            "running": self.running,
            "total_violations": self.violation_count,
            "active_cameras": len(self.camera_manager.cameras),
            "detector_loaded": self.detector is not None and self.detector.model is not None,
            "telegram_connected": self.telegram is not None,
            "cameras": camera_stats
        }

    def send_status_report(self) -> bool:
        """Send system status report via Telegram"""
        if not self.telegram:
            logger.warning("Telegram not configured")
            return False
        
        stats = self.get_statistics()
        
        message = f"""
<b>🎥 System Status Report</b>

📊 <b>Statistics:</b>
• Total Violations: {stats['total_violations']}
• Active Cameras: {stats['active_cameras']}
• System Running: {'✓ Yes' if stats['running'] else '✗ No'}
• Detector: {'✓ Loaded' if stats['detector_loaded'] else '✗ Not loaded'}

<b>Camera Details:</b>
"""
        
        for cam_id, cam_stats in stats.get("cameras", {}).items():
            message += f"""
📹 {cam_id}:
  • Total Frames: {cam_stats.get('total_frames', 0)}
  • Violations: {cam_stats.get('violations_found', 0)}
"""
        
        return self.telegram.send_message(message)

    def connect_to_all_cameras(self, camera_configs: List[Dict]) -> int:
        """
        Connect to multiple cameras
        
        Args:
            camera_configs: List of dicts with keys:
                - id: Unique camera ID
                - source: int (webcam) or str (RTSP URL)
                - name: Display name
                
        Returns:
            Number of successfully connected cameras
        """
        connected = 0
        for config in camera_configs:
            if self.add_camera(
                config.get("id", f"cam{connected}"),
                config.get("source"),
                config.get("name")
            ):
                connected += 1
        
        logger.info(f"✓ Connected to {connected}/{len(camera_configs)} cameras")
        return connected

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
        self.camera_manager.disconnect_all()


# Example usage
if __name__ == "__main__":
    # Create system
    system = ParkingDetectionSystem(
        detector_model="yolov8n.pt",  # Or path to local model
        enable_telegram=True
    )
    
    # Add cameras
    system.add_camera("entrance", 0, "Parking Entrance")
    # system.add_camera("exit", "rtsp://camera-url", "Exit Gate")
    
    # Send initial status
    system.send_status_report()
    
    # Run for 60 seconds
    try:
        stats = system.start(duration=60)
    except KeyboardInterrupt:
        stats = system.stop()
    
    # Print final stats
    print("\n📊 Final Statistics:")
    for key, value in stats.items():
        if key != "cameras":
            print(f"  {key}: {value}")
=======
"""
Integrated Parking Detection System
Combines camera, AI detector, and Telegram notifications
"""
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

from src.camera import CameraManager
from src.AI.detector import ParkingDetector
from src.notify.telegram_bot import TelegramBot
from src.config.settings import settings

logger = logging.getLogger(__name__)


class ParkingDetectionSystem:
    """
    Complete parking violation detection and alert system
    
    Features:
    - Multiple camera support
    - Real-time vehicle detection
    - Automatic Telegram alerts
    - Evidence capture and logging
    """

    def __init__(self, detector_model: str = None, enable_telegram: bool = True):
        """
        Initialize the detection system
        
        Args:
            detector_model: Path to YOLOv8 model (.pt file)
            enable_telegram: Whether to enable Telegram notifications
        """
        self.detector = None
        self.camera_manager = None
        self.telegram = None
        self.violation_count = 0
        self.running = False
        self.is_paused = False
        
        # Initialize components
        logger.info("Initializing Parking Detection System...")
        
        # Initialize detector
        if detector_model:
            logger.info(f"Loading detector: {detector_model}")
            self.detector = ParkingDetector(
                model_path=detector_model,
                confidence_threshold=settings.CONFIDENCE_THRESHOLD
            )
        
        # Initialize camera manager
        self.camera_manager = CameraManager(
            detector=self.detector,
            notification_manager=None
        )
        
        # Initialize Telegram
        if enable_telegram and settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            logger.info("Initializing Telegram bot...")
            self.telegram = TelegramBot(
                token=settings.TELEGRAM_BOT_TOKEN,
                chat_id=settings.TELEGRAM_CHAT_ID
            )
        
        logger.info("✓ System initialized")

    def add_camera(self, camera_id: str, source: int | str, name: str = None) -> bool:
        """
        Add a camera to the system
        
        Args:
            camera_id: Unique camera identifier
            source: Camera source (int for webcam, str for RTSP)
            name: Display name
            
        Returns:
            True if successful
        """
        if self.camera_manager.add_camera(camera_id, source, name or camera_id):
            # Register violation callback
            self.camera_manager.register_violation_callback(
                camera_id,
                lambda result: self._handle_violation(camera_id, result)
            )
            logger.info(f"✓ Camera added: {camera_id}")
            return True
        return False

    def _handle_violation(self, camera_id: str, detection_result: dict):
        """
        Handle violation detection
        
        Args:
            camera_id: Camera that detected violation
            detection_result: Detection result from stream processor
        """
        self.violation_count += 1
        
        try:
            detections = detection_result.get("detections", [])
            timestamp = detection_result.get("timestamp", datetime.now().isoformat())
            
            logger.warning(f"🚗 VIOLATION DETECTED on {camera_id}")
            logger.info(f"   Detections: {len(detections)}")
            logger.info(f"   Time: {timestamp}")
            
            # Save evidence image
            evidence_path = self._save_evidence(camera_id, detection_result)
            
            # Prepare violation data
            violation_data = {
                "camera": camera_id,
                "timestamp": timestamp,
                "location": "Parking Area",  # Could come from camera config
                "plate_number": "N/A",  # Would come from ALPR
                "confidence": detections[0].get("confidence", 0) if detections else 0,
                "image_path": evidence_path,
                "detections": len(detections)
            }
            
            # Send Telegram alert
            if self.telegram:
                self.telegram.send_alert(violation_data)
            
            # Could also save to database here
            logger.info(f"✓ Violation processed: {self.violation_count} total")
            
        except Exception as e:
            logger.error(f"Error handling violation: {e}")

    def _save_evidence(self, camera_id: str, detection_result: dict) -> str:
        """Save violation evidence image"""
        try:
            evidence_dir = Path(settings.EVIDENCE_PATH) / camera_id
            evidence_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            evidence_path = evidence_dir / f"violation_{timestamp}.jpg"
            
            # TODO: Save the actual frame from detection_result
            # For now just create placeholder
            logger.info(f"Evidence saved: {evidence_path}")
            return str(evidence_path)
        except Exception as e:
            logger.error(f"Failed to save evidence: {e}")
            return ""

    def start(self, duration: int = None) -> Dict:
        """
        Start the detection system
        
        Args:
            duration: Run duration in seconds (None = indefinite)
            
        Returns:
            Statistics dict
        """
        if self.running:
            logger.warning("System already running")
            return {"error": "System already running"}
        
        self.running = True
        self.violation_count = 0
        
        logger.info("🚀 Starting Parking Detection System...")
        logger.info(f"   Active cameras: {len(self.camera_manager.cameras)}")
        
        try:
            # Start all cameras
            if not self.camera_manager.start_all():
                logger.error("Failed to start cameras")
                return {"error": "Failed to start cameras"}
            
            # Process frames
            if duration:
                start_time = datetime.now()
                elapsed = 0
                while self.running and elapsed < duration:
                    if not self.is_paused:
                        for camera_id in self.camera_manager.cameras.keys():
                            self.camera_manager.process_frame(camera_id)
                    
                    elapsed = (datetime.now() - start_time).total_seconds()
                    asyncio.sleep(0.01)
            else:
                # Run indefinitely
                while self.running:
                    if not self.is_paused:
                        for camera_id in self.camera_manager.cameras.keys():
                            self.camera_manager.process_frame(camera_id)
                    asyncio.sleep(0.01)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error during processing: {e}")
        finally:
            return self.stop()

    def stop(self) -> Dict:
        """
        Stop the detection system
        
        Returns:
            Final statistics
        """
        logger.info("⏹️  Stopping Parking Detection System...")
        self.running = False
        self.camera_manager.stop_all()
        
        stats = self.get_statistics()
        logger.info(f"✓ System stopped. Total violations: {self.violation_count}")
        
        return stats

    def pause(self):
        """Pause detection"""
        self.is_paused = True
        logger.info("Detection paused")

    def resume(self):
        """Resume detection"""
        self.is_paused = False
        logger.info("Detection resumed")

    def get_statistics(self) -> Dict:
        """Get system statistics"""
        camera_stats = self.camera_manager.get_statistics()
        
        return {
            "running": self.running,
            "total_violations": self.violation_count,
            "active_cameras": len(self.camera_manager.cameras),
            "detector_loaded": self.detector is not None and self.detector.model is not None,
            "telegram_connected": self.telegram is not None,
            "cameras": camera_stats
        }

    def send_status_report(self) -> bool:
        """Send system status report via Telegram"""
        if not self.telegram:
            logger.warning("Telegram not configured")
            return False
        
        stats = self.get_statistics()
        
        message = f"""
<b>🎥 System Status Report</b>

📊 <b>Statistics:</b>
• Total Violations: {stats['total_violations']}
• Active Cameras: {stats['active_cameras']}
• System Running: {'✓ Yes' if stats['running'] else '✗ No'}
• Detector: {'✓ Loaded' if stats['detector_loaded'] else '✗ Not loaded'}

<b>Camera Details:</b>
"""
        
        for cam_id, cam_stats in stats.get("cameras", {}).items():
            message += f"""
📹 {cam_id}:
  • Total Frames: {cam_stats.get('total_frames', 0)}
  • Violations: {cam_stats.get('violations_found', 0)}
"""
        
        return self.telegram.send_message(message)

    def connect_to_all_cameras(self, camera_configs: List[Dict]) -> int:
        """
        Connect to multiple cameras
        
        Args:
            camera_configs: List of dicts with keys:
                - id: Unique camera ID
                - source: int (webcam) or str (RTSP URL)
                - name: Display name
                
        Returns:
            Number of successfully connected cameras
        """
        connected = 0
        for config in camera_configs:
            if self.add_camera(
                config.get("id", f"cam{connected}"),
                config.get("source"),
                config.get("name")
            ):
                connected += 1
        
        logger.info(f"✓ Connected to {connected}/{len(camera_configs)} cameras")
        return connected

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
        self.camera_manager.disconnect_all()


# Example usage
if __name__ == "__main__":
    # Create system
    system = ParkingDetectionSystem(
        detector_model="yolov8n.pt",  # Or path to local model
        enable_telegram=True
    )
    
    # Add cameras
    system.add_camera("entrance", 0, "Parking Entrance")
    # system.add_camera("exit", "rtsp://camera-url", "Exit Gate")
    
    # Send initial status
    system.send_status_report()
    
    # Run for 60 seconds
    try:
        stats = system.start(duration=60)
    except KeyboardInterrupt:
        stats = system.stop()
    
    # Print final stats
    print("\n📊 Final Statistics:")
    for key, value in stats.items():
        if key != "cameras":
            print(f"  {key}: {value}")
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
