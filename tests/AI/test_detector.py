"""
Basic test for detector
"""
import pytest
from src.AI.detector import ParkingDetector


@pytest.fixture
def detector():
    """Fixture for detector instance"""
    return ParkingDetector(model_path="./data/models/")


def test_detector_initialization(detector):
    """Test detector initialization"""
    assert detector is not None
    assert detector.model_path == "./data/models/"


@pytest.mark.unit
def test_detector_model_loading(detector):
    """Test model loading"""
    # TODO: Implement test
    pass
