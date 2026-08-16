"""Lightweight, forward-compatible models.

Per the versioning policy, the API may add fields at any time. These models keep
the full original payload in ``raw`` and expose the documented fields as typed
attributes, so unknown fields never break a consumer.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any


@dataclass
class Integration:
    """One integration record (see spec/integration-node.schema.json)."""

    id: str = ""
    name: str = ""
    namespace: str = ""
    source_system: str = ""
    destination_system: str = ""
    owner: str = ""
    owner_email: str = ""
    data_owner: str = ""
    data_model_name: str = ""
    protocol: str = ""
    environment: str = ""
    data_classification: str = ""
    gdpr_basis: str = ""
    docs_url: str = ""
    description: str = ""
    source: str = ""
    last_seen: str = ""
    status: str = ""
    # Empty unless no source currently observes this integration (F79). Kept
    # separate from `status` so a node can be both deprecated and unobserved.
    missing_since: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Integration":
        known = {f.name for f in fields(cls)} - {"raw"}
        kwargs = {k: d[k] for k in known if k in d and d[k] is not None}
        return cls(**kwargs, raw=dict(d))

    @property
    def criticality(self) -> str:
        return (self.extra or {}).get("criticality", "")

    @property
    def missing(self) -> bool:
        """True when no configured source currently observes this integration."""
        return bool(self.missing_since)

    def __getitem__(self, key: str) -> Any:
        """Fall back to the raw payload for any field not modelled explicitly."""
        return self.raw.get(key)


@dataclass
class Stats:
    total_integrations: int = 0
    total_systems: int = 0
    by_status: dict[str, int] = field(default_factory=dict)
    by_environment: dict[str, int] = field(default_factory=dict)
    by_criticality: dict[str, int] = field(default_factory=dict)
    by_source: dict[str, int] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Stats":
        known = {f.name for f in fields(cls)} - {"raw"}
        kwargs = {k: d[k] for k in known if k in d and d[k] is not None}
        return cls(**kwargs, raw=dict(d))


@dataclass
class Meta:
    api_version: str = ""
    schema_version: int = 0
    product_version: str = ""
    data_source: str = ""
    node_count: int = 0
    generated_at: str = ""
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Meta":
        known = {f.name for f in fields(cls)} - {"raw"}
        kwargs = {k: d[k] for k in known if k in d and d[k] is not None}
        return cls(**kwargs, raw=dict(d))
