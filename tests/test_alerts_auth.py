"""Unauthenticated triage routes must be rejected."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.api.deps.auth import require_api_token


def _build_app() -> FastAPI:
    app = FastAPI()

    @app.post("/api/v1/alerts")
    async def _alerts(_auth: str = Depends(require_api_token)) -> dict:
        return {"ok": True}

    @app.get("/api/v1/health")
    async def _health() -> dict:
        return {"status": "ok"}

    return app


def test_alerts_post_without_auth_returns_401(monkeypatch):
    monkeypatch.setenv("ALERTSENTRY_API_TOKEN", "test-secret-token")
    resp = TestClient(_build_app()).post("/api/v1/alerts", json={})
    assert resp.status_code == 401


def test_alerts_post_with_bad_token_returns_401(monkeypatch):
    monkeypatch.setenv("ALERTSENTRY_API_TOKEN", "test-secret-token")
    resp = TestClient(_build_app()).post(
        "/api/v1/alerts",
        headers={"Authorization": "Bearer wrong"},
        json={},
    )
    assert resp.status_code == 401


def test_alerts_post_with_good_token_returns_200(monkeypatch):
    monkeypatch.setenv("ALERTSENTRY_API_TOKEN", "test-secret-token")
    resp = TestClient(_build_app()).post(
        "/api/v1/alerts",
        headers={"Authorization": "Bearer test-secret-token"},
        json={},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_alerts_post_without_configured_token_returns_503(monkeypatch):
    monkeypatch.delenv("ALERTSENTRY_API_TOKEN", raising=False)
    monkeypatch.delenv("API_TOKEN", raising=False)
    resp = TestClient(_build_app()).post(
        "/api/v1/alerts",
        headers={"Authorization": "Bearer anything"},
        json={},
    )
    assert resp.status_code == 503


def test_health_stays_public(monkeypatch):
    monkeypatch.delenv("ALERTSENTRY_API_TOKEN", raising=False)
    resp = TestClient(_build_app()).get("/api/v1/health")
    assert resp.status_code == 200
