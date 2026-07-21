<!-- encoding: UTF-8 -->

# CASE-001 Scope Invariant Report

## Canonical contract

`governance/adoption/scope_contract.py` owns normalization and exact equality for:

- `task_id`
- `task_goal`
- `execution_mode`
- `allowed_paths`
- `denied_paths`
- `known_safe_commands`
- `network_policy`
- `data_write_policy`
- `git_policy`

The same contract is revalidated at plan, selected candidate, confirmation, draft export, runtime compilation, approval candidate, installation input, and installation receipt boundaries. A mismatch fails with `SCOPE_CONTRACT_MISMATCH`.

## Mode rules

- `ACTIVE_DEVELOPMENT` requires a non-empty `allowed_paths` list.
- `OBSERVATION_ONLY` may use an empty list only when `owner_confirmed_empty_scope=true`.
- Invalid empty scopes fail with `EMPTY_ALLOWED_SCOPE_REQUIRES_EXPLICIT_OBSERVATION_MODE`.

## CASE-001 Phase 1 scope

The Owner-reviewable source is `case001_replay_phase1_scope.yaml`. Its allow-list is limited to core-platform implementation/tests and Phase 1 documentation/evidence. It does not contain `src/**`, `tests/**`, `data/**`, or `**`. CLI, workflow, server, dashboard, cache, model, state-machine, market-environment, regulatory, services, data, backup, credential, environment, and deployment paths are denied.

## Evidence

`tests/unit/test_case001_minimum_unblock.py` covers active/observation mode decisions, cross-boundary mismatches, target/framework binding mismatches, public-CLI generation, CRLF input, Chinese/space paths, and fail-closed installation conflicts.
