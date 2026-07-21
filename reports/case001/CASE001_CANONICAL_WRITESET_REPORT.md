<!-- encoding: UTF-8 -->

# CASE-001 Canonical Write-Set Report

## Result

`governance/adoption/writeset.py` is the single classifier and sidecar builder used by planning, runtime compilation, approval, installation, and receipts.

The formal runtime bundle contains, before any target write:

- `INSTALL_WRITESET.json`
- `PRE_INSTALL_HASHES.json`
- `ROLLBACK_MANIFEST.json`

Each file is schema-validated, digest-bound into `RUNTIME_ARTIFACT_MANIFEST.json`, created exclusively, and written as UTF-8/LF with flush/fsync semantics.

## Classifications

- `CREATE`: absent installable target.
- `MODIFY`: supported by the canonical model but not authorized by this new-files-only installer.
- `SKIP`: exact no-op asset state.
- `FAIL_ON_EXISTING`: `task.yaml` or `project_state.yaml` already exists.
- `MANUAL_ADOPTION_ASSET`: existing `AGENTS.md`, config, preset, or script requiring human reconciliation.

The installer consumes and revalidates the compiler-produced sidecars. It does not generate them after target writes. A partial write can only produce a manual-recovery receipt; automatic rollback remains unsupported.

## Identity policy

Machine artifacts use raw byte SHA-256 identity. Human-readable text comparisons retain both raw and explicitly named normalized-text SHA-256 digests, with CRLF/LF behavior covered by tests.
