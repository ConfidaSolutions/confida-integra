#!/usr/bin/env python3
"""Minimal CMDB sync example.

Pulls active integrations from the Confida Integra northbound API and "upserts"
them into a CMDB. The ``upsert_ci`` function is a stub that just prints the record
it would write — replace it with a real call to ServiceNow / iTop / Device42 / etc.

Run:
    pip install -r requirements.txt
    export CI_HOST="https://your-host"
    export CI_TOKEN="cnf_v1_<id><secret>"
    python sync.py
"""
from __future__ import annotations

import json
import os
import sys

from confida_integra import Client, ConfidaError


def upsert_ci(record: dict) -> None:
    """Replace this with your CMDB's create-or-update call."""
    print("UPSERT " + json.dumps(record, ensure_ascii=False))


def main() -> int:
    host = os.environ.get("CI_HOST", "https://your-host")
    token = os.environ.get("CI_TOKEN", "")
    if not token:
        print("error: set CI_TOKEN (and optionally CI_HOST)", file=sys.stderr)
        return 2

    try:
        with Client(host, token=token) as c:
            meta = c.meta()
            print(f"# Confida Integra {meta.product_version} "
                  f"({meta.node_count} integrations, source={meta.data_source})",
                  file=sys.stderr)

            count = 0
            for i in c.integrations(status="active"):
                upsert_ci({
                    "external_id":        i.id,
                    "name":               i.name or f"{i.source_system} -> {i.destination_system}",
                    "source_system":      i.source_system,
                    "destination_system": i.destination_system,
                    "protocol":           i.protocol,
                    "environment":        i.environment,
                    "criticality":        i.criticality,
                    "owner_email":        i.owner_email,
                    "classification":     i.data_classification,
                    "discovered_via":     i.source,   # "openshift" | "proxmox" | ...
                })
                count += 1
            print(f"# synced {count} active integrations", file=sys.stderr)
    except ConfidaError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
