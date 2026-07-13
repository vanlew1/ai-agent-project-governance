"""Suggested contract scope generation; this module does not enforce scope."""

from dataclasses import dataclass
from pathlib import PurePosixPath

from ..models.project_state import ProjectState
from ..models.task_request import TaskRequest
from .default_rules import DENY_PATTERNS
from ..adapters.registry import get as get_adapter


@dataclass(frozen=True)
class Scope:
    read_scope: tuple[str, ...]
    write_scope: dict[str, list[str]]


def normalize(paths: list[str]) -> tuple[str, ...]:
    normalized = []
    for raw in paths:
        value = raw.replace("\\", "/").strip()
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Invalid scope path: {raw}")
        if value and value not in {".", "./"}:
            normalized.append(value.rstrip("/"))
    return tuple(sorted(set(normalized)))


def resolve_scope(task: TaskRequest, state: ProjectState, status: str, code_task: bool) -> Scope:
    paths = normalize(list(task.hints["likely_paths"]))
    adapter = get_adapter(state.adapter)
    adapter_deny = adapter.sensitive_path_patterns() if adapter else ()
    deny = tuple(sorted(set((*state.high_risk_paths, *DENY_PATTERNS, *adapter_deny))))
    writable = list(paths) if status == "READY" and code_task else []
    return Scope(paths, {"allow": writable, "deny": list(deny)})
