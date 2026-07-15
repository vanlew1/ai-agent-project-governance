# AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B Independent Lifecycle Safety Audit

## Scope and method

Read-only independent review of the 04F-B implementation, its unit coverage, schemas, and reported validation evidence. No implementation, Schema, documentation, test, real project, network, Git write, or lifecycle execution was performed by this audit.

## Reuse matrix

| Lifecycle stage | Formal component | Adoption adapter | New evidence | Duplicate implementation |
|---|---|---|---|---|
| Preflight | `run_preflight` | `run_adoption_preflight` | Partial | No |
| Guard | `scope_guard.check` | `build_guard_evidence` | Partial | No |
| Test Plan | command registry | `build_adoption_test_plan` | Partial | No |
| Test Run | `command_runner.run` | `run_adoption_test_plan` | Partial | No |
| Verification | `verification_builder.build` | `verify_adoption` | Partial | No |
| Closure | `closure_evaluator.close` | `close_adoption` | Partial | No |
| State | atomic writer / ProjectState | `transition_project_state` | Partial | No |

The architecture does not reimplement the whole Runtime lifecycle, but the adapter boundary is not yet sufficiently provenance-bound to support 04F-R1.

## Findings

### P0 — Test runner can disclose sensitive test output

`governance/verification/command_runner.py` returns the final stdout/stderr lines verbatim. `run_adoption_test_plan` preserves those summaries unchanged. A synthetic secret in test output would therefore reach TestRunEvidence and potentially reports. This violates the required sensitive-data canary boundary.

### P1 — Lifecycle context omits required provenance and trusts caller-provided candidates

`AdoptionLifecycleContext` contains no Runtime manifest digest, final-install approval digest, compiler identity, blocked decisions, or independently recomputed confirmation provenance. `build_lifecycle_context` accepts confirmed candidate IDs from its caller instead of loading and validating the approved confirmation/plan. Modified Runtime manifests, final approvals, compiler identities, cross-bundle replay, and authority changes are consequently not fully fail-closed at the Preflight bridge.

### P1 — TaskContract-to-TaskRequest mapping loses security constraints

The mapping preserves allowed paths and forces external/production false, but it neither represents nor verifies denied scope, blocked decisions, confirmed candidates, Git/release restrictions, or unknown authority. The subsequent formal Preflight contract may add defaults but cannot prove that every original adoption restriction was preserved.

### P1 — State transition accepts arbitrary evidence labels and digests

`transition_project_state` validates only non-empty evidence type and a 64-character digest. It does not constrain the required evidence type for each transition, recompute evidence files, bind target identity, or reject a semantically wrong digest. It is atomic at the file-write level, but the evidence CAS contract is incomplete.

### P1 — Verification and Closure omit required provenance/state rechecks

`verify_adoption` only binds a caller-supplied context digest plus Guard/Test evidence. It does not independently bind install/activation provenance, current ProjectState digest, target identity, or required evidence-file digests. `close_adoption` only rechecks workspace freshness and formal Verification status; it does not recheck provenance, ProjectState digest, unresolved blockers, or denied-scope state.

## Confirmed positive controls

- The adapter calls the existing formal `run_preflight`; it does not duplicate Preflight decision logic.
- Scope Guard, command runner, Verification builder, Closure evaluator, and atomic writer are reused rather than rewritten.
- State edges are forward-only in `NEXT`; skipped/reverse stage requests are rejected.
- Test Plan validates an exact registry-command digest and rejects obvious install/network tokens.
- Workspace snapshot hashes paths, types, and file/symlink content references without returning file bodies.
- Closure output explicitly states `production_ready = false`, `released = false`, and `deployed = false`.

## Audit conclusion

The listed P0 and P1 findings block 04F-R1 and release-closeout. A follow-up implementation task must repair the findings, add adversarial tests for every listed canary, then request a new independent audit. This audit did not modify or restore 04F-R1.

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B-AUDIT
REQUIRES_REVISION
P0_SENSITIVE_TEST_OUTPUT_LEAK
P1_PROVENANCE_AND_EVIDENCE_CHAIN_INCOMPLETE
NOT_READY_FOR_04F-R1
NOT_READY_FOR_RELEASE_CLOSEOUT
```
