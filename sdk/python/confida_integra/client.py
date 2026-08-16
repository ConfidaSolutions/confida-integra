"""Sync and async clients for the Confida Integra northbound API."""
from __future__ import annotations

from typing import Any, AsyncIterator, Iterator

import httpx

from .exceptions import raise_for_status
from .models import Integration, Meta, Stats

_DEFAULT_TIMEOUT = 30.0


def _prepare_params(filters: dict[str, Any]) -> dict[str, Any]:
    """Translate keyword filters into northbound API query parameters."""
    params: dict[str, Any] = {}
    for key in ("env", "status", "criticality"):
        v = filters.get(key)
        if v is None:
            continue
        params[key] = list(v) if isinstance(v, (list, tuple, set)) else [v]
    for key in ("source", "system", "team"):
        if filters.get(key):
            params[key] = filters[key]
    fields = filters.get("fields")
    if fields:
        params["fields"] = ",".join(fields) if isinstance(fields, (list, tuple)) else fields
    us = filters.get("updated_since")
    if us is not None:
        params["updated_since"] = us.isoformat() if hasattr(us, "isoformat") else us
    if filters.get("per_page"):
        params["per_page"] = filters["per_page"]
    if filters.get("page"):
        params["page"] = filters["page"]
    return params


def _cache_key(path: str, params: dict[str, Any]) -> str:
    return path + "?" + str(sorted(params.items()))


def _detail(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        if isinstance(body, dict):
            return body.get("detail") or body.get("error") or ""
    except Exception:
        pass
    return ""


class _Base:
    def __init__(self, base_url: str, token: str, *, verify: bool = True,
                 timeout: float = _DEFAULT_TIMEOUT):
        if not token:
            raise ValueError("an API token is required")
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        self._verify = verify
        self._timeout = timeout
        self._etag: dict[str, tuple[str, Any]] = {}


class Client(_Base):
    """Synchronous client.

    >>> with Client("https://host", token="cnf_v1_...") as c:
    ...     for i in c.integrations(env="production", source="proxmox"):
    ...         print(i.id, i.source_system, "->", i.destination_system)
    """

    def __init__(self, base_url: str, token: str, **kw: Any):
        super().__init__(base_url, token, **kw)
        self._client = httpx.Client(base_url=self._base_url, headers=self._headers,
                                    verify=self._verify, timeout=self._timeout)

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = params or {}
        key = _cache_key(path, params)
        headers = {}
        cached = self._etag.get(key)
        if cached:
            headers["If-None-Match"] = cached[0]
        resp = self._client.get(path, params=params, headers=headers)
        if resp.status_code == 304 and cached:
            return cached[1]
        raise_for_status(resp.status_code, _detail(resp))
        body = resp.json()
        etag = resp.headers.get("ETag")
        if etag:
            self._etag[key] = (etag, body)
        return body

    def integrations(self, **filters: Any) -> Iterator[Integration]:
        """Yield every integration matching the filters, auto-paginating."""
        params = _prepare_params(filters)
        page = params.get("page", 1)
        while True:
            params["page"] = page
            env = self._get("/api/v1/integrations", params)
            for item in env.get("data", []):
                yield Integration.from_dict(item)
            pg = env.get("pagination", {})
            if page >= pg.get("total_pages", page):
                break
            page += 1

    def integration(self, integration_id: str) -> Integration:
        env = self._get(f"/api/v1/integrations/{integration_id}")
        return Integration.from_dict(env["data"])

    def stats(self) -> Stats:
        return Stats.from_dict(self._get("/api/v1/stats")["data"])

    def meta(self) -> Meta:
        return Meta.from_dict(self._get("/api/v1/meta"))


class AsyncClient(_Base):
    """Asynchronous client (same surface as :class:`Client`)."""

    def __init__(self, base_url: str, token: str, **kw: Any):
        super().__init__(base_url, token, **kw)
        self._client = httpx.AsyncClient(base_url=self._base_url, headers=self._headers,
                                         verify=self._verify, timeout=self._timeout)

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = params or {}
        key = _cache_key(path, params)
        headers = {}
        cached = self._etag.get(key)
        if cached:
            headers["If-None-Match"] = cached[0]
        resp = await self._client.get(path, params=params, headers=headers)
        if resp.status_code == 304 and cached:
            return cached[1]
        raise_for_status(resp.status_code, _detail(resp))
        body = resp.json()
        etag = resp.headers.get("ETag")
        if etag:
            self._etag[key] = (etag, body)
        return body

    async def integrations(self, **filters: Any) -> AsyncIterator[Integration]:
        params = _prepare_params(filters)
        page = params.get("page", 1)
        while True:
            params["page"] = page
            env = await self._get("/api/v1/integrations", params)
            for item in env.get("data", []):
                yield Integration.from_dict(item)
            pg = env.get("pagination", {})
            if page >= pg.get("total_pages", page):
                break
            page += 1

    async def integration(self, integration_id: str) -> Integration:
        env = await self._get(f"/api/v1/integrations/{integration_id}")
        return Integration.from_dict(env["data"])

    async def stats(self) -> Stats:
        return Stats.from_dict((await self._get("/api/v1/stats"))["data"])

    async def meta(self) -> Meta:
        return Meta.from_dict(await self._get("/api/v1/meta"))
