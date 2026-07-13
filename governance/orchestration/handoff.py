"""Structured handoff creation and validation; natural-language summaries are insufficient."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Mapping
from .freshness import check_freshness

def create_handoff(result: Mapping[str, Any], to_subtask_ids: list[str]) -> dict[str, Any]:
    return {"schema_version":"1.0","handoff_id":f"handoff-{result['subtask_id']}","orchestration_id":result["orchestration_id"],"task_id":result["task_id"],"from_subtask_id":result["subtask_id"],"to_subtask_ids":to_subtask_ids,"contract_digest":result["contract_digest"],"head_sha":result["head_sha"],"branch":result["branch"],"workspace_fingerprint":result["workspace_fingerprint"],"changed_files":result.get("changed_files",[]),"completed_artifacts":result.get("artifacts",[]),"verification_summary":result.get("test_results",[]),"open_risks":result.get("risks",[]),"required_next_actions":result.get("unresolved_items",[]),"created_at":datetime.now(timezone.utc).isoformat()}

def validate_handoff(handoff: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, Any]: return check_freshness(handoff, expected)
