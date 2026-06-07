"""
Basic test for camera handler
"""
import pytest
from src.camera.camera_handler import CameraHandler


@pytest.fixture
def camera():
    """Fixture for camera handler"""
    return CameraHandler(camera_id=0)


def test_camera_initialization(camera):
    """Test camera initialization"""
    assert camera is not None
    assert camera.camera_id == 0


@pytest.mark.unit
def test_camera_connection(camera):
    """Test camera connection"""
    # TODO: Implement test
    pass
