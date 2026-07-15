# Quickstart

This path was run locally against this repository.

```powershell
git clone https://github.com/vanlew1/coding-agent-governance.git
cd coding-agent-governance
python -m pip install -r requirements-governance.txt
python scripts/run_governance_ci.py
```

Expected final line: `Governance release gate: PASS (8/8 gates)`.

Detect a project without changing it:

```powershell
python scripts/agent_detect_adapter.py --root . detect
```

Use the existing lifecycle with your own TaskRequest and ProjectState:

```powershell
python scripts/agent_preflight.py --task-file task.yaml --project-state-file project_state.yaml --output-file contract.yaml
python scripts/agent_state.py init --project-state-file project_state.yaml
python scripts/agent_state.py activate --contract-file contract.yaml
python scripts/agent_guard.py check
python scripts/agent_test_plan.py create
python scripts/agent_test_run.py
python scripts/agent_verify.py
python scripts/agent_close.py
```

`agent_test_plan.py` accepts `create` or `show`; later commands use active `.agent_state/` files. `BLOCKED` is a safety outcome, not a status to bypass.

For a new project, use `python scripts/init_new_project.py --adapter auto`. It creates a new directory and does not adopt an existing project in place.
