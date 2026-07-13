"""Small AST guard for documented governance runtime dependency direction."""
from __future__ import annotations
import argparse, ast
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Check governance runtime dependency direction")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()

def imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path)); names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module: names.add(node.module)
    return names

def main():
    root = parse_args().root.resolve(); errors = []
    for path in (root / "governance").rglob("*.py"):
        relative, names = path.relative_to(root).as_posix(), imports(path)
        joined = " ".join(names)
        if relative.startswith("governance/models/") and ("governance.cli" in joined or "filesystem" in joined): errors.append(f"models forbidden dependency: {relative}")
        if relative.startswith("governance/policy/") and "governance.verification" in joined: errors.append(f"policy forbidden dependency: {relative}")
        if relative.startswith("governance/adapters/") and any(name.startswith(("src", "app", "project")) for name in names): errors.append(f"adapter project-code dependency: {relative}")
        if relative.startswith("governance/state/") and any(name.startswith(("openai", "requests", "http", "socket")) for name in names): errors.append(f"state external dependency: {relative}")
    if errors:
        print(f"Runtime dependencies: FAIL ({len(errors)} issue(s))"); print("\n".join(f"- {error}" for error in errors)); return 2
    print("Runtime dependencies: PASS (documented forbidden directions absent)"); return 0
if __name__ == "__main__": raise SystemExit(main())
