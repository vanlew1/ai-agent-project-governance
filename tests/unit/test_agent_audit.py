from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from governance.audit.checks import _read_text, run_audit
from governance.audit.renderer import render_json, render_text

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "agent_audit.py"


class AgentAuditTest(unittest.TestCase):
    def _project(self, root: Path, *, high_risk: bool = False) -> None:
        (root / "AGENTS.md").write_text(
            "Allowed scope: src/ only. Do not push. Run tests and report closure.\n"
            + ("External API and production access require approval.\n" if high_risk else ""),
            encoding="utf-8",
        )
        (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
        (root / "tests").mkdir()
        (root / ".gitignore").write_text(".env\n*.pem\n*.key\n", encoding="utf-8")

    def test_minimal_project_is_deterministic_and_recommends_lightweight(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            first = run_audit(root)
            second = run_audit(root)
            self.assertEqual(first.to_dict(), second.to_dict())
            self.assertEqual("lightweight", first.recommended_preset)
            self.assertEqual(first.to_dict(), json.loads(render_json(first)))
            self.assertIn("Recommended preset: lightweight", render_text(first))

    def test_high_risk_context_recommends_strict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self._project(Path(temporary), high_risk=True)
            self.assertEqual("strict", run_audit(Path(temporary)).recommended_preset)

    def test_cli_default_is_read_only_and_output_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            before = sorted(path.relative_to(root) for path in root.rglob("*"))
            normal = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(root), "--format", "json"], capture_output=True, text=True, check=False)
            self.assertEqual(0, normal.returncode, normal.stderr)
            self.assertEqual(before, sorted(path.relative_to(root) for path in root.rglob("*")))
            payload = json.loads(normal.stdout)
            self.assertEqual("1.0", payload["schema_version"])
            output = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(root), "--output", "reports/audit.txt"], capture_output=True, text=True, check=False)
            self.assertEqual(0, output.returncode, output.stderr)
            self.assertTrue((root / "reports" / "audit.txt").is_file())

    def test_cli_rejects_invalid_root_and_output_escape(self) -> None:
        missing = subprocess.run([sys.executable, str(SCRIPT), "--project-root", "does-not-exist"], capture_output=True, text=True, check=False)
        self.assertEqual(2, missing.returncode)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            escaped = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(root), "--output", "../outside.json"], capture_output=True, text=True, check=False)
            self.assertEqual(3, escaped.returncode)

    def test_strict_returns_nonzero_only_for_failed_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            (root / "README.md").write_text("broken \ufffd", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(root), "--strict"], capture_output=True, text=True, check=False)
            self.assertEqual(4, result.returncode, result.stderr)


    def test_empty_node_and_unicode_path_projects_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            empty = base / "empty"
            empty.mkdir()
            self.assertEqual("empty", run_audit(empty).project_root_display)

            node = base / "\u4e2d\u6587 node project"
            node.mkdir()
            (node / "AGENTS.md").write_text("Allowed scope: src/. Do not push. Run tests and report closure.\n", encoding="utf-8")
            (node / "package.json").write_text('{"scripts": {"test": "node --test"}}', encoding="utf-8")
            result = run_audit(node)
            self.assertEqual("\u4e2d\u6587 node project", result.project_root_display)
            self.assertEqual("PASS", next(check.status for check in result.checks if check.check_id == "adapter_signal"))

    def test_large_binary_and_permission_limited_documents_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            docs = root / "docs"
            docs.mkdir()
            (docs / "binary.md").write_bytes(b"\xff\xfe\x00")
            (docs / "large.md").write_bytes(b"x" * (129 * 1024))
            result = run_audit(root)
            encoding = next(check for check in result.checks if check.check_id == "document_encoding")
            self.assertEqual("WARN", encoding.status)
            with patch("pathlib.Path.read_text", side_effect=PermissionError):
                self.assertEqual((None, "unreadable or non-UTF-8"), _read_text(docs / "locked.md"))

    def test_json_contract_and_text_renderer_share_the_result_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            result = run_audit(root)
            payload = json.loads(render_json(result))
            self.assertTrue({"schema_version", "tool_version", "project_root_display", "score", "level", "recommended_preset", "checks"}.issubset(payload))
            allowed_statuses = {"PASS", "WARN", "FAIL", "NOT_APPLICABLE", "SKIPPED"}
            self.assertTrue(all(check["status"] in allowed_statuses for check in payload["checks"]))
            rendered = render_text(result)
            for check in result.checks:
                self.assertIn(f"[{check.status}] {check.check_id}", rendered)

    def test_current_repository_completes_without_accessing_network(self) -> None:
        result = run_audit(ROOT)
        self.assertEqual(ROOT.name, result.project_root_display)
        self.assertEqual(10, len(result.checks))


if __name__ == "__main__":
    unittest.main()
