from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

IGNORE_NAMES = shutil.ignore_patterns(
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
)

PLACEHOLDERS = {
    "<PROJECT_NAME>": "project_name",
    "<PROJECT_TYPE>": "project_type",
    "<OWNER>": "owner",
    "<WHAT_IT_DOES>": "summary",
}


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def prompt_yes_no(label: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    value = input(f"{label} ({hint}): ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes"}


def rename_template_files(target_dir: Path) -> None:
    for path in sorted(target_dir.rglob("*.template.*")):
        path.rename(path.with_name(path.name.replace(".template.", ".")))


def write_workspace_router(target_dir: Path) -> None:
    agents_dir = target_dir / ".agents"
    agents_dir.mkdir(exist_ok=True)
    content = "# Agent Workspace Entry\n\nRead the root `AGENTS.md` before doing any work in this workspace.\n"
    (agents_dir / "AGENTS.md").write_text(content, encoding="utf-8")


def replace_placeholders(target_dir: Path, values: dict[str, str]) -> None:
    for path in target_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        original = text
        for placeholder, key in PLACEHOLDERS.items():
            text = text.replace(placeholder, values[key])
        if text != original:
            path.write_text(text, encoding="utf-8")


def append_project_summary(target_dir: Path, values: dict[str, str]) -> None:
    readme = target_dir / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    insert = (
        "\n## Generated Project Summary\n\n"
        f"- Project name: {values['project_name']}\n"
        f"- Project type: {values['project_type']}\n"
        f"- Owner: {values['owner']}\n"
        f"- Summary: {values['summary']}\n"
    )
    if "## Generated Project Summary" not in text:
        readme.write_text(text.rstrip() + insert + "\n", encoding="utf-8")


def initialize_git_repo(target_dir: Path) -> None:
    subprocess.run(["git", "init"], cwd=target_dir, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=target_dir, check=True)


def main() -> int:
    template_dir = Path(__file__).resolve().parents[1]
    base_dir = template_dir.parent

    print("=" * 54)
    print("Agent Governance Template Setup")
    print("=" * 54)
    print("This wizard creates a new project folder from the template.")
    print()

    try:
        project_name = prompt_text("New project folder name")
        if not project_name:
            print("[ERROR] Project name cannot be empty.")
            return 1

        project_type = prompt_text("Project type", "AI-assisted software project")
        owner = prompt_text("Owner or team name", "TBD")
        summary = prompt_text("One-line project summary", "Fill this in after project setup")
        init_git = prompt_yes_no("Initialize a local Git repository", True)
    except KeyboardInterrupt:
        print("\n[Cancelled]")
        return 0

    target_dir = base_dir / project_name
    if target_dir.exists():
        print(f"[ERROR] Target directory already exists: {target_dir}")
        return 1

    values = {
        "project_name": project_name,
        "project_type": project_type,
        "owner": owner,
        "summary": summary,
    }

    shutil.copytree(template_dir, target_dir, ignore=IGNORE_NAMES)
    rename_template_files(target_dir)
    replace_placeholders(target_dir, values)
    write_workspace_router(target_dir)
    append_project_summary(target_dir, values)

    if init_git:
        try:
            initialize_git_repo(target_dir)
        except FileNotFoundError:
            print("[WARN] Git was not found. The project was created without Git initialization.")
        except subprocess.CalledProcessError as exc:
            print(f"[WARN] Git initialization failed: {exc}")

    print()
    print("[SUCCESS] Your new project has been created.")
    print(f"Project folder: {target_dir}")
    print()
    print("Review these files next:")
    print(f"- {target_dir / 'docs' / 'PROJECT_BRIEF_DRAFT.md'}")
    print(f"- {target_dir / 'docs' / 'OPEN_QUESTIONS.md'}")
    print(f"- {target_dir / 'docs' / 'BOOTSTRAP_DECISION.md'}")
    print(f"- {target_dir / 'docs' / 'IMPLEMENTATION_PLAN.md'}")
    print(f"- {target_dir / 'agent_rules' / '11_project_specific_rules.md'}")
    print(f"- {target_dir / 'agent_rules' / '15_plan_adaptation_rules.md'}")
    print(f"- {target_dir / 'docs' / 'ARCHITECTURE.md'}")
    print(f"- {target_dir / 'docs' / 'MODULE_REGISTRY.yaml'}")
    print(f"- {target_dir / 'docs' / 'TASK_REGISTRY.yaml'}")
    print(f"- {target_dir / 'docs' / 'CHANGELOG.md'}")
    print()
    print("Before EXECUTION, make sure:")
    print("- docs/IMPLEMENTATION_PLAN.md has every execution confirmation field filled in.")
    print("- External platform/API/data access method is confirmed or explicitly out of scope.")
    print("- Generated outputs, raw data, and private samples stay out of Git unless sanitized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
