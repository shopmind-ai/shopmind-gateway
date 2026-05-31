import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


def test_login_success(client):
    mock_user = {"id": 1, "username": "demo", "hashed_password": "$2b$12$placeholder"}
    with patch("routers.auth.get_user_by_username", return_value=mock_user), \
         patch("routers.auth.verify_password", return_value=True):
        resp = client.post("/auth/login", json={"username": "demo", "password": "shopmind2026"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()


def test_login_wrong_password(client):
    mock_user = {"id": 1, "username": "demo", "hashed_password": "$2b$12$placeholder"}
    with patch("routers.auth.get_user_by_username", return_value=mock_user), \
         patch("routers.auth.verify_password", return_value=False):
        resp = client.post("/auth/login", json={"username": "demo", "password": "wrong"})
    assert resp.status_code == 401


def test_login_user_not_found(client):
    with patch("routers.auth.get_user_by_username", return_value=None):
        resp = client.post("/auth/login", json={"username": "noone", "password": "x"})
    assert resp.status_code == 401


def test_protected_route_without_token(client):
    resp = client.get("/api/v1/usage/summary")
    assert resp.status_code == 401


def test_protected_route_with_valid_token(client):
    from utils.jwt import create_access_token
    token = create_access_token("demo")
    with patch("routers.usage.get_usage_summary", return_value={"by_agent": []}):
        resp = client.get("/api/v1/usage/summary", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
