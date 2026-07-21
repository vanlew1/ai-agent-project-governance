<!-- encoding: UTF-8 -->

# CASE-001 Findings Reconciliation Report

## Result

- Canonical JSON IDs: `CASE-001-FINDING-001` through `CASE-001-FINDING-009`, each exactly once.
- Canonical Markdown IDs: the same nine IDs, each exactly once.
- Every machine record has `status`, `evidence`, `resolution`, and `framework_version`.
- `CASE-001-FINDING-003` is `PARTIALLY_FIXED`; Toolchain Provenance Binding is not a keyed signature.
- `CASE-001-FINDING-005` is `PARTIALLY_FIXED`; deterministic manual-only classification does not claim automatic semantic merge.
- `CASE-001-FINDING-006` is `DEFERRED`; rejected legacy merge candidates are not reused.

## Preserved raw evidence

The Replay worktree remains the immutable source for the original ledger and rollup. It was not edited during remediation. The original Markdown ledger repeats Finding 009 and the JSON ledger omits status on Findings 001–008. The legacy rollup retains exactly three illegal C0 bytes (`0x07`, `0x07`, `0x00`). Those bytes are preserved for audit only and are excluded from the canonical current ledger and handoff.

## Authoritative current files

- `reports/case001/CASE001_FINDINGS_LEDGER.json`
- `reports/case001/CASE001_FINDINGS_RESOLUTION_MATRIX.md`
- `reports/case001/CASE001_FINDINGS_RECONCILIATION_REPORT.md`
