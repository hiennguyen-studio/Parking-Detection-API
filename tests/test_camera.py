<<<<<<< HEAD
"""
Test camera module
"""
import pytest
import cv2
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.camera import CameraHandler, StreamProcessor, CameraManager


class TestCameraHandler:
    """Test CameraHandler class"""

    def test_init(self):
        """Test camera initialization"""
        handler = CameraHandler(camera_source=0, name="Test Camera")
        assert handler.camera_source == 0
        assert handler.name == "Test Camera"
        assert not handler.is_connected

    @patch('cv2.VideoCapture')
    def test_connect_success(self, mock_capture):
        """Test successful camera connection"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        result = handler.connect()
        
        assert result is True
        assert handler.is_connected is True

    @patch('cv2.VideoCapture')
    def test_connect_failure(self, mock_capture):
        """Test failed camera connection"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        result = handler.connect()
        
        assert result is False
        assert handler.is_connected is False

    @patch('cv2.VideoCapture')
    def test_get_frame(self, mock_capture):
        """Test getting frame from camera"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, frame)
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        handler.connect()
        result = handler.get_frame()
        
        assert result is not None
        ret, captured_frame = result
        assert ret is True
        assert captured_frame is not None

    @patch('cv2.VideoCapture')
    @patch('cv2.imwrite')
    def test_save_frame(self, mock_imwrite, mock_capture):
        """Test saving frame"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        mock_imwrite.return_value = True
        
        handler = CameraHandler()
        handler.connect()
        
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = handler.save_frame(frame, "/tmp/test.jpg")
        
        assert result is True

    def test_get_info(self):
        """Test getting camera info"""
        handler = CameraHandler(camera_source=0, name="Test Camera")
        info = handler.get_info()
        
        assert info["name"] == "Test Camera"
        assert info["source"] == 0
        assert info["is_connected"] is False


class TestStreamProcessor:
    """Test StreamProcessor class"""

    @patch('cv2.VideoCapture')
    def test_init(self, mock_capture):
        """Test processor initialization"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        assert processor.camera_handler == camera
        assert processor.is_running is False

    @patch('cv2.VideoCapture')
    def test_add_callback(self, mock_capture):
        """Test adding callback"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        callback = Mock()
        processor.add_callback(callback)
        
        assert callback in processor.callbacks

    @patch('cv2.VideoCapture')
    def test_start_stop(self, mock_capture):
        """Test start and stop"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        assert processor.start() is True
        assert processor.is_running is True
        
        processor.stop()
        assert processor.is_running is False

    @patch('cv2.VideoCapture')
    def test_get_statistics(self, mock_capture):
        """Test getting statistics"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        stats = processor.get_statistics()
        
        assert "total_frames" in stats
        assert "processed_frames" in stats
        assert "violations_found" in stats


class TestCameraManager:
    """Test CameraManager class"""

    def test_init(self):
        """Test manager initialization"""
        manager = CameraManager()
        assert len(manager.cameras) == 0
        assert len(manager.processors) == 0

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_add_camera(self, mock_connect):
        """Test adding camera"""
        mock_connect.return_value = True
        
        manager = CameraManager()
        result = manager.add_camera("cam1", 0, "Test Camera")
        
        assert result is True
        assert "cam1" in manager.cameras

    def test_get_camera(self):
        """Test getting camera"""
        manager = CameraManager()
        handler = CameraHandler()
        manager.cameras["cam1"] = handler
        
        cam = manager.get_camera("cam1")
        assert cam == handler

    @patch('src.camera.camera_handler.CameraHandler.disconnect')
    def test_remove_camera(self, mock_disconnect):
        """Test removing camera"""
        manager = CameraManager()
        handler = CameraHandler()
        processor = StreamProcessor(handler)
        
        manager.cameras["cam1"] = handler
        manager.processors["cam1"] = processor
        
        result = manager.remove_camera("cam1")
        
        assert result is True
        assert "cam1" not in manager.cameras

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_get_all_cameras(self, mock_connect):
        """Test getting all cameras info"""
        mock_connect.return_value = True
        
        manager = CameraManager()
        manager.add_camera("cam1", 0, "Camera 1")
        manager.add_camera("cam2", 1, "Camera 2")
        
        cameras = manager.get_all_cameras()
        
        assert len(cameras) == 2
        assert "cam1" in cameras
        assert "cam2" in cameras

    @patch('src.camera.camera_handler.CameraHandler.disconnect')
    def test_disconnect_all(self, mock_disconnect):
        """Test disconnecting all cameras"""
        manager = CameraManager()
        handler = CameraHandler()
        processor = StreamProcessor(handler)
        
        manager.cameras["cam1"] = handler
        manager.processors["cam1"] = processor
        
        manager.disconnect_all()
        
        assert len(manager.cameras) == 0

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_context_manager(self, mock_connect):
        """Test context manager"""
        mock_connect.return_value = True
        
        with CameraManager() as manager:
            manager.add_camera("cam1", 0, "Camera 1")
            assert "cam1" in manager.cameras
        
        assert len(manager.cameras) == 0
=======
"""
Test camera module
"""
import pytest
import cv2
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.camera import CameraHandler, StreamProcessor, CameraManager


