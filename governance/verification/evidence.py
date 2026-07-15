"""Build redacted, reproducible local test-evidence records."""

from __future__ import annotations

from typing import Mapping, Sequence


def build_test_evidence(
    *,
    command: Sequence[str],
    working_directory: str,
    node_scope: str,
    marker: str | None,
    environment_variable_names: Sequence[str],
    dependency_summary: Mapping[str, str],
    basetemp: str | None,
    counts: Mapping[str, int],
    failed_nodes: Sequence[str],
    junit_path: str | None = None,
) -> dict[str, object]:
    """Return evidence without environment values, credentials, or timestamps."""
    names = tuple(environment_variable_names)
    if any("=" in name or not name for name in names):
        raise ValueError("environment_variable_names must contain names only")
    expected_counts = {"collected", "passed", "failed", "skipped", "warning"}
    if set(counts) != expected_counts or any(not isinstance(value, int) or value < 0 for value in counts.values()):
        raise ValueError("counts must include non-negative collected, passed, failed, skipped, and warning values")
    return {
        "command": list(command),
        "working_directory": working_directory,
        "node_scope": node_scope,
        "marker": marker,
        "environment_variable_names": list(names),
        "dependency_summary": dict(sorted(dependency_summary.items())),
        "basetemp": basetemp,
        "counts": dict(counts),
        "failed_nodes": list(failed_nodes),
        "junit_path": junit_path,
    }
