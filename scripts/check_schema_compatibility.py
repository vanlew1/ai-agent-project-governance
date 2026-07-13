"""Read-only P5 compatibility checks for stable governance schemas."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator

def parse_args():
    parser = argparse.ArgumentParser(description="Check governance schema compatibility")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()

def at_pointer(value, pointer):
    if pointer == "/": return value
    for part in pointer.split("/")[1:]:
        value = value[int(part)] if isinstance(value, list) and part.isdigit() and int(part) < len(value) else value.get(part, {}) if isinstance(value, dict) else {}
    return value

def main() -> int:
    root = parse_args().root.resolve()
    try:
        baseline = json.loads((root / "tests/fixtures/compatibility/schema_baseline.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Schema compatibility: ERROR ({exc})")
        return 1
    errors = []
    schemas = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in (root / "schemas").glob("*.schema.json")}
    if set(schemas) != set(baseline): errors.append("Schema file set differs from compatibility baseline")
    ids = set()
    for name, expected in baseline.items():
        schema = schemas.get(name)
        if schema is None: continue
        try: Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"Invalid {name}: {exc}"); continue
        if schema.get("additionalProperties") is not False: errors.append(f"{name} no longer rejects extra fields")
        if schema.get("$id") in ids: errors.append(f"Duplicate $id: {schema.get('$id')}")
        ids.add(schema.get("$id"))
        if schema.get("required", []) != expected["required"]: errors.append(f"{name} required fields differ from baseline")
        for pointer, values in expected.get("enums", {}).items():
            actual = at_pointer(schema, pointer).get("enum", [])
            if not set(values).issubset(actual): errors.append(f"{name} removed enum values for {pointer}")
        for pointer, expected_type in expected.get("types", {}).items():
            if at_pointer(schema, pointer).get("type") != expected_type: errors.append(f"{name} changed type for {pointer}")
    phase = schemas.get("rules_index.schema.json", {}).get("properties", {}).get("governance_runtime", {}).get("properties", {}).get("phase", {}).get("enum", [])
    if not {"PHASE_5_SELF_VALIDATION_AND_CI", "PHASE_6_MULTI_AGENT_ORCHESTRATION"}.issubset(phase): errors.append("P5 runtime phase is absent")
    if errors:
        print(f"Schema compatibility: FAIL ({len(errors)} issue(s))")
        print("\n".join(f"- {error}" for error in errors))
        return 2
    print(f"Schema compatibility: PASS ({len(schemas)} schemas, stable fields and enums)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
