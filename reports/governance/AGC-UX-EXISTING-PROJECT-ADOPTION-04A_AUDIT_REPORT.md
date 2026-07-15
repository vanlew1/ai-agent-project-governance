# AGC-UX-EXISTING-PROJECT-ADOPTION-04A Audit Report

## Result

`AGC-UX-EXISTING-PROJECT-ADOPTION-04A` — `AUDIT_COMPLETE`; `READY_FOR_IMPLEMENTATION_DECISION`.

The current repository provides the components for governed work, but its existing-project adoption journey is not yet executable end-to-end by an ordinary user. `docs/EXISTING_PROJECT_ADOPTION.md` exposes one copyable detection command and six high-level instructions; completing the documented runtime flow requires at least 13 operations, including two schema-sensitive manual configurations and four undocumented or insufficiently documented runtime stages. There is no formal `adopt` command in v1.0.0.

This was a read-only audit. No network, dependency download, real-project installation, runtime/schema/configuration change, or Git write operation was performed.

## Evidence and audit basis

| Evidence | Finding |
| --- | --- |
| `docs/EXISTING_PROJECT_ADOPTION.md` | Defines backup, adapter detection, selective asset copy, manual `task.yaml`/`project_state.yaml`, then Preflight → State → Guard; explicitly says no `adopt` command exists. |
| `docs/PRESETS.md` and `config/presets/*.yaml` | Defines `lightweight`, `standard`, and `strict`, but its executable initializer is explicitly for creating a new project, not in-place adoption. |
| `scripts/agent_*.py` CLI/source inspection | Confirms available Adapter, Preflight, State, Guard, TestPlan, TestRun, Verification, and Closure entry points. The last four are not presented as a public adoption sequence; TestPlan has only source-level `create`/`show` usage. |
| `docs/ADOPTION_AUDIT.md` and `scripts/agent_audit.py` | Supplies a useful, default read-only configuration-completeness audit and a preset recommendation, but not an adoption plan or file manifest. |
| Local commands | Adapter detection completed with `generic`/`FALLBACK`/low confidence; the local audit completed `READY`, score 95, with a `strict` recommendation. |

## Current adoption flow

```mermaid
flowchart LR
  A[Discover documents] --> B[Choose a preset manually]
  B --> C[Back up or create branch]
  C --> D[Detect adapter]
  D --> E[Manually choose and copy governance assets]
  E --> F[Hand-author task.yaml and project_state.yaml]
  F --> G[Preflight creates TaskContract]
  G --> H[Initialize and activate state]
  H --> I[Run Guard]
  I --> J[Create TestPlan and run tests]
  J --> K[Verification]
  K --> L[Closure and report]
```

The diagram is the actual required path reconstructed from the published adoption document plus the local runtime entry points. Only D has an adoption-document command. B, E, F, and J–L require the user to infer missing details from unrelated documents, script help, or source.

## Practical step list and user-friction score

Score: 1 = almost no barrier; 5 = an ordinary user is unlikely to complete it correctly alone.

| # | User action / local command or file | User must understand | Friction | Automation class |
| --- | --- | --- | ---: | --- |
| 1 | Find the adoption, preset, audit, and runtime documents | Which document is authoritative for an existing project | 3 | A: link and sequence documents |
| 2 | Choose `lightweight`, `standard`, or `strict` | Risk profile, multi-module scope, production/external boundaries | 4 | B: recommend, then confirm |
| 3 | Create a normal backup or branch | Recovery point and local Git policy | 2 | C: user confirms the recovery method |
| 4 | `python <runtime-root>/scripts/agent_detect_adapter.py --root . detect` | Runtime-root location; whether a detection result is credible | 3 | A: run read-only detection |
| 5 | Interpret adapter result and choose test-entry candidates | A detected stack is advice, not permission or an accurate test command | 4 | B: propose candidates, user confirms |
| 6 | Select and copy `governance/`, `schemas/`, `config/`, required `scripts/`, `AGENTS.md`, and `agent_rules/` | Ownership, minimum manifest, overwrite and upgrade consequences | 5 | B: generate manifest/diff; never copy without confirmation |
| 7 | Create project-specific `task.yaml` | narrow read/write scope, deny paths, reversible objective, test evidence | 5 | B: generate a draft, user confirms every boundary |
| 8 | Create project-specific `project_state.yaml` | project mode, plan status, high-risk paths, default forbidden operations | 5 | B: generate a draft, user confirms risk decisions |
| 9 | Run `agent_preflight.py --task-file … --project-state-file …` | paths, output handling, and TaskContract status/exit codes | 4 | A: produce an exact dry-run command after files are approved |
| 10 | `agent_state.py init …`, then `activate …` | `.agent_state` is local runtime state and activation changes execution posture | 4 | B: show commands and effects, user confirms activation |
| 11 | `agent_guard.py check` | working directory, active state, changed-path and approval outcomes | 4 | A: run after state is explicitly activated |
| 12 | Create TestPlan, run selected test commands | TestPlan's public UX is incomplete; commands can be expensive or semantically wrong | 5 | B: identify candidates, user approves final test plan |
| 13 | Run Verification and Closure | evidence freshness, closure report location, and whether a task is really closed | 5 | B: assemble evidence; user keeps release/production decisions |

