from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as etree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "examples" / "demo" / "run_visual_proof.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("demo_visual_proof", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def repository_state() -> tuple[str, object]:
    result = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode == 0:
        return "git", result.stdout
    git_pointer = ROOT / ".git"
    pointer_text = git_pointer.read_text(encoding="utf-8", errors="replace") if git_pointer.is_file() else ""
    if not pointer_text.startswith("gitdir: ") or ":/" not in pointer_text.replace("\\", "/"):
        raise AssertionError(f"unexpected Git status failure: {result.stderr}")
    snapshot = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        snapshot.append((path.relative_to(ROOT).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest()))
    return "windows-worktree-pointer-filesystem-fallback", snapshot


class DemoVisualProofTest(unittest.TestCase):
    def test_published_assets_are_sanitized_and_valid(self) -> None:
        asset_dir = ROOT / "docs" / "assets" / "demo"
        transcript = (asset_dir / "visual-proof-transcript.txt").read_text(encoding="utf-8")
        for value in ("/home/", "/tmp/", "C:\\Users\\", "api_key", "token", "secret", "password"):
            self.assertNotIn(value, transcript)
        self.assertNotIn("closure_evaluator.close(...", (asset_dir / "visual-proof.svg").read_text(encoding="utf-8"))
        etree.parse(asset_dir / "visual-proof.svg")

    def test_default_run_uses_temporary_output_without_repo_changes(self) -> None:
        before = repository_state()
        result = subprocess.run([sys.executable, str(RUNNER)], cwd=ROOT, text=True, capture_output=True, check=False, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(0, result.returncode, result.stderr)
        output = Path(result.stdout.strip().split(": ", 1)[1]).parent
        try:
            self.assertFalse(str(output).startswith(str(ROOT)))
            summary = json.loads((output / "visual-proof-summary.json").read_text(encoding="utf-8"))
            self.assertEqual([("BLOCKED", 3), ("BLOCKED", 3), ("CLOSED", 0)], [(item["status"], item["exit_code"]) for item in summary["scenarios"]])
            self.assertEqual(["BLOCKED", "PASS", "PASS"], [item["guard"]["status"] for item in summary["scenarios"]])
        finally:
            shutil.rmtree(output)
        after = repository_state()
        self.assertEqual(before, after)

    def test_real_test_failure_produces_failed_verification_and_nonzero_runner(self) -> None:
        runner = load_runner()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "proof"
            self.assertEqual(1, runner.run_demo(output, force_test_failure=True))
            summary = json.loads((output / "visual-proof-summary.json").read_text(encoding="utf-8"))
            failed = summary["scenarios"][2]
            self.assertEqual("FAIL", failed["test"]["status"])
            self.assertEqual("FAILED", failed["closure"]["verification"])
            self.assertEqual("FAILED", failed["status"])
            self.assertNotEqual(0, failed["exit_code"])
            self.assertIn("intentional synthetic test failure", failed["test"]["summary"])

    def test_publish_mode_is_explicit_and_output_inside_repo_requires_it(self) -> None:
        runner = load_runner()
        with tempfile.TemporaryDirectory() as temporary:
            fake_root = Path(temporary) / "repository"
            fake_root.mkdir()
            self.assertEqual(fake_root / "docs" / "assets" / "demo", runner.select_output(None, True, fake_root))
            with self.assertRaises(ValueError):
                runner.select_output(fake_root / "docs" / "assets" / "demo", False, fake_root)

    def test_demo_and_readmes_use_consistent_platform_guidance(self) -> None:
        demo = (ROOT / "docs" / "DEMO.md").read_text(encoding="utf-8")
        self.assertIn("python examples/demo/run_visual_proof.py", demo)
        self.assertIn("python3 examples/demo/run_visual_proof.py", demo)
        self.assertIn("--publish-assets", demo)
        for path in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
            self.assertIn("[Demo](docs/DEMO.md)", path.read_text(encoding="utf-8"))

    def test_published_transcript_uses_platform_neutral_python_label(self) -> None:
        transcript = (ROOT / "docs" / "assets" / "demo" / "visual-proof-transcript.txt").read_text(encoding="utf-8")
        self.assertNotIn("test_command: python -m unittest discover -s tests", transcript)
        self.assertEqual(2, transcript.count("test_command: <current-python> -m unittest discover -s tests"))


if __name__ == "__main__":
    unittest.main()
