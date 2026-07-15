# 04H Commit File Attribution

Baseline: `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1` on `ux/adoption-planner-04b-audit`.

| File | Commit | Type | Commit? | Note |
| --- | ---: | --- | ---: | --- |
| `README.md` | 1 | documentation | yes | Adoption CLI entry |
| `docs/EXISTING_PROJECT_ADOPTION.md` | 1 | documentation | yes | Planning/export and command surface |
| `governance/adoption/planner.py` | 1 | implementation | yes | Read-only planning |
| `scripts/agent_adopt.py` | 1 | CLI | yes | Commands, export, help registry |
| `schemas/adoption_plan.schema.json` | 1 | schema | yes | Plan contract |
| `schemas/adoption_confirmation.schema.json` | 1 | schema | yes | Confirmed draft contract |
| `tests/unit/test_agent_adopt.py` | 1 | test | yes | Planner and CLI help |
| `tests/unit/test_agent_adopt_export.py` | 1 | test | yes | External draft export |
| `governance/adoption/__init__.py` | 2 | public API | yes | Export/install public helpers |
| `governance/adoption/exporter.py` | 2 | implementation | yes | Draft export |
| `governance/adoption/installer.py` | 2 | implementation | yes | Controlled install/recovery |
| `governance/adoption/runtime_artifact_compiler.py` | 2 | implementation | yes | Runtime preview compiler |
| `schemas/adoption_final_approval.schema.json` | 2 | schema | yes | Final approval |
| `schemas/adoption_installation_receipt.schema.json` | 2 | schema | yes | Installation receipt |
| `schemas/adoption_rollback_approval.schema.json` | 2 | schema | yes | Rollback boundary |
| `schemas/rollback_assessment.schema.json` | 2 | schema | yes | Read-only assessment |
| `schemas/runtime_artifact_manifest.schema.json` | 2 | schema | yes | Preview manifest |
| `tests/unit/test_agent_adopt_install.py` | 2 | test | yes | Installation control |
| `tests/unit/test_agent_adopt_assessment_safety.py` | 2 | test | yes | Recovery assessment |
| `governance/adoption/activation.py` | 3 | implementation | yes | Approved activation |
| `governance/models/project_state.py` | 3 | model | yes | Activation state fields |
| `governance/state/store.py` | 3 | implementation | yes | Legacy fail-closed guard |
| `scripts/agent_state.py` | 3 | CLI | yes | Approved activation entry |
| `schemas/activation_approval.schema.json` | 3 | schema | yes | Activation approval |
| `schemas/activation_receipt.schema.json` | 3 | schema | yes | Activation receipt |
| `tests/unit/test_agent_adopt_activation.py` | 3 | test | yes | Activation provenance |
| `governance/adoption/lifecycle.py` | 4 | implementation | yes | Lifecycle bridge |
| `governance/adoption/lifecycle_context.py` | 4 | implementation | yes | Provenance/preflight context |
| `governance/adoption/evidence_registry.py` | 4 | implementation | yes | Evidence edge registry |
| `governance/security/output_sanitizer.py` | 4 | security | yes | Output redaction |
| `governance/verification/command_registry.py` | 4 | implementation | yes | Exact command authority |
| `governance/verification/command_runner.py` | 4 | implementation | yes | Shell-free sanitized runner |
| `schemas/adoption_lifecycle_evidence.schema.json` | 4 | schema | yes | Evidence contract |
| `tests/unit/test_adoption_lifecycle_foundation.py` | 4 | test | yes | State/evidence bridge |
| `tests/unit/test_adoption_remediation_security.py` | 4 | test | yes | Sanitizer/adversarial coverage |
| `docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml` | 5 | registry | yes | Adoption module scope |
| `docs/CHANGELOG.md` | 5 | changelog | yes | Public change record |
| `scripts/validate_governance.py` | 5 | validation | yes | Schema baseline |
| `schemas/project_state.schema.json` | 5 | schema | yes | Lifecycle state fields |
| `tests/fixtures/compatibility/schema_baseline.json` | 5 | fixture | yes | Compatibility baseline |
| `tests/unit/test_schema_contracts.py` | 5 | test | yes | Schema contract count |
| `tests/unit/test_public_adoption_assets.py` | 5 | test | yes | Public docs validation |
| `governance/security/__init__.py` | 5 | package | yes | Security package integration |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04C_GITHUB_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04D-A-R1_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04D-A_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04D-B_REMEDIATION_REPORT.md` | 6 | report | yes | Historical remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04D_IMPLEMENTATION_REPORT.md` | 6 | report | yes | Historical implementation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A-R1_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A-R2_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A-R3_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A_AUDIT_REPORT.md` | 6 | report | yes | Historical audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-B-R1_CONTRACT_REVISION_REPORT.md` | 6 | report | yes | Historical remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-B-R3_SPECIALIZED_TEST_REPORT.md` | 6 | report | yes | Historical tests |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C-A-R1_AUDIT_REPORT.md` | 6 | report | yes | Passing successor |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C-B-R1_REMEDIATION_REPORT.md` | 6 | report | yes | Historical remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C_AUDIT_REPORT.md` | 6 | report | yes | Preserved failed audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E-C_RUNTIME_ARTIFACT_REMEDIATION_REPORT.md` | 6 | report | yes | Historical remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04E_IMPLEMENTATION_REPORT.md` | 6 | report | yes | Historical implementation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-A-A-R1_AUDIT_REPORT.md` | 6 | report | yes | Passing activation audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-A-R1_ACTIVATION_IMPLEMENTATION_REPORT.md` | 6 | report | yes | Activation implementation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B-A-R1_AUDIT_REPORT.md` | 6 | report | yes | Passing lifecycle audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B-R1_REMEDIATION_REPORT.md` | 6 | report | yes | Lifecycle remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B_AUDIT_REPORT.md` | 6 | report | yes | Preserved failed audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-B_LIFECYCLE_FOUNDATION_IMPLEMENTATION_REPORT.md` | 6 | report | yes | Lifecycle implementation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-R2_AUDIT_REPORT.md` | 6 | report | yes | Final independent audit |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04F-R2_END_TO_END_ACCEPTANCE_REPORT.md` | 6 | report | yes | End-to-end acceptance |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04G_RELEASE_CLOSEOUT_REVIEW.md` | 6 | report | yes | Preserved failed closeout |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04G-R1_CLI_HELP_REMEDIATION_REPORT.md` | 6 | report | yes | CLI remediation |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04G-R1_RELEASE_CLOSEOUT_REVIEW.md` | 6 | report | yes | Passing closeout |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION_RELEASE_NOTES_DRAFT.md` | 6 | report | yes | Draft release notes |
| `reports/governance/AGC-UX-EXISTING-PROJECT-ADOPTION-04H_COMMIT_FILE_ATTRIBUTION.md` | 6 | report | yes | This attribution |

No unrelated, temporary, credential, cache, log, local-state, production-data, or binary file is scheduled for staging.
