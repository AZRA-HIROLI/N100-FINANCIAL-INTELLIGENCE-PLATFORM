import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_screener_valid():
    response = client.get("/api/v1/screener?min_roe=15")
    assert response.status_code == 200
    assert "results" in response.json()

def test_screener_invalid_param():
    response = client.get("/api/v1/screener?min_roe=150")
    assert response.status_code == 400
