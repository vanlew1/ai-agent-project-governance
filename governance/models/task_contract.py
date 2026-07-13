"""Schema-aligned immutable TaskContract model."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class TaskContract:
    schema_version: str
    task_id: str
    project_mode: str
    task_level: str
    status: str
    objective: tuple[str, ...]
    read_scope: tuple[str, ...]
    write_scope: Mapping[str, Any]
    autonomy: Mapping[str, Any]
    stop_conditions: tuple[str, ...]
    verification: Mapping[str, Any]
    report: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskContract":
        copied = dict(value)
        for name in ("objective", "read_scope", "stop_conditions"):
            copied[name] = tuple(copied[name])
        return cls(**copied)

    def to_mapping(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "task_id": self.task_id, "project_mode": self.project_mode, "task_level": self.task_level, "status": self.status, "objective": list(self.objective), "read_scope": list(self.read_scope), "write_scope": dict(self.write_scope), "autonomy": dict(self.autonomy), "stop_conditions": list(self.stop_conditions), "verification": dict(self.verification), "report": dict(self.report)}
