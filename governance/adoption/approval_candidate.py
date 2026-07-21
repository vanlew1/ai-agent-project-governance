"""Create an unapproved installation candidate bound to exact preview bytes."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from governance.adoption.exporter import _digest, _validate_confirmation, _validate_plan
from governance.adoption.io import write_yaml_exclusive
from governance.adoption.planner import target_identity
from governance.adoption.runtime_artifact_compiler import MANIFEST_FILENAME, canonical_digest, compiler_identity
from governance.adoption.scope_contract import assert_scope_equal, scope_digest
from governance.adoption.writeset import load_and_validate_sidecars
from governance.schema_loader import load_mapping, validate_mapping


BLOCKED = ("state_activation", "test_execution", "git_write", "network_access", "production_data", "external_api", "release", "security_bypass", "business_semantic_change")


def build_approval_candidate(
    *, plan_path: Path, confirmation_path: Path, draft_bundle: Path,
    runtime_bundle: Path, target_root: Path,
) -> dict[str, Any]:
    target = target_root.expanduser().resolve(strict=True)
    plan, confirmation = load_mapping(plan_path), load_mapping(confirmation_path)
    scope = _validate_plan(plan, target_root=target)
    _validate_confirmation(plan, confirmation)
    assert_scope_equal(scope, confirmation["scope_contract"], boundary="approval candidate confirmation")
    if plan["target_identity"] != target_identity(target):
        raise ValueError("target identity mismatch")
    export_manifest = load_mapping(draft_bundle / "EXPORT_MANIFEST.json")
    runtime_manifest = load_mapping(runtime_bundle / MANIFEST_FILENAME)
    validate_mapping(runtime_manifest, "runtime_artifact_manifest.schema.json")
    if runtime_manifest["manifest_digest"] != canonical_digest(runtime_manifest, "manifest_digest"):
        raise ValueError("runtime artifact manifest digest mismatch")
    if export_manifest.get("plan_digest") != plan["plan_digest"] or export_manifest.get("confirmation_digest") != _digest(confirmation, omitted_keys=()):
        raise ValueError("export manifest provenance mismatch")
    if runtime_manifest["export_manifest_digest"] != canonical_digest(export_manifest):
        raise ValueError("runtime export-manifest binding mismatch")
    sidecars = load_and_validate_sidecars(runtime_bundle)
    writeset = sidecars["INSTALL_WRITESET.json"]
    expected_sidecars = {
        "INSTALL_WRITESET.json": writeset["writeset_digest"],
        "PRE_INSTALL_HASHES.json": sidecars["PRE_INSTALL_HASHES.json"]["pre_install_hashes_digest"],
        "ROLLBACK_MANIFEST.json": sidecars["ROLLBACK_MANIFEST.json"]["rollback_manifest_digest"],
    }
    if runtime_manifest["sidecar_digests"] != expected_sidecars:
        raise ValueError("runtime manifest sidecar binding mismatch")
    if writeset["scope_contract_digest"] != scope_digest(scope):
        raise ValueError("SCOPE_CONTRACT_MISMATCH: approval candidate writeset")
    artifacts = {item["artifact_type"]: item for item in runtime_manifest["runtime_artifacts"]}
    value = {
        "schema_version": "1.0",
        "target_identity_digest": plan["target_identity"]["identity_digest"],
        "plan_digest": plan["plan_digest"],
        "confirmation_digest": _digest(confirmation, omitted_keys=()),
        "export_manifest_digest": canonical_digest(export_manifest),
        "runtime_artifact_manifest_digest": runtime_manifest["manifest_digest"],
        "provenance_receipt_digest": plan["provenance_receipt"]["provenance_receipt_digest"],
        "scope_contract": scope,
        "scope_contract_digest": scope_digest(scope),
        "writeset_digest": writeset["writeset_digest"],
        "pre_install_hashes_digest": sidecars["PRE_INSTALL_HASHES.json"]["pre_install_hashes_digest"],
        "rollback_manifest_digest": sidecars["ROLLBACK_MANIFEST.json"]["rollback_manifest_digest"],
        "compiler": compiler_identity(),
        "runtime_artifacts": {
            "task_contract": {"sha256": artifacts["TASK_CONTRACT"]["sha256"]},
            "project_state": {"sha256": artifacts["PROJECT_STATE"]["sha256"]},
        },
        "approved_by_user": False,
        "install_approved": False,
        "activate_approved": False,
        "approved_action": "NONE",
        "approved_files": writeset["classifications"]["CREATE"],
        "conflict_policy": "FAIL_ON_EXISTING",
        "rollback_on_failure": True,
        "blocked_decisions": {name: "BLOCKED" for name in BLOCKED},
    }
    validate_mapping(value, "adoption_approval_candidate.schema.json")
    return value


def write_approval_candidate(output: Path, value: dict[str, Any]) -> None:
    write_yaml_exclusive(output, value)


def approve_install_candidate(candidate_path: Path) -> dict[str, Any]:
    """Apply an explicit caller-supplied Owner decision without changing bound fields."""
    candidate = load_mapping(candidate_path)
    validate_mapping(candidate, "adoption_approval_candidate.schema.json")
    approval = dict(candidate)
    approval["approved_by_user"] = True
    approval["install_approved"] = True
    approval["approved_action"] = "INSTALL_NEW_FILES_ONLY"
    validate_mapping(approval, "adoption_final_approval.schema.json")
    return approval
