"""Project-mode decisions without inference."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModeDecision:
    mode: str
    code_writes_allowed: bool


def resolve_mode(project_mode: str) -> ModeDecision:
    return ModeDecision(project_mode, project_mode == "EXECUTION")
