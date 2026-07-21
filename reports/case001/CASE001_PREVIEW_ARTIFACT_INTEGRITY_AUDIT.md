<!-- encoding: UTF-8 -->
# CASE-001 Preview Artifact Integrity Audit

Preview root:

```text
C:/Users/范德彪/Desktop/ai数据/codex-worktrees/adoption-preview-v2
```

## Result

The nine present files form an internally consistent digest chain, but the Preview is not an admissible Phase 0.5 installation candidate. It lacks mandatory artifacts, contains the wrong scope, is not fresh enough to bind the live Git state, and was produced by an ad hoc script.

## Artifact inventory

Present:

```text
adoption-confirmation.yaml
adoption-plan.json
drafts/ADOPTION_CONFIRMATION_SUMMARY.md
drafts/EXPORT_MANIFEST.json
drafts/project_state.yaml.draft
drafts/task.yaml.draft
runtime/RUNTIME_ARTIFACT_MANIFEST.json
runtime/project_state.runtime.yaml
runtime/task_contract.runtime.yaml
```

Missing:

```text
formal scope input
standalone provenance receipt
INSTALL_WRITESET.json
PRE_INSTALL_HASHES.json
ROLLBACK_MANIFEST.json
approval candidate
```

The plan expects an `adoption-confirmations.yaml`-style formal confirmation artifact; the Preview contains a singular `adoption-confirmation.yaml` created by the ad hoc generator.

## Scope comparison

Confirmed Phase 1 task:

```text
task_id=WINDOWS_REPLAY_PHASE1_PLUGIN_PLATFORM
task_goal=建立最小插件平台骨架，不迁移真实业务模块。
```

Expected allowed scope:

```text
src/short_cycle_quant/core_platform/**
tests/core_platform/**
tests/test_core_platform*.py
reports/modularization/phase1/**
task-related governance state/evidence files only
```

Expected denied scope includes:

```text
src/short_cycle_quant/cli.py
src/short_cycle_quant/workflow.py
src/short_cycle_quant/server.py
src/short_cycle_quant/dashboard.py
src/short_cycle_quant/cache.py
src/short_cycle_quant/models.py
src/short_cycle_quant/state_machine.py
src/short_cycle_quant/market_environment.py
src/short_cycle_quant/regulatory/**
src/short_cycle_quant/services/**
data/**
backups/**
.env
credentials/**
deployment/**
```

Actual Preview allowed scope:

```text
src/**
tests/**
data/**
```

The actual scope is materially broader and directly allows `data/**`, which the Phase 1 plan explicitly denies. The plan-level task ID, objective, test command, and project mode remain unresolved. Network/data/Git policy fields are absent because the scope input was never used. Runtime compilation then hardcodes a generic objective and `EXECUTION` state.

## Digest and provenance integrity

Verified internal matches:

- plan digest and embedded receipt hashes validate;
- export manifest plan/confirmation digests match;
- runtime manifest digest validates;
- both runtime artifact SHA-256 values match exact bytes;
- compiler digest matches the current compiler/schema identity;
- planner source digest matches the current `planner.py` bytes.

Security meaning: internal consistency only. A fully rewritten plan plus recomputed receipt is accepted because no key or external signed attestation exists. The receipt can be described only as `TOOLCHAIN_PROVENANCE_BINDING`.

Additional provenance defects:

- `input_scope_digest=e3b0...b855`, the SHA-256 of empty bytes;
- receipt says its command contract is `agent_adopt.py dry-run`, but generation directly called `build_plan`;
- generator version is hardcoded `1.0` while repository `VERSION` is `1.2.0`;
- plan has no target branch or HEAD;
- plan has no framework commit;
- target identity binds only canonical path, marker-file digest, and `.git` presence;
- untracked target writes are invisible to target identity.

Current target branch/HEAD are `modularization/phase1-plugin-platform` and `7ebd5da92462be547e1ba19d30bdfa36d0be542f`, but the Preview cannot prove that it was generated against those values.

## Write-set comparison

| Layer | Evidence |
|---|---|
| Planner | asset manifest only; no canonical install write-set |
| Runtime manifest | two runtime artifacts, not installation paths |
| Approval | missing |
| Preview `INSTALL_WRITESET` | missing |
| Installer | recomputes write-set at install time |

For the current manifest, the helper would classify `task.yaml` and `project_state.yaml` as creates and governance assets as manual. Equality among planner, approval, manifest, and installer cannot be proven because three of those artifacts do not contain the same canonical structure.

The new write-set schema is not invoked by the helper or installer. Installer sidecars are written with ordinary truncating `open(..., "w")`, after target writes, without exclusive-create or schema validation. This is not an approval-bound Preview write-set.

## Line endings and C0

Preview C0 scan: 0 illegal characters.

Line endings are mixed:

| Files | Ending |
|---|---|
| plan, confirmation, runtime manifest | CRLF |
| draft bundle, runtime YAML artifacts | LF |

This violates the stable-LF acceptance criterion even though parsed/canonical digests remain internally consistent.

## Replay target mutation

Replay contains a separate untracked `adoption-preview-v2/` with two files:

```text
adoption-plan.json
adoption-confirmation.yaml
```

The confirmation SHA-256 equals the external Preview confirmation, and the plan has the same digest/scope. The files were therefore written into the target worktree during this regeneration sequence. No installation or activation file exists, but target zero-write proof fails.
