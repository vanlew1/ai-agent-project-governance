"""Stable, safe serialization for TaskContract output."""

from __future__ import annotations

import json
from typing import Any, Mapping

import yaml

from .errors import InputError


def normalize_format(value: str | None, output_name: str | None = None) -> str:
    if value:
        return value
    if output_name and output_name.lower().endswith(".json"):
        return "json"
    if output_name and output_name.lower().endswith((".yaml", ".yml")):
        return "yaml"
    return "yaml"


def dump_mapping(value: Mapping[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output_format == "yaml":
        return yaml.safe_dump(dict(value), allow_unicode=True, sort_keys=False)
    raise InputError(f"Unsupported output format: {output_format}")
