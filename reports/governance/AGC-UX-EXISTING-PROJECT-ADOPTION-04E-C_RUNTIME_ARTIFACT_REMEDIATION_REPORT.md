# AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C Runtime Artifact Remediation Report

## Blocker and architecture decision

04F-A identified that the former 04E installation copied adoption drafts into target `task.yaml` and `project_state.yaml`, while the Runtime requires a `TaskContract` and `ProjectState`. This remediation establishes the approved boundary:

```text
04D external drafts → 04E-C in-memory Runtime compiler → Schema-valid new files → external receipt
```

Activation does not compile or convert artifacts.

## Implementation

- Added `governance/adoption/runtime_artifact_compiler.py`.
- The compiler validates Plan, confirmation, manifest bindings, and exact untrusted-draft semantics before rendering Runtime inputs in memory.
- The compiler emits a deterministic Runtime `TaskContract` and `ProjectState`, validates both official schemas before target writes, and never writes files itself.
- `install-approved` now writes only the compiled Runtime artifacts. It retains new-files-only behavior and does not activate state, run Preflight, Guard, tests, Verification, Closure, network, or Git operations.
- Installation receipts record compiler version, source-draft digests, Runtime artifact paths/digests, and Runtime schema identifiers.
- Receipts without Runtime compiler metadata are fail-closed for assessment with `LEGACY_ADOPTION_DRAFT_INSTALL_UNSUPPORTED`.

## Runtime semantics

The Runtime schemas intentionally have no activation-status field. `INSTALLED_NOT_ACTIVATED` remains the bounded installation-receipt state; the installed Runtime contract is `DRAFT`, the project state is valid `EXECUTION` configuration, and no test, verification, closure, production, release, network, or Git-write authorization is created.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.unit.test_agent_adopt_install \
  tests.unit.test_agent_adopt_export \
  tests.unit.test_agent_adopt \
  tests.unit.test_agent_adopt_assessment_safety \
  tests.unit.test_public_adoption_assets
55 passed

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
132 passed

PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py
PASS (28 schemas, rules index, module registry, references)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py
PASSED (146 Python files)

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py
PASS (28 schemas, stable fields and enums)

git diff --check
PASS
```

## Boundaries and next step

All targets were synthetic local fixtures; no real project, credential, network request, Git write, activation, Runtime lifecycle command, or 04F/04F-A execution occurred. The next permitted step is the independent `04E-C-AUDIT`; this result does not authorize activation or 04F.

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C
IMPLEMENTED
RUNTIME_ARTIFACT_COMPILER_VERIFIED
TASK_CONTRACT_SCHEMA_VERIFIED
PROJECT_STATE_SCHEMA_VERIFIED
INSTALLED_NOT_ACTIVATED_RUNTIME_STATE_VERIFIED
READY_FOR_04E-C-AUDIT
```
