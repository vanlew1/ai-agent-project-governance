# Adopt an Existing Project

You do not need to rebuild a business application.

- The runtime does not automatically install dependencies, overwrite files, commit, or push.
- Adapter detection is marker-based advice, not migration or authorization.

1. Make a normal local backup or branch.
2. Run `python <runtime-root>/scripts/agent_detect_adapter.py --root . detect`.
3. Copy only governance assets you intend to own: `governance/`, `schemas/`, `config/`, required `scripts/`, `AGENTS.md`, and `agent_rules/`.
4. Create project-specific `task.yaml` and `project_state.yaml` with narrow write scope and known-safe commands.
5. Run Preflight, activate State, then Guard before accepting a test plan.
6. Start with one reversible task; deny production data, credentials, generated output, and deployment paths until reviewed.

There is no `adopt` command in v1.0.0. `scripts/init_new_project.py` is not an in-place adoption shortcut.
