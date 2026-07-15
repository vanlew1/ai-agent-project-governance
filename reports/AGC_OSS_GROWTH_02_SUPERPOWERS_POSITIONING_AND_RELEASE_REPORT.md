# AGC-OSS-GROWTH-02 — Positioning and public release report

## Status

`PARTIAL` — the verified local release candidate is committed; remote PR, merge, tag, GitHub Release, metadata update, and external distribution have not yet been performed.

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
- Push, PR, merge, tag, GitHub Release, repository metadata update, and external distribution: pending at this report checkpoint.

## Remaining external steps

1. Push the task branch and create a PR without bypassing required checks.
2. Verify remote CI; merge only if repository policy permits.
3. Create the `v1.1.0` tag and GitHub Release after merge.
4. Apply reviewed repository metadata, then publish only the prewritten, fact-checked external copy where the authenticated account and platform rules allow it.
