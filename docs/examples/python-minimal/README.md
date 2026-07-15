# Python minimal synthetic demo

This synthetic fixture begins with a Python project and test directory but without coding-agent instructions or change boundaries.

```bash
python scripts/agent_audit.py --project-root docs/examples/python-minimal
```

Expected recommendation: `standard`.

After creating a project with `--preset standard`, use the generated `AGENTS.md` and `config/governance_preset.yaml` to add explicit scope, tests, and closure expectations. This fixture is deliberately small and is not a real user case.
