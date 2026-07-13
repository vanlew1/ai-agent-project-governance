"""Deterministic, local multi-agent orchestration primitives (P6)."""

from .planner import build_plan, validate_plan
from .scheduler import schedule

__all__ = ["build_plan", "validate_plan", "schedule"]
