from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "preflight"


class AgentPreflightCliTest(unittest.TestCase):
    def command(self, task: str, state: str, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "scripts/agent_preflight.py", "--task-file", str(FIXTURES / task), "--project-state-file", str(FIXTURES / state), *extra], cwd=ROOT, text=True, capture_output=True, check=False)

    def test_exit_codes_and_stdout_contract(self) -> None:
        ready = self.command("task_safe_patch.yaml", "project_state_execution.yaml", "--format", "json", "--quiet")
        self.assertEqual(0, ready.returncode, ready.stderr)
        self.assertEqual("READY", json.loads(ready.stdout)["status"])
        self.assertEqual(2, self.command("task_missing_scope.yaml", "project_state_execution.yaml", "--quiet").returncode)
        self.assertEqual(3, self.command("task_external_api.yaml", "project_state_execution.yaml", "--quiet").returncode)

    def test_output_file_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            output = Path(directory) / "contract.json"
            first = self.command("task_safe_patch.yaml", "project_state_execution.yaml", "--output-file", str(output), "--quiet")
            second = self.command("task_safe_patch.yaml", "project_state_execution.yaml", "--output-file", str(output), "--quiet")
            forced = self.command("task_safe_patch.yaml", "project_state_execution.yaml", "--output-file", str(output), "--force", "--quiet")
        self.assertEqual((0, 1, 0), (first.returncode, second.returncode, forced.returncode))


if __name__ == "__main__":
    unittest.main()
