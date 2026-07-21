"""Fixed, read-only local release gate shared with GitHub Actions."""
from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
GATE_TIMEOUT_SECONDS = 300
DEFAULT_TEST_TIMEOUT_SECONDS = 600
MIN_TEST_TIMEOUT_SECONDS = 60
MAX_TEST_TIMEOUT_SECONDS = 3600
RELEASE_GATE_CONFIG = ROOT / "config" / "release_gate.yaml"
GATES = (
    ("governance", [PY, "scripts/validate_governance.py"]),
    ("schema-compatibility", [PY, "scripts/check_schema_compatibility.py"]),
    ("runtime-dependencies", [PY, "scripts/check_runtime_dependencies.py"]),
    ("bootstrap", [PY, "scripts/check_template_integrity.py"]),
    ("ci-security", [PY, "scripts/check_ci_security.py"]),
    ("tests", [PY, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
    ("quality", [PY, "scripts/check_code_quality.py"]),
    ("syntax", [PY, "scripts/check_python_syntax.py"]),
)


@dataclass(frozen=True)
class TimeoutPolicy:
    seconds: int
    source: str


def load_test_timeout_policy(config_path: Path = RELEASE_GATE_CONFIG) -> TimeoutPolicy:
    if not config_path.exists():
        return TimeoutPolicy(DEFAULT_TEST_TIMEOUT_SECONDS, "framework_default")
    try:
        value = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"invalid release gate config: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema_version", "release_gate"}:
        raise ValueError("release gate config must contain only schema_version and release_gate")
    if value["schema_version"] != "1.0":
        raise ValueError("release gate config schema_version must be 1.0")
    release_gate = value["release_gate"]
    if not isinstance(release_gate, dict) or set(release_gate) != {"test_timeout_seconds"}:
        raise ValueError("release_gate must contain only test_timeout_seconds")
    seconds = release_gate["test_timeout_seconds"]
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise ValueError("test_timeout_seconds must be an integer")
    if not MIN_TEST_TIMEOUT_SECONDS <= seconds <= MAX_TEST_TIMEOUT_SECONDS:
        raise ValueError(
            f"test_timeout_seconds must be between {MIN_TEST_TIMEOUT_SECONDS} and {MAX_TEST_TIMEOUT_SECONDS}"
        )
    return TimeoutPolicy(seconds, "framework_config")


def run(name, argv, *, timeout_seconds=GATE_TIMEOUT_SECONDS, timeout_source="gate_default"):
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be a positive finite integer")
    started = time.monotonic()
    command = subprocess.list2cmdline(argv)
    try:
        result = subprocess.run(
            argv,
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - started
        print(
            f"{name}: TIMEOUT elapsed_seconds={elapsed:.1f} "
            f"effective_timeout_seconds={timeout_seconds} timeout_source={timeout_source} "
            f"timeout_result=TIMEOUT exit_classification=TIMEOUT command={command}"
        )
        return False
    except OSError as exc:
        elapsed = time.monotonic() - started
        print(
            f"{name}: ERROR ({exc}) elapsed_seconds={elapsed:.1f} "
            f"effective_timeout_seconds={timeout_seconds} timeout_source={timeout_source} "
            f"timeout_result=NOT_STARTED exit_classification=ERROR command={command}"
        )
        return False
    elapsed = time.monotonic() - started
    summary = (result.stdout or result.stderr).strip().splitlines()
    detail = summary[-1] if summary else "no output"
    classification = "PASS" if result.returncode == 0 else "FAIL"
    print(
        f"{name}: {classification} elapsed_seconds={elapsed:.1f} "
        f"effective_timeout_seconds={timeout_seconds} timeout_source={timeout_source} "
        f"timeout_result=COMPLETED exit_classification={classification} "
        f"command={command} detail={detail[:240]}"
    )
    return result.returncode == 0


def main():
    try:
        test_policy = load_test_timeout_policy()
    except ValueError as exc:
        print(f"Release gate configuration: ERROR ({exc}) exit_classification=CONFIGURATION_ERROR")
        return 2
    results = []
    for name, argv in GATES:
        if name == "tests":
            results.append(
                run(
                    name,
                    argv,
                    timeout_seconds=test_policy.seconds,
                    timeout_source=test_policy.source,
                )
            )
        else:
            results.append(
                run(
                    name,
                    argv,
                    timeout_seconds=GATE_TIMEOUT_SECONDS,
                    timeout_source="gate_default",
                )
            )
    status = "PASS" if all(results) else "FAIL"
    print(f"Governance release gate: {status} ({sum(results)}/{len(results)} gates)")
    return 0 if all(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
