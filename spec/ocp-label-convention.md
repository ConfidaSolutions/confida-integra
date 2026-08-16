# OpenShift Label & Annotation Convention

Confida Integra discovers integrations from OpenShift project **labels** and
**annotations**. This is the canonical contract: any project annotated this way
becomes discoverable, with no application changes required.

> **Prefix.** The label/annotation prefix is **configurable** in the product
> (the deployment's "label prefix" setting). This document uses
> `ict.example.org/` as the placeholder; substitute the prefix your deployment
> is configured with. The plain `team` label is the one exception (it has no
> prefix, see below).

## Required label — the opt-in marker

The collector picks up **only** projects carrying this label; without it the
project is ignored entirely:

```yaml
labels:
  ict.example.org/app-type: integration
```

## Team label and filtering

Projects are also filtered by team. Lookup order:

1. `ict.example.org/team` — prefixed label (recommended)
2. `team` — plain label (fallback)

A project is accepted **only** if one of these matches the deployment's
configured team name (default `integration`).

## Recommended labels

| Label | Values | Description |
|---|---|---|
| `ict.example.org/environment` | `dev` `test` `qa` `production` | Environment (inferred from the namespace name if missing) |
| `ict.example.org/criticality` | `low` `medium` `high` `critical` | Criticality of the integration |
| `ict.example.org/org` | free text | Organisational unit / team identifier |
| `app.kubernetes.io/version` | e.g. `1.4.2` | Integration / application version |

## Annotations

**Required — at least one of:**

| Annotation | Example |
|---|---|
| `ict.example.org/source-system` | `SAP` |
| `ict.example.org/destination-system` | `ASPA` |

**Recommended:**

| Annotation | Example | Notes |
|---|---|---|
| `ict.example.org/source-interface` | `rest-json` | Combined into `protocol` |
| `ict.example.org/destination-interface` | `sql` | Combined into `protocol` |
| `ict.example.org/owner-name` | `Jane Smith` | Technical owner |
| `ict.example.org/owner-email` | `jane@example.org` | |
| `ict.example.org/data-owner` | `HR Services` | Data steward / owning team |
| `ict.example.org/data-classification` | `internal` | `public` / `internal` / `confidential` / `secret` |
| `ict.example.org/description` | `Transfers HR changes` | Short description |

**Optional:**

| Annotation | Example |
|---|---|
| `ict.example.org/gdpr-basis` | `legitimate-interest` |
| `ict.example.org/data-models` | `HRModel;PersonModel` (semicolon-separated) |
| `ict.example.org/docs` | `https://wiki.example.org/int/hr-sap` |

## Example project manifest

```yaml
apiVersion: project.openshift.io/v1
kind: Project
metadata:
  name: hr-sap-to-aspa-prod
  annotations:
    openshift.io/display-name: "HR SAP → ASPA"
    ict.example.org/source-system: SAP
    ict.example.org/destination-system: ASPA
    ict.example.org/source-interface: rest-json
    ict.example.org/destination-interface: soap
    ict.example.org/owner-name: Jane Smith
    ict.example.org/owner-email: jane@example.org
    ict.example.org/data-owner: HR Services
    ict.example.org/data-classification: confidential
    ict.example.org/gdpr-basis: legal-obligation
    ict.example.org/data-models: EmployeeRecord
    ict.example.org/description: Transfers HR changes from SAP to ASPA
    ict.example.org/docs: https://wiki.example.org/integrations/hr-sap-aspa
  labels:
    ict.example.org/app-type: integration
    ict.example.org/team: integration
    team: integration
    ict.example.org/environment: production
    ict.example.org/criticality: high
    ict.example.org/org: hr
    app.kubernetes.io/version: "2.1.0"
```

A runnable copy of this manifest is in
[`../examples/openshift-deployment/`](../examples/openshift-deployment/).

## Applying it

```bash
oc apply -f project.yaml

# or on an existing project:
oc label   project hr-sap-to-aspa-prod ict.example.org/app-type=integration
oc annotate project hr-sap-to-aspa-prod \
  ict.example.org/source-system=SAP \
  ict.example.org/destination-system=ASPA
```

The resulting record conforms to
[`integration-node.schema.json`](integration-node.schema.json) with
`source: "openshift"`.
