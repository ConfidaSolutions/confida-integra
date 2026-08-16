# Changelog — Public Surface

All notable changes to the **public contracts and reference clients** are
documented here. This changelog tracks the *public-surface* version
([`VERSION`](VERSION)), which is decoupled from the commercial product version.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/) as scoped in
[`spec/versioning-policy.md`](spec/versioning-policy.md).

---

## [Unreleased]

## [0.1.0] — 2026-06-09

Initial public surface, published alongside the product's northbound API.

### Added
- **Metadata conventions** — `spec/metadata-conventions.md` (umbrella),
  `spec/ocp-label-convention.md` (OpenShift) and
  `spec/proxmox-metadata-convention.md` (Proxmox `confida` notes block + tags).
- **`spec/integration-node.schema.json`** — JSON Schema (Draft 2020-12) for an
  integration record.
- **`spec/openapi.yaml`** — OpenAPI 3.1 for the northbound API, covering
  `GET /api/v1/integrations`, `/integrations/{id}`, `/stats`, `/meta`.
- **`examples/curl/`** — curl cookbook (auth, filters incl. `source=proxmox`,
  pagination, `ETag`/`If-None-Match` conditional requests).
- **`sdk/python/`** — `confida-integra-client`, a sync + async client with
  `ETag`-aware caching, covering integrations / stats / meta.
- **Examples** — `python-cmdb-sync`, `openshift-deployment`, `proxmox-guest`.
- **`charts/confida-integra/`** — Helm chart **skeleton** (clearly marked;
  production-ready once full Kubernetes manifests ship).
- Standard repo files: `README.md`, `LICENSE` (Apache-2.0), `NOTICE`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`.

### Not yet included
- **`/systems` endpoints** — present on the product but intentionally not part
  of this public contract yet; will be added as an additive MINOR once the
  system data model is finalised for external consumers.
- TypeScript SDK; production-ready Helm chart.

> **PyPI publication pending.** `github.com/ConfidaSolutions/confida-integra`
> is the canonical repository. The package `confida-integra-client` is not on
> PyPI yet; this entry is updated when `0.1.0` is uploaded.
