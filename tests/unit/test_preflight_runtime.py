from __future__ import annotations

import unittest
from pathlib import Path

from governance.preflight.engine import run_preflight
from governance.schema_loader import load_mapping


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "preflight"


def load(name: str) -> dict:
    return load_mapping(FIXTURES / name)


class PreflightRuntimeTest(unittest.TestCase):
    def preflight(self, task: str, state: str = "project_state_execution.yaml"):
        return run_preflight(load(task), load(state))

    def test_safe_patch_is_ready_and_stable(self) -> None:
        first = self.preflight("task_safe_patch.yaml")
        second = self.preflight("task_safe_patch.yaml")
        self.assertEqual(0, first.exit_status)
        self.assertEqual("READY", first.contract.status)
        self.assertEqual(first.contract.to_mapping(), second.contract.to_mapping())

    def test_architecture_is_c_but_not_blocked(self) -> None:
        result = self.preflight("task_architecture.yaml")
        self.assertEqual(("C", "READY", 0), (result.classification.task_level, result.contract.status, result.exit_status))

    def test_high_risks_block_and_missing_scope_drafts(self) -> None:
        for task in ("task_external_api.yaml", "task_production_write.yaml"):
            result = self.preflight(task)
            self.assertEqual(("BLOCKED", 3), (result.contract.status, result.exit_status))
        result = self.preflight("task_missing_scope.yaml")
        self.assertEqual(("DRAFT", 2, []), (result.contract.status, result.exit_status, result.contract.write_scope["allow"]))

    def test_non_execution_code_task_is_draft(self) -> None:
        result = self.preflight("task_safe_patch.yaml", "project_state_discovery.yaml")
        self.assertEqual(("DRAFT", []), (result.contract.status, result.contract.write_scope["allow"]))

    def test_test_failure_text_is_not_a_blocker(self) -> None:
        task = load("task_safe_patch.yaml")
        task["title"] = "Fix failing test"
        task["description"] = "A test failed; fix it locally."
        result = run_preflight(task, load("project_state_execution.yaml"))
        self.assertEqual("READY", result.contract.status)


    def test_governance_levels_are_deterministic_and_backward_compatible(self) -> None:
        task = load("task_safe_patch.yaml")
        task["governance_context"] = {"project_event": "first_takeover"}
        result = run_preflight(task, load("project_state_execution.yaml"))
        self.assertEqual("LEVEL_1_PROJECT_INITIALIZATION", result.contract.governance["level"])
        self.assertIn("task_goal", result.contract.governance["confirmation_fields"])
        ordinary = self.preflight("task_safe_patch.yaml")
        self.assertEqual("LEVEL_2_TASK", ordinary.contract.governance["level"])

    def test_unknown_risk_fails_closed(self) -> None:
        task = load("task_safe_patch.yaml")
        task["governance_context"] = {"risk_status": "unknown"}
        result = run_preflight(task, load("project_state_execution.yaml"))
        self.assertEqual(("BLOCKED", 3), (result.contract.status, result.exit_status))
        self.assertIn("risk_or_scope_unclear", result.contract.stop_conditions)


if __name__ == "__main__":
    unittest.main()
