"""Scope subset and single-writer checks for declared paths/globs."""
from __future__ import annotations
import fnmatch
from typing import Any, Mapping

def _covered(path: str, scopes: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, scope) or path.startswith(scope.rstrip("/*") + "/") for scope in scopes)

def validate_ownership(parent: Mapping[str, Any], subtasks: list[Mapping[str, Any]]) -> list[str]:
    allowed=list(parent.get("write_scope", {}).get("allow", [])); denied=list(parent.get("write_scope", {}).get("deny", [])); errors=[]
    for subtask in subtasks:
        for path in subtask.get("write_scope", []):
            if not _covered(path, allowed): errors.append(f"scope escape: {subtask['subtask_id']}:{path}")
            if _covered(path, denied): errors.append(f"denied write: {subtask['subtask_id']}:{path}")
    for index,left in enumerate(subtasks):
        for right in subtasks[index+1:]:
            overlap=set(left.get("write_scope", [])) & set(right.get("write_scope", []))
            serial=(left["subtask_id"] in right.get("depends_on", []) or right["subtask_id"] in left.get("depends_on", []))
            if overlap and not serial: errors.append(f"parallel write conflict: {left['subtask_id']},{right['subtask_id']}:{','.join(sorted(overlap))}")
    return errors
