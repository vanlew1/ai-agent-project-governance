# GOV-RUNTIME-V1 Windows Smoke CLI Fix Report

## Status

GOV-RUNTIME-V1: LOCAL_COMPLETED
Remote validation: FAILED on prior workflow; local Windows smoke repair validated, awaiting scoped commit/push authorization.

## Root cause

The Windows workflow called `python scripts/agent_detect_adapter.py --root .` without the required `detect`, `list`, or `show` subcommand. The CLI rejected the invocation before Adapter detection.

## Repair

- Windows smoke now calls `python scripts/agent_detect_adapter.py --root . detect`.
- The template repository intentionally has no stack marker: existing tests define its `generic` `FALLBACK` detection as valid. The workflow therefore accepts only the CLI's documented fallback exit code `2`; all other exit codes still fail the job.
- Added a CI parity assertion for both the explicit `detect` command and the narrowly scoped fallback branch.

## Local verification (2026-07-13)

- Adapter detect: executed; generic `FALLBACK` accepted by Windows smoke policy.
- CI security: PASS.
- CI parity regression: 1 passed.
- Full regression: 50 passed.
- Governance validation: PASS, 22 schemas.
- Code quality: PASSED, 117 Python files scanned.
- Unified release gate: PASS, 8/8 gates.

## Boundaries

The Adapter CLI, its exit semantics, workflow permissions (`contents: read`), Secrets policy, Linux gate, publishing/deployment posture, and P0?P6 runtime behavior were not changed. No commit, push, tag, PR, Release, reset, restore, clean, stash, rebase, or force operation was performed.

## Next authorization

A scoped commit and push authorization is required for `.github/workflows/governance-ci.yml`, `tests/integration/test_p5_ci_command_parity.py`, and this report. The following Actions run must then be checked for both Linux governance and Windows smoke.
