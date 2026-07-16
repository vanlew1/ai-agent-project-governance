# Launch copy (review before posting)

## X / English

AI coding workflows can plan a change. This local-first runtime checks the next question: did the agent stay in scope, use fresh evidence, and earn Closure?

Coding Agent Governance includes an offline demo for denied diffs, stale verification, and successful closure. It complements upper workflows such as Superpowers; it is not an official integration. https://github.com/vanlew1/ai-agent-project-governance

## X / 中文

上层 AI 编码工作流可以帮助 Agent 规划和施工；这个本地优先运行时独立检查下一步：实际改动是否越界、证据是否仍有效、任务是否可以收口。

Coding Agent Governance 提供离线 Demo：越界 diff 阻断、旧验证失效、成功 Closure。它可与 Superpowers 等工作流配合，但不是官方集成。https://github.com/vanlew1/ai-agent-project-governance

## Reddit draft

**Title:** Show: local scope, evidence, and closure checks for AI coding-agent tasks

I built a local-first governance runtime for the gap after an AI coding workflow makes a plan: checking the actual diff against a TaskContract, recording relevant test evidence, and refusing Closure when verification is stale. The repository includes a reproducible offline demo with three synthetic outcomes. It is designed to complement planning workflows (including a documented Superpowers mapping), not replace them or claim official integration.

## Hacker News draft

**Title:** Show HN: Deterministic scope, evidence, and closure for coding agents

This is a local-first runtime that turns a bounded coding task into a TaskContract, checks the actual change scope, records test evidence, and blocks Closure when the workspace has changed since verification. The demo is offline and synthetic: one denied diff, one stale verification, and one successful Closure. It can sit beneath any planning workflow; the Superpowers relationship is a documented mapping, not an official integration.

## Awesome-list submission summary

Agent Governance for Coding Agents is a local-first, deterministic governance layer for AI coding-agent workflows. It provides TaskContract scope checks, protected paths, test evidence, stale-verification detection, Closure, and structured handoff. It complements planning tools instead of replacing them; its demo is offline and reproducible.
