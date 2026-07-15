# GitHub Repository Settings Checklist

Manual maintainer actions; this update does not call the GitHub API.

**Description**

```text
Deterministic local governance runtime for AI coding agents: scope guards, controlled tests, verified closure, adapters, CI, and multi-agent handoff.
```

**Topics**

```text
ai-agent
coding-agent
agent-governance
ai-agent-governance
agents-md
agent-instructions
codex
claude-code
cursor
github-copilot
multi-agent
developer-tools
python
github-actions
local-first
```

- [ ] Keep Issues enabled.
- [ ] Enable Discussions if questions will be maintained.
- [ ] Enable Template repository if copying is supported.
- [ ] Upload `docs/assets/social-preview.svg` as the social preview.
- [ ] Add the description and topics.
- [ ] Pin the repository if desired.
- [ ] Disable Wiki unless it has an owner.
- [x] A least-privilege workflow exists: `.github/workflows/governance-ci.yml`, named `Governance CI`.
- [x] The `v1.0.0` Release exists.

Status recorded for this documentation update: the repository contains the `Governance CI` workflow and has a `v1.0.0` Release. This local update did not query GitHub; it does not treat Release test results as the live CI status of the current `main` branch.
