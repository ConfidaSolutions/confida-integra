# Confida Integra — Public Contracts & Reference Clients

> Discover, document and expose live OpenShift and Proxmox integrations.

This repository holds the **public contracts and reference clients** for
Confida Integra. The product itself — the dashboard, the collector, the
reconciliation engine and the licensing system — is closed-source and
distributed as a signed Docker image. What you'll find here is everything you
need to **make your integrations discoverable** and to **consume the data** the
product exposes:

- the metadata conventions your DevOps teams annotate with (OpenShift labels and
  Proxmox VM notes/tags),
- the JSON Schema and OpenAPI spec for the data and the northbound API,
- a small Python client SDK, and
- runnable examples.

This is the well-trodden **open contracts, closed engine** model: you get
everything required to integrate, and nothing about the contracts is a secret.

## What this repository contains

| Path | What |
|---|---|
| [`spec/metadata-conventions.md`](spec/metadata-conventions.md) | How sources feed one `IntegrationNode` model |
| [`spec/ocp-label-convention.md`](spec/ocp-label-convention.md) | OpenShift label / annotation contract |
| [`spec/proxmox-metadata-convention.md`](spec/proxmox-metadata-convention.md) | Proxmox `confida` notes block + tag contract |
| [`spec/integration-node.schema.json`](spec/integration-node.schema.json) | JSON Schema (Draft 2020-12) for an integration record |
| [`spec/openapi.yaml`](spec/openapi.yaml) | OpenAPI 3.1 spec for the northbound API (`/api/v1`) |
| [`spec/versioning-policy.md`](spec/versioning-policy.md) | What counts as additive vs. breaking |
| [`examples/curl/`](examples/curl/) | Copy-paste `curl` cookbook for the API |
| [`sdk/python/`](sdk/python/) | `confida-integra-client` — sync + async |
| [`examples/`](examples/) | CMDB sync, OpenShift deployment, Proxmox guest |
| [`charts/`](charts/) | Helm chart **skeleton** (production-ready when full K8s manifests ship) |
| [`i18n/`](i18n/) | UI language packs — use them, or contribute one and it ships with the product |
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability |
| [`SECURITY-POSTURE.md`](SECURITY-POSTURE.md) | Frameworks assessed against, controls that ship, known limitations |

## Quickstart (Python SDK)

```python
pip install confida-integra-client          # not on PyPI yet - see note below

from confida_integra import Client
c = Client("https://your-host", token="cnf_v1_<id><secret>")
for i in c.integrations(env="production"):
    print(i.id, i.source_system, "->", i.destination_system)
```

…or with plain `curl`:

```bash
curl -H "Authorization: Bearer cnf_v1_<id><secret>" \
     "https://your-host/api/v1/integrations?env=production&source=proxmox"
```

See [`examples/curl/`](examples/curl/) for the full cookbook (filters,
pagination, and conditional `ETag` requests).

## Northbound API at a glance

`GET /api/v1/…`, bearer-token authenticated, paged, filterable, with strong
`ETag` caching (`If-None-Match` → `304`). The first public release documents:

- `GET /integrations` — paged, filter by `env` / `status` / `criticality` /
  `source` / `system` / `team` / `updated_since`
- `GET /integrations/{id}`
- `GET /stats`
- `GET /meta`

`/systems` endpoints exist on the product but are **not yet part of the public
contract** — they will be added in a later minor once the system data model is
finalised for external consumers. See
[`spec/versioning-policy.md`](spec/versioning-policy.md).

## Versioning and stability

This repository has its **own version** ([`VERSION`](VERSION), starting at
`0.1.0`), decoupled from the product version. Additive changes (new fields, new
endpoints, new enum values) are **MINOR**; breaking changes require `/api/v2/`
and are **MAJOR**. Details in
[`spec/versioning-policy.md`](spec/versioning-policy.md). The product's support
window is documented on the vendor site.

## Licensing

- **Code** (SDK, chart templates, examples): **Apache-2.0** — see
  [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
- **Specifications and documentation**: **CC-BY-4.0**.
- **Confida®** and **Confida Integra** are trademarks of Confida Solutions Oy.
  The Apache-2.0 grant does **not** include trademark rights.

## Contributing

Issues and PRs for typos, example improvements and documentation translations
are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The API contracts
themselves are maintained upstream in the product and mirrored here, so contract
changes are made on the vendor side.

**Translations are the exception, and the most useful thing you can send us.**
A language pack in [`i18n/`](i18n/) is not mirrored from anywhere — it is
authored here, and an accepted one is shipped inside the product, credited to
whoever wrote it. A partial translation is welcome: every key a pack does not
cover renders in English.

## Reporting security issues

**Do not open a public issue for a vulnerability.** Follow the private process
in [`SECURITY.md`](SECURITY.md). For what the product does about security —
frameworks assessed against, controls that ship, known limitations — see
[`SECURITY-POSTURE.md`](SECURITY-POSTURE.md).

---

> **Availability note.** This repository is the canonical one:
> [`github.com/ConfidaSolutions/confida-integra`](https://github.com/ConfidaSolutions/confida-integra).
> The PyPI package `confida-integra-client` is **not published yet** — until it
> is, install the SDK from source (see [`sdk/python/`](sdk/python/)).
