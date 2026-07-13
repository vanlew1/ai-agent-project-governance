"""Validate declared workspaces; P6 never creates or deletes worktrees."""
from pathlib import Path
from typing import Any, Mapping

KINDS={"CURRENT_WORKSPACE","EXISTING_WORKTREE","TEMPORARY_TEST_REPO","EXTERNAL_MANUAL"}
def validate_assignment(value: Mapping[str, Any], allowed_root: Path) -> list[str]:
    errors=[]; path=Path(value.get("workspace_path", ".")).resolve()
    if value.get("workspace_kind") not in KINDS: errors.append("invalid workspace kind")
    try: path.relative_to(allowed_root.resolve())
    except ValueError: errors.append("workspace path escapes allowed root")
    return errors
