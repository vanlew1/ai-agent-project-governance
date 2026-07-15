"""Stable text and JSON renderers for one audit result model."""
from __future__ import annotations

import json

from .models import AuditResult


def render_json(result: AuditResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_text(result: AuditResult, *, include_preset_hint: bool = True) -> str:
    lines = [
        "Agent adoption audit (local, deterministic, read-only)",
        f"Project: {result.project_root_display}",
        f"Score: {result.score}/100 ({result.level})",
        "",
    ]
    if include_preset_hint:
        lines.insert(3, f"Recommended preset: {result.recommended_preset}")
    for check in result.checks:
        lines.append(f"[{check.status}] {check.check_id}: {check.summary}")
        if check.safe_evidence:
            lines.append("  Evidence: " + ", ".join(check.safe_evidence))
        lines.append("  Next: " + check.recommendation)
    lines.extend(["", "This is a configuration-completeness check, not a security certification."])
    return "\n".join(lines) + "\n"