**Count:** 13 practical operations; at least 2 mandatory schema-sensitive files to author; 6 broad asset groups to select/copy; only 1 adoption-flow command is published verbatim. The published audit adds a valuable optional read-only command, but does not remove the manual setup burden.

## Five most failure-prone points

1. **No adoption-specific preset handoff.** The preset guide points to `init_new_project.py`, while the adoption document correctly forbids treating that initializer as an in-place shortcut. A user has to decide how a preset becomes `config/governance_preset.yaml` in an existing repository.
2. **Ambiguous copy manifest.** “Copy only governance assets you intend to own” names six broad groups but not a minimum, versioned manifest, overwrite policy, or upgrade policy. This risks both duplicate copying and omission of a required template/schema/script.
3. **Hand-authored scope and state files.** `task.yaml` and `project_state.yaml` determine permissions and guards, yet the adoption page gives neither a generated draft nor a guided field-level explanation. A small mistake can be over-broad or cause repeated blocking.
4. **Broken next-step continuity after Preflight.** The State/Guard/TestPlan/TestRun/Verify/Close sequence exists locally but is not documented as a copyable adoption runbook. TestPlan lacks normal CLI help and depends on generated local state, making the first successful run difficult to discover.
5. **Low-confidence adapter fallback has no decision path.** The detector is intentionally advice-only. Its `generic` fallback (observed in this repository) is safe, but the user is not told how to select/validate a test command after a low-confidence result.

## Safe automation versus mandatory human confirmation

### Safe, read-only automation

- Detect project markers and report Adapter confidence/evidence.
- Run the existing read-only configuration-completeness audit.
- Inventory candidate test files/configuration and report candidates without executing them.
- Compare a prospective governance asset manifest with the target and report conflicts/overwrites.
- Generate a dry-run adoption plan, command preview, health-check checklist, and rollback checklist.
- Recommend a preset using visible local signals, explicitly labeling it as a recommendation.

### Generate, then require explicit confirmation

- `task.yaml` allowed/denied paths and autonomy fields.
- `project_state.yaml`, high-risk paths, and default forbidden operations.
- A selected test command and its cost/network assumptions.
- The exact asset manifest and every overwrite/create operation.
- State activation and any command that persists runtime evidence.
- Multi-agent ownership boundaries.

### Must remain human decisions

- Production data, credentials, external APIs, cloud services, and data-retention policy.
- Release, deployment, real business-semantic change, and irreversible Git operations.
- Security policy weakening, exception approvals, or bypassing Guard/Preflight outcomes.
- The final meaning of a passing test/verification result for the user's product.

## Candidate capability priority

