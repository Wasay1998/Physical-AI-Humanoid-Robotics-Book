import pytest
from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "RAG Chatbot API for Interactive Books"


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"


def test_ingest_endpoint_exists():
    """Test that the ingest endpoint is available"""
    # This will return 405 since it requires POST with proper form data
    response = client.get("/api/v1/ingest")
    assert response.status_code in [405, 422]  # Method not allowed or validation error is expected


def test_query_endpoint_exists():
    """Test that the query endpoint is available"""
    # This will return 422 since it requires proper JSON body
    response = client.get("/api/v1/query")
    assert response.status_code == 422  # Validation error is expected