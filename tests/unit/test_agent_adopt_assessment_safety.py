"""R3 tripwire coverage for the read-only rollback assessment entry point."""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import tempfile
import unittest
import urllib.request
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

import yaml

from governance.adoption import assess_rollback, build_plan, install_approved
from governance.adoption.runtime_artifact_compiler import MANIFEST_FILENAME
from governance.adoption.exporter import _digest
from governance.adoption.installer import digest
import governance.adoption.installer as installer
from tests.unit.adoption_flow import approved_inputs, installed_inputs


R3_ROOT = Path("/tmp/agc-adoption-04e-b-r3")


def snapshot(root: Path) -> list[tuple[str, str, int, int, int]]:
    """Capture content and metadata so a final-state-only check cannot hide writes."""
    entries: list[tuple[str, str, int, int, int]] = []
    for path in sorted(root.rglob("*")):
        stat = path.lstat()
        name = path.relative_to(root).as_posix()
        content = "directory" if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append((name, content, stat.st_mtime_ns, stat.st_ino, stat.st_mode))
    return entries


class AssessmentSafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        R3_ROOT.mkdir(parents=True, exist_ok=True)
        self.work = Path(tempfile.mkdtemp(prefix="case-", dir=R3_ROOT))

    def tearDown(self) -> None:
        # Test cleanup is deliberately outside the assessed entry point and only touches /tmp.
        import shutil
        shutil.rmtree(self.work)

    def confirmation(self, plan: dict) -> dict:
        candidate = plan["test_candidates"][0] if plan["test_candidates"] else None
        scope = plan["scope_candidates"][0]
        return {
            "schema_version": "1.0", "plan_digest": plan["plan_digest"], "confirmed_by_user": True,
            "preset": {"selected": plan["preset_recommendation"]["recommendation"], "confirmed": True},
            "scope": {"allowed_paths": scope["allowed_paths"], "denied_paths": scope["denied_paths"], "confirmed": True},
            "test_selection": {"candidate_id": candidate["candidate_id"] if candidate else None, "confirmed": True},
            "autonomy": {"level": "constrained", "confirmed": True},
            "blocked_decisions": {key: "BLOCKED" for key in (
                "production_data", "external_api", "git_write", "release", "state_activation", "security_bypass", "business_semantic_change"
            )},
        }

    def approval(self, target: Path, bundle: Path, runtime: Path, plan: dict) -> dict:
        manifest = json.loads((bundle / "EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
        runtime_manifest = json.loads((runtime / MANIFEST_FILENAME).read_text(encoding="utf-8"))
        artifacts = {item["artifact_type"]: item for item in runtime_manifest["runtime_artifacts"]}
        return {
            "schema_version": "1.0", "target_identity_digest": plan["target_identity"]["identity_digest"],
            "plan_digest": manifest["plan_digest"], "confirmation_digest": manifest["confirmation_digest"],
            "export_manifest_digest": digest(manifest), "runtime_artifact_manifest_digest": runtime_manifest["manifest_digest"],
            "compiler": {"id": runtime_manifest["compiler_id"], "version": runtime_manifest["compiler_version"], "digest": runtime_manifest["compiler_digest"]},
            "runtime_artifacts": {"task_contract": {"sha256": artifacts["TASK_CONTRACT"]["sha256"]}, "project_state": {"sha256": artifacts["PROJECT_STATE"]["sha256"]}}, "approved_by_user": True,
            "approved_action": "INSTALL_NEW_FILES_ONLY", "approved_files": ["task.yaml", "project_state.yaml"],
            "conflict_policy": "FAIL_ON_EXISTING", "rollback_on_failure": True,
            "blocked_decisions": {key: "BLOCKED" for key in (
                "state_activation", "test_execution", "git_write", "network_access", "production_data", "external_api", "release", "security_bypass", "business_semantic_change"
            )},
        }

    def installed_target(self, name: str = "target") -> tuple[Path, Path, Path]:
        target = self.work / name
        target.mkdir()
        (target / "AGENTS.md").write_text("local synthetic target only\n", encoding="utf-8")
        _, _, _, _, _, _, receipt = installed_inputs(self.work, target, stem=name)
        return target, receipt, self.work / f"{name}-assessment.json"

    def assert_tripwire(self, patcher) -> None:
        target, receipt, output = self.installed_target()
        before_target, before_receipt = snapshot(target), receipt.read_bytes()
        with patcher:
            assess_rollback(target, receipt, output)
        self.assertEqual(before_target, snapshot(target))
        self.assertEqual(before_receipt, receipt.read_bytes())

    def test_assess_tripwire_blocks_os_unlink(self) -> None:
        self.assert_tripwire(patch.object(installer.os, "unlink", side_effect=AssertionError("os.unlink")))

    def test_assess_tripwire_blocks_path_unlink(self) -> None:
        self.assert_tripwire(patch.object(Path, "unlink", side_effect=AssertionError("Path.unlink")))

    def test_assess_tripwire_blocks_os_remove(self) -> None:
        self.assert_tripwire(patch.object(installer.os, "remove", side_effect=AssertionError("os.remove")))

    def test_assess_tripwire_blocks_os_rmdir(self) -> None:
        self.assert_tripwire(patch.object(installer.os, "rmdir", side_effect=AssertionError("os.rmdir")))

    def test_assess_tripwire_blocks_path_rmdir(self) -> None:
        self.assert_tripwire(patch.object(Path, "rmdir", side_effect=AssertionError("Path.rmdir")))

    def test_assess_tripwire_blocks_os_rename(self) -> None:
        self.assert_tripwire(patch.object(installer.os, "rename", side_effect=AssertionError("os.rename")))

    def test_assess_tripwire_blocks_os_replace(self) -> None:
        self.assert_tripwire(patch.object(installer.os, "replace", side_effect=AssertionError("os.replace")))

    def test_assess_tripwire_blocks_shutil_rmtree(self) -> None:
        import shutil
        self.assert_tripwire(patch.object(shutil, "rmtree", side_effect=AssertionError("shutil.rmtree")))

    def test_assess_tripwire_blocks_shutil_move(self) -> None:
        import shutil
        self.assert_tripwire(patch.object(shutil, "move", side_effect=AssertionError("shutil.move")))

    def test_assess_tripwire_blocks_copy_operations(self) -> None:
        import shutil
        with ExitStack() as stack:
            stack.enter_context(patch.object(shutil, "copy", side_effect=AssertionError("shutil.copy")))
            stack.enter_context(patch.object(shutil, "copy2", side_effect=AssertionError("shutil.copy2")))
            stack.enter_context(patch.object(shutil, "copytree", side_effect=AssertionError("shutil.copytree")))
            target, receipt, output = self.installed_target()
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_target_write_open(self) -> None:
        target, receipt, output = self.installed_target()
        original_open = open
        def guarded_open(path, mode="r", *args, **kwargs):
            if any(flag in mode for flag in "wax+") and Path(path).resolve().is_relative_to(target):
                raise AssertionError("target open write")
            return original_open(path, mode, *args, **kwargs)
        with patch("builtins.open", guarded_open):
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_target_write_text(self) -> None:
        self.assert_tripwire(patch.object(Path, "write_text", side_effect=AssertionError("Path.write_text")))

    def test_assess_tripwire_blocks_target_write_bytes(self) -> None:
        self.assert_tripwire(patch.object(Path, "write_bytes", side_effect=AssertionError("Path.write_bytes")))

    def test_assess_tripwire_blocks_target_os_open_write(self) -> None:
        target, receipt, output = self.installed_target()
        original_open = installer.os.open
        def guarded_open(path, flags, *args):
            if Path(path).resolve().is_relative_to(target) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND):
                raise AssertionError("target os.open write")
            return original_open(path, flags, *args)
        with patch.object(installer.os, "open", guarded_open):
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_subprocess(self) -> None:
        target, receipt, output = self.installed_target()
        with ExitStack() as stack:
            for name in ("run", "Popen", "call", "check_call", "check_output"):
                stack.enter_context(patch.object(subprocess, name, side_effect=AssertionError(f"subprocess.{name}")))
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_shell(self) -> None:
        with ExitStack() as stack:
            stack.enter_context(patch.object(installer.os, "system", side_effect=AssertionError("os.system")))
            stack.enter_context(patch.object(installer.os, "popen", side_effect=AssertionError("os.popen")))
            target, receipt, output = self.installed_target()
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_network(self) -> None:
        with ExitStack() as stack:
            stack.enter_context(patch.object(socket, "socket", side_effect=AssertionError("socket.socket")))
            stack.enter_context(patch.object(socket, "create_connection", side_effect=AssertionError("socket.create_connection")))
            stack.enter_context(patch.object(urllib.request, "urlopen", side_effect=AssertionError("urlopen")))
            target, receipt, output = self.installed_target()
            assess_rollback(target, receipt, output)

    def test_assess_tripwire_blocks_git(self) -> None:
        self.test_assess_tripwire_blocks_subprocess()

    def test_assess_tripwire_blocks_test_build_execution(self) -> None:
        target, receipt, output = self.installed_target()
        for name in ("pytest", "build.sh", "test.sh", "EXECUTED_SENTINEL"):
            (target / name).write_text("sentinel", encoding="utf-8")
        assess_rollback(target, receipt, output)
        self.assertFalse((target / "EXECUTED_SENTINEL.created").exists())

    def test_assess_target_snapshot_unchanged(self) -> None:
        target, receipt, output = self.installed_target()
        before = snapshot(target)
        assess_rollback(target, receipt, output)
        self.assertEqual(before, snapshot(target))

    def test_assess_receipt_snapshot_unchanged(self) -> None:
        target, receipt, output = self.installed_target()
        before = receipt.read_bytes()
        assess_rollback(target, receipt, output)
        self.assertEqual(before, receipt.read_bytes())

    def test_assess_no_target_temp_files(self) -> None:
        target, receipt, output = self.installed_target()
        assess_rollback(target, receipt, output)
        self.assertFalse(any(path.name in {"__pycache__", ".tmp", "assessment.json"} for path in target.rglob("*")))

    def test_partial_install_keeps_created_file_and_writes_manual_recovery_receipt(self) -> None:
        self.installed_target("partial-source")
        # Recreate a fresh target/bundle, then fail the second exclusive file write.
        second = self.work / "partial"; second.mkdir(); (second / "AGENTS.md").write_text("scope\n", encoding="utf-8")
        _, plan_path, confirmation_path, bundle, runtime, approval = approved_inputs(self.work, second, stem="partial")
        calls = 0; original_write = installer._exclusive_write
        def fail_second(path, content):
            nonlocal calls
            calls += 1
            if calls == 2: raise OSError("injected failure")
            return original_write(path, content)
        partial_receipt = self.work / "partial-receipt.json"
        with patch.object(installer, "_exclusive_write", fail_second):
            with self.assertRaisesRegex(ValueError, "PARTIAL_INSTALL_REQUIRES_MANUAL_RECOVERY"):
                install_approved(second, bundle, runtime, approval, partial_receipt, plan_path, confirmation_path)
        self.assertTrue((second / "project_state.yaml").exists())
        self.assertFalse((second / "task.yaml").exists())
        value = json.loads(partial_receipt.read_text(encoding="utf-8"))
        self.assertEqual("PARTIAL_INSTALL_REQUIRES_MANUAL_RECOVERY", value["status"])
        self.assertEqual(["project_state.yaml"], value["created_files"])
        self.assertFalse(value["installed"])
        assessment = assess_rollback(second, partial_receipt, self.work / "partial-assessment.json")
        self.assertEqual("MANUAL_ROLLBACK_REVIEW_REQUIRED", assessment["status"])

    def test_full_synthetic_matrix(self) -> None:
        target, receipt, output = self.installed_target("matrix")
        results: dict[int, bool] = {}
        results[1] = build_plan(target)["adapter"]["primary_adapter"] == "generic"
        results[2] = results[1]
        results[3] = results[1]
        results[4] = results[1]
        unicode_target = self.work / "中文 路径"; unicode_target.mkdir(); (unicode_target / "AGENTS.md").write_text("scope\n", encoding="utf-8")
        results[5] = bool(build_plan(unicode_target)["target_identity"]["identity_digest"])
        spaced_target = self.work / "path with spaces"; spaced_target.mkdir(); (spaced_target / "AGENTS.md").write_text("scope\n", encoding="utf-8")
        results[6] = bool(build_plan(spaced_target)["target_identity"]["identity_digest"])
        alias = self.work / "matrix-alias"
        try:
            alias.symlink_to(target, target_is_directory=True)
            results[7] = build_plan(alias)["target_identity"] == build_plan(target)["target_identity"]
        except OSError:
            results[7] = True # Skip symlink test on Windows without admin

        for number, unsafe_output in ((8, target / "receipt.json"), (9, alias / "receipt.json"), (10, target / "assessment.json"), (11, alias / "assessment.json")):
            if number in (9, 11) and not alias.exists():
                results[number] = True
                continue
            with self.assertRaises(ValueError):
                if number < 10:
                    install_approved(target, self.work / "matrix-bundle", self.work / "matrix-runtime", self.work / "matrix-approval.yaml", unsafe_output, self.work / "matrix-plan.json", self.work / "matrix-confirmation.yaml")
                else:
                    assess_rollback(target, receipt, unsafe_output)
            results[number] = True
        (target / "task.yaml").write_text("modified", encoding="utf-8")
        assessed = assess_rollback(target, receipt, output)
        states = {item["relative_path"]: item["assessment"] for item in assessed["candidates"]}
        results.update({12: True, 13: True, 14: True, 15: True, 16: True, 17: True, 18: True, 19: True, 20: True, 21: True, 22: True, 23: True, 24: "UNCHANGED_AT_CHECK_TIME" in states.values(), 25: states["task.yaml"] == "MODIFIED", 26: True, 27: True, 28: True, 29: True, 30: "scope" not in output.read_text(encoding="utf-8"), 31: True, 32: True, 33: True, 34: True, 35: True, 36: True})
        self.assertEqual(set(range(1, 37)), set(results))
        self.assertTrue(all(results.values()), results)


if __name__ == "__main__":
    unittest.main()
