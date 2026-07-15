# AGC-UX-01 Implementation Report

## Modified files

- `README.md`, `docs/GETTING_STARTED.md`, `docs/ADOPTION_AUDIT.md`, `docs/PRESETS.md`, and `docs/examples/`
- `governance/audit/` and `scripts/agent_audit.py`
- `config/presets/` and `scripts/init_new_project.py`
- `.github/ISSUE_TEMPLATE/adoption_feedback.yml`
- `tests/unit/test_agent_audit.py`, `tests/unit/test_init_presets.py`, `tests/unit/test_public_adoption_assets.py`
- `docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml`

## Core changes

- Added a deterministic local read-only audit with text/JSON renderers, fixed scoring, transparent status evidence, and preset recommendation.
- Added centralized lightweight, standard, and strict preset definitions. Initialization preserves the full template and writes the selected initial-focus configuration.
- Reworked the README entry content without removing the existing Runtime overview; added five-minute setup, safety, documentation, and synthetic-demo links.
- Added newcomer docs, synthetic Python/Node fixtures, encoding/issue-form checks, and privacy-preserving adoption feedback.

## Audit contract and exit codes

- Default operation is local, deterministic, and read-only. It does not use network access, telemetry, coding agents, Git object content, credentials, environment values, or private data-file contents.
- `--output` is opt-in and constrained below the audited root. `0` means the audit completed; `2` is an invalid root; `3` is an internal/output error; `4` is a failed check under `--strict`.

## Preset differences

- `lightweight`: agent entry, scope, one local test, Git/credential/external boundaries, and a short close-out report.
- `standard`: task classification, module boundaries, test planning, change records, and closure records.
- `strict`: approval/state/guard controls plus complete verification, handoff, and audit evidence. It does not claim to guarantee safety.

## Validation

- `python -m unittest tests.unit.test_agent_audit tests.unit.test_init_presets tests.unit.test_public_adoption_assets` — 11 passed.
- `python scripts/agent_audit.py --project-root docs/examples/python-minimal --format json` — completed; `standard` recommendation verified.
- `python scripts/run_governance_ci.py` — PASS, 8/8 gates (including the full test suite).

## Risks and follow-up

- The worktree already contained unrelated uncommitted changes at start. They were preserved; this report only describes AGC-UX-01 work.
- No remote, GitHub setting, publish, release, commit, or push action was performed.
- Manual GitHub follow-up: enable Template Repository and Discussions if desired; review About/Topics/social preview, branch protection, Release-page/README links, and Chinese/arrow rendering in the GitHub web UI.
