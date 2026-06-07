<<<<<<< HEAD
"""
Tests for AI detector, Telegram bot, and integration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from src.AI.detector import ParkingDetector
from src.notify.telegram_bot import TelegramBot
from src.parking_system import ParkingDetectionSystem


class TestParkingDetector:
    """Test parking detector"""

    def test_init(self):
        """Test detector initialization"""
        detector = ParkingDetector("yolov8n.pt", confidence_threshold=0.5)
        assert detector.model_path == "yolov8n.pt"
        assert detector.confidence_threshold == 0.5

    def test_get_info(self):
        """Test getting detector info"""
        detector = ParkingDetector("yolov8n.pt")
        info = detector.get_info()
        
        assert "model_path" in info
        assert "loaded" in info
        assert "confidence_threshold" in info

    def test_detect_no_model(self):
        """Test detection without loaded model"""
        detector = ParkingDetector("yolov8n.pt")
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        detections = detector.detect(frame)
        assert detections == []

    def test_is_violation(self):
        """Test violation check"""
        detector = ParkingDetector("yolov8n.pt")
        detection = {
            "class_id": 2,
            "class_name": "car",
            "confidence": 0.8,
            "bbox": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}
        }
        
        result = detector.is_violation(detection)
        assert isinstance(result, bool)


class TestTelegramBot:
    """Test Telegram bot"""

    def test_init(self):
        """Test bot initialization"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        assert bot.token == "test_token"
        assert bot.chat_id == "12345"

    def test_get_info(self):
        """Test getting bot info"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        info = bot.get_info()
        
        assert "token" in info
        assert "chat_id" in info
        assert info["chat_id"] == "12345"

    def test_register_handler(self):
        """Test registering command handler"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        handler = Mock()
        
        bot.register_handler("start", handler)
        
        assert "start" in bot.handlers
        assert bot.handlers["start"] == handler

    def test_send_message_no_bot(self):
        """Test sending message without bot"""
        bot = TelegramBot(token="", chat_id="12345")
        result = bot.send_message("Test message")
        assert result is False

    def test_send_photo_no_file(self):
        """Test sending non-existent photo"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        result = bot.send_photo("/nonexistent/file.jpg")
        assert result is False

    def test_send_alert_structure(self):
        """Test alert message structure"""
        bot = TelegramBot(token="", chat_id="12345")
        
        violation_data = {
            "timestamp": "2024-01-01T10:00:00",
            "camera": "entrance",
            "location": "Parking Lot A",
            "plate_number": "ABC123",
            "confidence": 0.95
        }
        
        # Since we don't have token, it should return False
        result = bot.send_alert(violation_data)
        assert result is False


class TestParkingDetectionSystem:
    """Test integrated system"""

    def test_init(self):
        """Test system initialization"""
        system = ParkingDetectionSystem(enable_telegram=False)
        assert system.camera_manager is not None
        assert system.running is False
        assert system.violation_count == 0

    @patch('src.camera.camera_manager.CameraManager.add_camera')
    def test_add_camera(self, mock_add):
        """Test adding camera to system"""
        mock_add.return_value = True
        
        system = ParkingDetectionSystem(enable_telegram=False)
        result = system.add_camera("cam1", 0, "Camera 1")
        
        assert result is True

    def test_get_statistics(self):
        """Test getting system statistics"""
        system = ParkingDetectionSystem(enable_telegram=False)
        stats = system.get_statistics()
        
        assert "running" in stats
        assert "total_violations" in stats
        assert "active_cameras" in stats
        assert stats["running"] is False
        assert stats["total_violations"] == 0

    @patch('src.camera.camera_manager.CameraManager.add_camera')
    def test_connect_to_multiple_cameras(self, mock_add):
        """Test connecting to multiple cameras"""
        mock_add.return_value = True
        
        system = ParkingDetectionSystem(enable_telegram=False)
        
        configs = [
            {"id": "cam1", "source": 0, "name": "Entrance"},
            {"id": "cam2", "source": "rtsp://camera", "name": "Exit"},
        ]
        
        connected = system.connect_to_all_cameras(configs)
        assert connected == 2

    def test_pause_resume(self):
        """Test pause and resume"""
        system = ParkingDetectionSystem(enable_telegram=False)
        
        assert system.is_paused is False
        system.pause()
        assert system.is_paused is True
        system.resume()
        assert system.is_paused is False

    def test_context_manager(self):
        """Test context manager"""
        with ParkingDetectionSystem(enable_telegram=False) as system:
            assert system is not None
            assert system.running is False


class TestIntegration:
    """Integration tests"""

    @patch('src.camera.camera_handler.CameraHandler.connect')
    @patch('src.camera.camera_handler.CameraHandler.get_frame')
    def test_full_flow(self, mock_get_frame, mock_connect):
        """Test full detection flow"""
        mock_connect.return_value = True
        mock_get_frame.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        
        system = ParkingDetectionSystem(enable_telegram=False)
        system.add_camera("cam1", 0, "Test Camera")
        
        assert "cam1" in system.camera_manager.cameras
        assert system.violation_count == 0

    def test_telegram_alert_structure(self):
        """Test Telegram alert message"""
        bot = TelegramBot(token="", chat_id="")
        
        violation_data = {
            "timestamp": "2024-01-01T10:00:00",
            "camera": "entrance",
            "location": "Parking Lot A",
            "plate_number": "ABC123",
            "confidence": 0.95,
            "image_path": None
        }
        
        # Alert should construct message even if sending fails
        result = bot.send_alert(violation_data)
        # Result is False because no valid token/chat_id, but alert was attempted
        assert isinstance(result, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
=======
"""
Tests for AI detector, Telegram bot, and integration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from src.AI.detector import ParkingDetector
from src.notify.telegram_bot import TelegramBot
from src.parking_system import ParkingDetectionSystem


