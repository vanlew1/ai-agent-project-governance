<!-- encoding: UTF-8 -->
# CASE-001 `generate_preview.py` Audit

## Classification

```text
AD_HOC_REGENERATION_SCRIPT_NOT_ACCEPTABLE
```

## Required questions

| Question | Answer | Evidence |
|---|---|---|
| Calls official `agent_adopt.py` CLI? | No | No subprocess/CLI invocation exists. |
| Directly imports internal functions? | Yes | Imports `build_plan`, `export_drafts`, `compile_runtime_bundle`, and private `_digest`. |
| Manually constructs plan? | Yes | Calls `build_plan(target)` without scope input, then edits task/scope fields. |
| Manually constructs confirmation? | Yes | Builds the full confirmation mapping in Python. |
| Manually constructs approval? | No final install approval | It nevertheless asserts `confirmed_by_user: true` without Owner input. |
| Manually recalculates digest? | Yes | Recomputes `plan_digest`, changes receipt payload, and recomputes receipt digest. |
| Writes fields without a formal scope artifact? | Yes | No `adoption_scope_input` is created or passed. |
| Bypasses Owner approval? | Yes | Writes confirmed preset/scope/test/autonomy and `confirmed_by_user: true`. |
| Bypasses provenance boundary? | Yes | Receipt is rewritten to legitimize the manual plan mutation. |
| Test/development-only marker? | No | No module docstring, CLI guard, environment gate, or development-only marker exists. |
| Could be mistaken for formal entry? | Yes | Top-level executable script with fixed real project paths and “Preview generated” success output. |

## Scope mutation

The script inserts:

```text
src/**
tests/**
data/**
```

This is neither the formal Phase 1 scope nor an approved owner confirmation. It directly conflicts with the Phase 1 denial of `data/**` and protection of existing business modules.

## Provenance misstatement

The embedded receipt claims the static contract digest for `agent_adopt.py dry-run`, but the script did not run that CLI. It called `build_plan` directly, modified the returned object, and then repaired the hashes. The planner source digest is real, but the execution-path claim is not.

## File-system behavior

- Uses fixed Windows paths for the live Replay target and external Preview.
- Creates the Preview directory if absent, but does not require it to be empty.
- Writes/overwrites plan and confirmation with ordinary `write_text`.
- Exporter/compiler refuse non-empty child directories, so reruns are not cleanly idempotent.
- No exception cleanup restores partial root files.
- No C0 scan is run for plan, confirmation, or runtime outputs.
- No approval candidate, canonical write-set, pre-install hashes, or rollback manifest is generated.

## Acceptance consequence

The current Preview must not be approved or installed. A replacement generator must only orchestrate public CLI commands in order, must accept an owner-supplied formal scope file, must not create confirmations/approvals, must not edit artifacts, and must not recompute digests.
