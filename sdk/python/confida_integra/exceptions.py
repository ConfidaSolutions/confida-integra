"""Exception hierarchy for the Confida Integra client."""
from __future__ import annotations


class ConfidaError(Exception):
    """Base class for all client errors."""


class APIError(ConfidaError):
    """A non-success HTTP response from the API."""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}" if message else f"HTTP {status_code}")


class AuthError(APIError):
    """401 — missing or invalid bearer token."""


class NotFoundError(APIError):
    """404 — the requested resource does not exist."""


class RateLimitError(APIError):
    """429 — per-token rate limit exceeded."""


def raise_for_status(status_code: int, detail: str = "") -> None:
    """Map an HTTP status to the appropriate exception (no-op for 2xx/304)."""
    if status_code < 400:
        return
    if status_code == 401:
        raise AuthError(status_code, detail or "unauthorized")
    if status_code == 404:
        raise NotFoundError(status_code, detail or "not found")
    if status_code == 429:
        raise RateLimitError(status_code, detail or "rate limit exceeded")
    raise APIError(status_code, detail)
