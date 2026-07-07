# Implementation Plan

## Purpose

This file is created during ADAPTATION mode and becomes actionable only after human confirmation.

Do not use this file as an execution contract until the `Execution Confirmation` section is fully filled in.

## Plan Status

- Status: `draft` / `ready_for_confirmation` / `confirmed` / `superseded`
- Owner: <OWNER>
- Last updated:
- Related project brief: `docs/PROJECT_BRIEF_DRAFT.md`
- Related open questions: `docs/OPEN_QUESTIONS.md`

## Problem Statement

Describe the problem this plan will solve.

## Target Outcome

Describe the expected result in user-visible terms.

## Scope

### In Scope

- Item 1:
- Item 2:

### Out Of Scope

- Item 1:
- Item 2:

## Proposed Architecture Adaptation

Explain how the generic governance framework should be adapted for this project.

- Recommended adoption mode: `full` / `partial` / `pilot_only` / `not_recommended`
- Initial governed scope:
- Files or directories that should remain read-only:
- Project-specific rules to add:
- Module registry changes needed:
- Task registry changes needed:

## External Access Plan

Fill this section before EXECUTION if the project touches any external platform, website, API, login state, scraper, browser automation, webhook, cloud service, production system, data import, or data export.

| Item | Decision |
| --- | --- |
| External system or platform | |
| Access method | official API / exported file / manual input / public page request / browser-assisted flow / mock adapter / other |
| Owner-approved scope | |
| Allowed frequency or scale | |
| Data retained locally | yes / no |
| Storage location | |
| Fallback when access fails | |
| Forbidden behaviors | |
| Approval or accepted risk | |

If access method is not confirmed, only interfaces, mocks, fixtures, or manual-input fallbacks may be implemented.

## Work Breakdown

| Step | Goal | Expected Files | Risk | Validation |
| --- | --- | --- | --- | --- |
| 1 | Example step | docs/example.md | low | Review only |

## Module Impact Draft

| Module Or Area | Expected Change | New Boundary Needed | Risk Level |
| --- | --- | --- | --- |
| Example module | Example change | yes / no | low / medium / high |

## Validation Plan

- Automated tests:
- Repeatable smoke checks:
- Manual one-off checks:
- Static checks:
- Rollback check:

## Rollout Plan

- Initial rollout scope:
- Expansion condition:
- Stop condition:

## Execution Confirmation

Fill every field before moving to EXECUTION mode. If any field is blank, stay in ADAPTATION.

| Field | Value |
| --- | --- |
| Confirmed by | |
| Confirmation date | |
| Confirmed scope | |
| Allowed write scope | |
| Forbidden scope | |
| Remaining accepted risks | |
| First execution task | |

## Execution Gate Checklist

- [ ] Plan status is `confirmed`.
- [ ] Owner confirmation is recorded in the table above.
- [ ] Allowed and forbidden write scopes are explicit.
- [ ] External access plan is complete or explicitly not applicable.
- [ ] Blocking questions are answered or accepted as risks.
- [ ] Validation plan separates automated tests, repeatable smoke checks, and manual one-off checks.
- [ ] Rollback path is available.
