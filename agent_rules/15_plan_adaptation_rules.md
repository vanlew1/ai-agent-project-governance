# 15 Plan Adaptation Rules

## Goal

These rules define how an AI assistant should work when a project plan is not yet confirmed.

The assistant must not turn early conversation into permanent architecture too soon. It should first discover the project shape, then adapt the governance framework, and only then execute confirmed work.

## Project Modes

### DISCOVERY

Use DISCOVERY when the user is still figuring out what to build.

Allowed actions:

- ask clarifying questions
- summarize current understanding
- compare possible approaches
- update `docs/PROJECT_BRIEF_DRAFT.md`
- update `docs/OPEN_QUESTIONS.md`
- update `docs/BOOTSTRAP_DECISION.md`

Forbidden actions:

- do not finalize `docs/ARCHITECTURE.md`
- do not finalize `docs/MODULE_REGISTRY.yaml`
- do not create or close formal tasks in `docs/TASK_REGISTRY.yaml`
- do not update `docs/CHANGELOG.md` as if implementation happened
- do not start code changes unless the user explicitly asks for a bounded prototype or spike

### ADAPTATION

Use ADAPTATION when the project direction is mostly clear, but execution has not been confirmed.

Allowed actions:

- draft `docs/IMPLEMENTATION_PLAN.md`
- propose updates to `docs/ARCHITECTURE.md`
- propose updates to `docs/MODULE_REGISTRY.yaml`
- propose project-specific rules for `agent_rules/11_project_specific_rules.md`
- identify validation commands and rollback points

Required behavior:

- separate confirmed facts from assumptions
- label assistant recommendations as `proposed` until the owner confirms them
- keep unresolved questions in `docs/OPEN_QUESTIONS.md`
- mark plan status as `draft` or `ready_for_confirmation`
- ask for human confirmation before EXECUTION

Forbidden actions:

- do not mark the implementation plan as `confirmed` without owner confirmation
- do not start broad code changes
- do not expand write scope beyond the proposed plan

### EXECUTION

Use EXECUTION only after the owner confirms the implementation plan.

The execution confirmation must be complete before any implementation starts. A valid confirmation includes:

- confirmed by
- confirmation date
- confirmed scope
- remaining accepted risks
- first execution task

If any field is missing, stay in ADAPTATION.

Allowed actions:

- implement confirmed work
- update `docs/TASK_REGISTRY.yaml`
- update `docs/MODULE_REGISTRY.yaml`
- update `docs/CHANGELOG.md` when a milestone closes
- run validation according to risk level

Required behavior:

- follow task classification rules
- keep edits inside confirmed scope
- update traceability files when the task requires it
- stop and return to ADAPTATION if scope changes materially
- record validation as automated tests, repeatable smoke checks, or manual one-off checks

## Mode Selection Rules

Start in DISCOVERY when any of these are true:

- no implementation plan exists
- the user is describing goals conversationally
- module boundaries are unknown
- validation commands are unknown
- high-risk write paths have not been identified

Move to ADAPTATION when:

- the project goal is understandable
- likely scope and non-scope can be stated
- major open questions are listed
- there is enough information to draft a plan

Move to EXECUTION when:

- `docs/IMPLEMENTATION_PLAN.md` is confirmed with all execution confirmation fields filled in
- `docs/BOOTSTRAP_DECISION.md` records EXECUTION mode
- allowed write scope is explicit
- validation expectations are documented
- external access risks are resolved, accepted, or explicitly out of scope

## External Access Gate

Use this gate before EXECUTION when a plan involves any external platform, website, API, login state, scraper, browser automation, webhook, cloud service, production system, data import, or data export.

Do not treat "use platform X" as permission to access it directly. The assistant must first document:

- access method: official API, exported file, manual input, public page request, browser-assisted flow, mock adapter, or other
- allowed frequency and scale
- data retention and storage location
- fallback behavior when access fails
- forbidden behavior such as login bypass, captcha handling, rate-limit evasion, account automation, or destructive writes
- owner approval or accepted risk

If the access method is not confirmed, implementation may only create interfaces, mocks, fixtures, or manual-input fallbacks. It must not implement real external access code.

## Confirmation Language Rules

The assistant must keep these categories separate:

- `confirmed`: explicitly stated or approved by the owner
- `proposed`: recommended by the assistant but not approved yet
- `assumed`: inferred from context and still needs review
- `accepted_risk`: not resolved, but explicitly accepted by the owner

In DISCOVERY, most recommendations should be `proposed` or `assumed`.

In ADAPTATION, a recommendation may become `confirmed` only after owner approval.

In EXECUTION, only `confirmed` items and `accepted_risk` items can drive implementation.

## Protected Formal Files

Until EXECUTION mode is confirmed, treat these files as protected from final updates:

- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

In DISCOVERY, do not update them except to add clearly marked draft placeholders.

In ADAPTATION, proposed updates are allowed, but the assistant must label them as draft or pending confirmation.

## Plan-To-Framework Mapping

When adapting a confirmed or nearly confirmed implementation plan into this framework:

1. Convert user goals into scope and non-scope.
2. Convert stable areas into module registry entries.
3. Convert risky areas into sensitive paths and forbidden operations.
4. Convert delivery steps into task registry entries only after confirmation.
5. Convert recurring project-specific constraints into `11_project_specific_rules.md`.
6. Convert validation expectations into task-level verification plans.

## Required Assistant Summary

At the start of a new project, the assistant should state:

- current mode
- why that mode was chosen
- files it may update
- files it must not finalize yet
- what evidence is needed to move to the next mode
