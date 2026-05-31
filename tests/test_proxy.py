import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from utils.jwt import create_access_token


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {create_access_token('demo')}"}


def _make_async_client_mock(method: str, response_data: dict, status_code: int = 200):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = response_data

    mock_client = AsyncMock()
    setattr(mock_client, method, AsyncMock(return_value=mock_response))

    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_client)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)
    return mock_ctx


def test_invoke_known_agent_success(client, auth_headers):
    mock_ctx = _make_async_client_mock("post", {
        "cleaned_data": [],
        "report": {},
        "usage": {"input_tokens": 100, "output_tokens": 50},
    })
    with patch("routers.proxy.httpx.AsyncClient", return_value=mock_ctx), \
         patch("routers.proxy.log_usage"):
        resp = client.post(
            "/api/v1/cleaning/invoke",
            json={"data": [], "data_type": "products"},
            headers=auth_headers,
        )
    assert resp.status_code == 200


def test_invoke_unknown_agent_returns_404(client, auth_headers):
    resp = client.post("/api/v1/unknown/invoke", json={}, headers=auth_headers)
    assert resp.status_code == 404


def test_invoke_without_auth_returns_401(client):
    resp = client.post("/api/v1/cleaning/invoke", json={})
    assert resp.status_code == 401


def test_health_check_proxied(client, auth_headers):
    mock_ctx = _make_async_client_mock("get", {"status": "ok"})
    with patch("routers.proxy.httpx.AsyncClient", return_value=mock_ctx):
        resp = client.get("/api/v1/cleaning/health", headers=auth_headers)
    assert resp.status_code == 200