class TestParkingDetector:
    """Test parking detector"""

    def test_init(self):
        """Test detector initialization"""
        detector = ParkingDetector("yolov8n.pt", confidence_threshold=0.5)
        assert detector.model_path == "yolov8n.pt"
        assert detector.confidence_threshold == 0.5

    def test_get_info(self):
        """Test getting detector info"""
        detector = ParkingDetector("yolov8n.pt")
        info = detector.get_info()
        
        assert "model_path" in info
        assert "loaded" in info
        assert "confidence_threshold" in info

    def test_detect_no_model(self):
        """Test detection without loaded model"""
        detector = ParkingDetector("yolov8n.pt")
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        detections = detector.detect(frame)
        assert detections == []

    def test_is_violation(self):
        """Test violation check"""
        detector = ParkingDetector("yolov8n.pt")
        detection = {
            "class_id": 2,
            "class_name": "car",
            "confidence": 0.8,
            "bbox": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}
        }
        
        result = detector.is_violation(detection)
        assert isinstance(result, bool)


class TestTelegramBot:
    """Test Telegram bot"""

    def test_init(self):
        """Test bot initialization"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        assert bot.token == "test_token"
        assert bot.chat_id == "12345"

    def test_get_info(self):
        """Test getting bot info"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        info = bot.get_info()
        
        assert "token" in info
        assert "chat_id" in info
        assert info["chat_id"] == "12345"

    def test_register_handler(self):
        """Test registering command handler"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        handler = Mock()
        
        bot.register_handler("start", handler)
        
        assert "start" in bot.handlers
        assert bot.handlers["start"] == handler

    def test_send_message_no_bot(self):
        """Test sending message without bot"""
        bot = TelegramBot(token="", chat_id="12345")
        result = bot.send_message("Test message")
        assert result is False

    def test_send_photo_no_file(self):
        """Test sending non-existent photo"""
        bot = TelegramBot(token="test_token", chat_id="12345")
        result = bot.send_photo("/nonexistent/file.jpg")
        assert result is False

    def test_send_alert_structure(self):
        """Test alert message structure"""
        bot = TelegramBot(token="", chat_id="12345")
        
        violation_data = {
            "timestamp": "2024-01-01T10:00:00",
            "camera": "entrance",
            "location": "Parking Lot A",
            "plate_number": "ABC123",
            "confidence": 0.95
        }
        
        # Since we don't have token, it should return False
        result = bot.send_alert(violation_data)
        assert result is False


class TestParkingDetectionSystem:
    """Test integrated system"""

    def test_init(self):
        """Test system initialization"""
        system = ParkingDetectionSystem(enable_telegram=False)
        assert system.camera_manager is not None
        assert system.running is False
        assert system.violation_count == 0

    @patch('src.camera.camera_manager.CameraManager.add_camera')
    def test_add_camera(self, mock_add):
        """Test adding camera to system"""
        mock_add.return_value = True
        
        system = ParkingDetectionSystem(enable_telegram=False)
        result = system.add_camera("cam1", 0, "Camera 1")
        
        assert result is True

    def test_get_statistics(self):
        """Test getting system statistics"""
        system = ParkingDetectionSystem(enable_telegram=False)
        stats = system.get_statistics()
        
        assert "running" in stats
        assert "total_violations" in stats
        assert "active_cameras" in stats
        assert stats["running"] is False
        assert stats["total_violations"] == 0

    @patch('src.camera.camera_manager.CameraManager.add_camera')
    def test_connect_to_multiple_cameras(self, mock_add):
        """Test connecting to multiple cameras"""
        mock_add.return_value = True
        
        system = ParkingDetectionSystem(enable_telegram=False)
        
        configs = [
            {"id": "cam1", "source": 0, "name": "Entrance"},
            {"id": "cam2", "source": "rtsp://camera", "name": "Exit"},
        ]
        
        connected = system.connect_to_all_cameras(configs)
        assert connected == 2

    def test_pause_resume(self):
        """Test pause and resume"""
        system = ParkingDetectionSystem(enable_telegram=False)
        
        assert system.is_paused is False
        system.pause()
        assert system.is_paused is True
        system.resume()
        assert system.is_paused is False

    def test_context_manager(self):
        """Test context manager"""
        with ParkingDetectionSystem(enable_telegram=False) as system:
            assert system is not None
            assert system.running is False


class TestIntegration:
    """Integration tests"""

    @patch('src.camera.camera_handler.CameraHandler.connect')
    @patch('src.camera.camera_handler.CameraHandler.get_frame')
    def test_full_flow(self, mock_get_frame, mock_connect):
        """Test full detection flow"""
        mock_connect.return_value = True
        mock_get_frame.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        
        system = ParkingDetectionSystem(enable_telegram=False)
        system.add_camera("cam1", 0, "Test Camera")
        
        assert "cam1" in system.camera_manager.cameras
        assert system.violation_count == 0

    def test_telegram_alert_structure(self):
        """Test Telegram alert message"""
        bot = TelegramBot(token="", chat_id="")
        
        violation_data = {
            "timestamp": "2024-01-01T10:00:00",
            "camera": "entrance",
            "location": "Parking Lot A",
            "plate_number": "ABC123",
            "confidence": 0.95,
            "image_path": None
        }
        
        # Alert should construct message even if sending fails
        result = bot.send_alert(violation_data)
        # Result is False because no valid token/chat_id, but alert was attempted
        assert isinstance(result, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
