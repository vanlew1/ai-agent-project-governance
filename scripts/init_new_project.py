from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import yaml
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

PRESETS = ("lightweight", "standard", "strict")


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
        destination = path.with_name(path.name.replace(".template.", "."))
        if destination.exists():
            destination.unlink()
        path.rename(destination)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a governed project")
    parser.add_argument("--adapter", choices=("auto", "generic", "python", "node", "wechat_miniprogram"), default="auto")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory in which to create the new project folder (defaults to the template's parent).",
    )
    parser.add_argument(
        "--preset", choices=PRESETS, default="standard",
        help="Initial governance focus (default: standard; existing template files are retained for every preset).",
    )
    return parser.parse_args()

def write_adapter_config(target_dir: Path, requested: str) -> None:
    from governance.adapters.detection import detect_adapters
    detected = detect_adapters(target_dir)
    adapter = detected.primary_adapter if requested == "auto" else requested
    config_dir = target_dir / "config"; config_dir.mkdir(exist_ok=True)
    value = {"schema_version": "1.0", "adapter": adapter, "auxiliary_adapters": list(detected.auxiliary_adapters if requested == "auto" else ()), "detection_status": detected.status if requested == "auto" else "DETECTED"}
    (config_dir / "project_adapter.yaml").write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    state_dir = target_dir / ".agent_state"; state_dir.mkdir(exist_ok=True)
    state = {"schema_version":"1.0","project_mode":"DISCOVERY","architecture_status":"draft","implementation_plan_status":"draft","repository_root":".","adapter":adapter,"auxiliary_adapters":value["auxiliary_adapters"],"adapter_detection_status":value["detection_status"],"high_risk_paths":[],"default_forbidden_operations":["production_write"]}
    (state_dir / "project_state.yaml").write_text(yaml.safe_dump(state, sort_keys=False), encoding="utf-8")


def write_preset_config(target_dir: Path, preset: str) -> dict[str, object]:
    if preset not in PRESETS:
        raise ValueError(f"Unsupported preset: {preset}")
    source = target_dir / "config" / "presets" / f"{preset}.yaml"
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("preset") != preset:
        raise ValueError(f"Invalid preset definition: {source}")
    destination = target_dir / "config" / "governance_preset.yaml"
    destination.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return data

def main() -> int:
    args = parse_args()
    template_dir = Path(__file__).resolve().parents[1]
    base_dir = args.output_dir.expanduser().resolve() if args.output_dir else template_dir.parent

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

    if base_dir.exists() and not base_dir.is_dir():
        print(f"[ERROR] Output path is not a directory: {base_dir}")
        return 1
    base_dir.mkdir(parents=True, exist_ok=True)

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
    write_adapter_config(target_dir, args.adapter)
    preset = write_preset_config(target_dir, args.preset)

    if init_git:
        try:
            initialize_git_repo(target_dir)
        except FileNotFoundError:
            print("[WARN] Git was not found. The project was created without Git initialization.")
        except subprocess.CalledProcessError as exc:
            print(f"[WARN] Git initialization failed: {exc}")

    print_next_steps(target_dir, preset)
    return 0


def print_next_steps(target_dir: Path, preset: dict[str, object]) -> None:
    print()
    print("[SUCCESS] Your new project has been created.")
    print(f"Project folder: {target_dir}")
    print()
    print("Review these files next:")
    for relative in (
        "docs/PROJECT_BRIEF_DRAFT.md", "docs/AGENT_QUICK_CONTEXT.md", "docs/OPEN_QUESTIONS.md",
        "docs/BOOTSTRAP_DECISION.md", "docs/IMPLEMENTATION_PLAN.md", "agent_rules/11_project_specific_rules.md",
        "agent_rules/15_plan_adaptation_rules.md", "docs/ARCHITECTURE.md", "docs/MODULE_REGISTRY.yaml",
        "docs/TASK_REGISTRY.yaml", "docs/CHANGELOG.md", "config/governance_preset.yaml",
    ):
        print(f"- {target_dir / relative}")
    print()
    print(f"Preset: {preset['preset']}: {preset['purpose']}")
    print("First focus:")
    for item in preset["initial_focus"]:
        print(f"- {item}")
    print("\nBefore EXECUTION, make sure:")
    print("- docs/IMPLEMENTATION_PLAN.md has every execution confirmation field filled in.")
    print("- External platform/API/data access method is confirmed or explicitly out of scope.")
    print("- Generated outputs, raw data, and private samples stay out of Git unless sanitized.")


if __name__ == "__main__":
    sys.exit(main())
