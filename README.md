# Agent Governance Template

A reusable governance template for AI-assisted software development with coding agents such as Codex, Antigravity-style auditors, and other autonomous development agents.

AI 辅助软件开发治理模板，适用于 Codex、Antigravity 风格审计代理和其他自动化开发代理。

This repository is a template layer, not a business project. It contains reusable governance rules, task routing, architecture placeholders, testing guidance, traceability scaffolding, and a beginner-friendly project bootstrap flow.

It also includes a staged project bootstrap model so an AI assistant can work safely before the implementation plan is fully known:

- `DISCOVERY`: clarify the project and keep notes as drafts
- `ADAPTATION`: turn the emerging plan into project-specific rules, scope, module boundaries, and validation expectations
- `EXECUTION`: implement only after the owner confirms the plan

For external platforms, APIs, websites, login state, browser automation, production systems, or data import/export, the assistant must also confirm the access method and risk boundaries before writing real access code.

## Start Here

If you are a beginner and want to use this template directly:

1. Download or clone this repository.
2. On Windows, double-click `START_HERE.bat`.
3. Fill in the prompts for your new project.
4. Open the generated project folder and continue from there.

If you prefer the command line, run:

`python scripts/init_new_project.py`

## What This Template Is For

This template provides a reusable governance layer for AI-assisted development. It helps solo developers and teams keep AI-assisted projects structured, traceable, testable, and safe as they grow.

AI coding agents are powerful, but without project-level guardrails they can easily:

- scan too much context
- modify files outside the intended scope
- create messy architecture
- skip tests
- overwrite important data
- lose track of why changes were made
- run expensive full-scale tests when smaller validation would be enough

## What It Includes

- task classification for light, standard, and major work
- a lightweight quick-context entry for small tasks
- rule routing so agents only read the rules they need
- `AGENTS.md` as the main entry point
- `agent_rules/RULES_INDEX.yaml` for machine-readable rule loading
- task cards for different work levels
- architecture and module registry templates
- a framework fit guide for AI assistants to assess adoption suitability
- discovery, open-question, bootstrap decision, and implementation-plan templates
- project-specific governance placeholders
- code quality gates
- testing and validation rules
- version, task, and change tracking guidance
- Git local backup rules
- cost-aware testing rules
- read-only audit workflow support
- a beginner-friendly initialization script and Windows launcher

## Who This Is For

This template is useful if you work with:

- AI coding agents
- Codex-like development agents
- multi-agent software workflows
- AI-assisted refactoring
- long-running personal software projects
- complex automation projects
- projects that need traceability, testing discipline, and rollback safety

## Core Idea

The goal is not to make every task heavy.

The goal is to make agents read the right rules at the right time.

Small tasks stay small.  
Major tasks get stronger safeguards.  
High-risk changes require stricter review, testing, and traceability.

## Lightweight Task Flow

Small tasks should not pay the full governance cost up front.

Use the lightweight entry when the work is limited to copy tweaks, small bug fixes, local tests, or narrow edits inside existing functions. In that mode, the agent should start from `docs/AGENT_QUICK_CONTEXT.md`, `README.md`, and directly relevant code or tests, then escalate to the full rule tree only if the task touches architecture, data safety, Git publication, external access, or broader project boundaries.

## How To Use It

1. Download or copy this template.
2. Run `START_HERE.bat` or `python scripts/init_new_project.py`.
3. The setup flow creates a new project folder and renames all template files automatically.
4. The setup flow fills basic placeholders for your new project.
5. Complete the remaining project-specific details in the generated files.

## Files You Must Review In A New Project

- `docs/AGENT_QUICK_CONTEXT.md`
- `agent_rules/11_project_specific_rules.md`
- `agent_rules/15_plan_adaptation_rules.md`
- `docs/PROJECT_BRIEF_DRAFT.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/BOOTSTRAP_DECISION.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

## Core File Roles

- `AGENTS.md`: the main entry point for agent behavior and governance rules
- `agent_rules/RULES_INDEX.yaml`: the machine-readable routing and rule index
- `agent_rules/task_cards/`: execution checklists for different task levels
- `agent_rules/15_plan_adaptation_rules.md`: rules for DISCOVERY, ADAPTATION, and EXECUTION modes
- `scripts/init_new_project.py`: the project bootstrap script
- `START_HERE.bat`: the Windows beginner launcher
- `docs/FRAMEWORK_FIT_GUIDE.md`: a guide for AI assistants to decide whether an existing project can safely adopt this framework

## Project Bootstrap Modes

New projects should not jump straight into formal architecture or code changes when the plan is still fuzzy.

Use `DISCOVERY` when the project is still conversational. The assistant may update draft brief and open-question files, but must not finalize architecture, module registry, task registry, or changelog entries.

Use `ADAPTATION` when the direction is clear enough to draft a project-specific implementation plan. The assistant may propose architecture, module, rule, and validation changes, but must wait for owner confirmation before execution.

Use `EXECUTION` only after the implementation plan is confirmed. At that point, normal task classification, module boundaries, validation, and traceability rules apply.

Execution confirmation is not just a casual "go ahead". The implementation plan must record who confirmed it, the date, the confirmed scope, allowed write scope, forbidden scope, accepted risks, and the first execution task.

If a task involves an external platform, API, website, scraper, browser automation, webhook, cloud service, production system, data import, or data export, first complete an external access plan. Until the access method is confirmed, agents may only build interfaces, mocks, fixtures, or manual-input fallbacks.

## How To Use TASK / CHG / CHANGELOG

- `TASK`: records task goals, scope, ownership, status, and validation plans
- `CHG`: records implementation changes, affected modules, risks, and rollback notes
- `CHANGELOG`: records externally visible milestone or version changes

A practical workflow is: define `TASK`, implement and document `CHG`, then update `CHANGELOG` when the work is closed.

Validation evidence should distinguish automated tests, repeatable smoke checks, and manual one-off checks. Do not present a one-time manual check as if it were repeatable automated validation.

## Git Local Backup Rules

- Use local commits as the default way to preserve rollback points.
- Stage only files related to the current task.
- Recheck ignored files, sensitive content, and publication scope before pushing to a remote repository.
- Keep generated outputs, raw data, private samples, local exports, and model outputs out of Git unless they are intentionally sanitized fixtures.

## Cost-Aware Testing Rules

- Prefer smoke tests, representative samples, partial regression, and dry-runs for expensive workflows.
- Escalate to heavier validation only when the risk level requires it.
- Do not present low-cost sampling as if it were full verification.

## Scope Boundary

This repository does not include:

- business-specific rules
- business code
- production data
- database snapshots
- private credentials
- project-local environment configuration

## Notes

This repository is intended to stay generic. It is a reusable governance template and should not contain project-specific business logic, project data, or private operational configuration.

## Governance Runtime Roadmap

This repository has started building a deterministic governance runtime. P0 establishes only the target architecture and Schema baseline; existing tasks remain governed by `AGENTS.md` and the current rule tree. Preflight, state reuse, scope guards, and automatic closure are not enabled. See [the formal runtime architecture](docs/GOVERNANCE_RUNTIME_ARCHITECTURE.md).

P1 adds a deterministic read-only Preflight CLI: `python scripts/agent_preflight.py --task-file task.yaml --project-state-file state.yaml`. It generates a contract only; state persistence, scope enforcement, test execution, and automatic closure remain disabled.

P2 flow: preflight ? state init ? activate ? approve (only for risk) ? guard check. Guards do not run tests or repair files; approvals are not a secret store; `.agent_state/` is ignored. A dirty worktree may correctly return WARN.
