"""Explicit, new-files-only installation for a reviewed adoption draft bundle."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import yaml

from governance.adoption.exporter import _validate_confirmation, _validate_plan
from governance.adoption.planner import target_identity
from governance.adoption.runtime_artifact_compiler import MANIFEST_FILENAME, canonical_digest, compiler_identity, digest_bytes
from governance.models.project_state import ProjectState
from governance.models.task_contract import TaskContract
from governance.schema_loader import load_mapping, validate_mapping


INSTALLABLE_FILES = {"task.yaml": "task.yaml.draft", "project_state.yaml": "project_state.yaml.draft"}
RUNTIME_TO_TARGET = {"task_contract.runtime.yaml": "task.yaml", "project_state.runtime.yaml": "project_state.yaml"}
BLOCKED = ("state_activation", "test_execution", "git_write", "network_access", "production_data", "external_api", "release", "security_bypass", "business_semantic_change")


def digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _load_draft_bundle(bundle: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    root = bundle.expanduser().resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("draft bundle must be a real directory")
    manifest_path = root / "EXPORT_MANIFEST.json"
    manifest = load_mapping(manifest_path)
    if manifest.get("status") != "DRAFT_EXPORTED" or manifest.get("installed") is not False:
        raise ValueError("draft bundle manifest is not an uninstalled export")
    expected = {"task.yaml.draft", "project_state.yaml.draft", "ADOPTION_CONFIRMATION_SUMMARY.md", "EXPORT_MANIFEST.json"}
    if set(manifest.get("files", [])) != expected:
        raise ValueError("draft bundle file manifest is not approved for installation")
    contents: dict[str, bytes] = {}
    for final_name, draft_name in INSTALLABLE_FILES.items():
        source = root / draft_name
        if not source.is_file() or source.is_symlink():
            raise ValueError("draft bundle contains a missing or unsafe configuration draft")
        contents[final_name] = source.read_bytes()
        if manifest.get("file_hashes", {}).get(draft_name) != hashlib.sha256(contents[final_name]).hexdigest():
            raise ValueError("draft bundle hash does not match its manifest")
    if set(path.name for path in root.iterdir()) != expected:
        raise ValueError("draft bundle contains unapproved extra files")
    return manifest, contents


def _load_runtime_bundle(bundle: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    root = bundle.expanduser().resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("runtime artifact bundle must be a real directory")
    expected = set(RUNTIME_TO_TARGET) | {MANIFEST_FILENAME}
    if {path.name for path in root.iterdir()} != expected:
        raise ValueError("runtime artifact bundle contains unapproved extra files")
    manifest = load_mapping(root / MANIFEST_FILENAME)
    validate_mapping(manifest, "runtime_artifact_manifest.schema.json")
    if manifest["manifest_digest"] != canonical_digest(manifest, "manifest_digest"):
        raise ValueError("runtime artifact manifest digest does not match its contents")
    artifacts = {item["relative_path"]: item for item in manifest["runtime_artifacts"]}
    if set(artifacts) != set(RUNTIME_TO_TARGET) or len(artifacts) != 2:
        raise ValueError("runtime artifact manifest does not declare exactly two artifacts")
    contents: dict[str, bytes] = {}
    for runtime_name, target_name in RUNTIME_TO_TARGET.items():
        path = root / runtime_name
        if not path.is_file() or path.is_symlink():
            raise ValueError("runtime artifact bundle contains a missing or unsafe artifact")
        value = path.read_bytes()
        if artifacts[runtime_name]["sha256"] != digest_bytes(value):
            raise ValueError("runtime artifact bytes do not match their manifest")
        contents[target_name] = value
    return manifest, contents


def _approval(approval_path: Path, draft_manifest: dict[str, Any], runtime_manifest: dict[str, Any], target: Path) -> dict[str, Any]:
    approval = load_mapping(approval_path)
    try:
        validate_mapping(approval, "adoption_final_approval.schema.json")
    except Exception as exc:
        raise ValueError("LEGACY_RUNTIME_ARTIFACT_APPROVAL_UNSUPPORTED: RECOMPILE_AND_REAPPROVE_RUNTIME_ARTIFACTS") from exc
    if approval["target_identity_digest"] != target_identity(target)["identity_digest"]:
        raise ValueError("target identity does not match final approval")
    if approval["plan_digest"] != draft_manifest.get("plan_digest") or approval["confirmation_digest"] != draft_manifest.get("confirmation_digest"):
        raise ValueError("final approval does not match draft bundle digests")
    if approval["export_manifest_digest"] != digest(draft_manifest):
        raise ValueError("final approval does not match export manifest digest")
    if approval["runtime_artifact_manifest_digest"] != runtime_manifest["manifest_digest"]:
        raise ValueError("final approval does not match runtime artifact manifest")
    if approval["compiler"] != {"id": runtime_manifest["compiler_id"], "version": runtime_manifest["compiler_version"], "digest": runtime_manifest["compiler_digest"]}:
        raise ValueError("final approval does not match compiler identity")
    if approval["compiler"] != compiler_identity():
        raise ValueError("runtime artifact compiler identity changed: RECOMPILE_AND_REAPPROVE_RUNTIME_ARTIFACTS")
    by_type = {item["artifact_type"]: item for item in runtime_manifest["runtime_artifacts"]}
    if approval["runtime_artifacts"] != {"task_contract": {"sha256": by_type["TASK_CONTRACT"]["sha256"]}, "project_state": {"sha256": by_type["PROJECT_STATE"]["sha256"]}}:
        raise ValueError("final approval does not match exact runtime artifact bytes")
    if set(approval["blocked_decisions"]) != set(BLOCKED):
        raise ValueError("all installation blocked decisions must remain blocked")
    if set(approval["approved_files"]) != set(INSTALLABLE_FILES) or len(approval["approved_files"]) != len(INSTALLABLE_FILES):
        raise ValueError("final approval must approve exactly the bounded installation files")
    return approval


def _safe_target(root: Path, name: str) -> Path:
    if name not in INSTALLABLE_FILES or Path(name).name != name:
        raise ValueError("unsafe installation path")
    root = root.expanduser().resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("target must be a real directory")
    path = root / name
    if path.exists() or path.is_symlink():
        raise ValueError("installation conflict: target file already exists")
    return path


def _exclusive_write(path: Path, content: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        os.write(descriptor, content)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _validated_install_inputs(target_root: Path, draft_bundle: Path, runtime_artifact_bundle: Path, final_approval: Path, plan_path: Path, confirmation_path: Path) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, bytes], dict[str, Any]]:
    target = target_root.expanduser().resolve(strict=True)
    plan = load_mapping(plan_path); confirmation = load_mapping(confirmation_path)
    _validate_plan(plan); _validate_confirmation(plan, confirmation)
    if plan["target_identity"] != target_identity(target):
        raise ValueError("current target does not match original plan identity")
    draft_manifest, drafts = _load_draft_bundle(draft_bundle)
    if draft_manifest["plan_digest"] != plan["plan_digest"] or draft_manifest["confirmation_digest"] != digest(confirmation):
        raise ValueError("draft bundle provenance does not match original inputs")
    runtime_manifest, contents = _load_runtime_bundle(runtime_artifact_bundle)
    if runtime_manifest["plan_digest"] != plan["plan_digest"] or runtime_manifest["confirmation_digest"] != digest(confirmation) or runtime_manifest["export_manifest_digest"] != digest(draft_manifest):
        raise ValueError("runtime artifact bundle provenance does not match original inputs")
    if runtime_manifest["source_draft_digests"] != {name: digest_bytes(value) for name, value in sorted(drafts.items())}:
        raise ValueError("runtime artifact bundle does not bind the exact source drafts")
    approval = _approval(final_approval, draft_manifest, runtime_manifest, target)
    task, state = load_mapping(runtime_artifact_bundle / "task_contract.runtime.yaml"), load_mapping(runtime_artifact_bundle / "project_state.runtime.yaml")
    validate_mapping(task, "task_contract.schema.json")
    validate_mapping(state, "project_state.schema.json")
    TaskContract.from_mapping(task)
    ProjectState.from_mapping(state)
    return target, draft_manifest, runtime_manifest, contents, approval


def install_approved(target_root: Path, draft_bundle: Path, runtime_artifact_bundle: Path, final_approval: Path, receipt_path: Path, plan_path: Path, confirmation_path: Path) -> dict[str, Any]:
    """Install only two new config files after all validation has passed."""
    target, draft_manifest, runtime_manifest, contents, approval = _validated_install_inputs(
        target_root, draft_bundle, runtime_artifact_bundle, final_approval, plan_path, confirmation_path
    )
    receipt = {
        "schema_version": "1.0", "status": "INSTALLED_NOT_ACTIVATED",
        "target_identity_digest": target_identity(target)["identity_digest"],
        "plan_digest": draft_manifest["plan_digest"], "confirmation_digest": draft_manifest["confirmation_digest"],
        "export_manifest_digest": digest(draft_manifest), "final_approval_digest": digest(approval),
        "runtime_artifact_manifest_digest": runtime_manifest["manifest_digest"], "compiler": approval["compiler"],
        "installed": True, "activated": False, "tests_executed": False,
        "verification_completed": False, "closure_completed": False,
        "created_files": sorted(INSTALLABLE_FILES), "created_directories": [],
        "file_hashes": {name: hashlib.sha256(contents[name]).hexdigest() for name in sorted(contents)},
        "blocked_decisions": list(BLOCKED), "automatic_rollback_available": False,
        "rollback_assessment_available": True, "rollback_mode": "MANUAL_ONLY",
        "compiler_version": runtime_manifest["compiler_version"],
        "source_draft_digests": runtime_manifest["source_draft_digests"],
        "runtime_artifacts": [
            {"artifact_type": "TASK_CONTRACT", "canonical_relative_path": "task.yaml", "runtime_digest": digest_bytes(contents["task.yaml"]), "schema": "task_contract.schema.json"},
            {"artifact_type": "PROJECT_STATE", "canonical_relative_path": "project_state.yaml", "runtime_digest": digest_bytes(contents["project_state.yaml"]), "schema": "project_state.schema.json"},
        ],
    }
    validate_mapping(receipt, "adoption_installation_receipt.schema.json")
    receipt_destination = receipt_path.expanduser().resolve(strict=False)
    if receipt_destination.exists():
        raise ValueError("receipt path must be new and outside the target project")
    try:
        receipt_destination.relative_to(target)
    except ValueError:
        pass
    else:
        raise ValueError("receipt path must be new and outside the target project")
    # Establish the external receipt location before touching the target. A later
    # target-write failure can therefore always be recorded for manual recovery.
    receipt_destination.parent.mkdir(parents=True, exist_ok=True)
    paths = {name: _safe_target(target, name) for name in INSTALLABLE_FILES}
    created: list[Path] = []
    try:
        for name in sorted(paths):
            _safe_target(target, name)
            _exclusive_write(paths[name], contents[name])
            created.append(paths[name])
        with os.fdopen(os.open(receipt_destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as handle:
            json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        return receipt
    except Exception as exc:
        if created:
            partial_receipt = dict(receipt)
            partial_receipt.update({
                "status": "PARTIAL_INSTALL_REQUIRES_MANUAL_RECOVERY",
                "installed": False,
                "created_files": [path.name for path in created],
                "file_hashes": {
                    path.name: hashlib.sha256(contents[path.name]).hexdigest()
                    for path in created
                },
            })
            validate_mapping(partial_receipt, "adoption_installation_receipt.schema.json")
            try:
                with os.fdopen(os.open(receipt_destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as handle:
                    json.dump(partial_receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
                    handle.write("\n")
            except OSError:
                pass
        raise ValueError("PARTIAL_INSTALL_REQUIRES_MANUAL_RECOVERY") from exc


def rollback_install(*_: Any) -> dict[str, Any]:
    raise ValueError("AUTOMATIC_ROLLBACK_UNSUPPORTED: USE_ASSESS_ROLLBACK")


def assess_rollback(target_root: Path, receipt_path: Path, output_path: Path) -> dict[str, Any]:
    target = target_root.expanduser().resolve(strict=True); receipt = load_mapping(receipt_path)
    validate_mapping(receipt, "adoption_installation_receipt.schema.json")
    if receipt.get("compiler_version") is None or not receipt.get("runtime_artifacts"):
        raise ValueError("LEGACY_ADOPTION_DRAFT_INSTALL_UNSUPPORTED: REGENERATE_WITH_RUNTIME_ARTIFACT_COMPILER")
    runtime_digests = {item["canonical_relative_path"]: item["runtime_digest"] for item in receipt["runtime_artifacts"]}
    if set(receipt["file_hashes"]) - set(runtime_digests) or any(
        runtime_digests[name] != value for name, value in receipt["file_hashes"].items()
    ):
        raise ValueError("runtime artifact receipt digests do not match installed file digests")
    if receipt["target_identity_digest"] != target_identity(target)["identity_digest"]:
        raise ValueError("target identity does not match installation receipt")
    output = output_path.expanduser().resolve(strict=False)
    if output.exists(): raise ValueError("assessment output already exists")
    try: output.relative_to(target)
    except ValueError: pass
    else: raise ValueError("assessment output must be outside target")
    candidates=[]; conflicts=[]
    for name in receipt["created_files"]:
        path=_safe_target_for_rollback(target,name)
        if not path.is_file() or path.is_symlink(): conflicts.append({"relative_path":name,"reason":"missing_or_unsafe"}); continue
        current=hashlib.sha256(path.read_bytes()).hexdigest(); expected=receipt["file_hashes"].get(name)
        candidates.append({"relative_path":name,"expected_sha256":expected,"current_sha256":current,"current_type":"regular_file","assessment":"UNCHANGED_AT_CHECK_TIME" if current==expected else "MODIFIED","manual_deletion_eligible_at_check_time":current==expected})
    value={"schema_version":"1.0","status":"MANUAL_ROLLBACK_REVIEW_REQUIRED","target_identity_match":True,"automatic_rollback_available":False,"rollback_mode":"MANUAL_ONLY","candidates":candidates,"conflicts":conflicts,"warnings":["Assessment is a point-in-time snapshot.","Recheck immediately before manual deletion."]}
    validate_mapping(value, "rollback_assessment.schema.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    with os.fdopen(os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),"w",encoding="utf-8") as handle: json.dump(value,handle,sort_keys=True);handle.write("\n")
    return value


def _safe_target_for_rollback(root: Path, name: str) -> Path:
    if name not in INSTALLABLE_FILES or Path(name).name != name:
        raise ValueError("unsafe rollback path")
    path = root / name
    if path.parent.is_symlink():
        raise ValueError("unsafe rollback path")
    return path
