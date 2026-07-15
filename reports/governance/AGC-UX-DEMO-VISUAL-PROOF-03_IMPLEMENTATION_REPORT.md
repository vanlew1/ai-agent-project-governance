# AGC-UX-DEMO-VISUAL-PROOF-03 Implementation Report

> Historical record. The two evidence-boundary issues identified in the final content audit were remediated by `AGC-UX-DEMO-VISUAL-PROOF-03R`; see `AGC-UX-DEMO-VISUAL-PROOF-03R_REMEDIATION_REPORT.md` for the current behavior and validation.

## Baseline

- Mode / level: EXECUTION, B, Level 2; local-only.
- Baseline branch / HEAD: `main` / `1860601f76e394569f71dab56443296ca2080f70`.
- No network, external API, production data, remote Git operation, commit, push, PR, tag, or release was used.

## Changes

- Replaced the recording instructions in `docs/DEMO.md` with a reproducible synthetic walkthrough and clear limitations.
- Added `examples/demo/run_visual_proof.py`, which creates disposable local repositories, invokes the existing Guard and verification/closure components, sanitizes the resulting summaries, and renders SVG plus transcript and JSON evidence.
- Added `docs/assets/demo/visual-proof.svg`, `visual-proof-transcript.txt`, and `visual-proof-summary.json`.
- Added a concise Demo entry in both README files and direct tests for generated assets and document links.

## Scenario Evidence

| Scenario | Command / local action | Exit | Result |
| --- | --- | ---: | --- |
| Scope block | `python <repository>/scripts/agent_guard.py check` after changing `restricted-change.txt` outside `src/` | 3 | `BLOCKED`; `denied_changes: [restricted-change.txt]` |
| Stale verification | Focused `python -m unittest discover -s tests`, then `closure_evaluator.close(..., stale=True)` after a synthetic workspace change | 3 | Verification `VERIFIED`; Closure `BLOCKED` with `verification_stale_after_workspace_change` |
| Fresh closure | Focused `python -m unittest discover -s tests`, then `closure_evaluator.close(..., stale=False)` | 0 | Verification `VERIFIED`; Closure `CLOSED` |

The complete sanitized command summaries are in `docs/assets/demo/visual-proof-transcript.txt` and `docs/assets/demo/visual-proof-summary.json`. The runner cleaned its disposable projects; no `agc-demo-visual-proof-*` temporary directory remains.

## Validation

- `python3 -m unittest tests.unit.test_demo_visual_proof tests.unit.test_public_adoption_assets` — PASS (7 tests).
- `python3 -m unittest` — PASS (78 tests).
- `python3 scripts/validate_governance.py` — PASS (22 schemas, rules index, module registry, references).
- `python3 scripts/check_code_quality.py` — PASS (135 Python files; no warnings).
- `git diff --check` — PASS.
- Privacy and claim-language searches over the public Demo scope — no matches after sanitization.

## Scope and Risks

- This task changed only Demo assets, documentation, directly related tests, and this report; Governance Runtime behavior, schemas, workflows, and Git configuration were not changed.
- The demo is explicitly synthetic. Scenario 2 demonstrates the existing closure evaluator with the observed stale condition supplied as input; it does not claim universal automatic change detection.
- Pre-existing modifications retained without alteration: `README.md`, `README.zh-CN.md`, `docs/COMPATIBILITY.md`, `docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md`, and two earlier governance reports. Only the small Demo-entry additions in the README files belong to this task.

## Final Status

`AGC-UX-DEMO-VISUAL-PROOF-03` — `IMPLEMENTED`, `VERIFICATION_PASSED`, `READY_FOR_CONTENT_AUDIT`.
