from pathlib import Path

from .models import DetectionEvidence


class WeChatMiniprogramAdapter:
    adapter_id = "wechat_miniprogram"
    display_name = "WeChat Mini Program"
    _markers = ("project.config.json", "project.private.config.json", "miniprogram", "app.json", "app.js", "app.wxss")
    def detect(self, repo_root: Path) -> DetectionEvidence:
        found = [name for name in self._markers if (repo_root / name).exists()]
        if not found:
            found = [path.name for path in sorted((*repo_root.glob("*.wxml"), *repo_root.glob("*.wxss")))[:1]]
        return DetectionEvidence(self.adapter_id, tuple(found), len(found) * 20, tuple(f"marker:{x}" for x in found))
    def source_patterns(self): return ("miniprogram/**", "**/*.wxml", "**/*.wxss")
    def test_patterns(self): return ("miniprogram/**/test/**", "tests/**")
    def sensitive_path_patterns(self): return ("project.private.config.json", "private.config.*", "cloudfunctions/**/config.json", "secrets/**")
    def generated_path_patterns(self): return ("miniprogram_npm/**", "node_modules/**", "dist/**", "coverage/**")
    def ignored_path_patterns(self): return ("miniprogram_npm/**", "node_modules/**", ".git/**")
    def default_test_command_ids(self): return ("node-npm-test",)
    def default_quality_command_ids(self): return ("node-npm-lint",)
    def root_markers(self): return self._markers
