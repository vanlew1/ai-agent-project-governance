"""Dependency graph validation without command execution."""
from __future__ import annotations
from typing import Any, Mapping

def validate_graph(subtasks: list[Mapping[str, Any]]) -> list[str]:
    ids = [str(item.get("subtask_id", "")) for item in subtasks]; known = set(ids); errors=[]
    if len(ids) != len(known): errors.append("duplicate subtask_id")
    edges=set()
    for item in subtasks:
        node=str(item.get("subtask_id", ""))
        for dep in item.get("depends_on", []):
            edge=(node, dep)
            if dep == node: errors.append(f"self dependency: {node}")
            elif dep not in known: errors.append(f"unknown dependency: {node}->{dep}")
            elif edge in edges: errors.append(f"duplicate dependency: {node}->{dep}")
            edges.add(edge)
    remaining={str(x.get("subtask_id")): set(x.get("depends_on", [])) for x in subtasks}
    while remaining:
        free=[node for node,deps in remaining.items() if not deps]
        if not free: errors.append("cyclic dependency graph"); break
        for node in free: remaining.pop(node)
        for deps in remaining.values(): deps.difference_update(free)
    return errors
