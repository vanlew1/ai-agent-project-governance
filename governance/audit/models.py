"""Result models shared by audit checks and renderers."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

CheckStatus = Literal["PASS", "WARN", "FAIL", "NOT_APPLICABLE", "SKIPPED"]


@dataclass(frozen=True)
class AuditCheck:
    check_id: str
    status: CheckStatus
    summary: str
    safe_evidence: tuple[str, ...]
    recommendation: str
    weight: int = 10

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["safe_evidence"] = list(self.safe_evidence)
        return value


@dataclass(frozen=True)
class AuditResult:
    schema_version: str
    tool_version: str
    project_root_display: str
    score: int
    level: str
    recommended_preset: str
    checks: tuple[AuditCheck, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "tool_version": self.tool_version,
            "project_root_display": self.project_root_display,
            "score": self.score,
            "level": self.level,
            "recommended_preset": self.recommended_preset,
            "checks": [check.to_dict() for check in self.checks],
        }
