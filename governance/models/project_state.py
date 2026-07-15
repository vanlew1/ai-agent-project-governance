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
    auxiliary_adapters: tuple[str, ...] = ()
    adapter_detection_status: str = "DETECTED"
    status: str = "UNSPECIFIED"
    activated: bool = False
    activation_status: str = "NOT_ACTIVATED"
    activation_approval_digest: str | None = None
    activation_receipt_digest: str | None = None
    preflight_executed: bool = False
    tests_executed: bool = False
    verification_completed: bool = False
    closure_completed: bool = False
    production_ready: bool = False
    release_authorized: bool = False
    network_authorized: bool = False
    git_write_authorized: bool = False
    lifecycle_stage: str = "UNSPECIFIED"
    lifecycle_evidence: tuple[Mapping[str, Any], ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ProjectState":
        copied = dict(value)
        copied["high_risk_paths"] = tuple(copied["high_risk_paths"])
        copied["default_forbidden_operations"] = tuple(copied["default_forbidden_operations"])
        copied["auxiliary_adapters"] = tuple(copied.get("auxiliary_adapters", ()))
        copied["lifecycle_evidence"] = tuple(dict(item) for item in copied.get("lifecycle_evidence", ()))
        return cls(**copied)

    def to_mapping(self) -> dict[str, Any]:
        return {**self.__dict__, "high_risk_paths": list(self.high_risk_paths), "default_forbidden_operations": list(self.default_forbidden_operations), "auxiliary_adapters": list(self.auxiliary_adapters), "lifecycle_evidence": [dict(item) for item in self.lifecycle_evidence]}
