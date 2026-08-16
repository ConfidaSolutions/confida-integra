# Example — Proxmox guest discoverable integration

How to make a Proxmox VM or container declare an integration: add a `confida`
block to its **Notes** and a few **tags**. No agent, no application change.

## 1. Notes / Description

In the Proxmox UI (VM/CT → **Summary → Notes → Edit**), paste:

````text
This VM hosts the billing→CRM bridge. Owned by the Integration Team.

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

Human prose above the fenced block is fine — only the ` ```confida ` block is
parsed. (An un-fenced Notes field also works if it *starts* with
`app-type: integration`.)

## 2. Tags

Add tags for the filterable dimensions (Datacenter → the guest → Tags, or the
chip editor). Order does not matter:

```text
env-production;crit-high;integration;status-active
```

## 3. Or from the CLI

```bash
# VM (qemu): vmid 104
qm set 104 --tags "env-production;crit-high;integration;status-active"
qm set 104 --description "$(cat notes.md)"     # notes.md contains the confida block

# Container (lxc): vmid 102
pct set 102 --tags "env-test;crit-low;integration"
```

## Result

On the next collector cycle the guest is discovered as a `vm` / `container`
*system*, and — because of the `confida` block — also produces an integration
with `source: "proxmox"`. See
[`../../spec/proxmox-metadata-convention.md`](../../spec/proxmox-metadata-convention.md)
for the full field and tag reference.

A guest **without** a `confida` block still shows up as a standalone system; it
just declares no integration.
