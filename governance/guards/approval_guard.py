from ..state import approval_store
from ..state.freshness import evaluate

def check(required_type, fingerprint, task_id, scope=None):
    if not required_type: return "not_required"
    candidates=[a for a in approval_store.load() if a.get("approval_type")==required_type]
    if not candidates: return "missing"
    statuses=[evaluate(a,fingerprint,task_id,scope) for a in candidates]
    return "valid" if "valid" in statuses else "scope_mismatch" if "scope_mismatch" in statuses else "state_mismatch" if "state_mismatch" in statuses else "expired"

def required(contract):
    text=" ".join(contract.get("objective",[])).casefold()
    return "external_api_access" if "api" in text else None
