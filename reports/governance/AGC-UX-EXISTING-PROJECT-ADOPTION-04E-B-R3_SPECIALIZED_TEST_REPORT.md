# AGC-UX-EXISTING-PROJECT-ADOPTION-04E-B-R3 Specialized Safety Test Report

## Scope and boundary

- Synthetic targets were confined to `/tmp/agc-adoption-04e-b-r3/`.
- No real project, network request, credential, production data, Git write, activation, test/build execution in a target, Verification, Closure, or 04F action occurred.
- Existing R1/R2 reports were preserved.

## Remediation

`install_approved` no longer deletes files after a later target write fails. It now preserves the already-created files and writes a receipt with `PARTIAL_INSTALL_REQUIRES_MANUAL_RECOVERY`, `installed: false`, and the exact created-file/hash subset. `assess-rollback` can read that receipt, but remains read-only.

## Destructive and execution tripwires

`tests.unit.test_agent_adopt_assessment_safety` monkeypatches the formal `assess_rollback` entry point against `os.unlink`, `Path.unlink`, `os.remove`, `os.rmdir`, `Path.rmdir`, `os.rename`, `os.replace`, `shutil.rmtree`, `shutil.move`, copy operations, target write APIs, `os.open` target-write flags, subprocess APIs, shell APIs, socket APIs, and `urllib.request.urlopen`.

All tripwire tests passed. Target and receipt snapshots include content hashes, mtime, inode, and mode. The assessment creates only its explicit external output; no target temporary file, log, cache, or `__pycache__` was observed.

## Output and synthetic matrix

The named `test_full_synthetic_matrix` covers matrix IDs 1–36 with synthetic Python/Node/generic/non-Git identities, Unicode and space paths, canonical symlink roots, target-internal receipt/output rejection, conflict/replay/tamper boundaries, partial-install handling, point-in-time state semantics, privacy, and execution sentinels. The matrix assertion completed with every scenario ID present and passing.

Assessment output inside the target or through a target symlink was rejected. A modified installed file was reported as `MODIFIED`; unchanged files remain `UNCHANGED_AT_CHECK_TIME`. Assessment output contains only hashes and relative names, not fixture body content.

## Partial-install verification

An injected second write failure left the first file in place, did not create the remaining file, generated the external partial receipt, and produced a read-only manual assessment. No automatic delete or recovery command was executed.

## Commands and results

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.unit.test_agent_adopt_install \
  tests.unit.test_agent_adopt_assessment_safety \
  tests.unit.test_agent_adopt_export \
  tests.unit.test_agent_adopt \
  tests.unit.test_public_adoption_assets
52 passed

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
129 passed

PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py
PASS (28 schemas, rules index, module registry, references)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py
PASSED (145 Python files)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py
PASS (28 schemas, stable fields and enums)

git diff --check
PASS
```

## Result

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04E-B-R3
SPECIALIZED_SAFETY_TESTS_PASSED
DESTRUCTIVE_TRIPWIRES_VERIFIED
FULL_SYNTHETIC_MATRIX_VERIFIED
```
