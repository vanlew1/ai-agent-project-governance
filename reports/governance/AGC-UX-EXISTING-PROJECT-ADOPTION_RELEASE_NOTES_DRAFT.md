# Existing Project Adoption — Release Notes Draft

Status: DRAFT — not approved for release or Git write.

## New capabilities

- Read-only Existing Project Adoption dry-run planning and external draft export.
- Immutable Runtime preview artifacts with exact-byte, compiler, and approval binding.
- Controlled new-files-only installation and separately approved activation.
- Formal Preflight, Guard, confirmed-candidate test planning, exact local test execution, stale-evidence Verification, and fail-closed Closure.

## Safety boundaries

- No automatic rollback, production activation, network access, or Git writes.
- `CLOSED` does not mean production-ready, released, or deployed.
- Acceptance evidence is synthetic-only and must not be treated as real-project authorization.

## Compatibility

- Legacy `activate` fails closed for adoption Runtime state; `activate-approved` is the bounded adoption entry point.
- Schema compatibility is validated locally for the Runtime models, confirmations, receipts, and lifecycle evidence.
- Generic/non-Git targets use the confirmed local smoke candidate. Node validation uses local `npm test` argv and excludes package-resolution commands.

## Closeout status

The CLI command surface was revalidated in 04G-R1: top-level help and every subcommand help expose the same six commands as the dispatcher. This remains a draft and does not grant Git-write, release, production, or real-project authorization.
