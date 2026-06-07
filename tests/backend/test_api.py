"""
Basic test for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.backend.main import app


@pytest.fixture
def client():
    """Fixture for test client"""
    return TestClient(app)


def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.integration
def test_list_violations(client):
    """Test list violations endpoint"""
    response = client.get("/api/v1/violations/")
    assert response.status_code == 200