| Capability | Value | Complexity / risk | Recommendation | Network / project writes | Dry-run first? |
| --- | --- | --- | --- | --- | --- |
| `adopt --dry-run` planner | Very high: turns discovery into one reviewed plan | Medium; must keep recommendations distinct from authorization | **P0, next phase** | None / none | Yes; this is the capability |
| Project scanner | High: reuses Adapter + Audit evidence | Low–medium; avoid duplicating existing `agent_audit` | **P0**, compose existing checks | None / none | Yes |
| Test-entry candidate finder | High: resolves a primary blocker | Medium: candidates must never silently run | **P0**, candidates only | None / none | Yes |
| Preset recommender | Medium: existing audit already recommends one | Low; recommendation can be misleading without rationale | **P1**, reuse audit output with explanations | None / none | Yes |
| Configuration draft generator | High once a plan is approved | Medium–high: scopes carry governance authority | **P1**, generate untrusted drafts | None / draft-only | Yes, plus confirmation |
| Post-adoption health check | High: detects incomplete copy/configuration | Low–medium; extend read-only audit | **P1** | None / none | Yes |
| Rollback checklist | Medium: improves confidence before any write | Low | **P1**, generate from manifest | None / none | Yes |
| Asset copier | Medium: saves time after a correct plan | High: overwrite, ownership, and version-drift hazards | **P2**, only after reviewed manifest | None / potentially writes | Mandatory |
| Interactive wizard | Medium: pleasant UX but broad surface | High: can conceal risk choices | **P2**, after planner proves demand | None / potentially writes | Mandatory |
| `adopt --plan-only` | Redundant if it is merely another spelling of dry-run | Low but increases command surface | Do not create separately; make it an explicit dry-run mode | None / none | Yes |

## Recommended next-stage minimum scope

Build a **read-only adoption planner** that composes, rather than replaces, `agent_detect_adapter.py` and `agent_audit.py`:

1. Scan locally and emit adapter evidence, audit result, preset recommendation, candidate test entries, and a proposed asset manifest.
2. Emit a machine-readable and human-readable plan with every proposed create/copy/overwrite operation marked `requires_confirmation`.
3. Generate draft `task.yaml` and `project_state.yaml` only as untrusted templates, with unresolved/high-risk fields blank or explicitly blocked.
4. Generate exact next commands only after the plan has a user-confirmed manifest and boundaries.
5. Add a read-only health check that explains the next missing prerequisite instead of merely returning a guard failure.

This gives the user immediate value without claiming that inference grants authority. It should have no network dependency and no write mode in the first stage.

## Not recommended for the next stage

- An in-place “one-click adopt” that copies files, initializes state, activates a task, and executes tests automatically.
- Automatic selection/execution of a test command from marker detection alone.
- Automatic approval of write scope, production/external access, Git, release, security, or business-semantic decisions.
- A separate `plan-only` command if the dry-run plan already provides the same behavior.
- Calling `init_new_project.py` from adoption; its documented/new-project behavior is intentionally not an in-place migration path.

## Verification

| Command / check | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_public_adoption_assets tests.unit.test_adapter_detection tests.unit.test_agent_audit` | PASS — 17 tests, 0 failures, 0.688 s. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_detect_adapter.py --root . detect` | Completed offline; `generic`, `FALLBACK`, low confidence. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_audit.py --project-root . --format json` | Completed offline; score 95, `READY`, recommended preset `strict`; Adapter signal is a warning. |
| Local entry existence/help inspection | `agent_detect_adapter`, `agent_preflight`, `agent_state`, `agent_guard`, `agent_audit`, and `init_new_project` expose local entry points. TestPlan/TestRun/Verify/Close source was inspected; they require local runtime state and are not safely runnable for this audit. |

## Not executed

- No real existing-project installation, copy, configuration generation, Preflight, state activation, Guard, TestPlan, TestRun, Verification, or Closure was run: each would create/modify project-local adoption/runtime state and is outside this read-only audit.
- No `init_new_project.py` invocation: it creates a project and is explicitly not an adoption shortcut.
- No network access, package installation, external API/browser activity, Git commit/push/tag/reset/clean/rebase/force, or production-data access.

## Workspace state

- Baseline: branch `main`; HEAD `1860601f76e394569f71dab56443296ca2080f70`; `VERSION` `1.0.0`.
- Pre-existing changes were preserved: `README.md`, `README.zh-CN.md`, `docs/COMPATIBILITY.md`, `docs/DEMO.md`, `docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md`, `tests/unit/test_public_adoption_assets.py`, `docs/assets/demo/`, `examples/demo/`, `tests/unit/test_demo_visual_proof.py`, and the listed preceding UX reports.
- Task-owned change: this audit report only.
- Final `git status --short`: the preceding entries remain, plus `?? reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04A_AUDIT_REPORT.md`; no baseline entry was removed or changed by this task.
