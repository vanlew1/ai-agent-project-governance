# Open Questions

## Purpose

This file tracks unresolved questions while the project is still in DISCOVERY or ADAPTATION mode.

Questions in this file should prevent premature architecture decisions. If a question materially affects modules, data, safety, or delivery scope, do not finalize execution files until it is resolved or explicitly accepted as a risk.

## Question Status Values

- `open`: unanswered
- `answered`: resolved and ready to apply
- `deferred`: intentionally postponed
- `accepted_risk`: unresolved, but the owner accepts the risk

## Questions

| ID | Question | Why It Matters | Blocks Execution | Owner | Status | Answer Or Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | What is the primary user workflow? | Defines module and UI/API scope. | yes | <OWNER> | open | |

## External Access Questions

Use this section whenever the project may touch an external platform, website, API, login state, scraper, browser automation, webhook, cloud service, production system, data import, or data export.

| ID | Question | Why It Matters | Blocks Execution | Owner | Status | Answer Or Decision |
| --- | --- | --- | --- | --- | --- | --- |
| EXT-001 | Which external system or platform is in scope? | Prevents vague platform adoption from becoming accidental broad access. | yes | <OWNER> | open | |
| EXT-002 | What access method is allowed? | Distinguishes API, export, manual input, public page request, mock adapter, and other strategies. | yes | <OWNER> | open | |
| EXT-003 | What scale or frequency is allowed? | Controls cost, rate-limit, stability, and policy risk. | yes | <OWNER> | open | |
| EXT-004 | What data may be stored, and where? | Prevents sensitive raw data or generated outputs from leaking into the repository. | yes | <OWNER> | open | |
| EXT-005 | What behaviors are forbidden? | Blocks login bypass, captcha handling, rate-limit evasion, destructive writes, and account automation. | yes | <OWNER> | open | |

## Blocking Questions

List questions that must be answered before EXECUTION mode.

- Q-001:

## Deferred Questions

List questions that can safely wait until a later task.

- Question:

## Accepted Risks

List unresolved questions the owner explicitly accepts.

- Question:
- Accepted by:
- Date:
- Risk note:

## Question Handling Rules

- `answered` means the owner or source of truth gave a usable answer.
- `deferred` means the question does not affect current execution.
- `accepted_risk` means execution may proceed despite uncertainty because the owner explicitly accepted the risk.
- Assistant recommendations are `proposed` until the owner confirms them.
- A question that affects external access, data writes, module boundaries, validation, rollback, or user-facing behavior should usually block EXECUTION.
