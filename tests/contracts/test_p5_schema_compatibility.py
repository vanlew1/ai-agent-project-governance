from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class P5SchemaCompatibility(unittest.TestCase):
 def test_current_baseline_passes_and_old_phase_removal_fails(self):
  self.assertEqual(0,subprocess.run([sys.executable,"scripts/check_schema_compatibility.py"],cwd=ROOT,capture_output=True,text=True).returncode)
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp); (root/"schemas").mkdir(parents=True); (root/"tests/fixtures/compatibility").mkdir(parents=True)
   for path in (ROOT/"schemas").glob("*.json"): (root/"schemas"/path.name).write_text(path.read_text(encoding="utf-8"),encoding="utf-8")
   baseline=ROOT/"tests/fixtures/compatibility/schema_baseline.json"; (root/"tests/fixtures/compatibility/schema_baseline.json").write_text(baseline.read_text(encoding="utf-8"),encoding="utf-8")
   target=root/"schemas/rules_index.schema.json"; target.write_text(target.read_text(encoding="utf-8").replace('"PHASE_4_ADAPTERS_AND_BOOTSTRAP",',''),encoding="utf-8")
   self.assertEqual(2,subprocess.run([sys.executable,"scripts/check_schema_compatibility.py","--root",str(root)],cwd=ROOT,capture_output=True,text=True).returncode)
