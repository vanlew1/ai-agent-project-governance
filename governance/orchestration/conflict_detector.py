"""Compatibility entry point for ownership conflict detection."""
from .ownership import validate_ownership
def detect(parent, subtasks): return validate_ownership(parent, subtasks)
