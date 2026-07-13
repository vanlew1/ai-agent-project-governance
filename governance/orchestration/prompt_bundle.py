"""Minimal, human-distributed Codex prompt bundle generator."""
from pathlib import Path
from .models import digest

def write_bundle(root: Path, plan: dict, subtask: dict) -> Path:
    path=root/"reports"/"orchestration"/plan["orchestration_id"]/f"{subtask['subtask_id']}_PROMPT.md"; path.parent.mkdir(parents=True,exist_ok=True)
    lines=[f"# {subtask['title']}",f"Role: {subtask['role']}","", "## Scope",f"Read: {', '.join(subtask.get('read_scope',[]))}",f"Write: {', '.join(subtask.get('write_scope',[]))}",f"Deny: {', '.join(subtask.get('deny_scope',[]))}","", "## Required checks",*subtask.get("required_command_ids",[]),"",f"Handoff: .agent_state/orchestration/{plan['orchestration_id']}/handoffs/","Stop after structured result and handoff. Do not create worktrees, branches, commits, or remote calls."]
    path.write_text("\n".join(lines)+"\n",encoding="utf-8"); return path
