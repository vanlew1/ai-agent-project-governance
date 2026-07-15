# AGC-UX-01 Close Report

## Release decision

`READY_FOR_PUBLIC_RELEASE`

The local release decision covers the checked repository contents only. It does not claim that remote GitHub settings, a published release, or a remote CI run has occurred.

## Git baseline and ownership

- Initial and final branch: `main`
- Baseline HEAD: `5024b4c6f0c9b50ddc973ce1e3b3843e2e6aa26b` (`fix: correct Windows adapter detection smoke`)
- No commit, push, release, reset, clean, or remote configuration action was performed.

The worktree was already dirty before AGC-UX-01. Pre-existing tracked modifications were: `AGENTS.md`, `README.md`, `START_HERE.bat`, `agent_rules/00_rule_router.md`, `agent_rules/15_plan_adaptation_rules.md`, `agent_rules/RULES_INDEX.yaml`, `docs/CHANGELOG.md`, `docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml`, `docs/IMPLEMENTATION_PLAN.template.md`, `governance/models/task_contract.py`, `governance/models/task_request.py`, `governance/preflight/contract_builder.py`, `governance/preflight/default_rules.py`, `governance/preflight/engine.py`, `governance/preflight/gate_resolver.py`, `governance/preflight/risk_detector.py`, `schemas/task_contract.schema.json`, `schemas/task_request.schema.json`, `scripts/init_new_project.py`, and `tests/unit/test_preflight_runtime.py`. Existing untracked community, documentation, Runtime, example, and prior-report assets were preserved. AGC-UX-01 edits to overlapping `README.md`, `scripts/init_new_project.py`, and the module registry were additive and confined to the documented feature.

AGC-UX-01 concrete files are:

- `.github/ISSUE_TEMPLATE/adoption_feedback.yml`
- `README.md`
- `config/presets/lightweight.yaml`
- `config/presets/standard.yaml`
- `config/presets/strict.yaml`
- `docs/ADOPTION_AUDIT.md`
- `docs/GETTING_STARTED.md`
- `docs/PRESETS.md`
- `docs/examples/README.md`
- `docs/examples/node-minimal/README.md`
- `docs/examples/node-minimal/package.json`
- `docs/examples/python-minimal/README.md`
- `docs/examples/python-minimal/pyproject.toml`
- `docs/examples/python-minimal/tests/test_placeholder.py`
- `docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml`
- `governance/audit/__init__.py`
- `governance/audit/checks.py`
- `governance/audit/models.py`
- `governance/audit/renderer.py`
- `governance/audit/scoring.py`
- `reports/governance/AGC-UX-01_IMPLEMENTATION_REPORT.md`
- `reports/governance/AGC-UX-01-CLOSE-REPORT.md`
- `scripts/agent_audit.py`
- `scripts/init_new_project.py`
- `tests/unit/test_agent_audit.py`
- `tests/unit/test_init_presets.py`
- `tests/unit/test_public_adoption_assets.py`

## Acceptance-to-test mapping

| Acceptance item | Test coverage |
| --- | --- |
| Empty directory, current repository, Python, Node, Chinese/space path | `test_empty_node_and_unicode_path_projects_complete`, `test_current_repository_completes_without_accessing_network`, `test_minimal_project_is_deterministic_and_recommends_lightweight`, `test_python_demo_recommends_standard` |
| Binary, oversized, and permission-limited documents | `test_large_binary_and_permission_limited_documents_are_safe` (permission error is simulated for portable Windows coverage) |
| Default read-only behavior, explicit output, deterministic results, text/JSON common model | `test_cli_default_is_read_only_and_output_is_explicit`, `test_minimal_project_is_deterministic_and_recommends_lightweight`, `test_json_contract_and_text_renderer_share_the_result_model` |
| Output-path limit and exit codes `0/2/3/4` | `test_cli_default_is_read_only_and_output_is_explicit`, `test_cli_rejects_invalid_root_and_output_escape`, `test_strict_returns_nonzero_only_for_failed_checks` |
| All presets, legacy default, and overwrite refusal | `test_all_presets_are_centrally_defined_and_distinct`, `test_default_cli_preset_preserves_the_existing_baseline`, `test_existing_target_is_not_silently_overwritten` |
| README/public-document encoding, internal links, issue YAML, and required community assets | `test_public_docs_are_utf8_without_mojibake`, `test_docs_reference_real_public_entrypoints`, `test_public_internal_links_and_community_files_exist`, `test_issue_forms_are_parseable` |

## JSON and CLI contract

The JSON renderer is tested for `schema_version`, `tool_version`, `project_root_display`, `score`, `level`, `recommended_preset`, and `checks`. Check statuses are constrained by test to `PASS`, `WARN`, `FAIL`, `NOT_APPLICABLE`, or `SKIPPED`.

Exit code `0` means the audit completed (warnings or failures may still be present); `2` is an invalid project root; `3` is an audit/output error such as a disallowed output path; `4` is a failed check under `--strict`.

## Community-file status

The following exist and the issue forms parse as YAML: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, and `.github/ISSUE_TEMPLATE/adoption_feedback.yml`.

## Verification evidence

- Working directory: `C:\Users\范德彪\Documents\github开源上传\ai-agent-project-governance`
- Python: `3.13.14`; dependency: `PyYAML 6.0.3`
- `python -m unittest tests.unit.test_agent_audit tests.unit.test_init_presets tests.unit.test_public_adoption_assets`: 18 passed, 0 failed, 0 skipped.
- `python scripts/validate_governance.py`: PASS (22 schemas, rules index, module registry, references).
- `python scripts/check_schema_compatibility.py`: PASS (22 schemas, stable fields and enums).
- `python scripts/check_template_integrity.py`: PASS (isolated adapters and Unicode path).
- `python scripts/run_governance_ci.py`: PASS (8/8 gates; tests, quality, and syntax included).
- `python -m unittest discover -s tests -p test_*.py`: 76 passed, 0 failed, 0 skipped.
- No JUnit or machine-readable test-summary file was generated. No warnings were emitted by the final quality gate.

## Risks and manual follow-up

- `git diff --check` reports a pre-existing trailing blank line in `START_HERE.bat`; this file was outside the close-plan write scope and was not modified.
- The worktree remains dirty and uncommitted by design; before publishing, stage only reviewed task files and reconcile the pre-existing changes separately.
- On GitHub, manually verify Template Repository/Discussions choice, About/Topics/social preview, default-branch protection, Release-page/README links, and Chinese/arrow rendering. These remote settings were not changed or verified locally.