class TestCameraHandler:
    """Test CameraHandler class"""

    def test_init(self):
        """Test camera initialization"""
        handler = CameraHandler(camera_source=0, name="Test Camera")
        assert handler.camera_source == 0
        assert handler.name == "Test Camera"
        assert not handler.is_connected

    @patch('cv2.VideoCapture')
    def test_connect_success(self, mock_capture):
        """Test successful camera connection"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        result = handler.connect()
        
        assert result is True
        assert handler.is_connected is True

    @patch('cv2.VideoCapture')
    def test_connect_failure(self, mock_capture):
        """Test failed camera connection"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        result = handler.connect()
        
        assert result is False
        assert handler.is_connected is False

    @patch('cv2.VideoCapture')
    def test_get_frame(self, mock_capture):
        """Test getting frame from camera"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, frame)
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        handler = CameraHandler()
        handler.connect()
        result = handler.get_frame()
        
        assert result is not None
        ret, captured_frame = result
        assert ret is True
        assert captured_frame is not None

    @patch('cv2.VideoCapture')
    @patch('cv2.imwrite')
    def test_save_frame(self, mock_imwrite, mock_capture):
        """Test saving frame"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        mock_imwrite.return_value = True
        
        handler = CameraHandler()
        handler.connect()
        
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = handler.save_frame(frame, "/tmp/test.jpg")
        
        assert result is True

    def test_get_info(self):
        """Test getting camera info"""
        handler = CameraHandler(camera_source=0, name="Test Camera")
        info = handler.get_info()
        
        assert info["name"] == "Test Camera"
        assert info["source"] == 0
        assert info["is_connected"] is False


class TestStreamProcessor:
    """Test StreamProcessor class"""

    @patch('cv2.VideoCapture')
    def test_init(self, mock_capture):
        """Test processor initialization"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        assert processor.camera_handler == camera
        assert processor.is_running is False

    @patch('cv2.VideoCapture')
    def test_add_callback(self, mock_capture):
        """Test adding callback"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        callback = Mock()
        processor.add_callback(callback)
        
        assert callback in processor.callbacks

    @patch('cv2.VideoCapture')
    def test_start_stop(self, mock_capture):
        """Test start and stop"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        assert processor.start() is True
        assert processor.is_running is True
        
        processor.stop()
        assert processor.is_running is False

    @patch('cv2.VideoCapture')
    def test_get_statistics(self, mock_capture):
        """Test getting statistics"""
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda x: 640 if x == 3 else (480 if x == 4 else 30)
        mock_capture.return_value = mock_cap
        
        camera = CameraHandler()
        camera.connect()
        processor = StreamProcessor(camera)
        
        stats = processor.get_statistics()
        
        assert "total_frames" in stats
        assert "processed_frames" in stats
        assert "violations_found" in stats


class TestCameraManager:
    """Test CameraManager class"""

    def test_init(self):
        """Test manager initialization"""
        manager = CameraManager()
        assert len(manager.cameras) == 0
        assert len(manager.processors) == 0

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_add_camera(self, mock_connect):
        """Test adding camera"""
        mock_connect.return_value = True
        
        manager = CameraManager()
        result = manager.add_camera("cam1", 0, "Test Camera")
        
        assert result is True
        assert "cam1" in manager.cameras

    def test_get_camera(self):
        """Test getting camera"""
        manager = CameraManager()
        handler = CameraHandler()
        manager.cameras["cam1"] = handler
        
        cam = manager.get_camera("cam1")
        assert cam == handler

    @patch('src.camera.camera_handler.CameraHandler.disconnect')
    def test_remove_camera(self, mock_disconnect):
        """Test removing camera"""
        manager = CameraManager()
        handler = CameraHandler()
        processor = StreamProcessor(handler)
        
        manager.cameras["cam1"] = handler
        manager.processors["cam1"] = processor
        
        result = manager.remove_camera("cam1")
        
        assert result is True
        assert "cam1" not in manager.cameras

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_get_all_cameras(self, mock_connect):
        """Test getting all cameras info"""
        mock_connect.return_value = True
        
        manager = CameraManager()
        manager.add_camera("cam1", 0, "Camera 1")
        manager.add_camera("cam2", 1, "Camera 2")
        
        cameras = manager.get_all_cameras()
        
        assert len(cameras) == 2
        assert "cam1" in cameras
        assert "cam2" in cameras

    @patch('src.camera.camera_handler.CameraHandler.disconnect')
    def test_disconnect_all(self, mock_disconnect):
        """Test disconnecting all cameras"""
        manager = CameraManager()
        handler = CameraHandler()
        processor = StreamProcessor(handler)
        
        manager.cameras["cam1"] = handler
        manager.processors["cam1"] = processor
        
        manager.disconnect_all()
        
        assert len(manager.cameras) == 0

    @patch('src.camera.camera_handler.CameraHandler.connect')
    def test_context_manager(self, mock_connect):
        """Test context manager"""
        mock_connect.return_value = True
        
        with CameraManager() as manager:
            manager.add_camera("cam1", 0, "Camera 1")
            assert "cam1" in manager.cameras
        
        assert len(manager.cameras) == 0
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
