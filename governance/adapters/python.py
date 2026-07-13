from pathlib import Path

from .models import DetectionEvidence


class PythonAdapter:
    adapter_id = "python"
    display_name = "Python"
    _markers = ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "tox.ini", "pytest.ini")
    def detect(self, repo_root: Path) -> DetectionEvidence:
        found = [name for name in self._markers if (repo_root / name).is_file()]
        if not found:
            found = [path.name for path in sorted(repo_root.glob("*.py"))[:1]]
        return DetectionEvidence(self.adapter_id, tuple(found), len(found) * 10, tuple(f"marker:{x}" for x in found))
    def source_patterns(self): return ("**/*.py",)
    def test_patterns(self): return ("tests/**/*.py", "test_*.py", "*_test.py")
    def sensitive_path_patterns(self): return (".env", ".env.*", "migrations/**", "data/production/**", "secrets/**")
    def generated_path_patterns(self): return ("__pycache__/**", "*.pyc", ".pytest_cache/**", ".mypy_cache/**", ".ruff_cache/**", "coverage/**", "dist/**", "build/**")
    def ignored_path_patterns(self): return (".venv/**", "venv/**", ".git/**")
    def default_test_command_ids(self): return ("python-unittest-discover", "python-pytest")
    def default_quality_command_ids(self): return ("python-py-compile", "python-ruff", "python-mypy")
    def root_markers(self): return self._markers
