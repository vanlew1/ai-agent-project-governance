# Agent Quick Context

## Purpose

This file gives coding agents a low-cost starting point for A-light tasks.

Use it to reduce unnecessary token usage on small changes while keeping enough local context to work safely.

## When To Use It

Use this file first when the task is limited to:

- copy or wording updates
- comments or documentation touch-ups
- small bug fixes
- narrow edits inside existing functions
- local test additions or fixes

## Default Read Path

For A-light tasks, read in this order:

1. `docs/AGENT_QUICK_CONTEXT.md`
2. `README.md`
3. the directly relevant source or test file

Only escalate to the full governance rule tree if the task touches architecture, module boundaries, data safety, external access, Git publication, irreversible operations, or unclear scope.

## Context Saving Rules

1. Use `rg` to locate relevant code before opening files.
2. Read only nearby functions, UI blocks, or tests.
3. Avoid full-file reads when a local slice is enough.
4. Summarize diffs instead of repeating large code blocks.
5. Keep test output to pass/fail summaries plus the failure reason.
6. Keep the final work report to modified files, core change, test result, and risk.

## Project Fill-In

Add concise project-specific notes here:

- project purpose
- common entrypoints
- common validation commands
- areas that usually stay out of scope
- the triggers that require escalation to full governance
