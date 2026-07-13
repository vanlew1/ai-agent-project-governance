"""Schema-aligned immutable TaskRequest model."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class TaskRequest:
    schema_version: str
    task_id: str
    title: str
    description: str
    requested_by: str
    requested_at: str
    hints: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskRequest":
        return cls(**dict(value))

    def to_mapping(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "task_id": self.task_id, "title": self.title, "description": self.description, "requested_by": self.requested_by, "requested_at": self.requested_at, "hints": dict(self.hints)}

    @property
    def text(self) -> str:
        return f"{self.title}\n{self.description}".casefold()
