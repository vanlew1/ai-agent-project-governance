<!-- encoding: UTF-8 -->
# CASE-001 Phase 0.5 再生成结果独立验收报告

审计日期：2026-07-21（Asia/Shanghai）
任务性质：只读独立验收；除本报告组和 Obsidian 移交外未修改源码、测试、Preview、Replay 或 Git 历史。
最终验收结论：

```text
REPLAY_TARGET_MUTATION_DETECTED
```

当前结果不得进入 Owner 安装复核，更不得安装或激活。

## 1. 开工门禁

| 项目 | 现场值 |
|---|---|
| Governance root | `C:/Users/范德彪/Desktop/ai数据/codex-worktrees/governance-case001-minimum-unblock` |
| Governance branch | `case001/minimum-adoption-unblock` |
| Governance HEAD | `74d90e68339daba7011d784a6ee0affa72611d25` |
| Governance commit | `74d90e6 Merge pull request #3 from vanlew1/codex/superpowers-positioning-release` |
| Governance remote | `origin https://github.com/vanlew1/ai-agent-project-governance.git` |
| Replay root | `C:/Users/范德彪/Desktop/ai数据/codex-worktrees/replay-modularization-phase1` |
| Replay branch | `modularization/phase1-plugin-platform` |
| Replay HEAD | `7ebd5da92462be547e1ba19d30bdfa36d0be542f` |
| Replay tracked changes | none |
| Replay untracked paths | `adoption-preview-v2/`, `reports/` |
| Replay `task.yaml` | absent |
| Replay `project_state.yaml` | absent |

Linux Git cannot directly parse the Windows absolute `.git` worktree pointers. The authoritative branch/HEAD/status evidence above was therefore collected with Windows Git; Linux Git was used only with an explicit translated `--git-dir/--work-tree` for object and semantic-diff inspection.

## 2. Source-change inventory

### Changed tracked files (17)

```text
VERSION
docs/EXISTING_PROJECT_ADOPTION.md
examples/demo/run_visual_proof.py
governance/adoption/activation.py
governance/adoption/exporter.py
governance/adoption/installer.py
governance/adoption/lifecycle.py
governance/adoption/planner.py
governance/adoption/runtime_artifact_compiler.py
schemas/adoption_plan.schema.json
scripts/agent_adopt.py
scripts/validate_governance.py
tests/unit/test_agent_adopt_activation.py
tests/unit/test_agent_adopt_assessment_safety.py
tests/unit/test_agent_adopt_export.py
tests/unit/test_agent_adopt_install.py
tests/unit/test_schema_contracts.py
```

### Relevant new files

```text
CASE001_FINDINGS_RESOLUTION_MATRIX.md
CHANGELOG.md
generate_preview.py
governance/adoption/c0_scanner.py
governance/adoption/writeset.py
reports/case001/CASE001_FINDINGS_RESOLUTION_MATRIX.md
schemas/adoption_install_writeset.schema.json
schemas/adoption_provenance_receipt.schema.json
schemas/adoption_scope_input.schema.json
tests/unit/test_case001_minimum_unblock.py
```

Deleted files: none.

### Behavioral, schema, compatibility, and security changes

- `agent_adopt.py dry-run` accepts `--scope-file`; planner parses a new scope schema and injects task ID, task goal, allow/deny paths, one test command, and execution mode.
- Empty active-development scope is rejected by the planner; observation-only empty scope is accepted only when the input contains `owner_confirmed_empty_scope=true`.
- Plans now require an embedded provenance receipt. The receipt binds the planner source digest, a static command-contract digest, input-scope digest, target identity, plan digest, and generation time.
- `_digest` now omits both `plan_digest` and `provenance_receipt` by default; confirmations explicitly use no omitted fields.
- Installer adds a generated write-set plus pre-install/rollback sidecar files; activation writers add `O_BINARY`, explicit LF handling, and fsync.
- Schema set increases from 32 to 35 and `adoption_plan.provenance_receipt` becomes required. The compatibility fixture was not updated, and the authoritative compatibility gate fails.
- Version changes from `1.1.0` to `1.2.0`; provenance still hardcodes generator version `1.0`.

## 3. Decisive acceptance failures

