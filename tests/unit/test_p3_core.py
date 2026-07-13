import unittest
from governance.verification.test_planner import create
from governance.verification.verification_builder import build
from governance.verification.closure_evaluator import close

C={'task_id':'T','task_level':'A'}
G={'status':'PASS'}
class P3CoreTest(unittest.TestCase):
 def test_plan_and_closure(self):
  p=create(C,G);self.assertEqual('READY',p['status']);self.assertEqual([1],p['levels']);self.assertEqual(['task_level_A'],p['selection_reasons'])
  r={'command_id':'x','status':'PASS','required':True};v=build(C,G,p,[r]);self.assertEqual('VERIFIED',v['completion_status']);self.assertEqual('CLOSED',close(v)['status'])
 def test_blocked(self): self.assertEqual('BLOCKED',create(C,{'status':'BLOCKED'})['status'])
