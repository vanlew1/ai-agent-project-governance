# AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C-B-R1 Remediation Report

## Result

P1-01 is remediated. 04E now fixes Runtime bytes before final approval and installs only those approved bytes. P1-02 remains in force: the official Schema validators and the formal `TaskContract.from_mapping` and `ProjectState.from_mapping` loaders run before target writes.

## Root cause and repair

The prior installer regenerated Runtime files from draft inputs after final approval. Its approval could bind the draft/export provenance but not the compiler identity or exact files that reached the target.

- Added `compile-runtime-artifacts`, which writes a target-external, empty-or-new Runtime preview bundle containing exactly two Runtime YAML files and `RUNTIME_ARTIFACT_MANIFEST.json`.
- The manifest records a canonical self-digest, exact byte digests, plan/confirmation/export provenance, source-draft digests, and compiler id/version/digest.
- Final approval now requires the Runtime manifest digest, compiler identity, and the two Runtime byte digests. Legacy draft-only approvals fail closed with `LEGACY_RUNTIME_ARTIFACT_APPROVAL_UNSUPPORTED`.
- `install-approved` now requires `--runtime-artifact-bundle`; it verifies every binding, recomputes compiler identity, validates exact preview bytes with both Schemas and official Runtime loaders, then writes the approved bytes using exclusive creation. It does not compile.
- Existing conflict refusal, target-external receipt, partial-install manual recovery, read-only rollback assessment, no activation, no network, and no Git-write boundaries remain covered.

The compiler output path additionally requires `--target-project-root`: the sanitized external plan intentionally omits the private absolute target path, so this explicit local-only argument is necessary to reject output inside the target or through a symlink.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
130 passed

PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py
PASS (29 schemas, rules index, module registry, references)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py
PASSED (146 Python files; no warnings)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py
PASS (29 schemas, stable fields and enums)

git diff --check
PASS
```

## Safety and scope

All validation used synthetic local fixtures under `/tmp`; no real project, credential, network operation, Git write, activation, Preflight, Guard, test execution against an adopted target, Verification, Closure, 04F-A, or 04F action occurred. The existing failed 04E-C audit report was preserved.

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C-B-R1
IMPLEMENTED
P1-01_REMEDIATED
P1-02_REGRESSION_PROTECTED
READY_FOR_04E-C-A-R1
NOT_READY_FOR_04F-A
NOT_READY_FOR_04F
```
