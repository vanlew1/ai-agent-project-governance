"""Run a deterministic, offline adoption audit without modifying a project by default."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from governance.audit.checks import run_audit  # noqa: E402
from governance.audit.renderer import render_json, render_text  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only, deterministic coding-agent adoption audit")
    parser.add_argument("--project-root", type=Path, required=True, help="Local directory to inspect")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path, help="Optional report path under --project-root")
    parser.add_argument("--preset-hint", action=argparse.BooleanOptionalAction, default=True, help="Show preset recommendation (enabled by default)")
    parser.add_argument("--strict", action="store_true", help="Return 4 when any check fails")
    return parser.parse_args()


def _output_path(root: Path, value: Path) -> Path:
    output = value.expanduser()
    destination = output.resolve() if output.is_absolute() else (root / output).resolve()
    try:
        destination.relative_to(root)
    except ValueError as exc:
        raise ValueError("--output must stay inside --project-root") from exc
    return destination


def main() -> int:
    args = parse_args()
    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        print(f"[ERROR] --project-root must be an existing directory: {args.project_root}", file=sys.stderr)
        return 2
    try:
        result = run_audit(root)
        rendered = render_json(result) if args.format == "json" else render_text(result, include_preset_hint=args.preset_hint)
        if args.output:
            destination = _output_path(root, args.output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (OSError, ValueError) as exc:
        print(f"[ERROR] Audit could not complete: {exc}. Check the path and output location.", file=sys.stderr)
        return 3
    if args.strict and any(check.status == "FAIL" for check in result.checks):
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
