"""Read-only adapter detection command."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from governance.adapters import all_adapters, detect_adapters, get  # noqa: E402
from governance.schema_loader import validate_mapping  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect the repository technology-stack adapter")
    parser.add_argument("command", choices=("detect", "list", "show"))
    parser.add_argument("adapter_id", nargs="?")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output-file", type=Path)
    args = parser.parse_args()
    if args.command == "list":
        print("\n".join(adapter.adapter_id for adapter in all_adapters()))
        return 0
    if args.command == "show":
        adapter = get(args.adapter_id or "")
        if not adapter:
            return 1
        print(yaml.safe_dump({"adapter_id": adapter.adapter_id, "display_name": adapter.display_name,
                              "root_markers": list(adapter.root_markers())}, sort_keys=False))
        return 0
    result = detect_adapters(args.root)
    value = result.to_mapping()
    validate_mapping(value, "adapter_detection.schema.json")
    text = yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    if args.output_file:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result.status == "DETECTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
