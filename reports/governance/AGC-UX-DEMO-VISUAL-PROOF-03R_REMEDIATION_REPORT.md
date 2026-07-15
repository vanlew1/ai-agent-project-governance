# AGC-UX-DEMO-VISUAL-PROOF-03R Remediation Report

## Scope

- Mode / level: EXECUTION, B, Level 2; local-only.
- Baseline branch / HEAD: `main` / `1860601f76e394569f71dab56443296ca2080f70`.
- No network, external API, production data, remote Git operation, commit, push, PR, tag, or release was used.

## Remediated Findings

- Real Guard and `unittest` subprocess results now feed the existing Verification builder and Closure evaluator. A real failing synthetic test produces `FAIL` → Verification `FAILED` → Closure `FAILED`; the runner returns non-zero.
- Default output now uses a new repository-external temporary directory. Repository-local `--output-dir` is rejected; only explicit `--publish-assets` writes `docs/assets/demo/`.
- The SVG is now a 600px vertical status-card view with 17–25px type and shortened commands. The transcript retains commands, real exit codes, Guard/test states, and sanitized output summaries.
- Demo instructions distinguish Windows PowerShell `python` from Linux / WSL / macOS `python3`.

## Real Demo Checks

| Mode | Command | Result |
| --- | --- | --- |
| Default | `python3 examples/demo/run_visual_proof.py` | Exit 0; output created under `/tmp`; `git status --short` unchanged. |
| Publish | `python3 examples/demo/run_visual_proof.py --publish-assets` | Exit 0; refreshed the three controlled assets under `docs/assets/demo/`. |
| Guardrail | `python3 examples/demo/run_visual_proof.py --output-dir docs/assets/demo` | Exit 2; repository-local default output rejected. |

Normal published evidence records:

1. Scope Guard: `BLOCKED`, exit `3`, denied `restricted-change.txt`.
2. Fresh test then observed stale condition: Verification `VERIFIED`, Closure `BLOCKED`, exit `3`.
3. Fresh Guard/test evidence: Verification `VERIFIED`, Closure `CLOSED`, exit `0`.

## Validation

- `python3 -m unittest tests.unit.test_demo_visual_proof` — PASS (5 tests), including an actual failing synthetic test and default/publish boundary checks.
- `python3 -m unittest tests.unit.test_public_adoption_assets` — PASS (5 tests).
- `python3 -m unittest` — PASS (81 tests).
- `python3 scripts/validate_governance.py` — PASS.
- `python3 scripts/check_code_quality.py` — PASS (135 Python files; no warnings).
- `git diff --check` — PASS.
- Privacy and high-risk claim searches over README, Demo, demo assets, and runner — no matches.

## Files and Boundaries

- Modified: Demo runner, Demo documentation, published demo SVG/transcript/summary, directly related tests, and the historical/report records.
- Retained without alteration: pre-existing README, compatibility, repository-settings, test, and earlier-report changes outside this remediation scope.
- A temporary output directory created during verification was removed. No `agc-demo-visual-proof-03-*` temporary directory remains.

## Residual Risk

Scenario 2 remains deliberately narrow: the stale condition is observed after a synthetic workspace change and explicitly supplied to the existing closure evaluator. It does not claim universal automatic workspace-change detection.

## Final Status

`AGC-UX-DEMO-VISUAL-PROOF-03R` — `IMPLEMENTED`, `VERIFICATION_PASSED`, `READY_FOR_REAUDIT`.
