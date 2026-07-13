from __future__ import annotations
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class P5CIParity(unittest.TestCase):
 def test_workflow_calls_fixed_gate_with_read_only_permissions(self):
  text=(ROOT/".github/workflows/governance-ci.yml").read_text(encoding="utf-8")
  self.assertIn("python scripts/run_governance_ci.py",text); self.assertIn("python scripts/agent_detect_adapter.py --root . detect",text); self.assertIn("if ($LASTEXITCODE -eq 2)",text); self.assertIn("contents: read",text); self.assertNotIn("pull_request_target",text); self.assertNotIn("secrets.",text)
