from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from governance.adoption.activation import activate_approved
from governance.adoption.lifecycle_context import build_lifecycle_context
from governance.adoption.evidence_registry import upstream_digests
from governance.adoption.lifecycle import build_adoption_test_plan, build_guard_evidence, close_adoption, run_adoption_test_plan, transition_project_state, verify_adoption
from governance.adoption.lifecycle_context import run_adoption_preflight
from governance.adoption.installer import digest
from governance.adoption.runtime_artifact_compiler import MANIFEST_FILENAME, digest_bytes
from governance.models.project_state import ProjectState
from governance.state import store
from tests.unit.adoption_flow import installed_inputs


R1_ROOT = Path("/tmp/agc-adoption-04f-a-r1")
R1_ROOT.mkdir(parents=True, exist_ok=True)


class ApprovedActivationTest(unittest.TestCase):
    def setup(self, base: Path, allowed_scope: list[str] | None = None, *, kind: str = "python", target_name: str = "target"):
        target = base / target_name; target.mkdir(); (target / "AGENTS.md").write_text("synthetic only\n", encoding="utf-8")
        if kind == "python":
            (target / "pyproject.toml").write_text("[project]\nname = 'synthetic'\nversion = '0.0.0'\n", encoding="utf-8")
            (target / "tests").mkdir()
            (target / "tests" / "__init__.py").write_text("", encoding="utf-8")
            (target / "tests" / "test_smoke.py").write_text("import unittest\n\nclass Smoke(unittest.TestCase):\n    def test_pass(self): self.assertTrue(True)\n", encoding="utf-8")
        elif kind == "node":
            (target / "package.json").write_text('{"name":"synthetic","scripts":{"test":"node -e \\\"process.exit(0)\\\"}}', encoding="utf-8")
        elif kind != "generic":
            raise ValueError(f"unsupported synthetic kind: {kind}")
        if allowed_scope is None:
            allowed_scope = ["src/core/**"]
        plan, plan_path, confirmation_path, drafts, runtime, final, install = installed_inputs(
            base, target, stem="activation", allowed_paths=allowed_scope,
        )
        manifest = json.loads((runtime / MANIFEST_FILENAME).read_text(encoding="utf-8")); receipt = json.loads(install.read_text(encoding="utf-8"))
        final_mapping = yaml.safe_load(final.read_text(encoding="utf-8"))
        approval = {"schema_version":"1.0","approved_by_user":True,"approved_action":"ACTIVATE_INSTALLED_RUNTIME","target_identity_digest":plan["target_identity"]["identity_digest"],"runtime_artifact_manifest_digest":manifest["manifest_digest"],"final_install_approval_digest":digest(final_mapping),"installation_receipt_digest":digest(receipt),"compiler":{"id":manifest["compiler_id"],"version":manifest["compiler_version"],"digest":manifest["compiler_digest"]},"runtime_artifacts":{"task_contract_sha256":digest_bytes((target / "task.yaml").read_bytes()),"project_state_sha256":digest_bytes((target / "project_state.yaml").read_bytes())},"expected_current_state":{"status":"INSTALLED_NOT_ACTIVATED","project_state_sha256":digest_bytes((target / "project_state.yaml").read_bytes())},"requested_transition":{"from":"INSTALLED_NOT_ACTIVATED","to":"ACTIVATED_NOT_PREFLIGHTED"},"blocked_decisions":{key:"BLOCKED" for key in ("production_data","external_api","network_access","git_write","release","security_bypass","business_semantic_change")}}
        activation = base / "activation.yaml"; activation.write_text(yaml.safe_dump(approval), encoding="utf-8")
        return target, runtime, final, install, activation

    def activate(self, base: Path, output: Path | None = None):
        target, runtime, final, install, activation = self.setup(base)
        result = activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, activation, output or base / "activation.json")
        return target, result

    def test_activate_approved_transitions_only_project_state(self) -> None:
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            base = Path(temp); target, result = self.activate(base)
            state = yaml.safe_load((target / "project_state.yaml").read_text(encoding="utf-8"))
            self.assertEqual("ACTIVATED_NOT_PREFLIGHTED", result["status"]); self.assertTrue(state["activated"])
            self.assertEqual("ACTIVATED_NOT_PREFLIGHTED", state["status"]); self.assertFalse(state["preflight_executed"])
            self.assertFalse(state["tests_executed"]); self.assertFalse(state["verification_completed"]); self.assertFalse(state["closure_completed"])

    def test_modified_task_or_state_blocks_before_state_change(self) -> None:
        for name in ("task.yaml", "project_state.yaml"):
            with self.subTest(name=name), tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
                base = Path(temp); target, runtime, final, install, approval = self.setup(base); before = (target / "project_state.yaml").read_bytes()
                (target / name).write_bytes((target / name).read_bytes() + b"# changed\n")
                with self.assertRaises(ValueError): activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, base / "activation.json")
                self.assertEqual(before if name == "task.yaml" else (target / name).read_bytes(), (target / "project_state.yaml").read_bytes())

    def test_loader_failure_and_internal_receipt_block_before_write(self) -> None:
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            base = Path(temp); target, runtime, final, install, approval = self.setup(base); before = (target / "project_state.yaml").read_bytes()
            with patch.object(ProjectState, "from_mapping", side_effect=ValueError("loader failed")):
                with self.assertRaisesRegex(ValueError, "loader failed"):
                    activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, base / "activation.json")
            self.assertEqual(before, (target / "project_state.yaml").read_bytes())
            with self.assertRaises(ValueError): activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, target / "activation.json")

    def test_legacy_activate_cannot_bypass_adoption_runtime(self) -> None:
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            target, _, _, _, _ = self.setup(Path(temp))
            with self.assertRaisesRegex(ValueError, "USE_ACTIVATE_APPROVED"):
                store.activate(target / "task.yaml")

    def test_context_reconstructs_approved_candidate_and_provenance(self) -> None:
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            base = Path(temp); target, runtime, final, install, approval = self.setup(base, ["src/**"])
            activation_receipt = base / "activation.json"
            activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, activation_receipt)
            context = build_lifecycle_context(
                target, target / "task.yaml", target / "project_state.yaml", install, activation_receipt,
                runtime_artifact_manifest=runtime / MANIFEST_FILENAME, final_install_approval=final,
                activation_approval=approval, confirmation=base / "activation-confirmation.yaml", plan=base / "activation-plan.json",
            )
            self.assertEqual((("python-project-tests", context.confirmed_test_candidates[0][1]),), context.confirmed_test_candidates)
            self.assertTrue(context.runtime_artifact_manifest_digest)
            changed = yaml.safe_load((base / "activation-confirmation.yaml").read_text(encoding="utf-8")); changed["scope"]["allowed_paths"] = ["other/**"]
            (base / "activation-confirmation.yaml").write_text(yaml.safe_dump(changed), encoding="utf-8")
            with self.assertRaises(ValueError):
                build_lifecycle_context(target, target / "task.yaml", target / "project_state.yaml", install, activation_receipt, runtime_artifact_manifest=runtime / MANIFEST_FILENAME, final_install_approval=final, activation_approval=approval, confirmation=base / "activation-confirmation.yaml", plan=base / "activation-plan.json")

    def test_end_to_end_python_adoption_closes(self) -> None:
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            base = Path(temp); target, runtime, final, install, approval = self.setup(base, ["src/**"])
            receipt = base / "activation.json"
            activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, receipt)
            state_path = target / "project_state.yaml"

            def context():
                return build_lifecycle_context(target, target / "task.yaml", state_path, install, receipt, runtime_artifact_manifest=runtime / MANIFEST_FILENAME, final_install_approval=final, activation_approval=approval, confirmation=base / "activation-confirmation.yaml", plan=base / "activation-plan.json")

            def evidence(name: str, evidence_type: str, status: str) -> Path:
                state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
                path = base / name
                path.write_text(json.dumps({"schema_version":"1.0", "evidence_type":evidence_type, "status":status, "target_identity_digest":context().target_identity_digest, "previous_state_digest":hashlib.sha256(state_path.read_bytes()).hexdigest(), "upstream_evidence_digests":upstream_digests(state), "payload":{}}, sort_keys=True), encoding="utf-8")
                return path

            preflight = run_adoption_preflight(context(), target / "task.yaml", state_path)
            transition_project_state(state_path, expected_current_stage="ACTIVATED_NOT_PREFLIGHTED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("preflight.json", "PreflightEvidence", "PASS"), requested_next_stage="PREFLIGHT_PASSED", target_identity_digest=context().target_identity_digest)
            contract = yaml.safe_load((target / "task.yaml").read_text(encoding="utf-8"))
            allowed = contract["write_scope"]["allow"][0].replace("**", "ok.txt")
            guard = build_guard_evidence(contract, preflight, target, [allowed])
            transition_project_state(state_path, expected_current_stage="PREFLIGHT_PASSED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("guard.json", "GuardEvidence", "PASS"), requested_next_stage="GUARDED", target_identity_digest=context().target_identity_digest)
            plan = build_adoption_test_plan(context().digest(), guard, dict(context().confirmed_test_candidates))
            transition_project_state(state_path, expected_current_stage="GUARDED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("test-plan-evidence.json", "TestPlanEvidence", "READY"), requested_next_stage="TEST_PLANNED", target_identity_digest=context().target_identity_digest)
            run = run_adoption_test_plan(target, plan)
            self.assertEqual("PASS", run["overall_status"])
            transition_project_state(state_path, expected_current_stage="TEST_PLANNED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("run.json", "TestRunEvidence", "PASS"), requested_next_stage="TEST_EXECUTED", target_identity_digest=context().target_identity_digest)
            current = context(); context_value = {**current.__dict__, "context_digest": current.digest(), "task_id": contract["task_id"]}
            verification = verify_adoption(context_value, guard, plan, run, target, current_state_path=state_path, expected_target_identity_digest=current.target_identity_digest)
            self.assertEqual("PASS", verification["status"])
            transition_project_state(state_path, expected_current_stage="TEST_EXECUTED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("verification.json", "VerificationEvidence", "PASS"), requested_next_stage="VERIFIED", target_identity_digest=current.target_identity_digest)
            closure = close_adoption(verification, target, current_state_path=state_path, expected_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), expected_target_identity_digest=current.target_identity_digest)
            self.assertTrue(closure["closed"])
            transition_project_state(state_path, expected_current_stage="VERIFIED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("closure.json", "ClosureEvidence", "CLOSED"), requested_next_stage="CLOSED", target_identity_digest=current.target_identity_digest)
            final_state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            self.assertEqual("CLOSED", final_state["lifecycle_stage"])
            self.assertFalse(closure["production_ready"])

    def test_node_generic_unicode_and_space_targets_reconstruct_and_run_confirmed_candidates(self) -> None:
        cases = (("node", "node-success"), ("generic", "generic-success"), ("generic", "中文项目"), ("generic", "project with spaces"))
        with tempfile.TemporaryDirectory(dir=R1_ROOT) as temp:
            for kind, name in cases:
                with self.subTest(kind=kind, name=name):
                    base = Path(temp) / name; base.mkdir()
                    target, runtime, final, install, approval = self.setup(base, ["src/**"], kind=kind, target_name=name)
                    receipt = base / "activation.json"
                    activate_approved(target, target / "task.yaml", target / "project_state.yaml", runtime / MANIFEST_FILENAME, final, install, approval, receipt)
                    state_path = target / "project_state.yaml"
                    def context():
                        return build_lifecycle_context(target, target / "task.yaml", state_path, install, receipt, runtime_artifact_manifest=runtime / MANIFEST_FILENAME, final_install_approval=final, activation_approval=approval, confirmation=base / "activation-confirmation.yaml", plan=base / "activation-plan.json")
                    def evidence(name: str, evidence_type: str, status: str) -> Path:
                        state = yaml.safe_load(state_path.read_text(encoding="utf-8")); path = base / name
                        path.write_text(json.dumps({"schema_version":"1.0", "evidence_type":evidence_type, "status":status, "target_identity_digest":context().target_identity_digest, "previous_state_digest":hashlib.sha256(state_path.read_bytes()).hexdigest(), "upstream_evidence_digests":upstream_digests(state), "payload":{}}, sort_keys=True), encoding="utf-8")
                        return path
                    preflight = run_adoption_preflight(context(), target / "task.yaml", state_path)
                    contract = yaml.safe_load((target / "task.yaml").read_text(encoding="utf-8"))
                    guard = build_guard_evidence(contract, preflight, target, ["src/ok.txt"])
                    transition_project_state(state_path, expected_current_stage="ACTIVATED_NOT_PREFLIGHTED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("preflight.json", "PreflightEvidence", "PASS"), requested_next_stage="PREFLIGHT_PASSED", target_identity_digest=context().target_identity_digest)
                    transition_project_state(state_path, expected_current_stage="PREFLIGHT_PASSED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("guard.json", "GuardEvidence", "PASS"), requested_next_stage="GUARDED", target_identity_digest=context().target_identity_digest)
                    plan = build_adoption_test_plan(context().digest(), guard, dict(context().confirmed_test_candidates))
                    transition_project_state(state_path, expected_current_stage="GUARDED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("test-plan-evidence.json", "TestPlanEvidence", "READY"), requested_next_stage="TEST_PLANNED", target_identity_digest=context().target_identity_digest)
                    run = run_adoption_test_plan(target, plan)
                    self.assertEqual("PASS", run["overall_status"])
                    self.assertEqual(target, (target / plan["selected"][0]["cwd"]).resolve())
                    self.assertFalse(any("npm install" in " ".join(item["argv"]) for item in plan["selected"]))
                    transition_project_state(state_path, expected_current_stage="TEST_PLANNED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("run.json", "TestRunEvidence", "PASS"), requested_next_stage="TEST_EXECUTED", target_identity_digest=context().target_identity_digest)
                    current = context(); context_value = {**current.__dict__, "context_digest": current.digest(), "task_id": contract["task_id"]}
                    verification = verify_adoption(context_value, guard, plan, run, target, current_state_path=state_path, expected_target_identity_digest=current.target_identity_digest)
                    self.assertEqual("PASS", verification["status"])
                    transition_project_state(state_path, expected_current_stage="TEST_EXECUTED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("verification.json", "VerificationEvidence", "PASS"), requested_next_stage="VERIFIED", target_identity_digest=current.target_identity_digest)
                    closure = close_adoption(verification, target, current_state_path=state_path, expected_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), expected_target_identity_digest=current.target_identity_digest)
                    transition_project_state(state_path, expected_current_stage="VERIFIED", expected_current_state_digest=hashlib.sha256(state_path.read_bytes()).hexdigest(), evidence_path=evidence("closure.json", "ClosureEvidence", "CLOSED"), requested_next_stage="CLOSED", target_identity_digest=current.target_identity_digest)
                    self.assertTrue(closure["closed"])
                    self.assertEqual("CLOSED", yaml.safe_load(state_path.read_text(encoding="utf-8"))["lifecycle_stage"])


if __name__ == "__main__":
    unittest.main()
