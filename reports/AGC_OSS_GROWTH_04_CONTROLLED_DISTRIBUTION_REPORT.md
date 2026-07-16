# AGC-OSS-GROWTH-04 — controlled distribution report

**Status:** `PASS`

**Date:** 2026-07-17

**Baseline:** `origin/main` at `3140d3a7d41968a6b3dd162979bbc2b68cb67679` (merged PR #5)
**Worktree:** `/home/liyouran1997/projects/agc-growth-04` on `codex/agc-growth-04`

## Scope and isolation

- An isolated worktree was created from `origin/main`; the original checkout's uncommitted Build Week files were neither moved nor copied.
- Changed paths are limited to public documentation, distribution tracking, historical-status reporting, and the focused public-assets test.
- Runtime, schemas, CLI, state-machine behavior, repository slug, and `origin` remote were not changed.
- No credential, account, private data, production system, or third-party repository was written.

## Naming status and historical clarification

Current public title: **Coding Agent Governance**.

The repository slug, clone URLs, and public links remain **`ai-agent-project-governance`**. The historical report that recorded an invalid GitHub CLI session remains unchanged. A follow-up clarification records that the blocker was subsequently resolved, PR #5 merged, and the display-name-only remote closeout completed.

The plan-referenced `AGC_OSS_NAMING_03_R1_DISPLAY_NAME_ONLY_REMOTE_CLOSEOUT_REPORT.md` was not present at the verified baseline. No replacement history was fabricated; the clarification names the absence and relies on the existing report plus the merged PR baseline.

## Public positioning and prepared assets

The public message is now aligned on:

> A governance layer for AI coding agents that keeps changes scoped, evidence-bound, reviewable, and explicitly closed.

Prepared assets:

- GitHub description: `Deterministic scope, evidence, and closure for AI coding-agent workflows.`
- X English and Chinese copy with the preserved repository URL.
- Reddit and Show HN drafts that disclose the author, state the synthetic-only acceptance boundary, and include `CLOSED != PRODUCTION_READY`.
- Existing Share Kit and Launch Copy retain explicit prohibitions on official-integration, production-proof, adoption, and autonomous-deployment claims.

No post, metadata update, login, CAPTCHA handling, or account automation was performed. Direct-channel entries are therefore `PREPARED_NOT_POSTED`.

## Candidate-directory review

Review date: 2026-07-17. “Active” means current public evidence of ongoing repository activity or maintained open contribution flow; it is not an endorsement. “Duplicate” was checked for the exact repository slug in the public rendered list where available. “Author disclosure” is included in every prepared submission even where it is not a stated target requirement.

| Target | Section | Topic match | Criteria | Active | Self-submission | Risk | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) | Governance controls / coding-agent systems | High | PASS | yes | yes | Low | READY_FOR_TARGETED_SUBMISSION |
| [ai-for-developers/awesome-ai-coding-tools](https://github.com/ai-for-developers/awesome-ai-coding-tools) | Developer Productivity Tools | High | PASS | yes | yes | Low | READY_FOR_TARGETED_SUBMISSION |
| [inmve/awesome-ai-coding-techniques](https://github.com/inmve/awesome-ai-coding-techniques) | Techniques, not a project directory | Medium | FAIL | yes | not established for project listing | Medium | REJECT_TARGET |
| [flatlogic/awesome-ai-software-development-agents](https://github.com/flatlogic/awesome-ai-software-development-agents) | AI software-development agents | Low | FAIL | yes | yes | Medium | REJECT_TARGET |
| [ColinEberhardt/awesome-ai-developer-tools](https://github.com/ColinEberhardt/awesome-ai-developer-tools) | Mature AI developer tools | Medium | FAIL | not sufficiently established | not established | Medium | REJECT_TARGET |
| [jamesmurdza/awesome-ai-devtools](https://github.com/jamesmurdza/awesome-ai-devtools) | Configuration & Context Management | Medium | FAIL | yes | contribution policy not found | Medium | REJECT_TARGET |
| [bureado/awesome-agent-runtime-security](https://github.com/bureado/awesome-agent-runtime-security) | Agent runtime security | Low | FAIL | not sufficiently established | contribution policy not found | High | REJECT_TARGET |
| [jim-schwoebel/awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) | Broad AI-agent tools | Low | FAIL | yes | yes | High | REJECT_TARGET |

### Contribution-rule evidence and decisions

1. **Picrew/awesome-agent-harness — ready.** Its [contribution guide](https://github.com/Picrew/awesome-agent-harness/blob/main/CONTRIBUTING.md) explicitly accepts coding-agent systems with inspectable workflows and guardrails, gateways, and governance controls. It requires active, clearly scoped, documented, non-duplicative projects, but has no hard star threshold. The repository described 56 commits, 24 open PRs, and a 2026-06-21 verification date at review. The exact project slug was not found in the rendered catalog. The correct data-driven section is governance controls; author disclosure is added below.
2. **ai-for-developers/awesome-ai-coding-tools — ready.** Its [contribution guide](https://github.com/ai-for-developers/awesome-ai-coding-tools/blob/main/CONTRIBUTING.md) accepts AI-powered or AI-enhanced tools useful to developers that are publicly accessible, have a free tier, are documented, and have a clear use case. It directs contributors to append an entry to the relevant section. The public repository showed 529 commits and 147 open PRs at review; the exact project slug was absent from its rendered list. The appropriate placement is Developer Productivity Tools. Author disclosure is added below.
3. **inmve/awesome-ai-coding-techniques — reject.** The project is active and has a contribution file, but its stated purpose is community techniques and practitioner experiences rather than a catalog of projects. A self-listing would not have a sufficiently clear section match.
4. **flatlogic/awesome-ai-software-development-agents — reject.** The published contribution instruction asks for an AI software-development *agent*. This repository governs coding-agent workflows rather than acting as an agent, so the topic/section criterion fails.
5. **ColinEberhardt/awesome-ai-developer-tools — reject.** The public positioning emphasizes mature tools. No contribution policy or acceptance path was established in this review, so the gate fails closed.
6. **jamesmurdza/awesome-ai-devtools — reject.** The configuration/context section is adjacent but not a direct governance-controls section; no contribution policy was found in the reviewed public material.
7. **bureado/awesome-agent-runtime-security — reject.** The list focuses on runtime security, identity, gateways, and operational controls. This project does not claim that scope, so submission would be weakly matched.
8. **jim-schwoebel/awesome_ai_agents — reject.** The broad directory welcomes contributions but lacks a focused governance/workflow placement; this would be low-signal self-promotion.

The earlier closed PR `brandonhimpfen/awesome-ai-coding-agents#39` was not reopened, commented on, or resubmitted.

## Target-specific submission drafts

No third-party PR, fork, branch, issue, or comment was created. These drafts become actionable only after the owner authorizes one named target. Even if the owner authorizes every passing target, submit to **at most one** target and stop.

### Picrew/awesome-agent-harness

- **Target:** `Picrew/awesome-agent-harness`
- **Match reason:** Its contribution policy explicitly names coding-agent systems with inspectable workflows and governance controls.
- **Section:** Governance controls (data entry in `data/projects.yaml`).
- **Proposed diff:** Add one YAML entry using the target's required fields; run its documented metadata sync, rendering, and catalog verification commands in the target fork.

```yaml
- name: Coding Agent Governance
  repo_url: https://github.com/vanlew1/ai-agent-project-governance
  category: governance
  summary_en: Deterministic scope, evidence freshness, and explicit closure checks for bounded AI coding-agent tasks.
  summary_zh: 为受限 AI 编码任务提供确定性范围、证据新鲜度与显式收口检查。
  tags: [coding-agent, governance, task-contract, verification]
  stars_snapshot: <refresh-at-submission>
  updated_at: <refresh-at-submission>
  why_included: Inspectable TaskContract scope checks, stale-verification protection, and structured closure for coding-agent workflows.
```

- **PR title:** `Add Coding Agent Governance to governance controls`
- **PR body:**

  ```text
  I am the author of Coding Agent Governance and am submitting it for the governance-controls section.

  It is an open-source governance layer for bounded AI coding-agent tasks: explicit TaskContract scope checks, task-relevant evidence, stale-verification protection, and structured closure. Its public demo is offline and synthetic-only; CLOSED != PRODUCTION_READY.

  Repository: https://github.com/vanlew1/ai-agent-project-governance

  I followed the data-entry and generated-file workflow described in CONTRIBUTING.md. Please reject or adjust the entry if it does not fit the catalog's governance-controls scope.
  ```

### ai-for-developers/awesome-ai-coding-tools

- **Target:** `ai-for-developers/awesome-ai-coding-tools`
- **Match reason:** The policy accepts documented, publicly accessible AI-enhanced developer tools with a clear use case; the repository has a free local/offline path.
- **Section:** Developer Productivity Tools.
- **Proposed diff:** Append this single line to the end of the target section:

  ```markdown
  - **[Coding Agent Governance](https://github.com/vanlew1/ai-agent-project-governance)** – Open-source scope, evidence, stale-verification, and explicit-closure checks for bounded AI coding-agent tasks.
  ```

- **PR title:** `Add Coding Agent Governance to Developer Productivity Tools`
- **PR body:**

  ```text
  I am the author of Coding Agent Governance. It is a documented, publicly accessible open-source governance layer for AI coding-agent workflows, with a local/offline path and a clear developer-workflow use case.

  The project checks TaskContract scope, protected paths, task-relevant evidence, stale verification, and explicit closure. Its demo is synthetic-only and offline; CLOSED != PRODUCTION_READY.

  Repository: https://github.com/vanlew1/ai-agent-project-governance
  ```

## Distribution tracker

`docs/PROJECT_DISTRIBUTION_TRACKER.md` records the baseline status, target, action, safe URL, result, and next review. It deliberately excludes credentials and private-account information. Its terms express workflow state only, not endorsement or adoption.

## Verification record

Run from `/home/liyouran1997/projects/agc-growth-04` against baseline `3140d3a7d41968a6b3dd162979bbc2b68cb67679`:

| Type | Command | Result |
| --- | --- | --- |
| Level 1 automated | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_public_adoption_assets` | PASS — 7 tests |
| Level 1 smoke | `git diff --check` | PASS |
| Level 2 automated | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_governance_ci.py` | PASS — completed successfully |
| Scope review | `git diff --check`, `git status --short`, and changed-path review | PASS — only the planned public documentation, reports, tracker, task registry, and focused test are changed; Build Week paths are absent |

No environment variables, dependencies, live APIs, database writes, production assets, or automated external submissions were used.

## Self-repository PR and next step

The intended self-repository PR is:

- Branch: `codex/agc-growth-04`
- Title: `docs(project): add controlled distribution assets and tracking`
- Body:

  ```text
  - No Runtime, Schema, CLI, or state-machine changes.
  - Repository slug remains ai-agent-project-governance.
  - Historical authentication blockers are preserved and clarified.
  - No third-party promotional PR was created automatically.
  - External submissions require target-specific approval.
  ```

Push, PR creation, merge commit, and merge remain owner-facing remote operations and are not performed in this task. The next safe action is to review the local diff and, if desired, authorize a self-repository PR separately; authorize one named third-party target separately before any external submission.

## Completion state

`AGC-OSS-GROWTH-04 PASS`

`BUILD_WEEK_ISOLATED`

`NAMING_STATUS_CLARIFIED`

`PUBLIC_POSITIONING_ALIGNED`

`DISTRIBUTION_ASSETS_READY`

`CONTROLLED_SUBMISSION_MATRIX_READY`

`DIRECT_CHANNEL_COPY_READY`

`TRACKING_BASELINE_CREATED`

`READY_FOR_TARGETED_SUBMISSION_AUTHORIZATION`

`NO_BULK_PROMOTION`

`NO_WEAK_MATCH_SUBMISSION`

`NO_RUNTIME_CHANGE`
`STOP`
