"""Human- and machine-readable renderers for untrusted adoption plans."""
from __future__ import annotations

import json
from typing import Any


def render_json(plan: dict[str, object]) -> str:
    return json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) or "- None"


def _json_block(value: Any) -> str:
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n```"


def _candidate_rows(candidates: list[dict[str, object]]) -> list[str]:
    if not candidates:
        return ["No reliable candidate was found. This is unresolved; do not guess or execute a test command."]
    return [
        f"`{item['command']}` — evidence: {', '.join(item['evidence'])}; confidence: {item['confidence']}; confirmation required."
        for item in candidates
    ]


def _manifest_rows(manifest: list[dict[str, object]]) -> list[str]:
    return [
        f"`{item['source']}` → `{item['target']}` — `{item['operation']}`; confirmation required. {item['ownership_note']}"
        for item in manifest
    ]


def _confirmation_rows(items: list[dict[str, str]], key: str) -> list[str]:
    return [f"**{item[key]}** — {item['reason']}" for item in items]


def render_markdown(plan: dict[str, object]) -> str:
    """Render a compact review plan without leaking the target's absolute path."""
    adapter = plan["adapter"]
    audit = plan["audit"]
    preset = plan["preset_recommendation"]
    lines = [
        "# Existing Project Adoption Plan (dry run)",
        "",
        "## Project scan summary",
        "",
        f"- Target: `{plan['project_root']}` (absolute paths are intentionally hidden)",
        f"- Read-only: `{plan['read_only']}`. This run did not modify the target project.",
        f"- Adapter: `{adapter['primary_adapter']}` (`{adapter['status']}`, detection confidence `{adapter['detection_confidence']}`).",
        f"- Audit: `{audit['configuration_completeness_score']}/100` configuration completeness (`{audit['level']}`).",
        "",
        "## Read indicators correctly",
        "",
        _bullets([f"**{name}**: {details['meaning']} {details['does_not_mean']}" for name, details in plan["field_semantics"].items()]),
        "",
        "## Recommended preset",
        "",
        f"- Recommendation: `{preset['recommendation']}` — **requires confirmation**.",
        f"- Reason: {preset['reason']}",
        f"- Evidence: {', '.join(preset['evidence'])}",
        f"- Alternatives: {', '.join(preset['alternatives'])}",
        "",
        "## Test candidates",
        "",
        _bullets(_candidate_rows(plan["test_candidates"])),
        "",
        "## Proposed governance asset manifest",
        "",
        _bullets(_manifest_rows(plan["asset_manifest"])),
        "",
        "## Conflicts and overwrite risks",
        "",
        _bullets(_manifest_rows(plan["conflicts"]) if plan["conflicts"] else ["No file-content conflicts were detected; every future copy still requires confirmation."]),
        "",
        "## task.yaml draft (not authorized)",
        "",
        _json_block(plan["task_draft"]),
        "",
        "## project_state.yaml draft (not authorized)",
        "",
        _json_block(plan["project_state_draft"]),
        "",
        "## Required human confirmations",
        "",
        _bullets(_confirmation_rows(plan["required_confirmations"], "area")),
        "",
        "## Forbidden automatic decisions",
        "",
        _bullets(_confirmation_rows(plan["blocked_decisions"], "decision")),
        "",
        "## Next command preview",
        "",
        _bullets([f"`{item['command']}` — {item['note']}" for item in plan["next_commands"]]),
        "",
        "## Rollback checklist",
        "",
        _bullets(plan["rollback_checklist"]),
        "",
        "## Warnings",
        "",
        _bullets(plan["warnings"]),
        "",
        "This plan is a recommendation and untrusted draft, not authorization to copy files, create configuration, activate state, run tests, access external systems, or perform Git/release operations.",
    ]
    return "\n".join(lines) + "\n"
