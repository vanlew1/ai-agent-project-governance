"""Canonical pre-write manifests for bounded existing-project installation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from governance.adoption.io import write_json_exclusive
from governance.adoption.planner import target_identity
from governance.adoption.scope_contract import scope_digest
from governance.schema_loader import load_mapping, validate_mapping


INSTALL_SOURCES = {
    "task.yaml": "task_contract.runtime.yaml",
    "project_state.yaml": "project_state.runtime.yaml",
}
SIDECAR_FILES = ("INSTALL_WRITESET.json", "PRE_INSTALL_HASHES.json", "ROLLBACK_MANIFEST.json")


def _digest(value: Mapping[str, Any], digest_key: str) -> str:
    payload = {key: item for key, item in value.items() if key != digest_key}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def classify_install_paths(asset_manifest: list[dict[str, Any]], root: Path) -> dict[str, list[str]]:
    classifications = {name: [] for name in ("CREATE", "MODIFY", "SKIP", "FAIL_ON_EXISTING", "MANUAL_ADOPTION_ASSET")}
    for name in sorted(INSTALL_SOURCES):
        classifications["FAIL_ON_EXISTING" if (root / name).exists() else "CREATE"].append(name)
    classifications["MANUAL_ADOPTION_ASSET"] = sorted({str(item["target"]) for item in asset_manifest})
    return classifications


def generate_canonical_writeset(
    *, plan: Mapping[str, Any], root: Path, runtime_files: Mapping[str, bytes],
) -> dict[str, Any]:
    classifications = classify_install_paths(list(plan["asset_manifest"]), root)
    install_files = {
        target: {
            "source_artifact": source,
            "expected_sha256": hashlib.sha256(runtime_files[source]).hexdigest(),
        }
        for target, source in sorted(INSTALL_SOURCES.items())
    }
    value: dict[str, Any] = {
        "schema_version": "1.0",
        "artifact_type": "INSTALL_WRITESET",
        "target_identity_digest": target_identity(root)["identity_digest"],
        "plan_digest": plan["plan_digest"],
        "scope_contract_digest": scope_digest(plan["scope_contract"]),
        "classifications": classifications,
        "install_files": install_files,
        "generated_before_target_write": True,
    }
    value["writeset_digest"] = _digest(value, "writeset_digest")
    validate_mapping(value, "adoption_install_writeset.schema.json")
    return value


def generate_pre_install_hashes(*, writeset: Mapping[str, Any], root: Path) -> dict[str, Any]:
    entries: dict[str, Any] = {}
    for name in sorted(INSTALL_SOURCES):
        path = root / name
        entries[name] = {
            "exists": path.exists(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        }
    value: dict[str, Any] = {
        "schema_version": "1.0",
        "artifact_type": "PRE_INSTALL_HASHES",
        "target_identity_digest": writeset["target_identity_digest"],
        "writeset_digest": writeset["writeset_digest"],
        "entries": entries,
        "generated_before_target_write": True,
    }
    value["pre_install_hashes_digest"] = _digest(value, "pre_install_hashes_digest")
    validate_mapping(value, "adoption_pre_install_hashes.schema.json")
    return value


def generate_rollback_manifest(*, writeset: Mapping[str, Any]) -> dict[str, Any]:
    actions = [
        {
            "relative_path": name,
            "expected_installed_sha256": writeset["install_files"][name]["expected_sha256"],
            "action": "MANUAL_DELETE_IF_UNCHANGED",
        }
        for name in writeset["classifications"]["CREATE"]
    ]
    value: dict[str, Any] = {
        "schema_version": "1.0",
        "artifact_type": "ROLLBACK_MANIFEST",
        "target_identity_digest": writeset["target_identity_digest"],
        "writeset_digest": writeset["writeset_digest"],
        "automatic_rollback_available": False,
        "actions": actions,
        "generated_before_target_write": True,
    }
    value["rollback_manifest_digest"] = _digest(value, "rollback_manifest_digest")
    validate_mapping(value, "adoption_rollback_manifest.schema.json")
    return value


def canonical_sidecars(
    *, plan: Mapping[str, Any], root: Path, runtime_files: Mapping[str, bytes],
) -> dict[str, dict[str, Any]]:
    writeset = generate_canonical_writeset(plan=plan, root=root, runtime_files=runtime_files)
    pre_install = generate_pre_install_hashes(writeset=writeset, root=root)
    rollback = generate_rollback_manifest(writeset=writeset)
    return {
        "INSTALL_WRITESET.json": writeset,
        "PRE_INSTALL_HASHES.json": pre_install,
        "ROLLBACK_MANIFEST.json": rollback,
    }


def write_sidecars(output: Path, sidecars: Mapping[str, Mapping[str, Any]]) -> None:
    for name in SIDECAR_FILES:
        write_json_exclusive(output / name, sidecars[name])


def load_and_validate_sidecars(bundle: Path) -> dict[str, dict[str, Any]]:
    schemas = {
        "INSTALL_WRITESET.json": "adoption_install_writeset.schema.json",
        "PRE_INSTALL_HASHES.json": "adoption_pre_install_hashes.schema.json",
        "ROLLBACK_MANIFEST.json": "adoption_rollback_manifest.schema.json",
    }
    result: dict[str, dict[str, Any]] = {}
    for name, schema in schemas.items():
        value = load_mapping(bundle / name)
        validate_mapping(value, schema)
        digest_key = {
            "INSTALL_WRITESET.json": "writeset_digest",
            "PRE_INSTALL_HASHES.json": "pre_install_hashes_digest",
            "ROLLBACK_MANIFEST.json": "rollback_manifest_digest",
        }[name]
        if value[digest_key] != _digest(value, digest_key):
            raise ValueError(f"{name} digest mismatch")
        result[name] = value
    writeset = result["INSTALL_WRITESET.json"]
    if result["PRE_INSTALL_HASHES.json"]["writeset_digest"] != writeset["writeset_digest"]:
        raise ValueError("PRE_INSTALL_HASHES.json is not bound to INSTALL_WRITESET.json")
    if result["ROLLBACK_MANIFEST.json"]["writeset_digest"] != writeset["writeset_digest"]:
        raise ValueError("ROLLBACK_MANIFEST.json is not bound to INSTALL_WRITESET.json")
    return result


# Backward-compatible public name retained for callers that only need classification.
def generate_legacy_classification(asset_manifest: list[dict[str, Any]], root: Path) -> dict[str, list[str]]:
    return classify_install_paths(asset_manifest, root)

