from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from governance.adoption import provenance
from governance.errors import SchemaValidationError


class GitHeadBlobProvenanceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "repository"
        self.root.mkdir()
        for relative_path in provenance.GENERATOR_INPUTS:
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{relative_path}\n", encoding="utf-8", newline="\n")
        self.git("init")
        self.git("config", "user.email", "provenance-test@example.invalid")
        self.git("config", "user.name", "Provenance Test")
        self.git("add", ".")
        self.git("commit", "-m", "initial generator sources")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(cwd or self.root), *args],
            check=True,
            capture_output=True,
        )

    def expected_digest_from_head(self, root: Path | None = None) -> str:
        repository = root or self.root
        rows = {
            path: hashlib.sha256(self.git("show", f"HEAD:{path}", cwd=repository).stdout).hexdigest()
            for path in provenance.GENERATOR_INPUTS
        }
        return provenance.canonical_digest(rows)

    def test_digest_comes_from_head_blobs_and_is_order_stable(self) -> None:
        expected = self.expected_digest_from_head()
        self.assertEqual(expected, provenance.generator_source_digest(root=self.root))
        self.assertEqual(
            expected,
            provenance.generator_source_digest(root=self.root, inputs=tuple(reversed(provenance.GENERATOR_INPUTS))),
        )

    def test_clean_crlf_and_lf_checkouts_of_one_commit_match(self) -> None:
        source = self.root
        bare = Path(self.temp_dir.name) / "repository.git"
        lf = Path(self.temp_dir.name) / "lf"
        crlf = Path(self.temp_dir.name) / "crlf"
        subprocess.run(["git", "clone", "--bare", str(source), str(bare)], check=True, capture_output=True)
        subprocess.run(["git", "clone", str(bare), str(lf)], check=True, capture_output=True)
        subprocess.run(["git", "clone", str(bare), str(crlf)], check=True, capture_output=True)
        self.git("config", "core.autocrlf", "false", cwd=lf)
        self.git("config", "core.autocrlf", "true", cwd=crlf)
        self.git("reset", "--hard", "HEAD", cwd=lf)
        self.git("reset", "--hard", "HEAD", cwd=crlf)

        self.assertNotIn(b"\r\n", (lf / "VERSION").read_bytes())
        self.assertIn(b"\r\n", (crlf / "VERSION").read_bytes())
        self.assertEqual(provenance.generator_source_digest(root=lf), provenance.generator_source_digest(root=crlf))

    def test_dirty_or_staged_generator_source_fails_closed(self) -> None:
        source = self.root / provenance.GENERATOR_INPUTS[1]
        source.write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "working tree is dirty"):
            provenance.generator_source_digest(root=self.root)
        self.git("add", provenance.GENERATOR_INPUTS[1])
        with self.assertRaisesRegex(ValueError, "index contains staged"):
            provenance.generator_source_digest(root=self.root)

    def test_missing_untracked_and_non_git_inputs_fail_closed(self) -> None:
        untracked = self.root / "untracked.py"
        untracked.write_text("untracked\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not tracked"):
            provenance.generator_source_digest(root=self.root, inputs=("untracked.py",))
        with self.assertRaisesRegex(ValueError, "not tracked"):
            provenance.generator_source_digest(root=self.root, inputs=("missing.py",))

        non_git = Path(self.temp_dir.name) / "non-git"
        non_git.mkdir()
        (non_git / "input.py").write_text("value\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Git provenance unavailable"):
            provenance.generator_source_digest(root=non_git, inputs=("input.py",))

    def test_source_change_in_a_new_commit_changes_digest(self) -> None:
        first = provenance.generator_source_digest(root=self.root)
        source = self.root / provenance.GENERATOR_INPUTS[2]
        source.write_text("changed\n", encoding="utf-8")
        self.git("add", provenance.GENERATOR_INPUTS[2])
        self.git("commit", "-m", "change generator source")
        self.assertNotEqual(first, provenance.generator_source_digest(root=self.root))

    def test_legacy_receipt_without_v2_contract_fields_is_rejected(self) -> None:
        legacy = {
            "schema_version": "1.0",
            "binding_type": "TOOLCHAIN_PROVENANCE_BINDING",
            "generator_id": "ai-agent-project-governance-planner",
            "generator_version": "1.2.0",
            "generator_source_digest": "0" * 64,
            "generation_path": provenance.PUBLIC_GENERATION_PATH,
            "generation_command_contract_digest": "0" * 64,
            "formal_scope_input_digest": "0" * 64,
            "formal_scope_normalized_text_digest": "0" * 64,
            "target_identity": {},
            "target_branch": "main",
            "target_head": "0" * 40,
            "framework_commit": "0" * 40,
            "plan_payload_digest": "0" * 64,
            "generated_at": "2026-07-21T00:00:00+00:00",
        }
        legacy["provenance_receipt_digest"] = provenance.canonical_digest(legacy)
        with self.assertRaisesRegex(SchemaValidationError, "generator_source_basis"):
            provenance.validate_provenance_receipt({"plan_digest": "0" * 64, "provenance_receipt": legacy}, require_public_cli=True)


if __name__ == "__main__":
    unittest.main()
