# Northbound API — `curl` Cookbook

Copy-paste `curl` recipes for the Confida Integra northbound API
(`/api/v1`). Every endpoint is read-only and requires a bearer token.

## Setup

Create an API token in the product (Admin → API Tokens), then export it and your
host. The token format is `cnf_v1_<id><secret>`:

```bash
export CI_HOST="https://your-host"
export CI_TOKEN="cnf_v1_<id><secret>"
# convenience: reuse the auth header
auth=(-H "Authorization: Bearer $CI_TOKEN")
```

> If your deployment uses a self-signed certificate in a lab, add `-k`. Don't
> use `-k` against production.

## 1. Sanity check — `/meta`

Confirms the token authenticates and shows API / schema / product versions:

```bash
curl -s "${auth[@]}" "$CI_HOST/api/v1/meta" | jq
```

```json
{
  "api_version": "1.0",
  "schema_version": 10,
  "product_version": "0.9.6",
  "data_source": "live",
  "node_count": 53,
  "generated_at": "2026-06-09T08:00:00Z"
}
```

## 2. List integrations

```bash
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations" | jq
```

The response is an envelope — `data` is the array, plus `pagination`, `links`
and `generated_at`:

```json
{
  "data": [ { "id": "a1b2c3...", "source_system": "billing-api", "destination_system": "crm", "...": "..." } ],
  "pagination": { "page": 1, "per_page": 100, "total_items": 53, "total_pages": 1 },
  "links": { "self": "/api/v1/integrations?page=1&per_page=100", "first": "...", "last": "...", "prev": null, "next": null },
  "generated_at": "2026-06-09T08:00:00Z"
}
```

## 3. Filter

Filters combine with AND. `env`, `status` and `criticality` are repeatable;
`env` accepts both `production` and the short `prod`.

```bash
# Production integrations only
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?env=production"

# Only integrations discovered from Proxmox
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?source=proxmox" | jq '.data[].source_system'

# High + critical, in production
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?env=prod&criticality=high&criticality=critical"

# Everything touching a given system (substring match on source or destination)
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?system=crm"

# Changed since a timestamp (RFC 3339) — useful for incremental CMDB sync
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?updated_since=2026-06-01T00:00:00Z"

# Project only the fields you need
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?fields=id,source_system,destination_system,status"
```

## 4. Paginate

```bash
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations?page=2&per_page=50" | jq '.pagination'
```

Follow `links.next` until it is `null`:

```bash
next="/api/v1/integrations?page=1&per_page=100"
while [ "$next" != "null" ] && [ -n "$next" ]; do
  resp=$(curl -s "${auth[@]}" "$CI_HOST$next")
  echo "$resp" | jq -c '.data[] | {id, source_system, destination_system}'
  next=$(echo "$resp" | jq -r '.links.next')
done
```

## 5. Single integration

```bash
curl -s "${auth[@]}" "$CI_HOST/api/v1/integrations/a1b2c3d4e5f60718" | jq '.data'
```

## 6. Stats

```bash
curl -s "${auth[@]}" "$CI_HOST/api/v1/stats" | jq '.data'
```

```json
{
  "total_integrations": 53,
  "total_systems": 41,
  "by_status":      { "active": 49, "stale": 3, "deprecated": 1 },
  "by_environment": { "production": 30, "test": 14, "dev": 9 },
  "by_criticality": { "high": 12, "medium": 20, "low": 18, "critical": 3 },
  "by_source":      { "openshift": 48, "proxmox": 5 }
}
```

## 7. Conditional requests — `ETag` / `304`

Every successful response carries an `ETag`. Send it back as `If-None-Match` and
the server answers `304 Not Modified` (empty body) when the data is unchanged —
cheap polling.

```bash
# Capture the ETag (-D - dumps headers)
etag=$(curl -s -D - "${auth[@]}" "$CI_HOST/api/v1/integrations" -o /dev/null \
        | awk -F': ' 'tolower($1)=="etag"{print $2}' | tr -d '\r')

# Re-request with the cached validator → 304 when nothing changed
curl -s -o /dev/null -w "%{http_code}\n" \
     "${auth[@]}" -H "If-None-Match: $etag" \
     "$CI_HOST/api/v1/integrations"
# -> 304
```

## Notes

- **Rate limiting:** each token has a per-minute budget; exceeding it returns
  `429 Too Many Requests`. Back off and retry.
- **`/systems`** endpoints are **not** part of the public contract yet — see
  [`../../spec/versioning-policy.md`](../../spec/versioning-policy.md).
- Full contract: [`../../spec/openapi.yaml`](../../spec/openapi.yaml).
