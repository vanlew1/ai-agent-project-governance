"""Truthful toolchain-provenance binding for public adoption planning."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from governance.schema_loader import validate_mapping


SOURCE_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_GENERATION_PATH = "scripts/agent_adopt.py:dry-run"
GENERATOR_INPUTS = (
    "VERSION",
    "scripts/agent_adopt.py",
    "governance/adoption/planner.py",
    "governance/adoption/provenance.py",
    "governance/adoption/scope_contract.py",
    "schemas/adoption_plan.schema.json",
    "schemas/adoption_scope_input.schema.json",
    "schemas/adoption_provenance_receipt.schema.json",
)


def canonical_digest(value: Mapping[str, Any], *, omit: tuple[str, ...] = ()) -> str:
    payload = {key: item for key, item in value.items() if key not in omit}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@lru_cache(maxsize=1)
def framework_version() -> str:
    return (SOURCE_ROOT / "VERSION").read_text(encoding="utf-8").strip()


@lru_cache(maxsize=1)
def generator_source_digest() -> str:
    rows = {name: hashlib.sha256((SOURCE_ROOT / name).read_bytes()).hexdigest() for name in GENERATOR_INPUTS}
    return canonical_digest(rows)


@lru_cache(maxsize=1)
def command_contract_digest() -> str:
    return canonical_digest({
        "entrypoint": PUBLIC_GENERATION_PATH,
        "required": ["--project-root", "--scope-file", "--format", "--output", "dry-run"],
        "target_write_policy": "FORBIDDEN",
    })


@lru_cache(maxsize=1)
def git_executable() -> str | None:
    """Resolve Git without assuming Windows GUI PATH inheritance."""
    discovered = shutil.which("git")
    if discovered:
        return discovered
    if os.name == "nt":
        candidates = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "cmd" / "git.exe",
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Git" / "cmd" / "git.exe",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    return None


def git_metadata(root: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        executable = git_executable()
        if executable is None:
            return "UNAVAILABLE"
        try:
            result = subprocess.run(
                [executable, "-C", str(root), *args], text=True, encoding="utf-8", errors="replace",
                capture_output=True, check=False,
            )
        except OSError:
            return "UNAVAILABLE"
        return result.stdout.strip() if result.returncode == 0 else "UNAVAILABLE"
    return {"branch": run("branch", "--show-current") or "DETACHED", "head": run("rev-parse", "HEAD")}


def build_provenance_receipt(
    *, target_identity: Mapping[str, Any], target_root: Path, plan_payload_digest: str,
    formal_scope_digests: Mapping[str, str] | None, generation_path: str,
) -> dict[str, Any]:
    target_git = git_metadata(target_root)
    framework_git = git_metadata(SOURCE_ROOT)
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "binding_type": "TOOLCHAIN_PROVENANCE_BINDING",
        "generator_id": "ai-agent-project-governance-planner",
        "generator_version": framework_version(),
        "generator_source_digest": generator_source_digest(),
        "generation_path": generation_path,
        "generation_command_contract_digest": command_contract_digest(),
        "formal_scope_input_digest": (formal_scope_digests or {}).get("raw_sha256", hashlib.sha256(b"").hexdigest()),
        "formal_scope_normalized_text_digest": (formal_scope_digests or {}).get("normalized_text_sha256", hashlib.sha256(b"").hexdigest()),
        "target_identity": dict(target_identity),
        "target_branch": target_git["branch"],
        "target_head": target_git["head"],
        "framework_commit": framework_git["head"],
        "plan_payload_digest": plan_payload_digest,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    receipt["provenance_receipt_digest"] = canonical_digest(receipt)
    validate_mapping(receipt, "adoption_provenance_receipt.schema.json")
    return receipt


def validate_provenance_receipt(
    plan: Mapping[str, Any], *, target_root: Path | None = None, require_public_cli: bool,
) -> dict[str, Any]:
    receipt = plan.get("provenance_receipt")
    if not isinstance(receipt, dict):
        raise ValueError("SUPERSEDED_REQUIRES_FRESH_DRY_RUN")
    validate_mapping(receipt, "adoption_provenance_receipt.schema.json")
    if receipt["provenance_receipt_digest"] != canonical_digest(receipt, omit=("provenance_receipt_digest",)):
        raise ValueError("provenance receipt digest does not match receipt contents")
    if receipt["plan_payload_digest"] != plan.get("plan_digest"):
        raise ValueError("provenance plan payload digest does not match plan digest")
    if receipt["generator_version"] != framework_version():
        raise ValueError("generator version does not match repository VERSION")
    if receipt["generator_source_digest"] != generator_source_digest():
        raise ValueError("generator source digest does not match current toolchain")
    if receipt["generation_command_contract_digest"] != command_contract_digest():
        raise ValueError("generation command contract digest does not match public CLI")
    if require_public_cli and receipt["generation_path"] != PUBLIC_GENERATION_PATH:
        raise ValueError("FORMAL_SCOPE_FLOW_ONLY: private planner calls cannot masquerade as public CLI")
    if git_metadata(SOURCE_ROOT)["head"] != receipt["framework_commit"]:
        raise ValueError("framework commit mismatch")
    if target_root is not None:
        current = git_metadata(target_root)
        if current["branch"] != receipt["target_branch"] or current["head"] != receipt["target_head"]:
            raise ValueError("target branch/HEAD mismatch")
    return receipt
