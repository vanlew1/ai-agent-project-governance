from __future__ import annotations

import argparse
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "scratch",
    ".pytest_cache",
}
MAX_FUNCTION_LINES = 80
MAX_FILE_LINES_SOFT = 500
MAX_FILE_LINES_HARD = 800


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def iter_python_files() -> list[Path]:
    return [path for path in ROOT.rglob("*.py") if not should_skip(path)]


def check_required_files() -> list[str]:
    required_groups = [
        ["AGENTS.md"],
        ["agent_rules/RULES_INDEX.yaml"],
        ["docs/AGENT_QUICK_CONTEXT.md", "docs/AGENT_QUICK_CONTEXT.template.md"],
        ["agent_rules/11_project_specific_rules.md", "agent_rules/11_project_specific_rules.template.md"],
        ["docs/MODULE_REGISTRY.yaml", "docs/MODULE_REGISTRY.template.yaml"],
        ["docs/TASK_REGISTRY.yaml", "docs/TASK_REGISTRY.template.yaml"],
        ["docs/CHANGELOG.md", "docs/CHANGELOG.template.md"],
    ]
    warnings = []
    for group in required_groups:
        if not any((ROOT / item).exists() for item in group):
            warnings.append(f"[WARN] Missing required governance file: {' or '.join(group)}")
    return warnings


def check_file_lengths(paths: list[Path]) -> list[str]:
    warnings = []
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            warnings.append(f"[WARN] Cannot read as UTF-8: {path.relative_to(ROOT)}")
            continue
        line_count = len(lines)
        rel = path.relative_to(ROOT)
        if line_count > MAX_FILE_LINES_HARD:
            warnings.append(f"[HARD] File too long ({line_count} lines): {rel}")
        elif line_count > MAX_FILE_LINES_SOFT:
            warnings.append(f"[SOFT] File long ({line_count} lines): {rel}")
    return warnings


def check_function_lengths(paths: list[Path]) -> list[str]:
    warnings = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception as exc:
            warnings.append(f"[WARN] Cannot parse {path.relative_to(ROOT)}: {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and getattr(node, "end_lineno", None):
                length = node.end_lineno - node.lineno + 1
                if length > MAX_FUNCTION_LINES:
                    warnings.append(f"[SOFT] Function too long ({length} lines): {path.relative_to(ROOT)}::{node.name}")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic governance code quality check")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on warnings")
    args = parser.parse_args()

    py_files = iter_python_files()
    warnings = []
    warnings.extend(check_required_files())
    warnings.extend(check_file_lengths(py_files))
    warnings.extend(check_function_lengths(py_files))

    print("# Code Quality Gate Report")
    print()
    print(f"Scanned Python files: {len(py_files)}")
    print()

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
        print()
        print("Result: WARNINGS_FOUND")
        return 1 if args.strict else 0

    print("No warnings found.")
    print("Result: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
