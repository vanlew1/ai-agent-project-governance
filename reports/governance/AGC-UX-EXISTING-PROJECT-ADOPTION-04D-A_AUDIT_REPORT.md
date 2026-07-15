# AGC-UX-EXISTING-PROJECT-ADOPTION-04D-A Audit Report

## Scope and workspace attribution

- Mode: independent local read-only security audit; no network, credentials, target-project writes, Git writes, or 04E actions.
- Baseline HEAD: `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1`, branch `ux/adoption-planner-04b-audit`.
- At audit start, all modified code, docs, schemas, registry, tests, and the 04D implementation report were attributable to 04D. The pre-existing `AGC-UX-EXISTING-PROJECT-ADOPTION-04C_GITHUB_AUDIT_REPORT.md` remained separate and untouched.
- This audit added only this report in the repository; temporary canaries were isolated under `/tmp/agc-adoption-04d-a/`.

## Positive verification

- CLI exposes `dry-run` and `export-drafts`; the latter rejects missing required arguments. `apply` is rejected as an unknown mode.
- Plan digest uses canonical JSON (sorted keys and compact separators), and confirmation digest is recorded in the manifest. Mismatched confirmation digests are rejected.
- Schema rejects false confirmation, unknown confirmation fields, invalid blocked-decision values, and unsupported confirmation fields.
- Socket tripwire canaries exported Python, Node, generic, and Chinese/space-path targets without socket use, target file-tree/hash/mtime change, `.agent_state`, sentinel execution, or secret/private-key content in drafts.
- Internal, `..`, symlink-to-target, and non-empty output paths were rejected. Static review found no subprocess, shell, package-manager, Git, HTTP, or socket call in the 04D export path; its only writes are the explicitly requested external draft directory.
- Generated drafts and manifest consistently state untrusted/not-installed/not-activated/non-executed status. Manifest contains the required false flags, file list, digests, unresolved fields, and blocked-decision list. Deterministic content generation is supported by canonical digests and fixed file ordering.

## Findings

### P1 — Plan is not bound to target-project identity

`adoption_plan.schema.json` fixes `project_root` to `<target-project>` and `build_plan()` hashes that sanitized value. The export CLI accepts a separate `--target-project-root`, but does not compare it with any Plan-bound target identity. The audit reproduced exporting a valid Plan/confirmation generated for one synthetic target while supplying a different synthetic target root. This does not write either target in 04D, but it violates the required target-identity/digest binding and is unsafe as a prerequisite for 04E.

### P1 — Duplicate test candidate IDs are accepted

The Plan schema has no uniqueness constraint for `test_candidates[].candidate_id`, and `_validate_confirmation()` converts IDs to a set. A Plan with two candidates using the same ID, recomputed valid Plan digest, and matching confirmation was accepted; draft generation resolves the first matching command. This makes a user selection ambiguous and violates fail-closed candidate binding.

## Consistency and privacy

- The normal successful bundle was internally consistent for selected candidate, confirmed scope, denied paths, blocked decisions, and both digests.
- Target paths are sanitized in the manifest; audit fixtures containing an API key and private-key text did not appear in any exported file.
- Misleading-term search found only explicit negative/status wording such as `NOT_INSTALLED`, `NOT_ACTIVATED`, “not authorized”, and “not approved”; no positive completion claim was found in the export implementation.

## Verification

- Directed: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_agent_adopt_export tests.unit.test_agent_adopt tests.unit.test_public_adoption_assets` — 17 passed.
- Full: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest` — 94 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py` — passed.
- `git diff --check` — passed.

## Not executed

- No real external network, production data, credentials, package manager, build, candidate test, Git write, or target-project operation was executed.
- Windows-only path normalization and intentional permission-denied paths were not independently executed in this Linux-only synthetic audit; they are not needed to establish the two P1 findings.

## Conclusion

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04D-A
REQUIRES_REVISION
CLOSEOUT_BLOCKED
NOT_READY_FOR_04E
```

04E must remain blocked until target identity becomes a Plan-bound, privacy-preserving verified value and duplicate candidate identifiers fail closed. Re-audit those fixes before a 04E decision.
