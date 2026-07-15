# AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B-R1 Remediation Report

## Scope and authorization

The supplied baseline authorization was verified before implementation. Existing uncommitted governance changes were treated as the approved 04C–04F-B baseline; no reset, cleanup, commit, push, merge, rebase, or remote access occurred. The implementation remained local and synthetic-only.

| Baseline area | Attribution | This remediation |
|---|---|---|
| `governance/adoption/`, Runtime models, schemas, adoption tests | 04E–04F-B approved baseline | Modified only for the audited P0/P1 boundaries |
| Existing reports and public docs | 04C–04F-B approved baseline | Original failed audit preserved; documentation extended |
| Unrelated business code or production assets | Not in authorized baseline | Not touched |

## Root cause and repair

### P0 — sensitive output

`command_runner` previously returned raw output tails. A shared `governance.security.output_sanitizer` now redacts dotenv credentials, token/secret/password assignments, bearer values, private keys, credentialed URLs, cloud access keys, and synthetic canaries. It records only redacted tails, raw-byte digests, redaction count, and rule version. `run_adoption_test_plan` whitelists this safe contract so a mocked or exceptional runner cannot copy an unsafe text field into TestRunEvidence.

### P1 — provenance and TaskContract mapping

`build_lifecycle_context` now independently reloads and validates the plan, confirmation, Runtime manifest, final approval, installation receipt, activation approval, activation receipt, installed TaskContract, and ProjectState. It recomputes all digest links, compiler identity, target identity, selected registry command identity, candidate-set digest, blocked-decision digest, and workspace snapshot. Contract-to-request mapping now has a deterministic restriction sidecar for denied scope, blockers, candidate allowlist, Git/release/network/production restrictions, and autonomy; unknown authority or a reduced blocker set fails closed.

### P1 — evidence registry and state CAS

`governance.adoption.evidence_registry` is the sole registered mapping from every forward state edge to its required evidence type and status. State transition re-reads the evidence file, schema-validates it, recomputes the file digest, checks target identity, prior state, and every persisted upstream evidence file under a lifecycle lock before using the existing atomic writer. Changed or missing upstream evidence blocks the next transition.

### P1 — Verification and Closure

Verification binds current-state, target, installation/activation provenance, denial status, blocker status, workspace freshness, and formal verification output. Closure rechecks those bindings before calling the existing closure evaluator and retains `production_ready=false`, `released=false`, and `deployed=false`.

## Adversarial coverage

The added coverage exercises synthetic secret redaction and digest preservation, unsafe mocked output exclusion, wrong evidence type rejection, modified prior evidence rejection, confirmed-candidate reconstruction, and modified confirmation rejection. Existing lifecycle tests continue to cover forward-only ordering, Guard denial, exact command identity, failed/stale verification, and non-production closure.

## Verification evidence

Executed from `/home/liyouran1997/projects/ai-agent-project-governance` with `PYTHONDONTWRITEBYTECODE=1`:

| Command | Result |
|---|---|
| `python3 -m unittest tests.unit.test_adoption_lifecycle_foundation tests.unit.test_adoption_remediation_security tests.unit.test_agent_adopt_activation tests.unit.test_agent_adopt_assessment_safety tests.unit.test_agent_adopt_export tests.unit.test_agent_adopt_install tests.unit.test_public_adoption_assets tests.unit.test_schema_contracts` | PASS, 65 tests |
| `python3 -m unittest` | PASS, 144 tests |
| `python3 scripts/validate_governance.py` | PASS, 32 schemas |
| `python3 scripts/check_code_quality.py` | PASS, 155 Python files, no warnings |
| `python3 scripts/check_schema_compatibility.py` | PASS, 32 schemas |

No network request, package installation, real-project access, production write, or Git write was performed. The original `04F-B_AUDIT_REPORT.md` remains unchanged.

## Result

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B-R1
REMEDIATION_PASSED_PENDING_READ_ONLY_REAUDIT
SENSITIVE_OUTPUT_REDACTION_VERIFIED
LIFECYCLE_PROVENANCE_CHAIN_VERIFIED
EVIDENCE_REGISTRY_AND_CAS_VERIFIED
VERIFICATION_AND_CLOSURE_RECHECKS_VERIFIED
```
