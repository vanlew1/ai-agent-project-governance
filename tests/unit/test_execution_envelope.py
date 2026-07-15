from __future__ import annotations

import unittest

from governance.policy.execution_envelope import (
    classify_blocker,
    confirmation_requirement,
    governance_level,
    inherits_authorization,
)
from governance.verification.evidence import build_test_evidence


class ExecutionEnvelopeTest(unittest.TestCase):
    def test_governance_levels_and_confirmation_requirements(self) -> None:
        self.assertEqual("LEVEL_1_PROJECT_INITIALIZATION", governance_level({"project_event": "first_takeover"}))
        self.assertEqual("LEVEL_2_TASK", governance_level({"project_event": "ordinary_task"}))
        self.assertEqual("LEVEL_3_HIGH_RISK", governance_level({}, ("external",)))
        self.assertEqual(("task_goal", "allowed_scope", "forbidden_scope", "required_tests", "report_path"), confirmation_requirement("LEVEL_2_TASK"))
        self.assertIn("confirmed_by", confirmation_requirement("LEVEL_3_HIGH_RISK"))

    def test_recoverable_and_hard_blockers_are_closed(self) -> None:
        for action in ("fixture", "test_helper", "basetemp", "test_report", "test_marker", "test_network_isolation", "test_extension"):
            self.assertTrue(classify_blocker(action, {}).may_continue, action)
        self.assertTrue(classify_blocker("local_dependency", {"local_dependency_available": True}).may_continue)
        for action in ("network_download", "external_api", "production_write", "protected_asset", "production_registry", "production_semantics", "destructive_operation", "product_decision"):
            self.assertEqual("HARD_BLOCKER", classify_blocker(action, {}).classification, action)
        self.assertEqual("HARD_BLOCKER", classify_blocker("fixture", {"scope_changed": True}).classification)
        self.assertEqual("HARD_BLOCKER", classify_blocker("unknown", {}).classification)

    def test_authorization_inheritance_stops_on_boundary_change(self) -> None:
        parent = {"task_id": "AGC-GOV-01", "task_goal": "governance", "allowed_scope": ["governance/"], "forbidden_scope": ["data/"], "risk_level": "B", "production_scope": "none"}
        child = {**parent, "parent_task_id": "AGC-GOV-01", "action_type": "test_report"}
        self.assertTrue(inherits_authorization(parent, child).may_continue)
        self.assertEqual("HARD_BLOCKER", inherits_authorization(parent, {**child, "risk_level": "C"}).classification)
        self.assertEqual("HARD_BLOCKER", inherits_authorization(parent, {**child, "task_goal": "different"}).classification)

    def test_end_to_end_parent_task_recovery_continues_without_new_task(self) -> None:
        parent = {
            "task_id": "AGC-GOV-01", "task_goal": "governance close", "allowed_scope": ["tests/"],
            "forbidden_scope": ["data/"], "risk_level": "B", "production_scope": "none",
        }
        for action_type in ("fixture", "test_helper", "basetemp"):
            child = {**parent, "parent_task_id": "AGC-GOV-01", "action_type": action_type}
            decision = inherits_authorization(parent, child)
            self.assertEqual("RECOVERABLE_BLOCKER", decision.classification)
            self.assertTrue(decision.may_continue)
            self.assertEqual(parent["task_id"], child["task_id"])

    def test_end_to_end_hard_blocker_ends_parent_authorization(self) -> None:
        parent = {
            "task_id": "AGC-GOV-01", "task_goal": "governance close", "allowed_scope": ["tests/"],
            "forbidden_scope": ["data/"], "risk_level": "B", "production_scope": "none",
        }
        for action_type in ("external_api", "production_write"):
            child = {**parent, "parent_task_id": "AGC-GOV-01", "action_type": action_type}
            decision = inherits_authorization(parent, child)
            self.assertEqual("HARD_BLOCKER", decision.classification)
            self.assertFalse(decision.may_continue)
            self.assertEqual("GOV-BLOCKER-001", decision.rule_id)

    def test_test_evidence_is_reproducible_and_redacts_values(self) -> None:
        evidence = build_test_evidence(
            command=["python", "-m", "pytest", "tests/unit"], working_directory=".", node_scope="tests/unit",
            marker=None, environment_variable_names=["PYTHONDONTWRITEBYTECODE"], dependency_summary={"pytest": "8.0"},
            basetemp=".tmp/pytest", counts={"collected": 2, "passed": 2, "failed": 0, "skipped": 0, "warning": 0}, failed_nodes=[],
        )
        self.assertEqual(["PYTHONDONTWRITEBYTECODE"], evidence["environment_variable_names"])
        with self.assertRaises(ValueError):
            build_test_evidence(command=["pytest"], working_directory=".", node_scope="tests", marker=None, environment_variable_names=["TOKEN=value"], dependency_summary={}, basetemp=None, counts={"collected": 0, "passed": 0, "failed": 0, "skipped": 0, "warning": 0}, failed_nodes=[])


if __name__ == "__main__":
    unittest.main()
