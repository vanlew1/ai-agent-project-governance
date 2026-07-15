from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from governance.adoption import assess_rollback, build_plan, compile_runtime_bundle, export_drafts, install_approved, rollback_install
from governance.adoption.exporter import _digest
from governance.adoption.installer import digest
from governance.adoption.runtime_artifact_compiler import MANIFEST_FILENAME, canonical_digest, compiler_identity
from governance.models.project_state import ProjectState
from governance.models.task_contract import TaskContract
from governance.schema_loader import load_mapping, validate_mapping


class ApprovedInstallTest(unittest.TestCase):
    blocked = ("production_data", "external_api", "git_write", "release", "state_activation", "security_bypass", "business_semantic_change")

    def confirmation(self, plan: dict) -> dict:
        candidate = plan["test_candidates"][0] if plan["test_candidates"] else None
        scope = plan["scope_candidates"][0]
        return {"schema_version":"1.0","plan_digest":plan["plan_digest"],"confirmed_by_user":True,"preset":{"selected":plan["preset_recommendation"]["recommendation"],"confirmed":True},"scope":{"allowed_paths":scope["allowed_paths"],"denied_paths":scope["denied_paths"],"confirmed":True},"test_selection":{"candidate_id":candidate["candidate_id"] if candidate else None,"confirmed":True},"autonomy":{"level":"constrained","confirmed":True},"blocked_decisions":{key:"BLOCKED" for key in self.blocked}}

    def setup(self, base: Path) -> tuple[Path, Path, Path, Path, Path, dict]:
        target = base / "target"; target.mkdir(); (target / "AGENTS.md").write_text("scope\n", encoding="utf-8")
        plan = build_plan(target); plan_path, confirmation_path = base / "plan.json", base / "confirmation.yaml"
        plan_path.write_text(json.dumps(plan), encoding="utf-8"); confirmation_path.write_text(yaml.safe_dump(self.confirmation(plan)), encoding="utf-8")
        drafts = base / "drafts"; export_drafts(plan_path, confirmation_path, drafts, target)
        runtime = base / "runtime"; compile_runtime_bundle(plan_path, confirmation_path, drafts, runtime, target)
        return target, drafts, runtime, plan_path, confirmation_path, plan

    def approval(self, target: Path, drafts: Path, runtime: Path, plan: dict) -> dict:
        export_manifest = json.loads((drafts / "EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
        manifest = json.loads((runtime / MANIFEST_FILENAME).read_text(encoding="utf-8"))
        artifacts = {item["artifact_type"]: item for item in manifest["runtime_artifacts"]}
        return {"schema_version":"1.0","target_identity_digest":plan["target_identity"]["identity_digest"],"plan_digest":export_manifest["plan_digest"],"confirmation_digest":export_manifest["confirmation_digest"],"export_manifest_digest":digest(export_manifest),"runtime_artifact_manifest_digest":manifest["manifest_digest"],"compiler":{"id":manifest["compiler_id"],"version":manifest["compiler_version"],"digest":manifest["compiler_digest"]},"runtime_artifacts":{"task_contract":{"sha256":artifacts["TASK_CONTRACT"]["sha256"]},"project_state":{"sha256":artifacts["PROJECT_STATE"]["sha256"]}},"approved_by_user":True,"approved_action":"INSTALL_NEW_FILES_ONLY","approved_files":["task.yaml","project_state.yaml"],"conflict_policy":"FAIL_ON_EXISTING","rollback_on_failure":True,"blocked_decisions":{key:"BLOCKED" for key in ("state_activation","test_execution","git_write","network_access","production_data","external_api","release","security_bypass","business_semantic_change")}}

    def install(self, base: Path):
        target, drafts, runtime, plan_path, confirmation_path, plan = self.setup(base)
        approval_path = base / "approval.yaml"; approval_path.write_text(yaml.safe_dump(self.approval(target, drafts, runtime, plan)), encoding="utf-8")
        receipt_path = base / "receipt.json"
        result = install_approved(target, drafts, runtime, approval_path, receipt_path, plan_path, confirmation_path)
        return target, drafts, runtime, approval_path, receipt_path, plan_path, confirmation_path, result

    def test_compile_preview_is_external_deterministic_and_declared_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, drafts, runtime, plan_path, confirmation_path, _ = self.setup(base)
            self.assertEqual({"task_contract.runtime.yaml", "project_state.runtime.yaml", MANIFEST_FILENAME}, {path.name for path in runtime.iterdir()})
            self.assertFalse((target / "task.yaml").exists())
            manifest = load_mapping(runtime / MANIFEST_FILENAME)
            self.assertEqual(manifest["manifest_digest"], canonical_digest(manifest, "manifest_digest"))
            self.assertEqual(compiler_identity(), {"id": manifest["compiler_id"], "version": manifest["compiler_version"], "digest": manifest["compiler_digest"]})
            empty = base / "empty-runtime"; empty.mkdir()
            second = compile_runtime_bundle(plan_path, confirmation_path, drafts, empty, target)
            self.assertEqual(manifest["manifest_digest"], second["manifest_digest"])
            with self.assertRaisesRegex(ValueError, "empty"):
                compile_runtime_bundle(plan_path, confirmation_path, drafts, runtime, target)
            with self.assertRaisesRegex(ValueError, "outside target"):
                compile_runtime_bundle(plan_path, confirmation_path, drafts, target / "runtime", target)

    def test_install_uses_exact_approved_preview_bytes_without_compilation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, _, runtime, _, _, _, _, result = self.install(base)
            self.assertEqual((runtime / "task_contract.runtime.yaml").read_bytes(), (target / "task.yaml").read_bytes())
            self.assertEqual((runtime / "project_state.runtime.yaml").read_bytes(), (target / "project_state.yaml").read_bytes())
            self.assertEqual("INSTALLED_NOT_ACTIVATED", result["status"])
            self.assertFalse(result["activated"])

    def test_approval_and_provenance_tampering_block_before_target_write(self) -> None:
        for path_name in ("task_contract.runtime.yaml", "project_state.runtime.yaml", MANIFEST_FILENAME):
            with self.subTest(path_name=path_name), tempfile.TemporaryDirectory() as temp:
                base = Path(temp); target, _, runtime, approval, receipt, plan, confirmation, _ = self.install_inputs(base)
                path = runtime / path_name; path.write_bytes(path.read_bytes() + b"# changed\n")
                with self.assertRaises(Exception): install_approved(target, base / "drafts", runtime, approval, receipt, plan, confirmation)
                self.assertFalse((target / "task.yaml").exists())

    def install_inputs(self, base: Path):
        target, drafts, runtime, plan_path, confirmation_path, plan = self.setup(base)
        approval = base / "approval.yaml"; approval.write_text(yaml.safe_dump(self.approval(target, drafts, runtime, plan)), encoding="utf-8")
        return target, drafts, runtime, approval, base / "receipt.json", plan_path, confirmation_path, plan

    def test_legacy_approval_and_extra_bundle_file_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, drafts, runtime, approval, receipt, plan, confirmation, data = self.install_inputs(base)
            legacy = self.approval(target, drafts, runtime, data); legacy.pop("runtime_artifacts")
            approval.write_text(yaml.safe_dump(legacy), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "LEGACY_RUNTIME_ARTIFACT_APPROVAL_UNSUPPORTED"):
                install_approved(target, drafts, runtime, approval, receipt, plan, confirmation)
            approval.write_text(yaml.safe_dump(self.approval(target, drafts, runtime, data)), encoding="utf-8")
            (runtime / "extra.txt").write_text("no", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "extra"):
                install_approved(target, drafts, runtime, approval, receipt, plan, confirmation)

    def test_formal_loaders_run_before_writes_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, drafts, runtime, approval, receipt, plan, confirmation, _ = self.install_inputs(base)
            with patch.object(TaskContract, "from_mapping", side_effect=ValueError("loader failed")):
                with self.assertRaisesRegex(ValueError, "loader failed"):
                    install_approved(target, drafts, runtime, approval, receipt, plan, confirmation)
            self.assertFalse((target / "task.yaml").exists())
            with patch.object(ProjectState, "from_mapping", side_effect=ValueError("loader failed")):
                with self.assertRaisesRegex(ValueError, "loader failed"):
                    install_approved(target, drafts, runtime, approval, receipt, plan, confirmation)
            self.assertFalse((target / "project_state.yaml").exists())

    def test_existing_target_and_rollback_safety_remain(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, drafts, runtime, approval, receipt, plan, confirmation, _ = self.install_inputs(base)
            (target / "task.yaml").write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "conflict"):
                install_approved(target, drafts, runtime, approval, receipt, plan, confirmation)
            self.assertFalse((target / "project_state.yaml").exists())
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); target, _, _, _, receipt, _, _, result = self.install(base)
            with self.assertRaisesRegex(ValueError, "AUTOMATIC_ROLLBACK_UNSUPPORTED"):
                rollback_install(target, receipt)
            assessment = assess_rollback(target, receipt, base / "assessment.json")
            self.assertEqual("MANUAL_ROLLBACK_REVIEW_REQUIRED", assessment["status"])


if __name__ == "__main__":
    unittest.main()
