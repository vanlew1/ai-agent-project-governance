from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from governance.adoption import build_plan, export_drafts
from governance.adoption.exporter import _digest


class AgentAdoptExportTest(unittest.TestCase):
    def target(self, root: Path, kind: str = "python") -> None:
        (root / "AGENTS.md").write_text("Local scope only.\n", encoding="utf-8")
        if kind == "python":
            (root / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_sentinel.py").write_text("raise RuntimeError('must not run')\n", encoding="utf-8")
        elif kind == "node":
            (root / "package.json").write_text('{"scripts":{"test":"node --test"}}', encoding="utf-8")

    def confirmation(self, plan: dict[str, object]) -> dict[str, object]:
        candidate = plan["test_candidates"][0] if plan["test_candidates"] else None
        scope = plan["scope_candidates"][0]
        return {
            "schema_version": "1.0",
            "plan_digest": plan["plan_digest"],
            "confirmed_by_user": True,
            "preset": {"selected": plan["preset_recommendation"]["recommendation"], "confirmed": True},
            "scope": {"allowed_paths": scope["allowed_paths"], "denied_paths": scope["denied_paths"], "confirmed": True},
            "test_selection": {"candidate_id": candidate["candidate_id"] if candidate else None, "confirmed": True},
            "autonomy": {"level": "constrained", "confirmed": True},
            "blocked_decisions": {name: "BLOCKED" for name in (
                "production_data", "external_api", "git_write", "release", "state_activation", "security_bypass", "business_semantic_change"
            )},
        }

    def write_inputs(self, base: Path, plan: dict[str, object], confirmation: dict[str, object]) -> tuple[Path, Path]:
        plan_path = base / "plan.json"
        confirmation_path = base / "confirmation.yaml"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        confirmation_path.write_text(yaml.safe_dump(confirmation, sort_keys=False), encoding="utf-8")
        return plan_path, confirmation_path

    def test_export_writes_only_external_untrusted_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "中文 target with spaces"
            target.mkdir()
            self.target(target)
            before = sorted(path.relative_to(target).as_posix() for path in target.rglob("*"))
            plan = build_plan(target)
            plan_path, confirmation_path = self.write_inputs(base, plan, self.confirmation(plan))
            output = base / "drafts"
            export_drafts(plan_path, confirmation_path, output, target)
            self.assertEqual(before, sorted(path.relative_to(target).as_posix() for path in target.rglob("*")))
            self.assertEqual({"task.yaml.draft", "project_state.yaml.draft", "ADOPTION_CONFIRMATION_SUMMARY.md", "EXPORT_MANIFEST.json"}, {path.name for path in output.iterdir()})
            self.assertIn("UNTRUSTED_DRAFT", (output / "task.yaml.draft").read_text(encoding="utf-8"))
            self.assertIn("NOT_ACTIVATED", (output / "project_state.yaml.draft").read_text(encoding="utf-8"))
            manifest = json.loads((output / "EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["installed"])
            self.assertFalse(manifest["tests_executed"])

    def test_rejects_mismatched_confirmation_and_blocked_decision_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            self.target(target)
            plan = build_plan(target)
            confirmation = self.confirmation(plan)
            confirmation["plan_digest"] = "0" * 64
            plan_path, confirmation_path = self.write_inputs(base, plan, confirmation)
            with self.assertRaisesRegex(ValueError, "digest"):
                export_drafts(plan_path, confirmation_path, base / "drafts", target)
            confirmation = self.confirmation(plan)
            confirmation["blocked_decisions"]["git_write"] = "ALLOWED"
            _, confirmation_path = self.write_inputs(base, plan, confirmation)
            with self.assertRaisesRegex(Exception, "BLOCKED"):
                export_drafts(plan_path, confirmation_path, base / "drafts", target)

    def test_rejects_internal_and_symlinked_output_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            self.target(target)
            plan = build_plan(target)
            plan_path, confirmation_path = self.write_inputs(base, plan, self.confirmation(plan))
            with self.assertRaisesRegex(ValueError, "outside"):
                export_drafts(plan_path, confirmation_path, target / "drafts", target)
            linked = base / "linked"
            linked.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "outside"):
                export_drafts(plan_path, confirmation_path, linked / "drafts", target)

    def test_export_rejects_different_target_project_without_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            first = base / "first"
            second = base / "second"
            first.mkdir()
            second.mkdir()
            self.target(first)
            self.target(second)
            plan = build_plan(first)
            plan_path, confirmation_path = self.write_inputs(base, plan, self.confirmation(plan))
            output = base / "drafts"
            with self.assertRaisesRegex(ValueError, "target identity"):
                export_drafts(plan_path, confirmation_path, output, second)
            self.assertFalse(output.exists())

    def test_export_accepts_same_canonical_target_via_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            self.target(target)
            alias = base / "alias"
            alias.symlink_to(target, target_is_directory=True)
            plan = build_plan(target)
            plan_path, confirmation_path = self.write_inputs(base, plan, self.confirmation(plan))
            export_drafts(plan_path, confirmation_path, base / "drafts", alias)

    def test_target_identity_is_private_and_stable_for_business_file_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()
            self.target(target)
            first = build_plan(target)["target_identity"]
            (target / "src.py").write_text("print('ordinary change')\n", encoding="utf-8")
            second = build_plan(target)["target_identity"]
            self.assertEqual(first, second)
            self.assertNotIn(str(target), json.dumps(first))

    def test_target_identity_changes_for_key_marker_without_leaking_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()
            self.target(target)
            first = build_plan(target)["target_identity"]
            (target / "pyproject.toml").write_text("[project]\nname='changed'\nsecret='token-value'\n", encoding="utf-8")
            second = build_plan(target)["target_identity"]
            self.assertNotEqual(first, second)
            self.assertNotIn("token-value", json.dumps(second))

    def test_duplicate_test_candidate_ids_are_rejected_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            self.target(target)
            plan = build_plan(target)
            original = plan["test_candidates"][0]
            duplicate = dict(original, command="different command")
            plan["test_candidates"] = [original, duplicate]
            plan["plan_digest"] = _digest(plan, "plan_digest")
            confirmation = self.confirmation(plan)
            plan_path, confirmation_path = self.write_inputs(base, plan, confirmation)
            output = base / "drafts"
            with self.assertRaisesRegex(ValueError, "duplicate test candidate ID"):
                export_drafts(plan_path, confirmation_path, output, target)
            self.assertFalse(output.exists())

    def test_tampered_candidate_id_variants_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            self.target(target)
            for variant in ("TEST-PYTHON3", " test-python3", "test-python3 ", "ｅｓｔ-python3"):
                plan = build_plan(target)
                plan["test_candidates"][0]["candidate_id"] = variant
                plan["plan_digest"] = _digest(plan, "plan_digest")
                plan_path, confirmation_path = self.write_inputs(base, plan, self.confirmation(plan))
                with self.assertRaises(Exception):
                    export_drafts(plan_path, confirmation_path, base / "drafts", target)

    def test_canary_exports_python_node_generic_and_non_git_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            inputs = base / "inputs"
            inputs.mkdir()
            for name, kind in (("python", "python"), ("node", "node"), ("generic", "generic"), ("non-git", "generic")):
                target = base / name
                target.mkdir()
                self.target(target, kind)
                plan = build_plan(target)
                plan_path, confirmation_path = self.write_inputs(inputs, plan, self.confirmation(plan))
                export_drafts(plan_path, confirmation_path, base / f"{name}-drafts", target)
                self.assertFalse((target / ".agent_state").exists())


if __name__ == "__main__":
    unittest.main()
