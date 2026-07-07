# Architecture

## Purpose Of This File

This file is not only an architecture summary. It is also the main document an AI assistant should read to decide whether the current project can adopt this governance framework safely and usefully.

The goal is to help an AI assistant answer four questions:

1. What kind of project is this?
2. Where are the stable module boundaries?
3. Which paths, data stores, and workflows are risky?
4. Should this project adopt the framework fully, partially, gradually, or not at all?

## Project Overview

- Project name:
- Project type:
- Primary goal:
- Main users:
- Primary runtime:
- Main languages:
- Deployment style:

## Framework Fit Summary

Use this section first. It gives the AI assistant a quick decision surface.

- Recommended adoption mode: `full` / `partial` / `pilot_only` / `not_recommended`
- Current project mode: `DISCOVERY` / `ADAPTATION` / `EXECUTION`
- Why this recommendation was chosen:
- Safe starting scope for adoption:
- High-risk areas that must stay guarded:
- Required human approvals before broad rollout:

## Project Definition Stage

Before treating this architecture as final, check whether the project is still in DISCOVERY, ADAPTATION, or EXECUTION.

- DISCOVERY: goals and boundaries are still forming. Keep architecture notes draft-only and update `PROJECT_BRIEF_DRAFT.md` plus `OPEN_QUESTIONS.md`.
- ADAPTATION: the direction is mostly clear. Convert the emerging plan into this architecture file, the module registry, project-specific rules, and validation expectations, but keep changes pending confirmation.
- EXECUTION: the owner has confirmed the implementation plan. This architecture can be used as an execution reference.

Do not use this file as an execution authority until `BOOTSTRAP_DECISION.md` and `IMPLEMENTATION_PLAN.md` show that EXECUTION is confirmed.

## Project Shape Checklist

Mark each item as `yes`, `partial`, or `no`.

- Clear repository root and project boundary:
- Stable module or folder ownership:
- Read/write boundaries can be described:
- Testing entry points exist:
- Git-based rollback is available:
- High-risk data or production paths are identifiable:
- The team wants structured AI collaboration:

### Interpretation Guide

- Mostly `yes`: this project is usually a good candidate for full adoption.
- Mixed `yes` and `partial`: adopt the framework gradually, starting with scoped tasks and read-only governance.
- Multiple `no`: use only a light subset first, or avoid adoption until the project becomes more structured.

## Layered Architecture View

Describe the current project using the layers below. Not every project needs every layer, but the AI assistant should be able to map the real codebase into an equivalent structure.

| Layer | Purpose | Typical Contents | AI Governance Focus |
| --- | --- | --- | --- |
| Entry Layer | Human or system entry points | CLI, app entry, API routes, jobs | Safe invocation, task scope, operator intent |
| Orchestration Layer | Coordinates flows across modules | services, workflows, schedulers | Scope control, cross-module impact |
| Domain Layer | Core business or project logic | rules, models, processors | Ownership, invariants, correctness |
| Data Access Layer | Reads and writes state | repositories, ORM, SQL, filesystem adapters | Write boundaries, rollback, data safety |
| Integration Layer | External services and tools | APIs, queues, webhooks, SDKs | Cost control, retries, dependency risk |
| Presentation Layer | User-facing interaction | UI, reports, dashboards, docs | Output correctness, no hidden side effects |
| Governance Layer | Meta-control over change | AGENTS, rules, registries, audits | Routing, traceability, review discipline |

## Module Inventory

List the real modules in the project, then map each one to a layer.

| Module | Layer | Responsibility | Inputs | Outputs | Owner | Risk Level |
| --- | --- | --- | --- | --- | --- | --- |
| example_module | domain | Example responsibility | Example input | Example output | <OWNER> | medium |

## Dependency Direction Rules

Document the allowed direction of dependencies so an AI assistant can detect structural drift.

- Entry layer may call orchestration and presentation logic.
- Orchestration may call domain, data access, and integration modules.
- Domain logic should not depend directly on UI concerns.
- Data access should not silently change domain rules.
- Governance files may constrain all layers, but should not become a hidden business runtime dependency.

Project-specific dependency rules:

- Add rule 1:
- Add rule 2:
- Add rule 3:

## Writable Boundaries

An AI assistant should never guess write scope. Fill this section with explicit boundaries.

### Allowed Write Areas

- Path or module:
- Path or module:

### Sensitive Or High-Risk Areas

- Production data:
- Secrets or local environment files:
- External systems requiring approval:
- Critical workflows requiring extra review:

### Read-Only Or Audit-Only Areas

- Path or module:
- Path or module:

## Data And State Classification

Classify the state handled by this project.

| State Type | Location | Read/Write | Risk | Notes |
| --- | --- | --- | --- | --- |
| Source code | repository | read/write | medium | |
| Local config | | | | |
| Database | | | | |
| External API state | | | | |
| Generated artifacts | | | | |

## Execution Modes

Describe how work is normally run.

- Normal development flow:
- Test flow:
- Release flow:
- Maintenance flow:
- Audit or review flow:

## AI Assistant Decision Rules

Use this section to help the AI assistant decide whether the framework can be integrated into the current project.

### Full Adoption Is Usually Suitable When

- the project has clear module boundaries
- task scope can be limited to known paths
- rollback is practical through Git or equivalent versioning
- tests or validation commands exist
- risky write paths can be isolated

### Partial Adoption Is Usually Better When

- the project is mid-refactor
- some modules are stable but others are unclear
- there are legacy areas with poor ownership
- AI should only work in selected folders or workflows first

### Pilot-Only Adoption Is Usually Better When

- the team is still testing AI-assisted workflows
- only documentation, scripts, or low-risk utilities should be governed first
- the project has not yet defined stable module ownership

### Adoption Is Not Recommended Yet When

- the repository boundary is unclear
- code and production state are mixed together
- the team cannot identify safe write areas
- no rollback path exists
- autonomous edits would create hidden operational risk

## Recommended Adoption Plan

If the project is a candidate, define a rollout sequence.

1. Start with the safest layer or module.
2. Limit AI write scope explicitly.
3. Turn on task routing and task classification.
4. Add module registry and risk boundaries.
5. Expand to broader workflows only after validation succeeds.

## Validation Commands

List the minimum commands an AI assistant should use to validate work in this project.

- Lint:
- Unit tests:
- Smoke tests:
- Build:
- Type check:
- Local run command:

## Known Architectural Risks

Document the failure modes an AI assistant must watch for.

- Cross-module edits that bypass ownership
- Hidden writes in helper scripts
- Long-running flows with side effects
- Incomplete rollback coverage
- Ambiguous config paths

Project-specific risks:

- Risk 1:
- Risk 2:
- Risk 3:

## Final Fit Decision

Summarize the final recommendation in a form an AI assistant can reuse.

- Final decision: `full` / `partial` / `pilot_only` / `not_recommended`
- Initial adoption scope:
- Forbidden areas during adoption:
- Required validation before merge:
- Required human checkpoints:
