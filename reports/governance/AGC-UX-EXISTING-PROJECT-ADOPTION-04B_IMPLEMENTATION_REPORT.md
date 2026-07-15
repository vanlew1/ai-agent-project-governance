# AGC-UX-EXISTING-PROJECT-ADOPTION-04B Implementation Report

## Result

`AGC-UX-EXISTING-PROJECT-ADOPTION-04B` — `IMPLEMENTED`; `READ_ONLY_BOUNDARY_VERIFIED`; `READY_FOR_CONTENT_AND_SAFETY_AUDIT`.

## Baseline

- Branch: `main`; HEAD: `1860601f76e394569f71dab56443296ca2080f70`; version: `1.0.0`.
- The pre-existing UX documentation, demo assets, reports, and public-asset test changes were retained without modification.

## Implementation

- Added `scripts/agent_adopt.py` with one public mode: `dry-run`.
- Added `governance/adoption/` to compose existing Adapter detection and adoption Audit evidence into an untrusted plan.
- Added `schemas/adoption_plan.schema.json`; the planner validates every JSON plan before rendering it.
- Added a minimal Existing Project Adoption document entry. It explains stdout/external-output behavior and states that no apply, install, activate, or one-click mode exists.
- Registered the planner module and updated the schema-count validation expectations from 22 to 23.

CLI:

```bash
python3 scripts/agent_adopt.py --project-root /path/to/project --format markdown dry-run
python3 scripts/agent_adopt.py --project-root /path/to/project --format json --output /tmp/adoption-plan.json dry-run
```

## Output and safety boundary

The JSON and Markdown plan provide Adapter evidence, local audit result, Preset recommendation, test candidates, asset manifest/conflicts, untrusted `task.yaml` and `project_state.yaml` drafts, confirmations, blocked decisions, next-command preview, rollback checklist, and warnings.

The planner sanitizes the target root in output, never creates `.agent_state`, never runs candidate tests, and never copies assets or creates formal configuration. It rejects `--output` paths inside the scanned project and refuses to overwrite an existing output. Confidence fields are explicitly defined as static evidence completeness; they do not imply safety, test success, authorization, or automatic selection.

## Canary and verification

- Isolated Python, Node, and generic CLI canaries each ran in `dry-run` mode; the synthetic target file-tree/content snapshot was unchanged and no `.agent_state` appeared.
- Unicode and space-containing target paths are covered by the CLI tests.

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_agent_adopt` | PASS — 8 tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_agent_adopt tests.unit.test_adapter_detection tests.unit.test_agent_audit tests.unit.test_public_adoption_assets` | PASS — 24 tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest` | PASS — 90 tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py` | PASS — 23 schemas, rules index, module registry, and references. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py` | PASS — no warnings. |
| `git diff --check` | PASS — no whitespace errors. |

## Privacy and risk-word review

The required pattern search found only existing governance controls/tests and the planner's explicit deny-path wording (for example, `secrets/**`). It found no personal absolute path or credential value introduced by this task. The “one-click adopt” wording appears only in a negative statement that the feature does not exist.

## Not executed

- No real project installation, asset copy, configuration creation, state activation, Guard, test execution, Verification, or Closure.
- No network, package manager, build, external API, production-data, credential, remote, workflow, release, commit, push, PR, tag, reset, clean, rebase, or force operation.

## Remaining risks

- The asset manifest is intentionally conservative: existing directories are not recursively compared, so they require human ownership/conflict review.
- Test candidates are static suggestions only; their network/write behavior and correctness remain unresolved until the owner approves a real test plan.
- 04C must audit the rendered wording and read-only boundary before any separately authorized draft-export or copy feature.

## Changed files

Task-owned tracked changes:

- `docs/EXISTING_PROJECT_ADOPTION.md`
- `docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml`
- `scripts/validate_governance.py`
- `tests/unit/test_schema_contracts.py`

Task-owned new files:

- `governance/adoption/__init__.py`
- `governance/adoption/planner.py`
- `governance/adoption/renderer.py`
- `schemas/adoption_plan.schema.json`
- `scripts/agent_adopt.py`
- `tests/unit/test_agent_adopt.py`
- this report

## Workspace state

Pre-existing tracked changes remain in `README.md`, `README.zh-CN.md`, `docs/COMPATIBILITY.md`, `docs/DEMO.md`, `docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md`, and `tests/unit/test_public_adoption_assets.py`. Pre-existing untracked demo assets, examples, UX reports, and `tests/unit/test_demo_visual_proof.py` were preserved. No temporary test files remain in the repository.

No Git commit was created.
