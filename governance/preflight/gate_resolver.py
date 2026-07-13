"""Translate risks and mode constraints into P1 contract status."""

from dataclasses import dataclass

from .risk_detector import RiskSummary


@dataclass(frozen=True)
class GateDecision:
    status: str
    stop_conditions: tuple[str, ...]


def resolve_gate(risks: RiskSummary, code_task: bool, code_writes_allowed: bool) -> GateDecision:
    blockers = {"external": "new_user_permission_required", "production": "production_data_write_required", "destructive": "irreversible_operation_required", "release": "new_user_permission_required", "secret": "new_user_permission_required"}
    stops = tuple(sorted({blockers[risk] for risk in risks.kinds if risk in blockers}))
    if stops:
        return GateDecision("BLOCKED", stops)
    if "scope" in risks.kinds or (code_task and not code_writes_allowed):
        return GateDecision("DRAFT", ())
    return GateDecision("READY", ())
