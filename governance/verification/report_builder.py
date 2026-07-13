from pathlib import Path

def build(task_id, verification, closure, changed_paths=()):
    lines=[f"# {task_id} Implementation Report","","## Modified Files",*([f"- {p}" for p in changed_paths] or ["- none"]),"","## Core Changes","- Deterministic allowlisted verification.","","## Guard Result",f"- {verification['guard_status']}","","## Test Results",*([f"- {r['command_id']}: {r['status']}" for r in verification['tests']] or ["- none"]),"","## Risks and Remaining Work",*([f"- {r}" for r in verification['remaining_risks']] or ["- none"]),"","## Acceptance Status",f"- {closure['status']}","","## Next Phase","- P4 only after this closure is CLOSED."]
    return "\n".join(lines)+"\n"

def write(root, task_id, verification, closure, changed_paths=()):
    path=Path(root)/"reports"/"governance"/f"{task_id}_IMPLEMENTATION_REPORT.md"; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(build(task_id,verification,closure,changed_paths),encoding="utf-8"); return str(path.relative_to(root)).replace("\\","/")
