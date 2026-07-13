import unittest
from datetime import datetime, timedelta, timezone
from governance.state.freshness import evaluate

FINGERPRINT={"repository_root":"repo","current_branch":"main","head_commit":"a","task_id":"T","contract_digest":"d"}
BASE={"status":"approved","task_id":"T","environment_fingerprint":FINGERPRINT,"scope":{"provider":"x"}}

class ApprovalLifecycleTest(unittest.TestCase):
 def test_valid_and_scope(self):
  self.assertEqual("valid",evaluate(BASE,FINGERPRINT,"T",{"provider":"x"}))
  self.assertEqual("scope_mismatch",evaluate(BASE,FINGERPRINT,"T",{"provider":"y"}))
 def test_freshness_matrix(self):
  for field,value in (("task_id","X"),("environment_fingerprint",{}),("status","expired")):
   item=dict(BASE);item[field]=value;self.assertNotEqual("valid",evaluate(item,FINGERPRINT,"T"))
  item=dict(BASE);item["expires_at"]=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat();self.assertEqual("expired",evaluate(item,FINGERPRINT,"T"))
