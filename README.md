# Agent Governance for Coding Agents

> Scoped, testable, traceable, and cost-aware local governance for Codex, Claude Code, Cursor, and similar coding agents.

[![Python](https://img.shields.io/badge/runtime-Python-blue)](requirements-governance.txt)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)

[English](README.md) | [简体中文](README.zh-CN.md)

## Start safely

In a few minutes, you can limit an agent's change scope, select task-relevant tests, and keep a traceable implementation result.

```bash
python scripts/agent_audit.py --project-root .
python scripts/init_new_project.py --preset lightweight
```

| Before | After |
| --- | --- |
| An agent receives broad instructions and guesses what to validate. | A project has explicit scope, focused tests, and a short closure record. |

Everything runs locally by default. The audit is read-only unless you explicitly pass `--output`; there is no telemetry, no automatic network, production-system, or Git-remote access.

New here? Read [Getting started](docs/GETTING_STARTED.md), [audit details](docs/ADOPTION_AUDIT.md), [preset guide](docs/PRESETS.md), and [synthetic examples](docs/examples/README.md).

This is not a prompt collection: it checks scope, registered tests, verification, closure, and multi-agent ownership.

> The public repository currently has no published release or Actions workflow, so release/CI success badges are intentionally absent. See the [settings checklist](docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md).

## What it prevents

- Changes outside a TaskContract scope.
- Claims of completion without required tests.
- Closure using stale verification after workspace changes.
- Parallel workers writing one file without single-writer protection.

## 5-minute quickstart

```powershell
git clone https://github.com/vanlew1/ai-agent-project-governance.git
cd ai-agent-project-governance
python -m pip install -r requirements-governance.txt
python scripts/run_governance_ci.py
```

## How it works

![Governance runtime architecture](docs/assets/architecture-overview.svg)

| Static instructions | Governance Runtime |
| --- | --- |
| Tells agents not to exceed scope | Guard checks actual scope |
| Asks agents to run tests | TestPlan selects registered commands |
| Relies on completion claims | Verification and Closure decide completion |
| Natural-language handoff | Structured Handoff |
| Manual coordination | DAG and single-writer protection |
| Stale validation may be reused | Workspace changes block Closure |

[Quickstart](docs/QUICKSTART.md) · [Demo](docs/DEMO.md) · [Examples](examples/README.md) · [Existing-project adoption](docs/EXISTING_PROJECT_ADOPTION.md) · [Compatibility](docs/COMPATIBILITY.md)

The runtime does not start agents, create worktrees, call remote APIs, install dependencies, commit, push, deploy, or publish automatically.

## Community

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Support](SUPPORT.md) · [Roadmap](docs/OPEN_SOURCE_ROADMAP.md)

## License

MIT. See [LICENSE](LICENSE).
