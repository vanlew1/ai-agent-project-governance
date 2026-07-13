# Agent Quick Context

## Purpose

This file gives coding agents a low-cost starting point for A-light tasks.

Use it to reduce unnecessary token usage on small changes while keeping enough local context to work safely.

This file is a lightweight entry, not the source of truth for governance rules. If it conflicts with `AGENTS.md`, `agent_rules/RULES_INDEX.yaml`, or files under `agent_rules/`, follow the full rule tree.

## When To Use It

Use this file first when the task is limited to:

- copy or wording updates
- small README edits
- comments or documentation touch-ups
- local formatting fixes
- very small fixes inside existing functions
- a single local test addition

Use the lightweight path only when all of these stay true:

1. the change scope is small
2. the impact area is clear
3. the result can be validated quickly
4. no production data or sensitive assets are involved
5. no new module or file is introduced
6. no architecture boundary changes
7. no Git publication, external API, LLM API, web fetching, or large-scale testing

## Default Read Path

For A-light tasks, read in this order:

1. `docs/AGENT_QUICK_CONTEXT.md`
2. `README.md`
3. the directly relevant source or test file

Immediately escalate to the full governance rule tree if any of these appears:

- adding a file or module
- changing an architecture boundary
- changing database, cache, production, or formal evidence storage
- changing Git archive, push, or remote behavior
- calling an LLM API, external API, or web scraping/fetching
- full scans, large test runs, or high-cost work
- security, privacy, secrets, tokens, or credentials
- cross-module edits
- unclear task scope

If any escalation trigger appears during execution, stop the lightweight path and report:

Current task hit an escalation trigger and cannot continue as a lightweight task.
Switch to the full governance rule tree and reconfirm task type, allowed scope, forbidden scope, and validation method before continuing.

## Context Saving Rules

1. Use `rg` to locate relevant code before opening files.
2. Read only nearby functions, UI blocks, or tests.
3. Avoid full-file reads when a local slice is enough.
4. Summarize diffs instead of repeating large code blocks.
5. Keep test output to pass/fail summaries plus the failure reason.
6. Keep the final work report to modified files, core change, test result, and risk.

## Minimum Report

Even A-light tasks must report:

- modified files
- core changes
- tests/checks
- untouched high-risk scope
- whether escalation is required

When no escalation is needed, say that the task remains A-light.

## Sync Reminder

When any of the following changes, check whether this file also needs an update:

- `AGENTS.md`
- `agent_rules/RULES_INDEX.yaml`
- `agent_rules/00_rule_router.md`
- `agent_rules/01_task_classification.md`
- `agent_rules/task_cards/A_light_task.md`
- `agent_rules/task_cards/B_standard_task.md`
- `agent_rules/task_cards/C_major_task.md`
- any newly added or retired core governance rule file

## Project Fill-In

Add concise project-specific notes here:

- project purpose
- common entrypoints
- common validation commands
- areas that usually stay out of scope
- the triggers that require escalation to full governance
