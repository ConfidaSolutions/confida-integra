# Proxmox VE Metadata Convention

Confida Integra reads **Proxmox VE** as an infrastructure-discovery source.
Every node, VM and container is read as a *system*; a guest additionally
**declares an integration** when its **Notes / Description** carries a `confida`
block. Tags supply the filterable dimensions.

This contract requires no agent and no application change — just the standard
Proxmox VM **Notes** field and **tags**.

## Declaring an integration — the `confida` Notes block

Put a fenced ` ```confida ` block in the guest's **Notes / Description**. It is
parsed as simple `key: value` lines (the same vocabulary as the OpenShift
annotations, minus the prefix):

````
```confida
app-type: integration
source-system: billing-api
destination-system: crm
source-interface: rest-json
destination-interface: sql
data-models: invoice-v2
criticality: high
environment: production
owner-name: Integration Team
owner-email: integrations@example.org
data-classification: confidential
docs: https://wiki.example.org/billing-crm
```
````

Rules:

- The fenced ` ```confida ` form is **recommended** — it renders as a clean code
  block in the Proxmox UI and lets you keep human prose in the same Notes field.
- An **un-fenced** Notes field also works **only if** it begins with the
  sentinel `app-type: integration` (so ordinary prose is never misread as a
  card).
- Keys mirror the OpenShift annotation names; `protocol` is composed as
  `source-interface → destination-interface`.
- A guest **without** a `confida` block is still discovered as a *system*; it
  simply declares no integration.

## Tags — filterable dimensions

Proxmox tags (semicolon-separated, order-independent) supply the dimensions used
for filtering. Each is matched by convention prefix:

| Tag | Maps to |
|---|---|
| `env-<value>` | `environment` (`dev` / `test` / `qa` / `production`) |
| `crit-<value>` | `criticality` (`low` / `medium` / `high` / `critical`) |
| `status-<value>` | `status` (`active` / `stale` / `deprecated`) |
| `integration` | marks the guest as carrying an integration declaration |
| `team-<value>` | team / owner hint |

Example tag string (Proxmox stores tags sorted alphabetically, which is fine —
order is never significant):

```
crit-high;env-production;integration;status-active
```

A configurable tag **prefix** can be stripped before matching (e.g. `ci-` so
`ci-env-prod` is read as `env-prod`) to avoid clashing with an existing tag
scheme.

## Read-only access

Discovery uses the Proxmox API read-only. Create an API token for a user with
the **`PVEAuditor`** role; the product never issues write calls. Note the common
Proxmox gotcha: a **privilege-separated** token does not inherit the user's role
and must be granted `PVEAuditor` on its own, or every listing comes back empty
instead of returning a permission error.

## Resulting record

Integrations declared this way conform to
[`integration-node.schema.json`](integration-node.schema.json) with
`source: "proxmox"`. A worked example (Notes block + tag set for a sample VM) is
in [`../examples/proxmox-guest/`](../examples/proxmox-guest/).
