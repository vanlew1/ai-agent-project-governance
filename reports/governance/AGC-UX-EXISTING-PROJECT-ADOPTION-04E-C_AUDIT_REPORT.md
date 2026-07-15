# AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C Independent Audit Report

## Scope

Read-only independent audit of 04E-C. No implementation, test, Schema, or documentation file was modified. No activation, 04F-A, 04F, real target, network request, or Git write operation occurred.

## Verified evidence

- The compiler is an in-memory function and has no filesystem, subprocess, network, Git, activation, Guard, test, Verification, or Closure call.
- The compiler explicitly validates the adoption Plan and confirmation, constrains draft keys, checks confirmed scopes, and validates generated mappings against `task_contract.schema.json` and `project_state.schema.json` before installation.
- The installer retains exclusive new-file creation, external receipt handling, partial-install manual recovery, and target-internal receipt rejection.
- Generated Runtime task/state files are covered by the directed installation tests and pass their formal schemas.
- Receipts record compiler version, source-draft digests, Runtime artifact paths/digests, and schema identifiers. Draft-only receipts are rejected by assessment.
- Directed adoption suite: 55 passed. Full suite: 132 passed. Governance validation, code quality, Schema compatibility, and `git diff --check` passed.

## Findings

### P1 — final approval does not bind the compiled Runtime bytes

`adoption_final_approval` binds Plan, confirmation, and export-manifest digests, but it contains neither compiler version nor expected Runtime artifact digests. The compiler is deterministic today, yet a future compiler change can produce different `task.yaml` / `project_state.yaml` bytes under an unchanged approval. The receipt records the result only after the approval has been consumed.

This does not satisfy the 04E-C requirement that final install approval bind the formal Runtime files. The missing binding prevents approving 04F-A.

### P1 — installation does not independently invoke Runtime model loaders

The compiler uses JSON Schema validation, but `install_approved` does not independently construct the Runtime `TaskContract` and `ProjectState` model objects before writing. The intended Schema-plus-loader pre-write sequence is therefore not fully demonstrated.

## Matrix and provenance conclusion

The positive schema/install/legacy-receipt path is supported by the directed tests. The complete audit matrix cannot pass while the two P1 findings remain: a runtime-artifact approval can become stale after compiler behavior changes, and the explicit Runtime-loader pre-write invariant is incomplete. No repair was made because this is an audit.

## Final status

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C-AUDIT
REQUIRES_REVISION
NOT_READY_FOR_04F-A
NOT_READY_FOR_04F
```

Recommended next step: a bounded 04E-C remediation that makes Runtime artifact digests and compiler version approval-bound, then invokes the existing Runtime model loaders during pre-write validation. Re-run this audit afterward.
