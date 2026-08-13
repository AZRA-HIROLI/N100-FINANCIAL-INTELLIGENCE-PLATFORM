import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert "companies" in data

def test_get_company_profile_valid():
    response = client.get("/api/v1/companies/TCS")
    assert response.status_code == 200
    assert response.json()["ticker"] == "TCS"

def test_get_company_profile_invalid():
    response = client.get("/api/v1/companies/INVALID_TICKER")
    assert response.status_code == 404
