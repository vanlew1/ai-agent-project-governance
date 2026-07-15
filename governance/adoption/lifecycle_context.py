"""Read-only provenance context and formal Preflight bridge for adopted Runtimes."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from governance.adoption.exporter import _validate_confirmation, _validate_plan
from governance.adoption.installer import digest
from governance.adoption.planner import target_identity
from governance.adoption.runtime_artifact_compiler import canonical_digest, compiler_identity
from governance.models.project_state import ProjectState
from governance.models.task_contract import TaskContract
from governance.preflight.engine import run_preflight
from governance.schema_loader import load_mapping, validate_mapping
from governance.verification.command_registry import get as registry_command


def _bytes_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_workspace(root: Path) -> str:
    """Hash paths, file types and bytes without returning file contents."""
    rows: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        # Runtime state transitions are lifecycle metadata, not target-workspace
        # changes; including them would make every successful transition stale.
        if relative in {"project_state.yaml", ".project_state.yaml.lifecycle.lock"}:
            continue
        if path.is_symlink():
            rows.append((relative, "symlink", str(path.readlink())))
        elif path.is_file():
            rows.append((relative, "file", hashlib.sha256(path.read_bytes()).hexdigest()))
        elif path.is_dir():
            rows.append((relative, "directory", ""))
    return hashlib.sha256(json.dumps({"version": "1.0", "entries": rows}, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _blocked_mapping(value: Mapping[str, Any], *, source: str) -> set[str]:
    if not isinstance(value, Mapping) or not value or any(item != "BLOCKED" for item in value.values()):
        raise ValueError(f"{source} blocked-decision authority is invalid")
    return set(value)


def _contract_blockers(contract: Mapping[str, Any]) -> set[str]:
    prefix = "BLOCKED_DECISION:"
    result = {item[len(prefix):] for item in contract["stop_conditions"] if item.startswith(prefix)}
    if not result:
        raise ValueError("TaskContract must explicitly retain blocked decisions")
    return result


def restriction_sidecar(contract: Mapping[str, Any], context: "AdoptionLifecycleContext") -> dict[str, Any]:
    """Carry restrictions TaskRequest cannot natively represent, without defaults."""
    if contract.get("governance", {}).get("level") not in {"LEVEL_2_TASK", "LEVEL_3_HIGH_RISK"}:
        raise ValueError("unknown TaskContract authority")
    allowed, denied = contract["write_scope"].get("allow"), contract["write_scope"].get("deny")
    if not isinstance(allowed, list) or not allowed or not isinstance(denied, list):
        raise ValueError("TaskContract scope is incomplete")
    blockers = _contract_blockers(contract)
    if not blockers.issubset(set(context.blocked_decisions)):
        raise ValueError("TaskContract attempts to unlock an approved blocker")
    if any(context.blocked_decisions.count(item) != 1 for item in context.blocked_decisions):
        raise ValueError("blocked-decision chain is ambiguous")
    return {
        "allowed_paths": list(allowed), "denied_paths": list(denied),
        "blocked_decisions": list(context.blocked_decisions),
        "confirmed_candidates": dict(context.confirmed_test_candidates),
        "network_authorized": False, "git_write_authorized": False,
        "production_authorized": False, "release_authorized": False,
        "autonomy": dict(contract["autonomy"]),
    }


def task_request_from_contract(contract: dict[str, Any]) -> dict[str, Any]:
    """Deterministically map only fields represented by the formal TaskRequest schema."""
    allowed = list(contract["write_scope"]["allow"])
    if not allowed or any(not isinstance(path, str) or not path for path in allowed):
        raise ValueError("TaskContract has no confirmed writable scope for lifecycle preflight")
    return {
        "schema_version": "1.0", "task_id": contract["task_id"], "title": contract["objective"][0],
        "description": "\n".join(contract["objective"]), "requested_by": "adoption_runtime",
        "requested_at": "1970-01-01T00:00:00+00:00",
        "hints": {"likely_paths": allowed, "external_access": False, "production_write": False},
        "governance_context": {"project_event": "ordinary_task", "risk_status": "known_low", "parent_task_id": contract["task_id"]},
    }


@dataclass(frozen=True)
class AdoptionLifecycleContext:
    target_identity_digest: str
    task_contract_digest: str
    project_state_digest: str
    runtime_artifact_manifest_digest: str
    final_install_approval_digest: str
    installation_receipt_digest: str
    activation_approval_digest: str
    activation_receipt_digest: str
    compiler_id: str
    compiler_version: str
    compiler_digest: str
    confirmation_digest: str
    confirmed_test_candidates: tuple[tuple[str, str], ...]
    confirmed_test_candidate_set_digest: str
    blocked_decisions: tuple[str, ...]
    blocked_decisions_digest: str
    workspace_snapshot_digest: str

    def digest(self) -> str:
        return digest({**self.__dict__, "confirmed_test_candidates": list(self.confirmed_test_candidates), "blocked_decisions": list(self.blocked_decisions)})


def build_lifecycle_context(
    target: Path, task_path: Path, state_path: Path, installation_receipt: Path, activation_receipt: Path,
    *, runtime_artifact_manifest: Path, final_install_approval: Path, activation_approval: Path,
    confirmation: Path, plan: Path,
) -> AdoptionLifecycleContext:
    """Independently reconstruct every approval and Runtime-provenance fact."""
    target = target.expanduser().resolve(strict=True)
    if task_path.expanduser().resolve(strict=True) != target / "task.yaml" or state_path.expanduser().resolve(strict=True) != target / "project_state.yaml":
        raise ValueError("lifecycle context requires canonical installed Runtime paths")
    task, state = load_mapping(task_path), load_mapping(state_path)
    validate_mapping(task, "task_contract.schema.json"); TaskContract.from_mapping(task)
    validate_mapping(state, "project_state.schema.json"); ProjectState.from_mapping(state)
    manifest = load_mapping(runtime_artifact_manifest); final = load_mapping(final_install_approval)
    install = load_mapping(installation_receipt); activation = load_mapping(activation_receipt)
    approval = load_mapping(activation_approval); confirmation_value = load_mapping(confirmation); plan_value = load_mapping(plan)
    validate_mapping(manifest, "runtime_artifact_manifest.schema.json")
    validate_mapping(final, "adoption_final_approval.schema.json")
    validate_mapping(install, "adoption_installation_receipt.schema.json")
    validate_mapping(activation, "activation_receipt.schema.json")
    validate_mapping(approval, "activation_approval.schema.json")
    _validate_plan(plan_value); _validate_confirmation(plan_value, confirmation_value)
    if manifest["manifest_digest"] != canonical_digest(manifest, "manifest_digest"):
        raise ValueError("runtime manifest digest mismatch")
    identity = {"id": manifest["compiler_id"], "version": manifest["compiler_version"], "digest": manifest["compiler_digest"]}
    if identity != compiler_identity() or identity != final["compiler"] or identity != approval["compiler"] or identity != install["compiler"]:
        raise ValueError("compiler identity provenance mismatch")
    target_digest = target_identity(target)["identity_digest"]
    if any(value != target_digest for value in (install["target_identity_digest"], final["target_identity_digest"], approval["target_identity_digest"], activation["target_identity_digest"])):
        raise ValueError("cross-project provenance replay")
    final_digest, install_digest, approval_digest, activation_digest = digest(final), digest(install), digest(approval), digest(activation)
    if final["runtime_artifact_manifest_digest"] != manifest["manifest_digest"] or install["runtime_artifact_manifest_digest"] != manifest["manifest_digest"] or approval["runtime_artifact_manifest_digest"] != manifest["manifest_digest"] or activation["runtime_artifact_manifest_digest"] != manifest["manifest_digest"]:
        raise ValueError("cross-runtime-manifest provenance replay")
    if install["final_approval_digest"] != final_digest or approval["final_install_approval_digest"] != final_digest or activation["final_install_approval_digest"] != final_digest:
        raise ValueError("final approval provenance mismatch")
    if approval["installation_receipt_digest"] != install_digest or activation["installation_receipt_digest"] != install_digest:
        raise ValueError("installation receipt provenance mismatch")
    if activation["activation_approval_digest"] != approval_digest or state.get("activation_approval_digest") != approval_digest or state.get("activation_receipt_digest") != activation["activation_receipt_binding_digest"]:
        raise ValueError("activation provenance mismatch")
    if plan_value["plan_digest"] != confirmation_value["plan_digest"] or confirmation_value["plan_digest"] != final["plan_digest"] or confirmation_value["plan_digest"] != install["plan_digest"]:
        raise ValueError("confirmation provenance mismatch")
    confirmation_digest = digest(confirmation_value)
    if final["confirmation_digest"] != confirmation_digest or install["confirmation_digest"] != confirmation_digest or manifest["confirmation_digest"] != confirmation_digest:
        raise ValueError("modified confirmation provenance")
    selected = confirmation_value["test_selection"]["candidate_id"]
    candidate = next((item for item in plan_value["test_candidates"] if item["candidate_id"] == selected), None)
    command = registry_command(selected) if candidate else None
    if not selected or not candidate or not command or candidate["command"] != " ".join(command["argv"]):
        raise ValueError("confirmed test candidate provenance mismatch")
    candidates = ((selected, digest(command)),)
    candidate_digest = digest({"confirmed_test_candidates": list(candidates)})
    confirmation_blocked = _blocked_mapping(confirmation_value["blocked_decisions"], source="confirmation")
    final_blocked = _blocked_mapping(final["blocked_decisions"], source="final approval")
    activation_blocked = _blocked_mapping(approval["blocked_decisions"], source="activation approval")
    contract_blocked = _contract_blockers(task)
    if not (contract_blocked.issubset(final_blocked | activation_blocked) and confirmation_blocked.issubset(final_blocked | activation_blocked)):
        raise ValueError("blocked decision was reduced or unlocked")
    blocked = tuple(sorted(final_blocked | activation_blocked | confirmation_blocked | contract_blocked))
    if state.get("network_authorized") or state.get("git_write_authorized") or state.get("release_authorized"):
        raise ValueError("Runtime state unlocks a blocked decision")
    if state.get("lifecycle_stage") not in {"ACTIVATED_NOT_PREFLIGHTED", "PREFLIGHT_PASSED", "GUARDED", "TEST_PLANNED", "TEST_EXECUTED", "VERIFIED", "CLOSED"} or state.get("status") != "ACTIVATED_NOT_PREFLIGHTED":
        raise ValueError("STATE_NOT_ACTIVATED")
    return AdoptionLifecycleContext(
        target_digest, _bytes_digest(task_path), _bytes_digest(state_path), manifest["manifest_digest"], final_digest,
        install_digest, approval_digest, activation_digest, identity["id"], identity["version"], identity["digest"],
        confirmation_digest, candidates, candidate_digest, blocked, digest({"blocked_decisions": list(blocked)}), snapshot_workspace(target),
    )


def run_adoption_preflight(context: AdoptionLifecycleContext, task_path: Path, state_path: Path) -> dict[str, Any]:
    contract, state = load_mapping(task_path), load_mapping(state_path)
    sidecar = restriction_sidecar(contract, context)
    request = task_request_from_contract(contract)
    result = run_preflight(request, state)
    if result.exit_status != 0 or result.contract.write_scope["allow"] != sidecar["allowed_paths"] or not set(sidecar["denied_paths"]).issubset(result.contract.write_scope["deny"]):
        raise ValueError("PREFLIGHT_BLOCKED")
    evidence = {
        "context_digest": context.digest(), "task_contract_digest": context.task_contract_digest,
        "project_state_digest_before": context.project_state_digest, "task_request_digest": digest(request),
        "mapping_digest": digest(sidecar), "restriction_sidecar": sidecar,
        "target_identity_digest": context.target_identity_digest,
        "installation_receipt_digest": context.installation_receipt_digest,
        "activation_receipt_digest": context.activation_receipt_digest,
        "workspace_snapshot_digest": context.workspace_snapshot_digest,
        "formal_preflight_result_digest": digest(result.contract.to_mapping()), "status": "PASS",
    }
    evidence["evidence_digest"] = digest(evidence)
    return evidence
