import json
from pathlib import Path

from .models import DetectionEvidence


class NodeAdapter:
    adapter_id = "node"
    display_name = "Node.js"
    _markers = ("package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "tsconfig.json")
    def detect(self, repo_root: Path) -> DetectionEvidence:
        found = [name for name in self._markers if (repo_root / name).is_file()]
        if not found:
            found = [path.name for path in sorted((*repo_root.glob("*.js"), *repo_root.glob("*.ts")))[:1]]
        reasons = tuple(f"marker:{x}" for x in found)
        return DetectionEvidence(self.adapter_id, tuple(found), len(found) * 10, reasons)
    def package_scripts(self, repo_root: Path) -> tuple[str, ...]:
        path = repo_root / "package.json"
        if not path.is_file() or path.stat().st_size > 1_000_000: return ()
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            scripts = value.get("scripts", {})
            return tuple(sorted(key for key, command in scripts.items() if isinstance(key, str) and isinstance(command, str)))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError): return ()
    def source_patterns(self): return ("**/*.js", "**/*.ts", "**/*.tsx")
    def test_patterns(self): return ("test/**", "tests/**", "**/*.test.js", "**/*.test.ts")
    def sensitive_path_patterns(self): return (".env", ".env.*", "node_modules/**", "secrets/**", "config/production/**")
    def generated_path_patterns(self): return ("node_modules/**", "dist/**", "build/**", "coverage/**", ".next/**", ".nuxt/**")
    def ignored_path_patterns(self): return ("node_modules/**", ".git/**")
    def default_test_command_ids(self): return ("node-npm-test",)
    def default_quality_command_ids(self): return ("node-npm-lint", "node-npm-typecheck")
    def root_markers(self): return self._markers
