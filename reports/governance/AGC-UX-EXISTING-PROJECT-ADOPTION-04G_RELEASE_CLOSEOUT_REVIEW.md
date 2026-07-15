# AGC-UX-EXISTING-PROJECT-ADOPTION-04G Release Closeout Review

Status: `REQUIRES_REVISION` — `NOT_READY_FOR_GIT_WRITE`

## Baseline and workspace

- Branch: `ux/adoption-planner-04b-audit`
- HEAD: `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1`
- Staged files: none.
- Workspace: authorized 04D/04E/04F adoption-runtime implementation, Schema, CLI, test, documentation, and historical-report changes; no deleted files, unknown binary files, production data, or real-project artifacts were found.

## 04F-R2 conclusion

The latest implementation and independent audit reports remain the current effective evidence: five synthetic targets (Python, Node, Generic/non-Git, Unicode path, and space path) reached `CLOSED` through dry-run, draft export, Runtime compilation, final approval, controlled install, approved activation, formal Preflight, Guard, exact test planning/execution, Verification, and Closure. `CLOSED != PRODUCTION_READY != RELEASED != DEPLOYED`.

## Attribution and proposed logical commits

| Commit | Proposed subject | Files |
| --- | --- | --- |
| 1 | `feat(adoption): add governed existing-project planning and draft export` | `governance/adoption/planner.py`, `scripts/agent_adopt.py`, `schemas/adoption_plan.schema.json`, `tests/unit/test_agent_adopt.py`, `tests/unit/test_agent_adopt_export.py`, initial README/adoption docs |
| 2 | `feat(adoption): bind approved runtime artifacts and controlled installation` | `governance/adoption/exporter.py`, `governance/adoption/runtime_artifact_compiler.py`, `governance/adoption/installer.py`, receipt/approval/rollback/runtime-manifest schemas, installation/assessment tests |
| 3 | `feat(adoption): add provenance-bound approved activation` | `governance/adoption/activation.py`, `scripts/agent_state.py`, activation schemas, ProjectState/store changes, activation tests |
| 4 | `feat(adoption): bridge formal lifecycle with evidence-bound state transitions` | `governance/adoption/lifecycle.py`, `lifecycle_context.py`, `evidence_registry.py`, `governance/security/`, command runner/registry, lifecycle schema, lifecycle/remediation tests |
| 5 | `test(adoption): verify fail-closed end-to-end lifecycle` | lifecycle E2E tests, schema compatibility fixture/baseline updates, module registry, public adoption documentation |
| 6 | `docs(governance): record adoption audits and release-closeout evidence` | all `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04*.md` reports and this release-notes/closeout pair |

No `/tmp` output, cache, credential, local state, or log is included in this plan. Each listed file belongs to one proposed commit only; the plan is not a staging operation.

## Public-security review

The repository-wide credential-pattern search found only expected safety rules, documentation examples, and synthetic canaries. Review of the canary tests confirms their values are synthetic and sanitizer assertions prevent persistence of raw output. No real key, credentialed remote, personal path, production target, or raw secret was found in release-candidate content.

## API, Schema, and document review

- Legacy adoption activation fails closed; `activate-approved` is separately approved and does not run Preflight, tests, Verification, or Closure.
- Installation does not activate; Preflight does not run tests; Verification requires fresh evidence; Closure does not authorize production.
- Runtime model, Schema, receipt, evidence, status-transition, Generic/non-Git, Node-local-test, Unicode-path, and space-path contracts are covered by the current local suite.
- Historical failing reports `04E-C_AUDIT` and `04F-B_AUDIT` remain intact for traceability. Their passing successors are `04E-C-A-R1` and `04F-B-A-R1`; the current end-to-end state is `04F-R2` and `04F-R2_AUDIT`.

## P1 blocker

`scripts/agent_adopt.py --help` advertises only `dry-run`. The command dispatcher nevertheless implements `export-drafts`, `compile-runtime-artifacts`, `install-approved`, `assess-rollback`, and `rollback-install`. This violates the 04G requirement that new CLI help be complete and creates a public discoverability/operability gap. It is an implementation-level P1 finding, so this review did not repair it.

## Final local verification

Executed from `/home/liyouran1997/projects/ai-agent-project-governance`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest                         # 147 passed, 15.947s
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py      # PASS, 32 schemas
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py       # PASS, 155 Python files, no warnings
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py # PASS, 32 schemas
git diff --check                                                       # PASS
```

## Operations not executed

No `git add`, commit, push, merge, rebase, reset, clean, stash, tag, PR, release, deployment, network access, real-project access, or production-data operation was performed.

## Next step

Repair the `agent_adopt` command parser/help surface, add direct CLI-help regression coverage, then rerun the complete 04G closeout review. Only after a passing re-review may the owner decide whether to authorize Git writes.
