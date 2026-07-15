"""Create a local, read-only adoption plan for an existing project."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from governance.adoption import build_plan, render_json, render_markdown  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a read-only existing-project governance adoption plan")
    parser.add_argument("--project-root", type=Path, required=True, help="Existing local project to inspect")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Explicit output path outside --project-root; stdout by default")
    parser.add_argument("mode", choices=("dry-run",), help="The only supported mode; it never changes the target project")
    return parser.parse_args()


def _output_path(root: Path, output: Path) -> Path:
    destination = output.expanduser().resolve()
    try:
        destination.relative_to(root)
    except ValueError:
        return destination
    raise ValueError("--output must be outside --project-root; target-project writes are forbidden")


def main() -> int:
    args = parse_args()
    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        print(f"[ERROR] --project-root must be an existing directory: {args.project_root}", file=sys.stderr)
        return 2
    try:
        plan = build_plan(root)
        rendered = render_markdown(plan) if args.format == "markdown" else render_json(plan)
        if args.output:
            destination = _output_path(root, args.output)
            if destination.exists():
                raise ValueError("--output already exists; refusing to overwrite it")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] Adoption planner could not complete: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
