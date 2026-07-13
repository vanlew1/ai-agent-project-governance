"""Bootstrap integrity check using only isolated temporary directories."""
from __future__ import annotations
import argparse, shutil, sys, tempfile
from pathlib import Path
import yaml

def parse_args():
    p=argparse.ArgumentParser(description="Check bootstrap template integrity"); p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); return p.parse_args()
def main():
    root=parse_args().root.resolve(); errors=[]
    required=("AGENTS.md","agent_rules/RULES_INDEX.yaml","docs/GOVERNANCE_RUNTIME_ARCHITECTURE.md","schemas/project_state.schema.json","scripts/validate_governance.py")
    for item in required:
        if not (root/item).is_file(): errors.append(f"Missing template file: {item}")
    with tempfile.TemporaryDirectory(prefix="governance-p5-") as temp:
        target=Path(temp)/"generated-\u4e2d\u6587"
        shutil.copytree(root,target,ignore=shutil.ignore_patterns(".git","__pycache__",".agent_state",".tmp"))
        sys.path.insert(0, str(root))
        from scripts.init_new_project import rename_template_files, replace_placeholders, write_adapter_config, write_workspace_router
        rename_template_files(target); replace_placeholders(target,{"project_name":"generated","project_type":"test","owner":"P5","summary":"Unicode smoke"}); write_workspace_router(target)
        for adapter in ("generic","python","node","wechat_miniprogram"):
            write_adapter_config(target,adapter)
            value=yaml.safe_load((target/"config/project_adapter.yaml").read_text(encoding="utf-8"))
            if value["adapter"] != adapter: errors.append(f"Adapter config mismatch: {adapter}")
        remaining=[]
        for path in target.rglob("*"):
            if path.is_file() and path.suffix in {".md",".yaml",".yml",".txt",".py"}:
                remaining.extend(token for token in ("<PROJECT_NAME>","<PROJECT_TYPE>","<OWNER>","<WHAT_IT_DOES>") if token in path.read_text(encoding="utf-8") )
        if remaining: errors.append("Generated project retains required placeholders")
    if errors: print(f"Bootstrap integrity: FAIL ({len(errors)} issue(s))"); print("\n".join(f"- {e}" for e in errors)); return 2
    print("Bootstrap integrity: PASS (isolated adapters and Unicode path)"); return 0
if __name__ == "__main__": raise SystemExit(main())
