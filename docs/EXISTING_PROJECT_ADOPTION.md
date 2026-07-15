# Adopt an Existing Project

You do not need to rebuild a business application.

- The runtime does not automatically install dependencies, overwrite files, commit, or push.
- Adapter detection is marker-based advice, not migration or authorization.

## Plan before changing a project

Start with the local, read-only planner. It detects local markers, reuses the configuration audit, proposes a Preset, lists test candidates and prospective governance assets, and embeds untrusted configuration drafts. It does not copy assets, create configuration, activate state, run tests, or modify the target project.

```bash
python3 scripts/agent_adopt.py --project-root /path/to/project --format markdown dry-run
python3 scripts/agent_adopt.py --project-root /path/to/project --format json --output /tmp/adoption-plan.json dry-run
```

`--output` is optional and must point outside the target project. The plan labels recommendations, drafts, required confirmations, and forbidden automatic decisions separately. In particular, a detected Adapter, a Preset recommendation, or a test candidate is not authorization to execute or apply anything.

1. Make a normal local backup or branch.
2. Run `python <runtime-root>/scripts/agent_detect_adapter.py --root . detect`.
3. Copy only governance assets you intend to own: `governance/`, `schemas/`, `config/`, required `scripts/`, `AGENTS.md`, and `agent_rules/`.
4. Create project-specific `task.yaml` and `project_state.yaml` with narrow write scope and known-safe commands.
5. Run Preflight, activate State, then Guard before accepting a test plan.
6. Start with one reversible task; deny production data, credentials, generated output, and deployment paths until reviewed.

`agent_adopt.py` supports `dry-run` only. There is no apply, install, activate, or one-click adoption mode. `scripts/init_new_project.py` is not an in-place adoption shortcut.
