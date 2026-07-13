"""Build and validate deterministic plans; it never starts agents or Git actions."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Mapping
from .models import digest
from .roles import validate_role
from .task_graph import validate_graph
from .ownership import validate_ownership

def build_plan(contract: Mapping[str, Any], subtasks: list[dict[str, Any]], orchestration_id: str, head_sha: str, branch: str, strategy="HYBRID") -> dict[str, Any]:
    now=datetime.now(timezone.utc).isoformat(); parent_digest=digest(contract)
    normalized=[]
    for item in subtasks:
        item={**item, "schema_version":"1.0", "task_id":contract["task_id"], "orchestration_id":orchestration_id, "status":item.get("status", "PENDING"), "parent_contract_digest":parent_digest, "created_at":now, "deny_scope":item.get("deny_scope", contract.get("write_scope",{}).get("deny",[])), "conditional_scope":item.get("conditional_scope", [])}
        normalized.append(item)
    plan={"schema_version":"1.0","orchestration_id":orchestration_id,"task_id":contract["task_id"],"parent_contract_digest":parent_digest,"head_sha":head_sha,"branch":branch,"strategy":strategy,"subtasks":normalized,"dependency_edges":[[s["subtask_id"],d] for s in normalized for d in s.get("depends_on",[])],"workspace_assignments":[],"conflict_status":"UNKNOWN","plan_status":"DRAFT","created_at":now}
    return validate_plan(plan, contract)

def validate_plan(plan: dict[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    errors=validate_graph(plan.get("subtasks",[]))+validate_ownership(contract, plan.get("subtasks",[]))
    errors += [f"invalid role: {s.get('subtask_id')}" for s in plan.get("subtasks",[]) if not validate_role(s.get("role",""))]
    result=dict(plan); result["conflict_status"]="BLOCKED" if errors else "CLEAR"; result["plan_status"]="BLOCKED" if errors else "VALIDATED"; result["validation_errors"]=errors
    return result
