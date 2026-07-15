# AGC-UX-EXISTING-PROJECT-ADOPTION-04F-A-R1 Activation Implementation Report

## Result

Implemented the bounded Existing Project Adoption transition:

```text
INSTALLED_NOT_ACTIVATED → ACTIVATED_NOT_PREFLIGHTED
```

The new `agent_state.py activate-approved` entry point is restricted to local synthetic targets and never executes Preflight, Guard, test planning/running, Verification, Closure, network activity, Git writes, or production access.

## Controls implemented

- Added activation approval and receipt Schemas with strict unknown-field rejection.
- Revalidates target identity, Runtime manifest digest, final-install approval digest, installation-receipt digest, compiler id/version/digest, installed TaskContract bytes, and current ProjectState bytes.
- Runs TaskContract and ProjectState Schema plus formal model loader validation before any state write; validates the new ProjectState the same way.
- Preserves TaskContract, scopes, blocked decisions, compiler provenance, and lifecycle booleans. Only the approved ProjectState activation fields change.
- Creates a new target-external pending receipt before atomic ProjectState replacement. A post-write receipt-finalization failure leaves the activated state and pending receipt for manual review; no automatic rollback or deletion occurs.
- Uses a deterministic receipt-binding digest in ProjectState to avoid an impossible circular dependency between final receipt bytes and the required after-state digest.
- Legacy `agent_state.py activate` detects adoption Runtime state and blocks with `USE_ACTIVATE_APPROVED`.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_agent_adopt_activation
4 passed

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
134 passed

PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py
PASS (31 schemas)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py
PASSED (148 Python files; no warnings)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py
PASS (31 schemas)

git diff --check
PASS
```

## Scope and residual boundary

All executed paths used temporary local fixtures only. No real project was activated. No network, credentials, production data, subprocess, Git write, package manager, test/build runner, Preflight, Guard, Verification, Closure, rollback-install, or 04F end-to-end acceptance was run by the activation entry point.

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04F-A-R1
IMPLEMENTED
ACTIVATION_APPROVAL_BOUNDARY_VERIFIED
ACTIVATED_NOT_PREFLIGHTED_SEMANTICS_VERIFIED
READY_FOR_READ_ONLY_AUDIT
```
