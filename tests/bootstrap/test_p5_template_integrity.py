from __future__ import annotations
import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class P5Bootstrap(unittest.TestCase):
 def test_isolated_unicode_bootstrap_passes(self):
  result=subprocess.run([sys.executable,"scripts/check_template_integrity.py"],cwd=ROOT,capture_output=True,text=True)
  self.assertEqual(0,result.returncode,result.stdout+result.stderr)
