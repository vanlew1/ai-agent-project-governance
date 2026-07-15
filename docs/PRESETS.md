# Initialization presets

All presets preserve the complete template and future upgrade path. They only set the initial focus in `config/governance_preset.yaml`; no preset guarantees safety.

| Preset | Choose it for | First focus | Upgrade when |
| --- | --- | --- | --- |
| `lightweight` | Personal repositories and narrow changes | Agent entry, scope, one test command, Git/credential/external boundaries, short report | The repository becomes multi-module or long-lived |
| `standard` | Long-lived or multi-module work | Task classification, module boundaries, test plan, change and closure records | Production, external systems, multiple agents, or high-risk work enter scope |
| `strict` | Production data, external systems, multiple agents, high-risk work | Approval, task state, guards, full verification, handoff, audit evidence | Keep it while those risks apply |

```bash
python scripts/init_new_project.py --preset lightweight
python scripts/init_new_project.py --preset standard
python scripts/init_new_project.py --preset strict
```

Running `python scripts/init_new_project.py` without arguments remains supported and uses `standard`, the current full-template baseline. The initializer refuses to overwrite an existing target folder.
