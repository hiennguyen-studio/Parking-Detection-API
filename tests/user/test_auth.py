"""
Basic test for authentication
"""
import pytest
from src.user.auth import AuthManager


@pytest.fixture
def auth_manager():
    """Fixture for auth manager"""
    return AuthManager(secret_key="test-secret-key")


def test_auth_initialization(auth_manager):
    """Test auth manager initialization"""
    assert auth_manager is not None
    assert auth_manager.secret_key == "test-secret-key"


@pytest.mark.unit
def test_password_hashing(auth_manager):
    """Test password hashing"""
    # TODO: Implement test
    pass