1. `generate_preview.py` bypasses the formal CLI, directly imports internal functions, manually broadens scope, recomputes plan/provenance digests, and writes `confirmed_by_user: true`. Detailed result: `AD_HOC_REGENERATION_SCRIPT_NOT_ACCEPTABLE`.
2. The generated Preview uses `src/**`, `tests/**`, and `data/**`; Phase 1 instead allows only the core-platform/test/report slice and explicitly denies `data/**` plus existing business modules. The Preview therefore authorizes paths that the confirmed Phase 1 plan forbids.
3. Preview generation passed no scope file. `input_scope_digest` equals SHA-256 of empty bytes; task ID, task goal, and project mode remain `UNRESOLVED` in the plan. The script then altered the plan out of band.
4. Independent execution proves exporter/compiler do not fail closed across the full chain: an active-development plan with a non-empty `task_draft` but an empty confirmed `scope_candidate` reaches an empty-scope Runtime.
5. Replay contains an untracked `adoption-preview-v2/` with `adoption-plan.json` and `adoption-confirmation.yaml`. Its confirmation hash matches the sibling Preview. This is a real target-project write outside the approved external Preview directory.
6. The authoritative CI gate fails 2 of 8 gates: schema compatibility and full tests.
7. Windows-generated Preview files mix CRLF and LF, contradicting the stable-LF requirement. WSL reproduces an `EXISTS_SAME` → `EXISTS_DIFFERENT` failure caused by bytewise comparison across line-ending normalization.
8. Findings evidence is inconsistent: missing statuses, duplicate ID 009 in Markdown, conflicting matrices, and three retained illegal C0 characters.

## 4. Replay zero-write accounting

```text
business_source_writes=0
business_test_writes=0
database_writes=0
production_data_writes=0
task_yaml_created=false
project_state_yaml_created=false
AGENTS_md_modified=false
install_executed=false
activate_executed=false
target_project_preview_writes=2
```

The first nine values are supported by Windows Git status, file presence checks, and timestamps. They do not permit an overall “zero write” claim because two Preview files were created inside the Replay worktree.

## 5. Test evidence summary

| Scope | Result | Counts | Duration |
|---|---|---:|---:|
| Baseline HEAD archive | PASS | 152 passed | 20.033 s |
| Directed adoption/security suite | PASS | 57 passed | 25.605 s |
| Current full unittest | FAIL | 156 total; 154 passed, 1 failed, 1 error, 0 skipped | 88.572 s |
| Governance release gate | FAIL | 6/8 gates | 105.59 s |
| Independent tamper/line-ending/Preview checks | FAIL finding confirmed | 12 checks passed; 1 active-empty-runtime bypass reproduced | 1.54 s (initial set) |
| C0 scan: Preview | PASS | 0 illegal characters | n/a |
| C0 scan: Replay findings | FAIL | 3 illegal characters | n/a |

No new test failure was observed in the 57-test directed suite. The full-suite failure and error are both new relative to the 152-test clean baseline archive. Windows-native Python verification could not be executed because no Windows Python or `py` launcher is installed; this is an evidence gap, not a pass.

Exact commands are recorded in the specialized reports.

## 6. Git and publication state

- No CASE-001 implementation commit exists; all implementation changes remain uncommitted on HEAD `74d90e6`.
- This audit did not commit, push, reset, clean, stash, rebase, amend, install, or activate.
- Since no new commit exists, there is nothing from this branch that could have been pushed as the CASE-001 upgrade.
- Commit closeout is not allowed yet. The implementation, Preview, compatibility baseline, cross-platform tests, and findings evidence must first be corrected and independently re-audited.

## 7. Required next step

Create a new remediation task. At minimum it must:

1. replace `generate_preview.py` with a wrapper that invokes only the public CLI and never writes confirmations or digests;
2. generate a formal scope-input artifact using the exact Phase 1 allow/deny set;
3. enforce non-empty confirmed scope independently in exporter, compiler, approval, and installer;
4. include preview write-set/approval candidates and bind branch/HEAD/framework commit;
5. normalize all formal Windows outputs to LF and pass Linux/WSL plus Windows-native tests;
6. remove the Replay-local Preview through an explicitly authorized cleanup task;
7. reconcile Findings 001–009 and preserve corrected C0-clean evidence.

Stop here. Do not install.
