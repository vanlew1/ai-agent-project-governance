"""Governance runtime namespace; P1 exposes deterministic Preflight only."""

__version__ = "0.2.0-dev"
RUNTIME_PHASE = "PHASE_1_MINIMUM_RUNTIME"
RUNTIME_BEHAVIOR_ENABLED = True

__all__ = ["RUNTIME_BEHAVIOR_ENABLED", "RUNTIME_PHASE", "__version__"]
