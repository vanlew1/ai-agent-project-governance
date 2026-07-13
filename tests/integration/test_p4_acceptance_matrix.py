from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from governance.adapters.detection import detect_adapters
from governance.adapters.registry import get
from governance.guards.scope_guard import check as guard_check
from governance.verification.test_planner import adapter_command_ids


class P4AcceptanceMatrix(unittest.TestCase):
    def project(self, files: dict[str, str]):
        context = tempfile.TemporaryDirectory()
        root = Path(context.name)
        for name, content in files.items():
            path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")
        return context, root

    def test_generic_fallback_has_no_commands(self):
        temp, root = self.project({})
        self.assertEqual("FALLBACK", detect_adapters(root).status)
        self.assertEqual((), adapter_command_ids(root, ("generic",)))
        temp.cleanup()

    def test_python_evidence(self):
        temp, root = self.project({"pyproject.toml": "[project]\nname='x'"})
        self.assertEqual("python", detect_adapters(root).primary_adapter)
        self.assertIn("python-pytest", adapter_command_ids(root, ("python",)))
        temp.cleanup()

    def test_node_evidence_and_allowed_script(self):
        temp, root = self.project({"package.json": '{"scripts":{"test":"node a.js","lint":"eslint ."}}'})
        self.assertEqual("node", detect_adapters(root).primary_adapter)
        self.assertEqual(("node-npm-test", "node-npm-lint"), adapter_command_ids(root, ("node",)))
        temp.cleanup()

    def test_damaged_package_json_is_safe(self):
        temp, root = self.project({"package.json": "{"})
        self.assertEqual((), adapter_command_ids(root, ("node",)))
        temp.cleanup()

    def test_miniprogram_and_node_auxiliary(self):
        temp, root = self.project({"project.config.json": "{}", "package.json": '{"scripts":{"test":"x"}}'})
        result = detect_adapters(root)
        self.assertEqual(("node",), result.auxiliary_adapters)
        self.assertEqual("wechat_miniprogram", result.primary_adapter)
        temp.cleanup()

    def test_python_node_is_mixed(self):
        temp, root = self.project({"pyproject.toml": "[project]", "package.json": "{}"})
        self.assertEqual("MIXED", detect_adapters(root).status)
        temp.cleanup()

    def test_adapter_guard_paths(self):
        contract = {"write_scope": {"allow": ["src/**"], "deny": ["private/**"]}}
        adapter = get("python")
        groups = guard_check(contract, [".env", "__pycache__/x.pyc", "tests/test_x.py", "private/x"], adapter.sensitive_path_patterns(), adapter.generated_path_patterns(), adapter.test_patterns())
        self.assertEqual([".env", "private/x"], groups["denied_changes"])
        self.assertEqual(["tests/test_x.py"], groups["conditional_changes"])
