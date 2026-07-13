"""Aggregate evidence only; it cannot fabricate worker success."""
from __future__ import annotations
from typing import Any, Mapping
from .freshness import check_freshness

def aggregate(plan: Mapping[str, Any], results: list[Mapping[str, Any]], handoffs: list[Mapping[str, Any]]) -> dict[str, Any]:
    by_id={r.get("subtask_id"):r for r in results}; handoff_ids={h.get("from_subtask_id") for h in handoffs}; issues=[]; passed=0
    for task in plan.get("subtasks",[]):
        ident=task["subtask_id"]; result=by_id.get(ident)
        if not result:
            if task.get("required", True): issues.append(f"MISSING_RESULT:{ident}")
            continue
        expected={"orchestration_id":plan["orchestration_id"],"task_id":plan["task_id"],"contract_digest":task["parent_contract_digest"],"head_sha":plan["head_sha"],"branch":plan["branch"]}
        stale=check_freshness(result, expected)["handoff_status"] == "STALE"
        if stale: issues.append(f"STALE:{ident}")
        elif result.get("status") != "SUCCEEDED": issues.append(f"FAILED:{ident}")
        elif task.get("depends_on") and ident not in handoff_ids: issues.append(f"MISSING_HANDOFF:{ident}")
        else: passed += 1
    status="READY_FOR_VERIFICATION" if not issues else ("STALE" if any(x.startswith("STALE") for x in issues) else "FAILED" if any(x.startswith("FAILED") for x in issues) else "BLOCKED")
    return {"schema_version":"1.0","orchestration_id":plan["orchestration_id"],"task_id":plan["task_id"],"status":status,"required_subtasks":sum(1 for x in plan["subtasks"] if x.get("required",True)),"verified_subtasks":passed,"issues":issues,"created_from_results":sorted(by_id)}
