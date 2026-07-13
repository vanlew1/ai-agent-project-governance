import unittest
from governance.verification.closure_evaluator import close

class ClosureFreshnessTest(unittest.TestCase):
 def verification(self): return {"task_id":"T","guard_status":"PASS","completion_status":"VERIFIED","remaining_risks":[]}
 def test_fresh_and_stale(self):
  self.assertEqual("CLOSED",close(self.verification())["status"])
  blocked=close(self.verification(),stale=True)
  self.assertEqual("BLOCKED",blocked["status"])
  self.assertIn("verification_stale_after_workspace_change",blocked["reasons"])
