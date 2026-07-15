# Workflow integration: plan to proof

This guide is workflow-agnostic. The label “Superpowers” is used only as a familiar example of an upper workflow; no installation or product integration is required.

## Minimal mapping

| Upper-plan field | Governance artifact | Enforcement |
| --- | --- | --- |
| Bounded objective | `TaskContract.objective` | Creates a reviewable task intent. |
| Files to change | `write_scope.allow` | Scope Guard rejects changes outside it. |
| Protected files | `write_scope.deny` | Guard reports denied changes. |
| Required checks | registered test plan | Verification consumes command evidence. |
| Owner / next agent | Handoff | Single-writer and structured results remain visible. |

```text
plan → TaskContract → Scope Guard → test evidence → Verification → Closure/Handoff
```

## Offline example

The [example directory](../examples/superpowers_compat/README.md) contains a small plan, its TaskContract, and expected output for three cases:

1. an unauthorized file is blocked;
2. a changed workspace makes verification stale; and
3. an allowed change, focused test, Verification, and Closure succeed.

Run the existing proof without installing any external workflow:

```bash
python3 examples/demo/run_visual_proof.py
```

This is a synthetic, local example. It demonstrates mapping semantics, not third-party certification or production adoption.
