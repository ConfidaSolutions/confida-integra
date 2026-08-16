# confida-integra-client

Python client for the [Confida Integra](https://confida.solutions) northbound
API — a read-only, paged, ETag-cached interface to a live register of OpenShift
and Proxmox integrations.

> **Availability.** The PyPI package name `confida-integra-client` and the
> repository `github.com/ConfidaSolutions/confida-integra` are the intended
> canonical locations; check the vendor site for live links.

## Install

```bash
pip install confida-integra-client
```

## Quickstart (sync)

```python
from confida_integra import Client

with Client("https://your-host", token="cnf_v1_<id><secret>") as c:
    print(c.meta().product_version)

    for i in c.integrations(env="production", source="proxmox"):
        print(i.id, i.source_system, "->", i.destination_system, f"[{i.status}]")

    s = c.stats()
    print(s.total_integrations, "integrations across", s.total_systems, "systems")
```

## Quickstart (async)

```python
import asyncio
from confida_integra import AsyncClient

async def main():
    async with AsyncClient("https://your-host", token="cnf_v1_...") as c:
        async for i in c.integrations(criticality=["high", "critical"]):
            print(i.id, i.criticality)

asyncio.run(main())
```

## Filtering

`integrations()` accepts the northbound filters and auto-paginates:

```python
c.integrations(
    env=["production", "qa"],     # repeatable; "prod" short form also accepted
    status="active",
    criticality=["high", "critical"],
    source="proxmox",
    system="crm",                 # substring match on source/destination
    team="integration",
    updated_since=datetime(2026, 6, 1, tzinfo=timezone.utc),  # or an RFC3339 str
    fields=["id", "source_system", "destination_system", "status"],
    per_page=200,
)
```

## Models

`Integration`, `Stats` and `Meta` are forward-compatible: documented fields are
typed attributes, and the full payload is always available via `.raw` (and
`integration["any_field"]`), so new API fields never break your code.

## Errors

```python
from confida_integra import AuthError, NotFoundError, RateLimitError, APIError

try:
    c.integration("does-not-exist")
except NotFoundError:
    ...
except RateLimitError:
    ...   # back off and retry
except AuthError:
    ...   # bad/expired token
```

## Caching

The client transparently sends `If-None-Match` with the last `ETag` it saw for
an identical request and returns the cached payload on a `304`. Repeated polling
of unchanged data is cheap.

## License

Apache-2.0. See the repository `LICENSE`.
