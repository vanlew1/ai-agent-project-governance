# Bootstrap Decision

## Purpose

This file records the decision about which project mode the AI assistant should use before development begins.

It prevents the assistant from treating early conversation notes as final architecture.

## Current Mode

- Mode: `DISCOVERY` / `ADAPTATION` / `EXECUTION`
- Decision date:
- Decided by:
- Reason:

## Mode Decision Guide

### Use DISCOVERY When

- the user is still exploring what to build
- the implementation plan is missing or unstable
- major goals, users, data flows, or boundaries are unclear
- the assistant should ask questions, compare options, and draft notes only

### Use ADAPTATION When

- the project direction is mostly clear
- the assistant can turn the draft into a project-specific plan
- module boundaries and rule changes are being proposed
- the owner has not yet confirmed execution

### Use EXECUTION When

- the owner has confirmed the implementation plan
- allowed write scope is explicit
- validation commands are known or intentionally limited
- task records can be created and updated
- external access risks are resolved, accepted, or explicitly out of scope

## Evidence Checklist

- [ ] Project goal is clear enough.
- [ ] Main user workflow is known.
- [ ] In-scope and out-of-scope items are listed.
- [ ] Open blocking questions are resolved or accepted.
- [ ] Safe write scope is explicit.
- [ ] Validation path is known.
- [ ] Human owner confirmed execution.
- [ ] External access plan is complete or explicitly not applicable.
- [ ] Execution confirmation fields are complete.

## Allowed Actions By Mode

| Mode | Allowed | Not Allowed |
| --- | --- | --- |
| DISCOVERY | Ask questions, draft brief, list unknowns, sketch options | Finalize architecture, update module/task registries, claim execution readiness |
| ADAPTATION | Draft implementation plan, propose project-specific rules, identify module changes | Start code changes, mark tasks done, update changelog as if work shipped, implement real external access before access method is confirmed |
| EXECUTION | Implement confirmed tasks, update registries, validate, record changes | Expand scope without re-confirmation |

## Current Allowed Write Scope

- DISCOVERY:
- ADAPTATION:
- EXECUTION:

## Next Step

- Recommended next action:
- Owner input needed:
