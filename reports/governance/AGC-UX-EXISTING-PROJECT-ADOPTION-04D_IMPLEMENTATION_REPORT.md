# AGC-UX-EXISTING-PROJECT-ADOPTION-04D Implementation Report

## Baseline and scope

- Baseline HEAD: `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1`.
- Implemented `export-drafts` only in the framework repository. No target project, network, external API, runtime-state, Git, release, or production operation was performed.

## Delivered capability

- `scripts/agent_adopt.py export-drafts` requires a JSON Plan, YAML/JSON confirmations, explicit external output directory, and target root used solely for output-boundary validation.
- The Plan receives a stable SHA-256 digest; confirmations bind to it and have their own manifest digest.
- Confirmations may select only Plan-proposed preset, scope, and test candidate. All blocked decisions remain `BLOCKED`.
- The external bundle contains `task.yaml.draft`, `project_state.yaml.draft`, `ADOPTION_CONFIRMATION_SUMMARY.md`, and `EXPORT_MANIFEST.json`. It is explicitly untrusted, not installed, not activated, and requires final review.

## Zero-write and canary evidence

- Unit canaries exported drafts for Python, Node, generic, and non-Git synthetic targets, including paths with spaces, and checked for no `.agent_state` creation.
- Tests reject digest mismatches, blocked-decision changes, target-internal outputs, and symlinked paths that resolve inside the target.
- Export neither invokes candidate tests nor invokes network, package-manager, shell, or runtime commands.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest` — 94 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py` — passed (24 schemas).
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py` — passed.
- `git diff --check` — passed.

## Remaining risk and next step

- Draft export intentionally does not install or apply anything. A real-project write remains out of scope and requires the separate 04D-A audit plus explicit 04E authorization.
- The pre-existing untracked 04C GitHub audit report remains separate from this 04D work.
