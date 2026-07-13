"""Build schema-compatible TaskContract mappings from deterministic decisions."""

from ..models.task_request import TaskRequest
from .gate_resolver import GateDecision
from .scope_resolver import Scope


def build_contract(task: TaskRequest, project_mode: str, task_level: str, gate: GateDecision, scope: Scope) -> dict:
    architecture_change = task_level == "C" and "architecture" in task.text
    return {
        "schema_version": "1.0", "task_id": task.task_id, "project_mode": project_mode, "task_level": task_level, "status": gate.status,
        "objective": [task.title], "read_scope": list(scope.read_scope), "write_scope": scope.write_scope,
        "autonomy": {"may_debug_test_failures": True, "may_edit_adjacent_tests": True, "may_edit_same_module_helpers": "conditional", "must_not_expand_architecture": not architecture_change},
        "stop_conditions": list(gate.stop_conditions), "verification": {"level_1": [], "level_2": [], "level_3": []},
        "report": {"format": "compact", "fields": ["modified_files", "core_changes", "tests", "risks"]},
    }
