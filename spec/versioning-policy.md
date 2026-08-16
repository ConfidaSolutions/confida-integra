# Versioning & Stability Policy

This repository (the public contracts and reference clients) has its **own
version** ([`../VERSION`](../VERSION), starting at `0.1.0`), **decoupled** from
the commercial product version. The public surface evolves more slowly than the
product: additive changes are common, breaking changes are rare and deliberate.

## What "the public surface" covers

- the metadata conventions (`spec/*-convention.md`),
- `spec/integration-node.schema.json`,
- `spec/openapi.yaml` (the `/api/v1` contract),
- the public behaviour of the Python SDK (`sdk/python/`).

## SemVer rules for the public surface

| Bump | Triggered by |
|---|---|
| **PATCH** (`0.1.0 → 0.1.1`) | Typo / clarification fixes; no schema or contract impact. |
| **MINOR** (`0.1.0 → 0.2.0`) | **Additive, backward-compatible** changes: a new optional field, a new endpoint, a new enum value, a new `source` value, a new SDK method, a new query parameter. |
| **MAJOR** (`0.x → 1.0`, `1.x → 2.0`) | **Breaking** changes: renaming or removing a field/endpoint/parameter, changing a field's type or semantics, tightening validation. |

### What is *not* breaking (so consumers must tolerate it)

- New fields appearing in a response object (`additionalProperties` is allowed —
  see the schema).
- New `source` values (e.g. beyond `openshift` / `proxmox`).
- New enum values in additive positions.
- New endpoints and new optional query parameters.

Write consumers defensively: ignore unknown fields, do not assume the set of
`source` values is closed.

## API major versions and deprecation

The northbound API is versioned in its path (`/api/v1/…`). A breaking change to
the API requires a new path prefix (`/api/v2/…`). When that happens:

- the previous version (`/api/v1`) remains available during a deprecation window,
- responses on the deprecated version carry a `Sunset` HTTP header
  ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)) indicating the
  end-of-availability date,
- the deprecation is announced in [`../CHANGELOG.md`](../CHANGELOG.md).

## Initial version: `0.1.0`

`0.1.0` signals the maturity honestly: this is the first public northbound
contract and the SDK is new. `1.0.0` is reserved for the product GA milestone,
at which point the API is declared stable for the published support window.

## Currently outside the public contract

- **`/systems` endpoints.** They exist on the product but are intentionally not
  part of this public contract yet. They will be added as an **additive MINOR**
  bump once the system data model is finalised for external consumers. Until
  then, do not depend on `/api/v1/systems*` shapes from this repository.
- TypeScript SDK; production-ready Helm chart.
