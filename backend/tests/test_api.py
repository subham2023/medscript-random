from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Welcome to MedScript AI"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"
