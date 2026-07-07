# AI Agent Project Governance

A reusable project governance template for AI-assisted software development with coding agents such as Codex, Antigravity-style reviewers, and other autonomous development agents.

This template helps solo developers and teams keep AI-assisted projects structured, traceable, testable, and safe as they grow.

## What This Project Does

AI coding agents are powerful, but without project-level rules they can easily:

- scan too much context;
- modify files outside the intended scope;
- create messy architecture;
- skip tests;
- overwrite important data;
- lose track of why changes were made;
- run expensive full-scale tests when a smaller validation would be enough.

This template provides a reusable governance layer for AI-assisted development.

It includes:

- task classification for light, standard, and major work;
- rule routing so agents only read the rules they need;
- architecture and module registry templates;
- project-specific business rule placeholders;
- code quality gates;
- testing and validation rules;
- version, task, and change tracking;
- Git local backup rules;
- cost-aware testing rules;
- read-only audit workflow support.

## Who This Is For

This template is useful if you work with:

- AI coding agents;
- Codex-like development agents;
- multi-agent software workflows;
- AI-assisted refactoring;
- long-running personal software projects;
- complex automation projects;
- projects that need traceability, testing discipline, and rollback safety.

## Core Idea

The goal is not to make every task heavy.

The goal is to make agents read the right rules at the right time.

Small tasks stay small.  
Major tasks get stronger safeguards.  
High-risk changes require stricter review, testing, and traceability.

## Recommended Use

Copy this template into the root of a new project, then fill in the project-specific files:

- `agent_rules/11_project_specific_rules.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

After that, your AI coding agent can use `AGENTS.md` as the main entry point for project rules.
