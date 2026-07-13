"""Closed P6 role registry; no dynamic role or capability loading."""
from .models import ROLES

ROLE_RULES = {
    "COORDINATOR": {"writes_implementation": False, "final_verification": False},
    "IMPLEMENTER": {"writes_implementation": True, "final_verification": False},
    "VERIFIER": {"writes_implementation": False, "final_verification": True},
    "AUDITOR": {"writes_implementation": False, "final_verification": False},
}
def validate_role(role: str) -> bool: return role in ROLES
