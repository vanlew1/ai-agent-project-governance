<!-- encoding: UTF-8 -->
# CASE-001 Test Change Safety Audit

## Result

The modified suite is not sufficient to prove the empty-scope safety regression fixed. Green directed tests coexist with a reproducible exporter/compiler bypass and a failing authoritative release gate.

## Original test purpose and adaptations

- Activation tests originally exercised install/activate/lifecycle provenance, mutation rejection, loaders, Unicode/space paths, and synthetic end-to-end closure. The fixture now injects `src/**` and manually recomputes both plan and receipt digests.
- Assessment-safety tests originally proved rollback assessment performs no target, Git, network, shell, or destructive operation. Their fixtures now manually set only `task_draft.write_scope.allow`, forge a receipt, and leave `scope_candidates` empty.
- Export tests originally proved external-only output, target identity, candidate-ID rejection, and no target writes. The shared fixture now manually sets `task_draft` scope and provenance but leaves the confirmed scope candidate empty.
- Install tests originally proved exact-byte install, conflict refusal, loader validation, provenance rejection, and manual-only rollback. Their fixture likewise forges a non-empty task draft while confirming the original empty scope candidate.
- Schema tests only update the expected schema count from 32 to 35; the compatibility fixture is not updated.

These changes mostly preserve the original target assertions, but they introduce hand-built authority structures instead of using the new public scope-file flow. Several tests therefore continue through an empty confirmed Runtime while making the plan-level checker appear non-empty.

## Required negative cases

| Required case | Existing test evidence | Independent result |
|---|---|---|
| active development + `allowed_paths=[]` → reject | Only private `_parse_and_validate_scope` | PASS at planner; FAIL across exporter/compiler |
| observation-only + explicit Owner confirmation → accept | Private parser only | PASS |
| observation-only without confirmation → reject | Missing from repository tests | PASS in independent audit |

No repository test proves those cases through planner → exporter → compiler → approval → installer. There is no formal-scope-file end-to-end adoption fixture.

## Reproduced full-chain defect

Independent synthetic steps:

1. build a default plan;
2. set `task_draft.write_scope.allow=["src/**"]` and mode `ACTIVE_DEVELOPMENT`;
3. leave `scope_candidates[0].allowed_paths=[]`;
4. recompute the ordinary plan and receipt digests;
5. confirm the empty scope candidate;
6. export and compile.

Observed result: compilation succeeds and `task_contract.runtime.yaml` contains `write_scope.allow: []` while project mode is active development.

Root cause: `_validate_scope_not_empty` checks only `plan.task_draft.write_scope.allow` and mode. `_validate_confirmation` checks only that confirmation matches a listed scope candidate. No equality invariant requires the task draft, selected scope candidate, confirmation, draft, runtime, approval, and installer scope to all be the same non-empty set.

## Digest-test assessment

- The corrected `_digest(plan)` call now uses its default omitted fields and avoids self-reference.
- The omitted-field rule is not a named shared constant; it is a default literal on a private exporter helper.
- Planner computes its initial digest independently rather than calling the helper; exporter/compiler/tests import or duplicate rules.
- Independent tampering with task goal, allowed paths, target identity, or receipt and only recomputing the ordinary plan digest fails closed.
- Recomputing both ordinary plan and receipt digests is accepted, as expected for an unkeyed digest. The accurate claim is `TOOLCHAIN_PROVENANCE_BINDING`, not cryptographic anti-forgery.

## Exact commands and results

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.unit.test_case001_minimum_unblock \
  tests.unit.test_agent_adopt_export \
  tests.unit.test_agent_adopt_install \
  tests.unit.test_agent_adopt_activation \
  tests.unit.test_agent_adopt_assessment_safety \
  tests.unit.test_schema_contracts
```

Result: 57 passed, 0 failed, 0 errors, 0 skipped, 25.605 s.

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 /tmp/case001_independent_checks.py
```

Result: required parser and tamper checks passed; active-development empty confirmed scope reached Runtime.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q
```

Result: 156 total; 154 passed, 1 failed, 1 error, 0 skipped, 88.572 s.

Failed node:

```text
tests.unit.test_agent_adopt.AgentAdoptTest.test_manifest_reports_create_same_and_different_without_copying
```

Error node:

```text
tests.unit.test_demo_visual_proof.DemoVisualProofTest.test_default_run_uses_temporary_output_without_repo_changes
```

The error is WSL worktree-pointer incompatibility. The failure is a real line-ending portability defect in raw-byte asset comparison.

## Audit judgment

The suite contains reasonable fixture adaptation for old tests but lacks the safety assertions needed to prove the new boundary. It also changes symlink failures into platform skips/automatic success paths, which is understandable on unprivileged Windows but reduces cross-platform security evidence unless a privileged Windows job retains the assertions.

Required remediation: create public-interface tests using a real `--scope-file`, assert scope equality at every artifact boundary, add the missing observation-negative case, and retain adversarial mismatch fixtures.
