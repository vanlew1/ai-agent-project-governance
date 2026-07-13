"""Freshness checks bind handoffs/results to one immutable orchestration context."""
from __future__ import annotations
from typing import Any, Mapping

FRESH_FIELDS=("orchestration_id", "task_id", "contract_digest", "head_sha", "branch", "workspace_fingerprint")
def check_freshness(value: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, Any]:
    mismatches=[name for name in FRESH_FIELDS if expected.get(name) is not None and value.get(name)!=expected.get(name)]
    return {"handoff_status":"STALE" if mismatches else "FRESH", "mismatches":mismatches}
