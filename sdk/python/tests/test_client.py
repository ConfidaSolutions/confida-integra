"""Tests for the sync + async clients. Uses respx to mock the httpx transport."""
import httpx
import pytest
import respx

from confida_integra import (
    AsyncClient,
    AuthError,
    Client,
    NotFoundError,
    RateLimitError,
)

BASE = "https://host"
TOKEN = "cnf_v1_deadbeefcafef00d-secret"


def _page(items, page=1, total_pages=1, total=None):
    return {
        "data": items,
        "pagination": {"page": page, "per_page": 100,
                       "total_items": total if total is not None else len(items),
                       "total_pages": total_pages},
        "links": {"self": "", "first": "", "last": "", "prev": None, "next": None},
        "generated_at": "2026-06-09T00:00:00Z",
    }


def _node(i):
    return {"id": i, "source_system": "a", "destination_system": "b",
            "protocol": "rest-json → sql", "environment": "production",
            "status": "active", "source": "proxmox", "extra": {"criticality": "high"}}


@respx.mock
def test_token_required():
    with pytest.raises(ValueError):
        Client(BASE, token="")


@respx.mock
def test_integrations_single_page():
    respx.get(f"{BASE}/api/v1/integrations").mock(
        return_value=httpx.Response(200, json=_page([_node("x1"), _node("x2")]),
                                    headers={"ETag": '"e1"'}))
    with Client(BASE, token=TOKEN) as c:
        out = list(c.integrations(env="production", source="proxmox"))
    assert [i.id for i in out] == ["x1", "x2"]
    assert out[0].criticality == "high"
    # filters forwarded
    req = respx.calls.last.request
    assert "env=production" in str(req.url)
    assert "source=proxmox" in str(req.url)


@respx.mock
def test_integrations_paginates():
    route = respx.get(f"{BASE}/api/v1/integrations")
    route.side_effect = [
        httpx.Response(200, json=_page([_node("a")], page=1, total_pages=2, total=2)),
        httpx.Response(200, json=_page([_node("b")], page=2, total_pages=2, total=2)),
    ]
    with Client(BASE, token=TOKEN) as c:
        out = [i.id for i in c.integrations()]
    assert out == ["a", "b"]


@respx.mock
def test_etag_304_returns_cached():
    route = respx.get(f"{BASE}/api/v1/integrations")
    route.side_effect = [
        httpx.Response(200, json=_page([_node("a")]), headers={"ETag": '"v1"'}),
        httpx.Response(304),
    ]
    with Client(BASE, token=TOKEN) as c:
        first = [i.id for i in c.integrations()]
        second = [i.id for i in c.integrations()]
    assert first == second == ["a"]
    assert respx.calls.last.request.headers.get("If-None-Match") == '"v1"'


@respx.mock
def test_single_and_errors():
    respx.get(f"{BASE}/api/v1/integrations/x1").mock(
        return_value=httpx.Response(200, json={"data": _node("x1"), "generated_at": "t"}))
    respx.get(f"{BASE}/api/v1/integrations/missing").mock(
        return_value=httpx.Response(404, json={"detail": "not found"}))
    with Client(BASE, token=TOKEN) as c:
        assert c.integration("x1").id == "x1"
        with pytest.raises(NotFoundError):
            c.integration("missing")


@respx.mock
def test_auth_and_ratelimit():
    respx.get(f"{BASE}/api/v1/meta").mock(return_value=httpx.Response(401, json={"detail": "bad token"}))
    respx.get(f"{BASE}/api/v1/stats").mock(return_value=httpx.Response(429, json={"detail": "slow down"}))
    with Client(BASE, token=TOKEN) as c:
        with pytest.raises(AuthError):
            c.meta()
        with pytest.raises(RateLimitError):
            c.stats()


@respx.mock
def test_stats_and_meta():
    respx.get(f"{BASE}/api/v1/stats").mock(return_value=httpx.Response(
        200, json={"data": {"total_integrations": 3, "total_systems": 2,
                            "by_status": {"active": 3}}, "generated_at": "t"}))
    respx.get(f"{BASE}/api/v1/meta").mock(return_value=httpx.Response(
        200, json={"api_version": "1.0", "schema_version": 10,
                   "product_version": "0.9.6", "data_source": "live", "node_count": 3}))
    with Client(BASE, token=TOKEN) as c:
        assert c.stats().total_integrations == 3
        assert c.meta().product_version == "0.9.6"


@respx.mock
async def test_async_client():
    respx.get(f"{BASE}/api/v1/integrations").mock(
        return_value=httpx.Response(200, json=_page([_node("z")])))
    async with AsyncClient(BASE, token=TOKEN) as c:
        out = [i.id async for i in c.integrations()]
    assert out == ["z"]
