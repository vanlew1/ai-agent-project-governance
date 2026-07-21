from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from governance.adoption import provenance
from governance.errors import SchemaValidationError


class GitHeadBlobProvenanceTest(unittest.TestCase):
    def setUp(self) -> None:
        provenance._head_blob_digest.cache_clear()
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
        provenance._head_blob_digest.cache_clear()
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

    def test_repeated_same_head_uses_cached_blob_digest(self) -> None:
        expected = self.expected_digest_from_head()
        self.assertEqual(expected, provenance.generator_source_digest(root=self.root))
        first = provenance._head_blob_digest.cache_info()
        self.assertEqual(expected, provenance.generator_source_digest(root=self.root))
        second = provenance._head_blob_digest.cache_info()
        self.assertEqual(1, first.misses)
        self.assertEqual(first.misses, second.misses)
        self.assertEqual(first.hits + 1, second.hits)

    def test_cache_hit_rechecks_head_status_and_tracked_inputs(self) -> None:
        calls: list[tuple[str, ...]] = []
        original = provenance._run_git

        def recorded(root: Path, *args: str, **kwargs) -> subprocess.CompletedProcess[bytes]:
            calls.append(args)
            return original(root, *args, **kwargs)

        with mock.patch.object(provenance, "_run_git", side_effect=recorded):
            provenance.generator_source_digest(root=self.root)
            calls.clear()
            provenance.generator_source_digest(root=self.root)
        self.assertIn(("rev-parse", "HEAD"), calls)
        self.assertIn(("status", "--porcelain=v1", "--untracked-files=no", "--", *provenance.GENERATOR_INPUTS), calls)
        self.assertIn(("ls-files", "--error-unmatch", "--", *provenance.GENERATOR_INPUTS), calls)
        self.assertNotIn(("cat-file", "--batch"), calls)

    def test_batched_blob_failure_fails_closed(self) -> None:
        original = provenance._run_git

        def failing_batch(root: Path, *args: str, **kwargs) -> subprocess.CompletedProcess[bytes]:
            if args == ("cat-file", "--batch"):
                return subprocess.CompletedProcess(["git"], 1, b"", b"batch failure")
            return original(root, *args, **kwargs)

        with mock.patch.object(provenance, "_run_git", side_effect=failing_batch):
            with self.assertRaisesRegex(ValueError, "batch read failed"):
                provenance.generator_source_digest(root=self.root)

    def test_head_input_contract_and_repository_change_invalidate_cache(self) -> None:
        first = provenance.generator_source_digest(root=self.root)
        self.assertEqual(1, provenance._head_blob_digest.cache_info().misses)
        source = self.root / provenance.GENERATOR_INPUTS[2]
        source.write_text("changed\n", encoding="utf-8")
        self.git("add", provenance.GENERATOR_INPUTS[2])
        self.git("commit", "-m", "change generator source")
        self.assertNotEqual(first, provenance.generator_source_digest(root=self.root))
        self.assertEqual(2, provenance._head_blob_digest.cache_info().misses)

        provenance.generator_source_digest(root=self.root, inputs=tuple(reversed(provenance.GENERATOR_INPUTS)))
        self.assertEqual(3, provenance._head_blob_digest.cache_info().misses)
        original_version = provenance.GENERATOR_SOURCE_CONTRACT_VERSION
        try:
            provenance.GENERATOR_SOURCE_CONTRACT_VERSION = original_version + 1
            provenance.generator_source_digest(root=self.root)
            self.assertEqual(4, provenance._head_blob_digest.cache_info().misses)
        finally:
            provenance.GENERATOR_SOURCE_CONTRACT_VERSION = original_version

        bare = Path(self.temp_dir.name) / "repository.git"
        clone = Path(self.temp_dir.name) / "other-repository"
        subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True, capture_output=True)
        subprocess.run(["git", "clone", str(bare), str(clone)], check=True, capture_output=True)
        provenance.generator_source_digest(root=clone)
        self.assertEqual(5, provenance._head_blob_digest.cache_info().misses)

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

    def test_dirty_or_staged_generator_source_fails_closed_even_with_cached_digest(self) -> None:
        provenance.generator_source_digest(root=self.root)
        self.assertEqual(1, provenance._head_blob_digest.cache_info().misses)
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
