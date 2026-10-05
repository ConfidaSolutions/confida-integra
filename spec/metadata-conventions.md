# Metadata Conventions

Confida Integra builds a live register of integrations by **reading metadata
your teams already attach to their workloads**. Each discovered integration is
normalised into a single **`IntegrationNode`** record (see
[`integration-node.schema.json`](integration-node.schema.json)), regardless of
which source it came from.

```text
 OpenShift project (labels + annotations) ─┐
                                           ├─►  IntegrationNode  ─►  /api/v1/integrations
 Proxmox VM/CT  (confida notes + tags)  ───┘
```

Two source conventions are documented here; both produce the same record shape,
so a consumer of the northbound API never needs to know which source an
integration came from (though it can filter on the `source` field):

| Source | How you make an integration discoverable | Convention |
|---|---|---|
| **OpenShift / Kubernetes** | Labels + annotations on the Project / namespace | [`ocp-label-convention.md`](ocp-label-convention.md) |
| **Proxmox VE** | A `confida` block in a VM/container **Notes** field, plus tags | [`proxmox-metadata-convention.md`](proxmox-metadata-convention.md) |

## Shared vocabulary

Both conventions use the **same field names** (minus their source-specific
prefix/packaging), so the mental model is identical across sources:

| Concept | Field |
|---|---|
| This is an integration | `app-type: integration` (the opt-in marker) |
| Endpoints of the flow | `source-system`, `destination-system` |
| Interfaces | `source-interface`, `destination-interface` (combined into `protocol`) |
| Ownership | `owner-name`, `owner-email`, `data-owner` |
| Classification | `data-classification`, `gdpr-basis` |
| Lifecycle / risk | `environment`, `criticality`, `status` |
| Docs / data models | `docs`, `data-models` |

## Derived fields

- **`protocol`** is composed as `source-interface → destination-interface`; if
  only one side is set, it is used as-is.
- **`id`** is a deterministic fingerprint of seven attributes: the namespace
  locator, source and destination system, data model, protocol, environment
  and org. Changing any of those produces a *new* id — treat ids as stable only
  while those attributes are unchanged. The algorithm is published, with test
  vectors, in [`fingerprint.md`](fingerprint.md), so a tool outside Integra can
  compute the same id.
- **`environment`** can be inferred from the namespace/name when not set
  explicitly; setting it explicitly is recommended.

See [`integration-node.schema.json`](integration-node.schema.json) for the full
record shape and the allowed enum values.
