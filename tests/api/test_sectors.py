import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200
    assert "sectors" in response.json()

def test_get_sector_companies_valid():
    response = client.get("/api/v1/sectors/IT/companies")
    assert response.status_code == 200

def test_get_sector_companies_invalid():
    response = client.get("/api/v1/sectors/UNKNOWN_SECTOR/companies")
    assert response.status_code == 404
