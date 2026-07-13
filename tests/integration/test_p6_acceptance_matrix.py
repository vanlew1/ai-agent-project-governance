import unittest
from governance.orchestration.closure import closure_allowed
class P6AcceptanceMatrixTest(unittest.TestCase):
 def test_required_auditor_and_result_gate(self):
  self.assertEqual((False,"required_auditor_missing"),closure_allowed({"status":"READY_FOR_VERIFICATION"},True,None))
  self.assertEqual((False,"orchestration_not_ready"),closure_allowed({"status":"FAILED"}))
  self.assertEqual((True,"ready_for_p3_verification"),closure_allowed({"status":"READY_FOR_VERIFICATION"}))
