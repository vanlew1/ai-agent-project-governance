# Governance Runtime CI Guide

Run `python scripts/run_governance_ci.py` before release-oriented changes. It is read-only and uses fixed Python argv: governance and reference validation, schema compatibility, dependency direction, isolated bootstrap, CI security, tests, quality, and syntax checks. GitHub Actions calls the same script on Linux; its Windows smoke separately covers Unicode bootstrap and compilation. The workflow uses only `contents: read`, no secrets, and no write or publish operations.

## Release test timeout policy

The tests gate uses `config/release_gate.yaml` and `release_gate.test_timeout_seconds`. The framework default is 600 seconds when that file is absent. Explicit values must be integers from 60 through 3600; zero, negative, boolean, float, string, null, empty, out-of-range, malformed, and unexpected configuration values fail closed. The other seven gates keep their existing 300-second finite timeout.

This timeout is a hang guard, not a performance benchmark. It does not change the test command, selection, ordering, or pass/fail handling.

Audit fields have these meanings:

- `effective_timeout_seconds`: finite subprocess limit selected from the framework config or fallback default; it is not a speed target.
- `timeout_source`: `framework_config`, `framework_default`, or `gate_default`; it identifies policy origin, not trust or approval.
- `elapsed_seconds`: monotonic wall-clock duration observed by the runner; it is not CPU time.
- `timeout_result`: `COMPLETED`, `TIMEOUT`, or `NOT_STARTED`; `COMPLETED` does not mean tests passed.
- `exit_classification`: `PASS`, `FAIL`, `TIMEOUT`, `ERROR`, or `CONFIGURATION_ERROR`.

For example, a failing test process that returns after 420 seconds reports `timeout_result=COMPLETED` and `exit_classification=FAIL`; it is not mislabeled as a timeout or a performance failure.

## V1 release preparation

A local PASS verifies the eight fixed gates only. It does not prove a remote GitHub Actions run; commit, push, and remote-run observation require explicit user authorization.
