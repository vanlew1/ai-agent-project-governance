import unittest
from governance.guards.scope_guard import check
from governance.autonomy.failure_classifier import classify

CONTRACT={"write_scope":{"allow":["src/","docs/a.md"],"deny":["data/production/**"]}}
class GuardAcceptanceTest(unittest.TestCase):
 def test_pass_warn_blocked_matrix(self):
  self.assertEqual(["src/a.py"],check(CONTRACT,["src/a.py"])["allowed_changes"])
  self.assertEqual(["tests/a.py"],check(CONTRACT,["tests/a.py"])["conditional_changes"])
  self.assertEqual(["data/production/a"],check(CONTRACT,["data/production/a"])["denied_changes"])
 def test_failure_boundaries(self):
  self.assertEqual("AUTONOMOUS_ENGINEERING",classify("test_failed"));self.assertEqual("HUMAN_CHECKPOINT",classify("secret_required"));self.assertEqual("UNKNOWN",classify("unknown"))
