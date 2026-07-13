import unittest
from unittest.mock import patch
from governance.guards.approval_guard import check

class ApprovalGuardTest(unittest.TestCase):
 def test_missing_and_valid(self):
  with patch('governance.guards.approval_guard.approval_store.load',return_value=[]): self.assertEqual('missing',check('external_api_access',{},'T'))
  record={'approval_type':'external_api_access','status':'approved','task_id':'T','environment_fingerprint':{},'scope':{}}
  with patch('governance.guards.approval_guard.approval_store.load',return_value=[record]): self.assertEqual('valid',check('external_api_access',{},'T'))
