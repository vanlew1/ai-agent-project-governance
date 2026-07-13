"""Pure ready-queue calculator.  It does not execute commands or agents."""
from typing import Any, Mapping

def schedule(plan: Mapping[str, Any], results: Mapping[str, Mapping[str, Any]] | None = None, handoffs: Mapping[str, Mapping[str, Any]] | None = None) -> dict[str, list[str]]:
    results=results or {}; handoffs=handoffs or {}; groups={key:[] for key in ("ready","waiting","blocked","completed","failed")}
    if plan.get("plan_status") not in {"VALIDATED","ACTIVE","COMPLETED"}: groups["blocked"]=[s["subtask_id"] for s in plan.get("subtasks",[])]; return groups
    for task in plan.get("subtasks",[]):
        ident=task["subtask_id"]; result=results.get(ident,{}); status=result.get("status", task.get("status"))
        if status in {"VERIFIED","SUCCEEDED"}: groups["completed"].append(ident); continue
        if status in {"FAILED","ERROR","STALE","BLOCKED","PARTIAL"}: groups["failed" if status in {"FAILED","ERROR"} else "blocked"].append(ident); continue
        dependencies=task.get("depends_on",[])
        fresh=all(results.get(dep,{}).get("status") in {"VERIFIED","SUCCEEDED"} and handoffs.get(dep,{}).get("handoff_status", "FRESH")=="FRESH" for dep in dependencies)
        groups["ready" if fresh else "waiting"].append(ident)
    return groups
