from __future__ import annotations
import subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class P5AcceptanceMatrix(unittest.TestCase):
 def test_ci_write_permission_is_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp); workflow=root/".github/workflows"; workflow.mkdir(parents=True)
   text=(ROOT/".github/workflows/governance-ci.yml").read_text(encoding="utf-8").replace("contents: read","contents: write")
   (workflow/"governance-ci.yml").write_text(text,encoding="utf-8")
   result=subprocess.run([sys.executable,"scripts/check_ci_security.py","--root",str(root)],cwd=ROOT,capture_output=True,text=True)
   self.assertEqual(2,result.returncode)
