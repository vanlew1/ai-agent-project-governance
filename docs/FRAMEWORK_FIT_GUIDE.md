# Framework Fit Guide

## Goal

This document helps an AI assistant determine whether an existing project can be integrated into the Agent Governance Template.

The question is not only whether the project uses AI. The real question is whether the project has enough architectural clarity and operational safety to benefit from structured AI governance.

## What The Assistant Should Analyze

Before recommending adoption, the assistant should inspect these dimensions:

1. Repository boundary
2. Module boundary
3. Write safety
4. Data sensitivity
5. Validation maturity
6. Rollback maturity
7. Collaboration maturity

## Decision Process

### Step 0: Identify The Project Mode

Before judging framework fit, determine whether the project is in:

- `DISCOVERY`: the idea is still being explored
- `ADAPTATION`: the plan is being translated into project-specific governance
- `EXECUTION`: the plan is confirmed and normal task execution can begin

If the project is still in DISCOVERY, do not recommend broad rollout yet. Start by drafting `PROJECT_BRIEF_DRAFT.md`, `OPEN_QUESTIONS.md`, and `BOOTSTRAP_DECISION.md`.

### Step 1: Identify The Unit Of Change

The assistant should first determine what a normal change looks like in this project.

Examples:

- one function in one module
- one pipeline stage
- one API handler plus one service
- one document generation flow
- one automation script plus one config file

If the unit of change is too ambiguous, framework adoption should start small.

### Step 2: Identify Stable Boundaries

The assistant should ask:

- Are modules separated by responsibility?
- Can the project name its orchestration, domain, data, and integration areas?
- Are there paths that should never be edited without approval?

If these answers are unclear, the framework should not be rolled out broadly yet.

### Step 3: Identify Risk Concentration

The assistant should locate:

- production data paths
- destructive scripts
- external integrations
- credentials and environment files
- long-running workflows
- irreversible operations

Projects with high-risk concentration can still adopt the framework, but only if those risks are explicitly documented.

### Step 4: Assess Validation Quality

The assistant should check whether the project has:

- a build command
- at least one test or smoke-test path
- a way to verify output correctness
- a rollback mechanism

Without validation, AI governance becomes procedural only and does not add enough safety.

### Step 5: Recommend One Adoption Mode

Use one of these outcomes:

- `full`: clear structure, safe boundaries, validation exists
- `partial`: structure is usable but not complete
- `pilot_only`: use only in low-risk folders or documentation first
- `not_recommended`: boundaries and rollback are too weak

## Minimum Good Candidate Profile

A project is usually a good candidate when it has all of the following:

- a clearly defined repository root
- named modules or stable folders
- known safe write areas
- identifiable risky areas
- a validation path
- local version control or equivalent rollback

## Weak Candidate Signals

The assistant should be cautious if the project has one or more of these traits:

- code and live state mixed in the same workspace
- no reliable test or smoke-test entry point
- unknown ownership of critical folders
- scripts with hidden side effects
- frequent manual hotfixes without traceability
- no practical rollback path

## How The Assistant Should Report The Result

The assistant should provide a short structured answer:

- Fit level
- Why
- Safe starting scope
- Unsafe areas
- Required human approvals
- Recommended next step

## Recommended Output Format

```text
Framework fit: partial
Why: module boundaries are mostly clear, but production write paths still need explicit documentation.
Safe starting scope: docs/, scripts/, and non-production service modules.
Unsafe areas: deployment scripts, production data paths, secret config.
Required approvals: any write to deployment or external system adapters.
Next step: complete ARCHITECTURE.md and MODULE_REGISTRY.yaml before expanding AI write scope.
```

## Relationship To Other Template Files

- `docs/ARCHITECTURE.md`: primary architecture and fit-assessment source
- `docs/PROJECT_BRIEF_DRAFT.md`: discovery-stage understanding before architecture is final
- `docs/IMPLEMENTATION_PLAN.md`: adaptation-stage plan before execution begins
- `docs/BOOTSTRAP_DECISION.md`: current DISCOVERY / ADAPTATION / EXECUTION decision
- `docs/OPEN_QUESTIONS.md`: unresolved questions that may block execution
- `docs/MODULE_REGISTRY.yaml`: module ownership and boundary source
- `agent_rules/11_project_specific_rules.md`: local red lines and forbidden areas
- `agent_rules/15_plan_adaptation_rules.md`: mode transition and plan-to-framework rules
- `agent_rules/RULES_INDEX.yaml`: routing logic for governance behavior

## Practical Recommendation

For most real projects, do not start with full rollout.

A safer path is:

1. document architecture
2. identify risky write paths
3. classify modules
4. test AI on a narrow low-risk scope
5. expand only after validation and review succeed
