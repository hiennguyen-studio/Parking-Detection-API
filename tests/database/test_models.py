<<<<<<< HEAD
"""
Basic test for database models
"""
import pytest
from src.database.models import User, Camera, Violation


def test_user_model():
    """Test user model creation"""
    user = User(username="testuser", email="test@example.com", hashed_password="hashed")
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_camera_model():
    """Test camera model creation"""
    camera = Camera(name="Camera 1", location="Intersection A", stream_url="rtsp://stream.url")
    assert camera.name == "Camera 1"
    assert camera.location == "Intersection A"


@pytest.mark.unit
def test_violation_model():
    """Test violation model creation"""
    violation = Violation(
        camera_id=1,
        plate_number="30A12345",
        confidence=0.95,
        image_path="/path/to/image.jpg",
        latitude=21.0285,
        longitude=105.8542
    )
    assert violation.plate_number == "30A12345"
    assert violation.confidence == 0.95
=======
"""
Basic test for database models
"""
import pytest
from src.database.models import User, Camera, Violation


def test_user_model():
    """Test user model creation"""
    user = User(username="testuser", email="test@example.com", hashed_password="hashed")
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_camera_model():
    """Test camera model creation"""
    camera = Camera(name="Camera 1", location="Intersection A", stream_url="rtsp://stream.url")
    assert camera.name == "Camera 1"
    assert camera.location == "Intersection A"


@pytest.mark.unit
def test_violation_model():
    """Test violation model creation"""
    violation = Violation(
        camera_id=1,
        plate_number="30A12345",
        confidence=0.95,
        image_path="/path/to/image.jpg",
        latitude=21.0285,
        longitude=105.8542
    )
    assert violation.plate_number == "30A12345"
    assert violation.confidence == 0.95
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
