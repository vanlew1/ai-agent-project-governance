from pathlib import Path

from .models import DetectionEvidence


class GenericAdapter:
    adapter_id = "generic"
    display_name = "Generic project"
    def detect(self, repo_root: Path) -> DetectionEvidence:
        return DetectionEvidence(self.adapter_id, (), 0, ("no supported stack marker",))
    def source_patterns(self): return ("**/*",)
    def test_patterns(self): return ()
    def sensitive_path_patterns(self): return (".env", ".env.*", "secrets/**", "credentials/**")
    def generated_path_patterns(self): return ("dist/**", "build/**", "coverage/**")
    def ignored_path_patterns(self): return (".git/**",)
    def default_test_command_ids(self): return ()
    def default_quality_command_ids(self): return ()
    def root_markers(self): return ()
