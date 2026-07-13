"""Schema-aligned immutable ProjectState model."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ProjectState:
    schema_version: str
    project_mode: str
    architecture_status: str
    implementation_plan_status: str
    repository_root: str
    adapter: str
    high_risk_paths: tuple[str, ...]
    default_forbidden_operations: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ProjectState":
        copied = dict(value)
        copied["high_risk_paths"] = tuple(copied["high_risk_paths"])
        copied["default_forbidden_operations"] = tuple(copied["default_forbidden_operations"])
        return cls(**copied)

    def to_mapping(self) -> dict[str, Any]:
        return {**self.__dict__, "high_risk_paths": list(self.high_risk_paths), "default_forbidden_operations": list(self.default_forbidden_operations)}
