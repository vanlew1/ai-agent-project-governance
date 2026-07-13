"""Small schema-aligned value helpers owned by the P6 orchestration layer."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
import hashlib, json

ROLES = frozenset({"COORDINATOR", "IMPLEMENTER", "VERIFIER", "AUDITOR"})
SUBTASK_STATES = frozenset({"PENDING", "READY", "RUNNING", "PARTIAL", "VERIFIED", "FAILED", "BLOCKED", "STALE", "CANCELLED"})

def digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass(frozen=True)
class SubtaskContract:
    value: Mapping[str, Any]
    @property
    def digest(self) -> str: return digest(self.value)
    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SubtaskContract":
        if value.get("role") not in ROLES: raise ValueError("unknown orchestration role")
        if value.get("status") not in SUBTASK_STATES: raise ValueError("unknown subtask status")
        return cls(dict(value))
