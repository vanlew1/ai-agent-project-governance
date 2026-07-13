import unittest
from governance.verification.test_planner import create
from governance.verification.verification_builder import build
from governance.verification.closure_evaluator import close

C={"task_id":"T","task_level":"A"}
class P3AcceptanceMatrix(unittest.TestCase):
 def test_pass_partial_blocked_failed(self):
  plan=create(C,{"status":"PASS"})
  verified=build(C,{"status":"PASS"},plan,[{"command_id":"x","status":"PASS","required":True}])
  self.assertEqual("CLOSED",close(verified)["status"])
  partial=build(C,{"status":"WARN"},plan,[{"command_id":"x","status":"PASS","required":True}])
  self.assertEqual("PARTIAL",close(partial)["status"])
  blocked=build(C,{"status":"BLOCKED"},create(C,{"status":"BLOCKED"}),[])
  self.assertEqual("BLOCKED",close(blocked)["status"])
  failed=build(C,{"status":"PASS"},plan,[{"command_id":"x","status":"FAIL","required":True}])
  self.assertEqual("FAILED",close(failed)["status"])
 def test_stale_is_blocked(self):
  plan=create(C,{"status":"PASS"});v=build(C,{"status":"PASS"},plan,[{"command_id":"x","status":"PASS","required":True}])
  self.assertEqual("BLOCKED",close(v,stale=True)["status"])
