from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

from governance.audit.checks import run_audit

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DOCS = (
    ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "docs" / "GETTING_STARTED.md",
    ROOT / "docs" / "ADOPTION_AUDIT.md", ROOT / "docs" / "PRESETS.md", ROOT / "docs" / "examples" / "README.md",
)
BAD_FRAGMENTS = ("\ufffd", "Ã", "Â", "â€", "ðŸ")


class PublicAdoptionAssetsTest(unittest.TestCase):
    def test_public_docs_are_utf8_without_mojibake(self) -> None:
        for path in PUBLIC_DOCS:
            text = path.read_text(encoding="utf-8")
            self.assertFalse(any(fragment in text for fragment in BAD_FRAGMENTS), path)

    def test_docs_reference_real_public_entrypoints(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_DOCS)
        self.assertIn("scripts/agent_audit.py", text)
        self.assertIn("scripts/init_new_project.py", text)
        self.assertTrue((ROOT / "scripts" / "agent_audit.py").is_file())

    def test_issue_forms_are_parseable(self) -> None:
        for path in (ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml"):
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertIsInstance(value, dict, path)

    def test_python_demo_recommends_standard(self) -> None:
        result = run_audit(ROOT / "docs" / "examples" / "python-minimal")
        self.assertEqual("standard", result.recommended_preset)


    def test_public_internal_links_and_community_files_exist(self) -> None:
        for path in PUBLIC_DOCS:
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
                if "://" in target or target.startswith("mailto:"):
                    continue
                self.assertTrue((path.parent / target).resolve().is_file(), f"{path}: {target}")
        required = (
            "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
            ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml", ".github/ISSUE_TEMPLATE/adoption_feedback.yml",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
