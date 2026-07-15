"""Fixed, explainable scoring for the adoption audit."""
from __future__ import annotations

from .models import AuditCheck


def score_checks(checks: tuple[AuditCheck, ...]) -> int:
    applicable = [check for check in checks if check.status != "NOT_APPLICABLE"]
    if not applicable:
        return 0
    earned = sum(
        check.weight if check.status == "PASS" else check.weight // 2 if check.status == "WARN" else 0
        for check in applicable
    )
    return round(earned * 100 / sum(check.weight for check in applicable))


def level_for(score: int) -> str:
    if score >= 80:
        return "READY"
    if score >= 50:
        return "PARTIAL"
    return "NEEDS_GUARDRAILS"


def recommended_preset(checks: tuple[AuditCheck, ...], document_text: str) -> str:
    statuses = {check.check_id: check.status for check in checks}
    high_risk_terms = ("production", "external api", "credential", "multi-agent", "multi agent")
    has_high_risk_context = any(term in document_text.lower() for term in high_risk_terms)
    if has_high_risk_context:
        return "strict"
    if statuses.get("test_command") == "PASS" and statuses.get("change_scope") == "PASS":
        return "lightweight"
    return "standard"
