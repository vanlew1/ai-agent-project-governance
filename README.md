# Agent Governance for Coding Agents

> A local, deterministic governance runtime that helps coding agents stay in scope, run the right checks, and leave verifiable closure evidence.

[![Python](https://img.shields.io/badge/runtime-Python-blue)](requirements-governance.txt)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)

[English](README.md) | [简体中文](README.zh-CN.md)

## Why this exists

When agents change a repository, the difficult part is often not generating code. It is keeping the change inside its intended scope, selecting meaningful tests, avoiding unsupported completion claims, coordinating concurrent work, and retaining evidence for handoff.

This repository provides a local governance runtime for that work:

- explicit task scope and protected paths;
- task-relevant test planning and verification evidence;
- closure that detects stale validation; and
- structured handoff with single-writer protection for multi-agent work.

### More than an `AGENTS.md` or prompt

An `AGENTS.md` file or prompt can guide an agent. This project adds executable checks around that guidance: contracts, scope guards, test planning, verification, and closure records. It reduces common failure modes; it does not claim to prevent every agent error or provide an official third-party product integration.

## Verify it locally

Run the existing local gate after cloning the repository:

```powershell
git clone https://github.com/vanlew1/ai-agent-project-governance.git
cd ai-agent-project-governance
python -m pip install -r requirements-governance.txt
python scripts/run_governance_ci.py
```

The final command runs the repository's existing governance checks and reports the result in the terminal.

## Status and boundaries at a glance

| Area | Current, cautious statement |
| --- | --- |
| Version | `1.0.0` |
| Automation | The repository includes the `Governance CI` GitHub Actions workflow. |
| Release | A `v1.0.0` Release exists; its test artifacts are historical and do not state the live status of current `main`. |
| Runtime coverage | Python, Node.js, WeChat Mini Program, and the generic fallback have local adapter acceptance evidence. See [compatibility](docs/COMPATIBILITY.md). |
| Agent compatibility | Codex is instruction-compatible only. Claude Code, Cursor, and GitHub Copilot have no recorded end-to-end validation. |

By default, the runtime does not automatically access production systems, write production data, call remote APIs, start third-party agents, install dependencies, create worktrees, commit, push, deploy, or publish. The local audit is read-only unless you explicitly pass `--output`.

## What it helps prevent

- Changes outside a TaskContract scope.
- Tests that are unrelated to the change, or skipped required checks.
- Claims of completion without verification evidence.
- Closure that reuses validation after the workspace has changed.
- Multiple agents writing the same file without single-writer protection.

## How it works

![Governance runtime architecture](docs/assets/architecture-overview.svg)

| Static guidance alone | This governance runtime adds |
| --- | --- |
| Tells an agent what not to change | Guard checks the actual change scope |
| Asks an agent to run tests | TestPlan selects registered commands |
| Relies on a completion claim | Verification and Closure decide completion |
| Leaves handoff in prose | Structured Handoff records ownership and results |
| Coordinates manually | DAG and single-writer protection expose conflicts |

## Continue by intent

| If you want to… | Start here |
| --- | --- |
| Run a short local introduction | [Getting started](docs/GETTING_STARTED.md) and [Quickstart](docs/QUICKSTART.md) |
| Choose a setup level | [Preset guide](docs/PRESETS.md) |
| Adopt the runtime in an existing repository | [Existing-project adoption](docs/EXISTING_PROJECT_ADOPTION.md) — use `agent_adopt.py --help` for the complete local-only dry-run/export/compile/install/recovery command surface |
| Activate an adopted Runtime | Use `scripts/agent_state.py activate-approved`; activation is separately approved and does not run Preflight, tests, verification, or closure |
| Review compatibility evidence | [Compatibility](docs/COMPATIBILITY.md) |
| Understand the audit and safety model | [Audit details](docs/ADOPTION_AUDIT.md) |
| Explore a concrete path | [Demo](docs/DEMO.md) — see an out-of-scope block, stale-verification block, and successful closure — plus [examples](examples/README.md) |
| Contribute or get help | [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), and [Support](SUPPORT.md) |

For repository-maintenance checks, see the [GitHub settings checklist](docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md). The runtime itself does not modify those remote settings.

## License

MIT. See [LICENSE](LICENSE).
