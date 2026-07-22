# AGC-OSS-GROWTH-02 — Positioning and public release report

## Status

`COMPLETE` — the verified release was merged, tagged, released, and published through GitHub; repository metadata was read back, and one relevant awesome-list submission PR was opened. X, Reddit, and Hacker News were not posted because the available browser session could not initialize safely.

## Scope and boundary result

- Positioning: **A deterministic scope, evidence, and closure layer for AI coding-agent workflows.**
- Superpowers relation: documented offline workflow mapping only; no official integration, plugin, installation requirement, or end-to-end compatibility claim.
- No production data, deployment, remote API implementation, credential export, destructive Git action, or unrelated worktree change was performed.

## Superpowers overlap audit

| Decision | Areas |
| --- | --- |
| KEEP | Task scope, protected paths, evidence freshness, Closure, Handoff, narrow single-writer checks. |
| DE-EMPHASIZE | Brainstorming, requirements, general planning, TDD methodology, review methodology, and generic Git/release workflow. |
| MERGE | Repeated public guidance now routes through the README, Demo, adoption path, and compatibility guide. |
| DEPRECATE-LATER | Do not market deterministic local multi-agent contracts as a general sub-agent orchestrator. |
| REMOVE-NOW (messaging only) | Worktree management is not claimed; no public runtime interface was deleted. |

## Delivered artifacts

- README first-screen positioning and one-command offline Demo entrypoint (English and Chinese).
- Superpowers compatibility statement, workflow integration guide, TaskContract mapping example, and synthetic case study.
- Existing-project adoption recommendation and coexistence guidance.
- Share kit, bilingual launch copy, GitHub metadata guidance, release notes, and changelog/version update to `1.1.0`.
- Public-document regression coverage and a template-check isolation fix for local `.agents` / `.codex` metadata.

## Evidence

Baseline command (before changes):

```text
python3 -m unittest -q tests.unit.test_demo_visual_proof tests.unit.test_public_adoption_assets tests.unit.test_agent_adopt tests.integration.test_p5_release_gate
```

Result: `24` tests passed.

Post-change targeted validation:

```text
python3 -m unittest -q tests.unit.test_demo_visual_proof tests.unit.test_public_adoption_assets tests.unit.test_agent_adopt tests.integration.test_p5_release_gate
python3 examples/demo/run_visual_proof.py
```

Result: `25` tests passed; the offline Demo generated all three expected scenarios (`BLOCKED`, `BLOCKED`, `CLOSED`).

Release gate:

```text
python3 scripts/run_governance_ci.py
```

Result: `PASS (8/8 gates)`; full suite passed. `git diff --check` passed before commit.

## Git and release state

- Baseline branch / HEAD: `main` / `dc36f58b05d65d5afb9bdcd66245f7806a1f4520`.
- Task branch: `codex/superpowers-positioning-release`.
- Local implementation commit: `b465a45ef3304646ec781660b033f583bae9bb82`.
- Remote state was read successfully; `origin/main` matched the baseline at the time checked.
- Release PR: [#3](https://github.com/vanlew1/ai-agent-project-governance/pull/3), merged after `governance` and `windows-smoke` both passed.
- Merge commit / current released `main`: `74d90e68339daba7011d784a6ee0affa72611d25`.
- Tag: [`v1.1.0`](https://github.com/vanlew1/ai-agent-project-governance/releases/tag/v1.1.0).
- GitHub Release: [v1.1.0](https://github.com/vanlew1/ai-agent-project-governance/releases/tag/v1.1.0).
- Repository description and homepage were updated and read back. GitHub had 11 existing Topics and a 20-topic cap; 9 positioning Topics were added without deleting existing metadata.
- Awesome-list submission: [brandonhimpfen/awesome-ai-coding-agents#39](https://github.com/brandonhimpfen/awesome-ai-coding-agents/pull/39).

## Remaining external steps

- X, Reddit, and Hacker News posts were not attempted because browser control failed before session discovery with a local `sandboxCwd` path error. No alternative automation, login bypass, credential handling, or unreviewed posting was attempted.
- The awesome-list PR is submitted and awaits the external maintainer's decision; it was not represented as accepted.
