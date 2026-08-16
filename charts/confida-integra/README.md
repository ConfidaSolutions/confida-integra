# Helm chart — SKELETON

> ⚠️ **This is a skeleton, not a production chart.** It exists so platform teams
> can see the intended shape and start a values file. It renders a single
> dashboard `Deployment` + `Service` only. The complete chart — collector
> workload, PVCs, Secrets, ServiceAccount/RBAC, Route/Ingress, security context —
> ships once the full Kubernetes manifests land upstream.

## Render / install (for evaluation)

```bash
helm template confida charts/confida-integra \
  --set image.repository=registry.example.org/confida/confida-integra \
  --set image.tag=0.9.6
```

## What's intentionally missing

- Collector workload (CronJob / Deployment)
- `Secret` for OCP / Proxmox tokens (today via `env:` only — do not commit tokens)
- `PersistentVolumeClaim` for `data/` and `config/`
- `ServiceAccount` + least-privilege `Role`/`RoleBinding`
- `Route` (OpenShift) / `Ingress`
- Pod & container `securityContext`

Track the production chart in the project changelog.
