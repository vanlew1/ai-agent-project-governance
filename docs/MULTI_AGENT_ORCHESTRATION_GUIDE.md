# Multi-Agent Orchestration Guide

Use `agent_orchestrate.py` only to calculate/validate plans and ready queues. Workers must return schema-valid results and handoffs. This layer never executes commands, starts an agent, creates a worktree, or performs Git writes.


V1 status: local orchestration acceptance is complete. Distribution remains manual and all Git/worktree operations remain outside the runtime.
