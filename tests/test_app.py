import os
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_generate_and_retrieve():
    payload = {
        "name": "Test User",
        "user_id": "TEST001",
        "age": "20",
        "weight": "60",
        "goal": "general wellness",
        "intensity": "low",
    }
    response = client.post("/generate-workout", data=payload)
    assert response.status_code == 200
    assert "7-Day Workout Plan" in response.text

    response = client.get("/api/users/TEST001")
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "Test User"

    client.post("/delete-user/TEST001")
