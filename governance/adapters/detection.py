"""Deterministic, bounded repository marker detection."""
from datetime import datetime, timezone
from pathlib import Path

from .models import AdapterDetection
from .registry import all_adapters

_ORDER = ("wechat_miniprogram", "python", "node", "generic")

def detect_adapters(repo_root: Path) -> AdapterDetection:
    root = repo_root.resolve()
    evidence = tuple(adapter.detect(root) for adapter in all_adapters())
    active = [item for item in evidence if item.adapter_id != "generic" and item.score > 0]
    active_ids = [item.adapter_id for item in sorted(active, key=lambda item: _ORDER.index(item.adapter_id))]
    if not active_ids:
        primary, detected, status, conflicts = "generic", ("generic",), "FALLBACK", ()
    elif active_ids[0] == "wechat_miniprogram":
        extras = tuple(item for item in active_ids[1:] if item != "node")
        primary, detected = "wechat_miniprogram", tuple(active_ids)
        status, conflicts = ("MIXED", extras) if extras else ("DETECTED", ())
    elif len(active_ids) > 1:
        primary, detected, status, conflicts = active_ids[0], tuple(active_ids), "MIXED", tuple(active_ids)
    else:
        primary, detected, status, conflicts = active_ids[0], tuple(active_ids), "DETECTED", ()
    return AdapterDetection("1.0", str(root), primary, detected, "high" if status == "DETECTED" else "low",
        evidence, conflicts, status, datetime.now(timezone.utc).isoformat(), tuple(item for item in detected if item != primary))
