# AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B Lifecycle Foundation Implementation Report

## Hard-blocker remediation

04F-R1 was blocked because an installed adoption Runtime could not safely enter the formal lifecycle. This change establishes a provenance-bound adapter; it does not run 04F-R1 end-to-end acceptance or a real-project lifecycle.

| Existing component | Reused | Adaptation / extension |
|---|---:|---|
| `run_preflight` | Yes | Deterministic TaskContract-to-TaskRequest bridge and provenance evidence |
| Scope Guard | Yes | Guard evidence binds Preflight and workspace snapshots |
| command registry / runner | Yes | Exact confirmed-candidate intersection; no shell composition |
| Verification / Closure | Yes | Adoption provenance and freshness checks wrap formal results |
| ProjectState / atomic writer | Yes | One CAS-only lifecycle transition service |

## Implemented boundaries

- `AdoptionLifecycleContext` independently binds target, installation/activation evidence, Runtime bytes, current ProjectState, workspace snapshot, and confirmed test candidates.
- The Preflight adapter fails closed unless the activated state and provenance are valid, maps only narrow approved scope, and invokes formal `run_preflight`.
- Lifecycle state is the existing ProjectState, extended with one forward-only stage field and evidence references. Every transition checks the raw current-state SHA-256 and writes atomically.
- Test plans only select exact, digest-matched confirmed registry candidates. Unknown, changed, duplicate, install, or network-like commands fail closed.
- Workspace snapshots use versioned path/type/content hashes without outputting file contents. Failed, incomplete, and stale Verification cannot reach Closure.
- Closure explicitly reports `production_ready = false`, `released = false`, and `deployed = false`.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_adoption_lifecycle_foundation
6 passed

Targeted adoption/schema suite
22 passed
```

The required full regression and independent 04F-B audit remain the next stage. No network, Git write, package installation, browser, external agent, production access, real target lifecycle, or 04F-R1 execution occurred.

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B
IMPLEMENTED_PENDING_FULL_REGRESSION
FORMAL_LIFECYCLE_BRIDGE_ESTABLISHED
READY_FOR_04F-B-AUDIT_AFTER_VALIDATION
```
