# ADR-0001: Deterministic Governance Runtime

- Status: Accepted
- Date: 2026-07-12

## Context

The framework currently expresses governance mostly through Markdown, YAML, and Agent compliance. That is useful, but it leaves repeated classification, scope, approval, and validation judgments to each task.

## Decision

The framework will add a deterministic local governance runtime while retaining the existing text rule layer. Framework-owned design files use the `GOVERNANCE_RUNTIME_*` name so they remain separate from the downstream `*.template.*` architecture files. JSON Schema is the unique structural source of truth for runtime data. P0 establishes architecture, contracts, validation, and tests only; it does not enable runtime behavior.

## Consequences

The positive effects are less repeated reading and judgment, reproducible validation, and fewer mistaken human blocks for ordinary engineering failures. The trade-off is a small Python validation surface and an ongoing maintenance cost.

## Alternatives Rejected

- Continue adding only Markdown: it cannot deterministically validate structured contracts.
- Implement the complete runtime at once: it combines high-risk behavior with unresolved boundaries and prevents phased validation.
- Put framework runtime architecture in `ARCHITECTURE.template.md`: it would mix framework truth with downstream project templates.

## Follow-up

Only after P0 acceptance may `GOV-RUNTIME-P1` begin the minimal runtime loop.
