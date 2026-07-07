# Agent Governance Template

A reusable governance template for AI-assisted software development with coding agents such as Codex, Antigravity-style auditors, and other autonomous development agents.

This repository is a template layer, not a business project. It contains reusable governance rules, task routing, architecture placeholders, testing guidance, and traceability scaffolding for projects that use AI coding agents.

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
- rule routing so agents only read the rules they need
- `AGENTS.md` as the main entry point
- `agent_rules/RULES_INDEX.yaml` for machine-readable rule loading
- task cards for different work levels
- architecture and module registry templates
- project-specific governance placeholders
- code quality gates
- testing and validation rules
- version, task, and change tracking guidance
- Git local backup rules
- cost-aware testing rules
- read-only audit workflow support

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

## How To Use It

1. Copy `AGENTS.md`, `agent_rules/`, `docs/`, and `scripts/` into the root of a new project.
2. Run `python scripts/init_new_project.py`, or manually rename all `*.template.*` files to their final names.
3. Fill in the project-specific files and placeholders.
4. Keep task records, change records, and version history inside the new project repository.

## Files You Must Fill In For A New Project

- `agent_rules/11_project_specific_rules.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

## Core File Roles

- `AGENTS.md`: the main entry point for agent behavior and governance rules
- `agent_rules/RULES_INDEX.yaml`: the machine-readable routing and rule index
- `agent_rules/task_cards/`: execution checklists for different task levels

## How To Use TASK / CHG / CHANGELOG

- `TASK`: records task goals, scope, ownership, status, and validation plans
- `CHG`: records implementation changes, affected modules, risks, and rollback notes
- `CHANGELOG`: records externally visible milestone or version changes

A practical workflow is: define `TASK`, implement and document `CHG`, then update `CHANGELOG` when the work is closed.

## Git Local Backup Rules

- Use local commits as the default way to preserve rollback points.
- Stage only files related to the current task.
- Recheck ignored files, sensitive content, and publication scope before pushing to a remote repository.

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
