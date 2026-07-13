"""P6 precondition for existing P3 verification/closure, not a duplicate evaluator."""
from typing import Mapping
def closure_allowed(orchestration_result: Mapping[str, object], auditor_required=False, auditor_result=None) -> tuple[bool, str]:
    if orchestration_result.get("status") != "READY_FOR_VERIFICATION": return False, "orchestration_not_ready"
    if auditor_required and auditor_result != "SUCCEEDED": return False, "required_auditor_missing"
    return True, "ready_for_p3_verification"
