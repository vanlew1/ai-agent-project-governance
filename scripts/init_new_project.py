from __future__ import annotations

import shutil
import sys
from pathlib import Path


def rename_template_files(target_dir: Path) -> None:
    for path in target_dir.rglob("*.template.*"):
        path.rename(path.with_name(path.name.replace(".template.", ".")))


def write_workspace_router(target_dir: Path) -> None:
    agents_dir = target_dir / ".agents"
    agents_dir.mkdir(exist_ok=True)
    content = """# Agent Workspace Entry\n\n在执行本工作区任务前，请先读取根目录 `AGENTS.md`。\n"""
    (agents_dir / "AGENTS.md").write_text(content, encoding="utf-8")


def main() -> int:
    template_dir = Path(__file__).resolve().parents[1]
    base_dir = template_dir.parent

    try:
        project_name = input("请输入新项目目录名称: ").strip()
    except KeyboardInterrupt:
        print("\n[已取消]")
        return 0

    if not project_name:
        print("[错误] 项目名称不能为空。")
        return 1

    target_dir = base_dir / project_name
    if target_dir.exists():
        print(f"[错误] 目录已存在: {target_dir}")
        return 1

    shutil.copytree(template_dir, target_dir)
    rename_template_files(target_dir)
    write_workspace_router(target_dir)

    print("[成功] 新项目模板已初始化。")
    print(f"后续请补齐: {target_dir / 'agent_rules' / '11_project_specific_rules.md'}")
    print(f"后续请补齐: {target_dir / 'docs' / 'ARCHITECTURE.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
