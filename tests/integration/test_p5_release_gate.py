from __future__ import annotations
import runpy, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class P5ReleaseGate(unittest.TestCase):
 def test_gate_has_fixed_read_only_steps(self):
  module=runpy.run_path(str(ROOT/"scripts/run_governance_ci.py"))
  names=[name for name,_ in module["GATES"]]
  self.assertEqual(["governance","schema-compatibility","runtime-dependencies","bootstrap","ci-security","tests","quality","syntax"],names)
