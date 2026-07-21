#!/usr/bin/env python3
"""Generate offline, sanitized proof for the public governance walkthrough."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as etree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLISHED_ASSETS = ROOT / "docs" / "assets" / "demo"
TEST_COMMAND = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]

PROJECT_STATE = {
    "schema_version": "1.0",
    "project_mode": "EXECUTION",
    "architecture_status": "confirmed",
    "implementation_plan_status": "confirmed",
    "repository_root": ".",
    "adapter": "generic",
    "high_risk_paths": [],
    "default_forbidden_operations": [],
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def contract(task_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "task_id": task_id,
        "project_mode": "EXECUTION",
        "task_level": "A",
        "status": "READY",
        "objective": ["Local synthetic governance proof"],
        "read_scope": ["src/", "tests/"],
        "write_scope": {"allow": ["src/"], "deny": ["restricted-change.txt"]},
        "autonomy": {
            "may_debug_test_failures": True,
            "may_edit_adjacent_tests": True,
            "may_edit_same_module_helpers": "conditional",
            "must_not_expand_architecture": True,
        },
        "stop_conditions": [],
        "verification": {"level_1": [], "level_2": [], "level_3": []},
        "report": {"format": "compact", "fields": ["tests"]},
    }


def setup_synthetic_repo(root: Path, task_id: str) -> None:
    root.mkdir()
    subprocess.run(["git", "init", "--quiet"], cwd=root, check=True, capture_output=True)
    (root / ".git" / "info" / "exclude").write_text(".agent_state/\ntests/\n", encoding="utf-8")
    write_json(root / ".agent_state" / "project_state.yaml", PROJECT_STATE)
    write_json(root / ".agent_state" / "active_task.yaml", contract(task_id))


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    import os
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", capture_output=True, check=False, env=env)


def sanitize(value: str, synthetic_root: Path) -> str:
    return value.replace(str(ROOT), "<repository>").replace(str(synthetic_root), "<synthetic-root>").strip()


def output_summary(process: subprocess.CompletedProcess[str], synthetic_root: Path) -> str:
    text = sanitize(f"{process.stdout}\n{process.stderr}", synthetic_root)
    return "\n".join(text.splitlines()[-8:]) or "(no output)"


def yaml_value(output: str, key: str) -> str:
    for line in output.splitlines():
        if line.startswith(f"{key}: "):
            return line.split(": ", 1)[1].strip()
    raise RuntimeError(f"Expected {key!r} in Guard output")


def yaml_list_value(output: str, key: str) -> str:
    lines = output.splitlines()
    for index, line in enumerate(lines):
        if line == f"{key}:" and index + 1 < len(lines) and lines[index + 1].startswith("- "):
            return f"{key}: [{lines[index + 1][2:]}]"
    raise RuntimeError(f"Expected non-empty {key!r} in Guard output")


def guard_result(root: Path) -> dict[str, object]:
    result = run([sys.executable, str(ROOT / "scripts" / "agent_guard.py"), "check"], root)
    try:
        status = yaml_value(result.stdout, "status")
        evidence = yaml_list_value(result.stdout, "denied_changes") if status == "BLOCKED" else "Guard completed."
    except RuntimeError:
        status = "ERROR"
        evidence = output_summary(result, root)
    return {"exit_code": result.returncode, "status": status, "summary": output_summary(result, root), "evidence": evidence}


def test_result(root: Path) -> dict[str, object]:
    result = run(TEST_COMMAND, root)
    return {
        "command_id": "synthetic-unittest",
        "command": "python -m unittest discover -s tests",
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "required": True,
        "exit_code": result.returncode,
        "summary": output_summary(result, root),
    }


def closure_command(guard: dict[str, object], test: dict[str, object], stale: bool) -> list[str]:
    payload = json.dumps({"guard_status": guard["status"], "test": test, "stale": stale})
    code = textwrap.dedent(
        """
        import json
        import sys
        from governance.verification.closure_evaluator import close
        from governance.verification.test_planner import create
        from governance.verification.verification_builder import build

        payload = json.loads(sys.argv[1])
        contract = {"task_id": "DEMO-CLOSURE", "task_level": "A"}
        plan = create(contract, {"status": payload["guard_status"]})
        verification = build(contract, {"status": payload["guard_status"]}, plan, [payload["test"]])
        closure = close(verification, stale=payload["stale"])
        print(json.dumps({"verification": verification["completion_status"], "closure": closure["status"], "reasons": closure["reasons"]}))
        raise SystemExit({"CLOSED": 0, "PARTIAL": 2, "BLOCKED": 3, "FAILED": 4}[closure["status"]])
        """
    )
    return [sys.executable, "-c", code, payload]


def closure_result(root: Path, guard: dict[str, object], test: dict[str, object], stale: bool) -> dict[str, object]:
    result = run(closure_command(guard, test, stale), ROOT)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Closure did not produce JSON: {result.stderr}") from exc
    return {"exit_code": result.returncode, **output, "summary": output_summary(result, root)}


def write_synthetic_test(root: Path, filename: str, source: str) -> None:
    test_dir = root / "tests"
    test_dir.mkdir()
    (test_dir / filename).write_text(source, encoding="utf-8")


def run_scenarios(workspace: Path, force_test_failure: bool = False) -> list[dict[str, object]]:
    scope_root = workspace / "scope-block"
    setup_synthetic_repo(scope_root, "DEMO-SCOPE-BLOCK")
    (scope_root / "restricted-change.txt").write_text("synthetic: true\n", encoding="utf-8")
    scope_guard = guard_result(scope_root)

    stale_root = workspace / "stale-closure"
    setup_synthetic_repo(stale_root, "DEMO-STALE-CLOSURE")
    (stale_root / "src").mkdir()
    (stale_root / "src" / "before_verification.py").write_text("value = 1\n", encoding="utf-8")
    stale_guard = guard_result(stale_root)
    write_synthetic_test(stale_root, "test_local_change.py", "import unittest\n\nclass LocalChangeTest(unittest.TestCase):\n    def test_local_change(self):\n        self.assertTrue(True)\n")
    stale_test = test_result(stale_root)
    (stale_root / "src" / "changed_after_verification.py").write_text("value = 2\n", encoding="utf-8")
    stale_closure = closure_result(stale_root, stale_guard, stale_test, stale=True)

    closed_root = workspace / "verified-closure"
    setup_synthetic_repo(closed_root, "DEMO-VERIFIED-CLOSURE")
    (closed_root / "src").mkdir()
    (closed_root / "src" / "compliant_change.py").write_text("value = 1\n", encoding="utf-8")
    closed_guard = guard_result(closed_root)
    assertion = "self.fail('intentional synthetic test failure')" if force_test_failure else "self.assertTrue((Path(__file__).parents[1] / 'src' / 'compliant_change.py').is_file())"
    write_synthetic_test(closed_root, "test_compliant_change.py", f"import unittest\nfrom pathlib import Path\n\nclass CompliantChangeTest(unittest.TestCase):\n    def test_change(self):\n        {assertion}\n")
    closed_test = test_result(closed_root)
    closed_closure = closure_result(closed_root, closed_guard, closed_test, stale=False)

    return [
        {"id": "scope_blocked", "title": "Out-of-scope change is blocked", "command": "Guard check", "guard": scope_guard, "test": None, "closure": None, "status": scope_guard["status"], "exit_code": scope_guard["exit_code"], "evidence": scope_guard["evidence"]},
        {"id": "stale_verification_blocked", "title": "Stale verification cannot close", "command": "Test + stale closure", "guard": stale_guard, "test": stale_test, "closure": stale_closure, "status": stale_closure["closure"], "exit_code": stale_closure["exit_code"], "evidence": f"reasons: {stale_closure['reasons']}"},
        {"id": "verified_closure_closed", "title": "Fresh verification closes the task", "command": "Test + fresh closure", "guard": closed_guard, "test": closed_test, "closure": closed_closure, "status": closed_closure["closure"], "exit_code": closed_closure["exit_code"], "evidence": "fresh evidence accepted" if closed_closure["closure"] == "CLOSED" else f"reasons: {closed_closure['reasons']}"},
    ]


def transcript(scenarios: list[dict[str, object]]) -> str:
    lines = [
        "AGC UX Demo: real local visual proof",
        "Environment: Windows PowerShell uses python; Linux, WSL, and macOS use python3.",
        "Default mode writes only to a new temporary output directory; --publish-assets is maintainer-only.",
    ]
    for index, scenario in enumerate(scenarios, start=1):
        guard = scenario["guard"]
        lines.extend(["", f"[{index}] {scenario['title']}", f"command: {scenario['command']}", f"guard_exit_code: {guard['exit_code']}", f"guard_status: {guard['status']}"])
        if scenario["test"]:
            test = scenario["test"]
            closure = scenario["closure"]
            lines.extend([f"test_command: {test['command']}", f"test_exit_code: {test['exit_code']}", f"test_status: {test['status']}", f"test_summary: {test['summary']}", f"closure_exit_code: {closure['exit_code']}", f"verification: {closure['verification']}"])
        lines.extend([f"status: {scenario['status']}", str(scenario["evidence"])])
    return "\n".join(lines) + "\n"


def render_svg(scenarios: list[dict[str, object]], output: Path) -> None:
    colors = {"BLOCKED": "#fecaca", "CLOSED": "#bbf7d0", "FAILED": "#fed7aa", "ERROR": "#fed7aa"}
    cards = []
    for index, scenario in enumerate(scenarios):
        y = 96 + index * 158
        cards.extend([
            f'<rect x="20" y="{y}" width="560" height="134" rx="12" fill="#1f2937"/>',
            f'<text class="title" x="44" y="{y + 36}">{html.escape(str(scenario["title"]))}</text>',
            f'<text class="body" x="44" y="{y + 66}">Command: {html.escape(str(scenario["command"]))}</text>',
            f'<text class="body" x="44" y="{y + 94}">Exit: {scenario["exit_code"]} · Status:</text>',
            f'<text class="status" x="260" y="{y + 94}" fill="{colors.get(str(scenario["status"]), "#d1d5db")}">{html.escape(str(scenario["status"]))}</text>',
            f'<text class="reason" x="44" y="{y + 120}">{html.escape(str(scenario["evidence"]))}</text>',
        ])
    svg = "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600" role="img" aria-labelledby="title description">',
        '<title id="title">AGC UX Demo local governance proof</title>',
        '<desc id="description">Three synthetic local scenarios: an out-of-scope change is blocked, stale verification is blocked, and fresh verification closes successfully.</desc>',
        '<rect width="100%" height="100%" rx="16" fill="#111827"/>',
        '<style>.heading{font:700 25px ui-sans-serif,system-ui,sans-serif;fill:#f9fafb}.title{font:700 20px ui-sans-serif,system-ui,sans-serif;fill:#f9fafb}.body{font:18px ui-sans-serif,system-ui,sans-serif;fill:#d1d5db}.status{font:700 20px ui-sans-serif,system-ui,sans-serif}.reason{font:17px ui-sans-serif,system-ui,sans-serif;fill:#d1d5db}</style>',
        '<text class="heading" x="24" y="52">Local governance proof</text>',
        '<text class="body" x="24" y="78">Synthetic, offline, and generated from local commands.</text>',
        *cards,
        '</svg>',
    ])
    etree.fromstring(svg)
    output.write_text(svg + "\n", encoding="utf-8")


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def select_output(output_dir: Path | None, publish_assets: bool, root: Path = ROOT) -> Path:
    if publish_assets:
        if output_dir is not None:
            raise ValueError("--publish-assets cannot be combined with --output-dir")
        return root / "docs" / "assets" / "demo"
    if output_dir is None:
        return Path(tempfile.mkdtemp(prefix="agc-demo-visual-proof-03-output-"))
    output = output_dir.resolve()
    if is_within(output, root):
        raise ValueError("Default demo output must be outside the repository; use --publish-assets for published assets")
    return output


def run_demo(output: Path, force_test_failure: bool = False) -> int:
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="agc-demo-visual-proof-03-") as temporary:
        scenarios = run_scenarios(Path(temporary), force_test_failure=force_test_failure)
    text = transcript(scenarios)
    (output / "visual-proof-transcript.txt").write_text(text, encoding="utf-8")
    write_json(output / "visual-proof-summary.json", {"synthetic": True, "scenarios": scenarios})
    render_svg(scenarios, output / "visual-proof.svg")
    expected = [("scope_blocked", "BLOCKED", 3), ("stale_verification_blocked", "BLOCKED", 3), ("verified_closure_closed", "CLOSED", 0)]
    actual = [(item["id"], item["status"], item["exit_code"]) for item in scenarios]
    return 0 if actual == expected else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate sanitized local governance demo proof.")
    parser.add_argument("--output-dir", type=Path, help="Temporary output directory outside this repository.")
    parser.add_argument("--publish-assets", action="store_true", help="Explicit maintainer mode: write docs/assets/demo/.")
    args = parser.parse_args()
    try:
        output = select_output(args.output_dir, args.publish_assets)
    except ValueError as exc:
        parser.error(str(exc))
    status = run_demo(output)
    print(f"Generated visual proof: {output / 'visual-proof.svg'}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
