# Superpowers and Agent Governance

## Accurate compatibility statement

Superpowers is an upper workflow and methodology layer: it can help an AI coding agent explore a problem, design a change, make a plan, use TDD, and coordinate work. Agent Governance is a lower, deterministic governance/evidence/closure layer.

They are complementary. This repository supplies a design-compatible, offline document mapping only. It does **not** include a Superpowers plugin, Hook, Skill, Marketplace integration, official endorsement, installation requirement, or end-to-end compatibility evidence.

## Division of responsibility

```text
Superpowers or another upper workflow
  → requirements, design, implementation plan, TDD, agent execution
  → bounded TaskContract (scope + protected paths + tests)
Agent Governance
  → Scope Guard → test evidence → Verification → Closure / Handoff
```

The guard treats a TaskContract the same way regardless of its source. A plan from an upper workflow is not authorization by itself.

## Overlap audit

| Capability area | Decision | Reason |
| --- | --- | --- |
| Task scope, protected paths, evidence freshness, Closure, Handoff | KEEP | These are the runtime's distinguishing governance responsibilities. |
| Requirements clarification and brainstorming | DE-EMPHASIZE | Useful upstream activities, but not this project's core product claim. |
| General implementation planning | DE-EMPHASIZE | This project accepts a bounded plan; it does not replace planning methods. |
| TDD methodology | DE-EMPHASIZE | It consumes registered test evidence rather than teaching or enforcing a universal TDD process. |
| Multi-agent single-writer checks and handoff | KEEP | Narrow ownership/conflict evidence remains in scope. |
| General sub-agent orchestration | DEPRECATE-LATER | Preserve the existing deterministic local contracts, but avoid presenting them as a generic orchestrator. |
| Worktree creation and management | REMOVE-NOW from messaging | The runtime does not create worktrees; do not imply that it owns this workflow. |
| Specification and code-review methodology | DE-EMPHASIZE | The runtime can surface evidence and risks, not replace human review methods. |
| Generic Git workflow, branch completion, and publishing | DE-EMPHASIZE | Repository maintenance is separate from runtime Closure. |
| Duplicate guidance across entry documents | MERGE | Route readers through the README, Demo, adoption path, and this guide. |

`REMOVE-NOW from messaging` changes only the public claim: no mature public interface or runtime capability is deleted by this release.

## Safe way to combine them

1. Use Superpowers, `AGENTS.md`, or another workflow to produce the plan.
2. Extract a narrow objective, allow/deny paths, and registered tests into a TaskContract.
3. Run Guard before relying on test evidence.
4. Register and verify test evidence.
5. Close only while evidence and workspace freshness are valid; create a Handoff when ownership changes.

The complete offline artifact set is in [the mapping example](../examples/superpowers_compat/README.md).
