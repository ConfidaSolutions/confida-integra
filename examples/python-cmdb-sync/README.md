# Example — CMDB sync

A ~40-line script that pulls active integrations from the northbound API and
upserts them into a CMDB. The CMDB write is stubbed (`upsert_ci` just prints), so
you can run it safely and then wire in your real CMDB client.

## Run

```bash
pip install -r requirements.txt
export CI_HOST="https://your-host"
export CI_TOKEN="cnf_v1_<id><secret>"
python sync.py
```

Output (stub):

```
# Confida Integra 0.9.6 (53 integrations, source=live)
UPSERT {"external_id": "a1b2...", "source_system": "billing-api", "destination_system": "crm", ...}
...
# synced 49 active integrations
```

## Make it incremental

For periodic sync, store the timestamp of the last run and pass it as
`updated_since` so you only process what changed:

```python
for i in c.integrations(status="active", updated_since=last_run_iso):
    upsert_ci(...)
```

Combine with the client's built-in `ETag` caching (automatic) to make frequent
polling cheap.

## Wire in a real CMDB

Replace `upsert_ci()` with a call to your system's API, mapping the
`IntegrationNode` fields (see [`../../spec/integration-node.schema.json`](../../spec/integration-node.schema.json))
to your CI attributes. `external_id` (the integration `id`) is a stable key for
create-or-update as long as the integration's core attributes are unchanged.
