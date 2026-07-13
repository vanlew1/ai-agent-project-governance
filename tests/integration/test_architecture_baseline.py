from __future__ import annotations

import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


class ArchitectureBaselineTest(unittest.TestCase):
    def run_validator(self, root: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_governance.py"), "--root", str(root)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_runtime_files_and_downstream_templates_are_distinct(self) -> None:
        self.assertTrue((ROOT / "docs/GOVERNANCE_RUNTIME_ARCHITECTURE.md").is_file())
        self.assertTrue((ROOT / "docs/ARCHITECTURE.template.md").is_file())
        self.assertNotEqual(
            (ROOT / "docs/GOVERNANCE_RUNTIME_ARCHITECTURE.md").read_text(encoding="utf-8"),
            (ROOT / "docs/ARCHITECTURE.template.md").read_text(encoding="utf-8"),
        )

    def test_registry_and_rules_index_validate_and_behavior_is_disabled(self) -> None:
        registry_schema = yaml.safe_load((ROOT / "schemas/governance_module_registry.schema.json").read_text(encoding="utf-8"))
        registry = yaml.safe_load((ROOT / "docs/GOVERNANCE_RUNTIME_MODULE_REGISTRY.yaml").read_text(encoding="utf-8"))
        Draft202012Validator(registry_schema).validate(registry)
        rules = yaml.safe_load((ROOT / "agent_rules/RULES_INDEX.yaml").read_text(encoding="utf-8"))
        self.assertTrue(rules["governance_runtime"]["runtime_behavior_enabled"])
        self.assertTrue(rules["governance_runtime"]["preflight_enabled"])
        self.assertTrue(rules["governance_runtime"]["state_persistence_enabled"])
        self.assertTrue(rules["governance_runtime"]["scope_enforcement_enabled"])

    def test_package_import_has_no_runtime_behavior(self) -> None:
        sys.dont_write_bytecode = True
        governance = importlib.import_module("governance")
        self.assertEqual("PHASE_1_MINIMUM_RUNTIME", governance.RUNTIME_PHASE)
        self.assertTrue(governance.RUNTIME_BEHAVIOR_ENABLED)

    def test_validator_succeeds_and_missing_baseline_fails(self) -> None:
        success = self.run_validator()
        self.assertEqual(0, success.returncode, success.stdout + success.stderr)
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            failure = self.run_validator(Path(directory))
        self.assertNotEqual(0, failure.returncode)
        self.assertIn("Required baseline file missing", failure.stdout)

    def test_initializer_retains_template_rename_behavior(self) -> None:
        initializer = (ROOT / "scripts/init_new_project.py").read_text(encoding="utf-8")
        self.assertIn('rglob("*.template.*")', initializer)
        self.assertNotIn("GOVERNANCE_RUNTIME", initializer)


if __name__ == "__main__":
    unittest.main()
