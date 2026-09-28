"""API bearer-token gate for triage endpoints."""

from __future__ import annotations

import hmac
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=False)


def _expected_token() -> str:
    # Prefer dedicated triage token; fall back to generic API token.
    token = (os.getenv("ALERTSENTRY_API_TOKEN") or os.getenv("API_TOKEN") or "").strip()
    return token


def require_api_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    """Require Authorization: Bearer <token>. Health stays public."""
    expected = _expected_token()
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API token not configured (set ALERTSENTRY_API_TOKEN)",
        )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    provided = credentials.credentials.strip()
    if not hmac.compare_digest(provided, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return provided
