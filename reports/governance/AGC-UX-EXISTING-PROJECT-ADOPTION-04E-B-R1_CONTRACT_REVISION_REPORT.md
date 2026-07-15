# 04E-B-R1 Contract Revision Report

## Contract

Automatic rollback is removed. `rollback-install` fails closed; `assess-rollback` is a point-in-time, read-only manual cleanup assessment. It does not delete, move, overwrite, or emit shell deletion commands.

## Security changes

- Installation requires original Plan and confirmation, revalidates their canonical digests, current target identity, manifest provenance, and draft hashes.
- Installation receipt paths are resolved and rejected when contained by the target; receipts remain external.
- Receipt semantics are now `MANUAL_ONLY`: automatic rollback is unavailable and assessment is available.
- Rollback assessment has a registered Schema and validates its output before external exclusive creation.

## Verification

- `python3 -m unittest` — 103 passed.
- Governance validation, code quality, Schema compatibility, and `git diff --check` — passed.
- No real project, network, Git write, test execution, build, activation, Verification, Closure, or 04F action was performed.

## Remaining verification scope

The targeted assessment tripwire/synthetic matrix described in the closeout plan has not yet been implemented as dedicated tests. The contract is safer by removing destructive rollback, but 04F readiness requires the accompanying independent re-audit to confirm those scenarios.
