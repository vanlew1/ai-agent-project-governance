"""Validate confirmed adoption plans and export conservative draft files only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from governance.adoption.io import write_text_exclusive
from governance.adoption.planner import target_identity, validate_unique_candidate_ids
from governance.adoption.provenance import validate_provenance_receipt
from governance.adoption.scope_contract import assert_scope_equal, scope_digest, validate_plan_scope
from governance.schema_loader import load_mapping, validate_mapping


BLOCKED_DECISIONS = (
    "production_data",
    "external_api",
    "git_write",
    "release",
    "state_activation",
    "security_bypass",
    "business_semantic_change",
)


def _digest(value: dict[str, Any], omitted_keys: tuple[str, ...] = ("plan_digest", "provenance_receipt")) -> str:
    canonical = {key: item for key, item in value.items() if key not in omitted_keys}
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def _validate_plan(plan: dict[str, Any], *, target_root: Path | None = None) -> dict[str, Any]:
    validate_mapping(plan, "adoption_plan.schema.json")
    if plan["plan_digest"] != _digest(plan):
        raise ValueError("plan digest does not match the plan contents")
    scope = validate_plan_scope(plan, require_formal=True)
    validate_unique_candidate_ids(plan["test_candidates"])
    validate_provenance_receipt(plan, target_root=target_root, require_public_cli=True)
    return scope


def _validate_confirmation(
    plan: dict[str, Any], confirmation: dict[str, Any], *, require_confirmed: bool = False,
) -> dict[str, Any]:
    validate_mapping(confirmation, "adoption_confirmation.schema.json")
    if confirmation["plan_digest"] != plan["plan_digest"]:
        raise ValueError("confirmation plan digest does not match the supplied plan")
    options = {plan["preset_recommendation"]["recommendation"], *plan["preset_recommendation"]["alternatives"]}
    if confirmation["preset"]["selected"] not in options:
        raise ValueError("confirmation selected a preset absent from the plan")
    scope = (confirmation["scope"]["allowed_paths"], confirmation["scope"]["denied_paths"])
    plan_scopes = {(tuple(item["allowed_paths"]), tuple(item["denied_paths"])) for item in plan["scope_candidates"]}
    if (tuple(scope[0]), tuple(scope[1])) not in plan_scopes:
        raise ValueError("confirmation selected scope paths absent from the plan")
    canonical = validate_plan_scope(plan, require_formal=True)
    assert_scope_equal(canonical, confirmation.get("scope_contract", {}), boundary="confirmation")
    if confirmation["scope"]["allowed_paths"] != canonical["allowed_paths"] or confirmation["scope"]["denied_paths"] != canonical["denied_paths"]:
        raise ValueError("SCOPE_CONTRACT_MISMATCH: confirmation paths")
    candidate_ids = {item["candidate_id"] for item in plan["test_candidates"]}
    selected = confirmation["test_selection"]["candidate_id"]
    if selected is not None and selected not in candidate_ids:
        raise ValueError("confirmation selected a test candidate absent from the plan")
    if selected is None and candidate_ids:
        raise ValueError("a plan test candidate must be selected or remain unresolved")
    if set(confirmation["blocked_decisions"]) != set(BLOCKED_DECISIONS):
        raise ValueError("all blocked decisions must remain blocked")
    flags = (
        confirmation["confirmed_by_user"], confirmation["preset"]["confirmed"],
        confirmation["scope"]["confirmed"], confirmation["test_selection"]["confirmed"],
        confirmation["autonomy"]["confirmed"],
    )
    if len(set(flags)) != 1 or (require_confirmed and flags[0] is not True):
        raise ValueError("owner confirmation is required and must be consistent")
    return canonical


def confirmation_candidate(plan: dict[str, Any], *, confirmed_by_user: bool = False) -> dict[str, Any]:
    """Build one reviewable candidate without inventing owner authorization."""
    scope = _validate_plan(plan)
    selected = plan["test_candidates"][0]["candidate_id"] if plan["test_candidates"] else None
    value = {
        "schema_version": "1.0",
        "plan_digest": plan["plan_digest"],
        "confirmed_by_user": confirmed_by_user,
        "scope_contract": scope,
        "preset": {"selected": plan["preset_recommendation"]["recommendation"], "confirmed": confirmed_by_user},
        "scope": {"allowed_paths": scope["allowed_paths"], "denied_paths": scope["denied_paths"], "confirmed": confirmed_by_user},
        "test_selection": {"candidate_id": selected, "confirmed": confirmed_by_user},
        "autonomy": {"level": "constrained", "confirmed": confirmed_by_user},
        "blocked_decisions": {name: "BLOCKED" for name in BLOCKED_DECISIONS},
    }
    _validate_confirmation(plan, value, require_confirmed=confirmed_by_user)
    return value


def _safe_output_dir(output_dir: Path, target_root: Path) -> Path:
    destination = output_dir.expanduser().resolve(strict=False)
    try:
        destination.relative_to(target_root)
    except ValueError:
        pass
    else:
        raise ValueError("--output-dir must be outside --target-project-root")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("--output-dir already exists and is not empty")
    return destination


def _yaml_draft(value: dict[str, Any], marker: str) -> str:
    return f"# {marker}\n# NOT_INSTALLED\n# REQUIRES_FINAL_REVIEW\n" + yaml.safe_dump(value, allow_unicode=True, sort_keys=False)


def _draft_payloads(plan: dict[str, Any], confirmation: dict[str, Any], output_dir: Path) -> dict[str, str]:
    scope_contract = validate_plan_scope(plan, require_formal=True)
    selected = confirmation["test_selection"]["candidate_id"]
    candidate = next((item for item in plan["test_candidates"] if item["candidate_id"] == selected), None)
    unresolved = ["test_selection"] if candidate is None else []
    task = {
        "draft_status": "UNTRUSTED_DRAFT",
        "installation_status": "NOT_INSTALLED",
        "review_status": "REQUIRES_FINAL_REVIEW",
        "task_id": scope_contract["task_id"],
        "objective": scope_contract["task_goal"],
        "execution_mode": scope_contract["execution_mode"],
        "scope_contract": scope_contract,
        "write_scope": {"allow": confirmation["scope"]["allowed_paths"], "deny": confirmation["scope"]["denied_paths"]},
        "test_candidate": candidate["command"] if candidate else "UNRESOLVED",
        "blocked_decisions": list(BLOCKED_DECISIONS),
    }
    state = {
        "draft_status": "UNTRUSTED_DRAFT",
        "activation_status": "NOT_ACTIVATED",
        "review_status": "REQUIRES_FINAL_REVIEW",
        "preflight_status": "NOT_RUN",
        "tests_status": "NOT_EXECUTED",
        "verification_status": "NOT_COMPLETED",
        "closure_status": "NOT_COMPLETED",
        "blocked_decisions": list(BLOCKED_DECISIONS),
        "execution_mode": scope_contract["execution_mode"],
        "scope_contract": scope_contract,
    }
    confirmation_digest = _digest(confirmation, omitted_keys=())
    manifest = {
        "schema_version": "1.0",
        "plan_digest": plan["plan_digest"],
        "confirmation_digest": confirmation_digest,
        "scope_contract_digest": scope_digest(scope_contract),
        "target_identity_digest": plan["target_identity"]["identity_digest"],
        "target_project": "<sanitized>",
        "output_directory": "<sanitized>",
        "status": "DRAFT_EXPORTED",
        "installed": False,
        "activated": False,
        "tests_executed": False,
        "files": ["task.yaml.draft", "project_state.yaml.draft", "ADOPTION_CONFIRMATION_SUMMARY.md", "EXPORT_MANIFEST.json"],
        "file_hashes": {},
        "unresolved_fields": unresolved,
        "blocked_decisions": list(BLOCKED_DECISIONS),
    }
    summary = "\n".join((
        "# Adoption confirmation draft export",
        "",
        "Status: `UNTRUSTED_DRAFT`, `NOT_INSTALLED`, `NOT_ACTIVATED`, `REQUIRES_FINAL_REVIEW`.",
        "",
        f"The user confirmed preset `{confirmation['preset']['selected']}` and one plan-proposed scope.",
        "No blocked decision was approved: production data, external APIs, Git writes, release, state activation, security bypass, and business-semantic changes remain blocked.",
        "",
        "Generated drafts: `task.yaml.draft`, `project_state.yaml.draft`, and this summary with `EXPORT_MANIFEST.json`.",
        "",
        "This export did not install assets, write the target project, activate state, run Preflight, Guard, tests, Verification, or Closure.",
        "A user must review these drafts again; they are not an adopted project configuration.",
        "",
    ))
    payloads = {
        "task.yaml.draft": _yaml_draft(task, "UNTRUSTED_DRAFT"),
        "project_state.yaml.draft": _yaml_draft(state, "NOT_ACTIVATED"),
        "ADOPTION_CONFIRMATION_SUMMARY.md": summary,
        "EXPORT_MANIFEST.json": json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    }
    manifest["file_hashes"] = {name: hashlib.sha256(content.encode("utf-8")).hexdigest() for name, content in payloads.items() if name != "EXPORT_MANIFEST.json"}
    payloads["EXPORT_MANIFEST.json"] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return payloads


def export_drafts(plan_path: Path, confirmation_path: Path, output_dir: Path, target_project_root: Path) -> Path:
    """Export a validated draft bundle without touching the target project."""
    plan = load_mapping(plan_path)
    confirmation = load_mapping(confirmation_path)
    _validate_plan(plan, target_root=target_project_root.expanduser().resolve(strict=True))
    _validate_confirmation(plan, confirmation)
    target = target_project_root.expanduser().resolve(strict=True)
    if not target.is_dir():
        raise ValueError("--target-project-root must be an existing directory")
    if target_identity(target) != plan["target_identity"]:
        raise ValueError("--target-project-root does not match the plan target identity")
    destination = _safe_output_dir(output_dir, target)
    payloads = _draft_payloads(plan, confirmation, destination)
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in payloads.items():
        write_text_exclusive(destination / name, content)
    return destination
