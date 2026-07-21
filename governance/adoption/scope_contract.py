"""Canonical governed-scope contract shared by every adoption boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from governance.adoption.io import raw_and_normalized_digests
from governance.schema_loader import load_mapping, validate_mapping


SCOPE_FIELDS = (
    "task_id",
    "task_goal",
    "execution_mode",
    "allowed_paths",
    "denied_paths",
    "known_safe_commands",
    "network_policy",
    "data_write_policy",
    "git_policy",
    "owner_confirmed_empty_scope",
)


def _path_is_safe(value: str) -> bool:
    path = PurePosixPath(value.replace("\\", "/"))
    return bool(value.strip()) and not path.is_absolute() and ".." not in path.parts


def canonical_scope(value: Mapping[str, Any], *, source: str) -> dict[str, Any]:
    candidate = {name: value.get(name, False if name == "owner_confirmed_empty_scope" else None) for name in SCOPE_FIELDS}
    validate_mapping(candidate, "adoption_scope_input.schema.json")
    allowed = list(candidate["allowed_paths"])
    denied = list(candidate["denied_paths"])
    commands = list(candidate["known_safe_commands"])
    if len(allowed) != len(set(allowed)) or len(denied) != len(set(denied)) or len(commands) != len(set(commands)):
        raise ValueError(f"SCOPE_CONTRACT_MISMATCH: duplicate scope value in {source}")
    if any(not _path_is_safe(item) for item in allowed + denied):
        raise ValueError(f"SCOPE_CONTRACT_MISMATCH: unsafe path in {source}")
    if set(allowed) & set(denied):
        raise ValueError(f"SCOPE_CONTRACT_MISMATCH: allowed and denied paths overlap in {source}")
    mode = candidate["execution_mode"]
    owner_confirmed_empty = candidate["owner_confirmed_empty_scope"] is True
    if mode == "ACTIVE_DEVELOPMENT" and not allowed:
        raise ValueError("EMPTY_ALLOWED_SCOPE_REQUIRES_EXPLICIT_OBSERVATION_MODE")
    if mode == "OBSERVATION_ONLY" and (allowed or not owner_confirmed_empty):
        raise ValueError("EMPTY_ALLOWED_SCOPE_REQUIRES_EXPLICIT_OBSERVATION_MODE")
    candidate["allowed_paths"] = sorted(allowed)
    candidate["denied_paths"] = sorted(denied)
    candidate["known_safe_commands"] = commands
    return candidate


def load_formal_scope(path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    raw = path.read_bytes()
    scope = canonical_scope(load_mapping(path), source="formal scope input")
    return scope, raw_and_normalized_digests(raw)


def scope_digest(value: Mapping[str, Any]) -> str:
    scope = canonical_scope(value, source="scope digest")
    payload = json.dumps(scope, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def assert_scope_equal(expected: Mapping[str, Any], actual: Mapping[str, Any], *, boundary: str) -> dict[str, Any]:
    left = canonical_scope(expected, source="canonical scope")
    right = canonical_scope(actual, source=boundary)
    if left != right:
        raise ValueError(f"SCOPE_CONTRACT_MISMATCH: {boundary}")
    return right


def validate_plan_scope(plan: Mapping[str, Any], *, require_formal: bool) -> dict[str, Any] | None:
    scope = plan.get("scope_contract")
    if scope is None:
        if require_formal:
            raise ValueError("FORMAL_SCOPE_FLOW_ONLY: --scope-file is required")
        return None
    canonical = canonical_scope(scope, source="plan.scope_contract")
    task = plan.get("task_draft", {})
    assert_scope_equal(canonical, task.get("scope_contract", {}), boundary="plan.task_draft")
    candidates = plan.get("scope_candidates", [])
    if len(candidates) != 1:
        raise ValueError("SCOPE_CONTRACT_MISMATCH: plan must contain exactly one formal scope candidate")
    assert_scope_equal(canonical, candidates[0].get("scope_contract", {}), boundary="selected scope candidate")
    if task.get("task_id") != canonical["task_id"] or task.get("objective") != canonical["task_goal"]:
        raise ValueError("SCOPE_CONTRACT_MISMATCH: task identity")
    if task.get("write_scope") != {"allow": canonical["allowed_paths"], "deny": canonical["denied_paths"]}:
        raise ValueError("SCOPE_CONTRACT_MISMATCH: task write scope")
    if plan.get("project_state_draft", {}).get("execution_mode") != canonical["execution_mode"]:
        raise ValueError("SCOPE_CONTRACT_MISMATCH: project execution mode")
    return canonical

