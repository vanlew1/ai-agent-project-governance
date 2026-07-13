"""Safe structured-input and JSON Schema loading helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator, ValidationError

from .errors import InputError, SchemaValidationError


ROOT = Path(__file__).resolve().parents[1]


def load_mapping(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON/YAML object without evaluating YAML tags."""
    if path.suffix.lower() not in {".json", ".yaml", ".yml"}:
        raise InputError(f"Unsupported input format: {path.suffix}")
    try:
        content = path.read_text(encoding="utf-8")
        value = json.loads(content) if path.suffix.lower() == ".json" else yaml.safe_load(content)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise InputError(f"Cannot read structured input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InputError(f"Structured input must be an object: {path}")
    return value


def load_schema(name: str) -> dict[str, Any]:
    path = ROOT / "schemas" / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InputError(f"Cannot load schema {name}: {exc}") from exc


def validate_mapping(value: Mapping[str, Any], schema_name: str) -> None:
    try:
        Draft202012Validator(load_schema(schema_name)).validate(dict(value))
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path) or "root"
        raise SchemaValidationError(f"{schema_name} invalid at {location}: {exc.message}") from exc
