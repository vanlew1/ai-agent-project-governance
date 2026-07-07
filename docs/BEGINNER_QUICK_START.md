# Beginner Quick Start

## Fastest Way On Windows

1. Download this repository.
2. Double-click `START_HERE.bat`.
3. Enter your new project name.
4. Enter the basic project information when prompted.
5. Open the generated project folder.

## What The Setup Script Does

The setup script:

- copies this template into a new project folder
- renames all `*.template.*` files automatically
- fills common placeholders with your project information
- creates a `.agents/AGENTS.md` workspace router
- can optionally initialize a new local Git repository
- creates draft files for clarifying the project before development starts

## First AI Conversation After Setup

Start in `DISCOVERY` mode if you are still deciding what to build.

Ask the AI assistant to first update the draft brief, open questions, and bootstrap decision. Do not ask it to finalize architecture or start coding until the implementation plan is clear enough to confirm.

If your project touches an external website, API, platform account, browser automation, cloud service, production system, data import, or data export, also decide how access is allowed before coding starts. Naming a platform is not enough; you still need to confirm the access method, data storage, frequency, fallback, and forbidden behaviors.

Before entering `EXECUTION`, make sure `docs/IMPLEMENTATION_PLAN.md` has every execution confirmation field filled in.

## What You Still Need To Review

After setup, review these files carefully:

- `docs/PROJECT_BRIEF_DRAFT.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/BOOTSTRAP_DECISION.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `agent_rules/11_project_specific_rules.md`
- `agent_rules/15_plan_adaptation_rules.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

## If Python Is Missing

Install Python 3 first, then run `START_HERE.bat` again.
