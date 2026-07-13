import unittest
from governance.orchestration.planner import build_plan
from governance.orchestration.scheduler import schedule
from governance.orchestration.result_aggregator import aggregate

CONTRACT={"task_id":"t1","write_scope":{"allow":["governance/*","docs/*"],"deny":[]}}
def task(i,path,deps=()): return {"subtask_id":i,"title":i,"role":"IMPLEMENTER","required":True,"depends_on":list(deps),"read_scope":[],"write_scope":[path],"required_command_ids":[],"required_artifacts":[],"workspace_assignment_id":"w"}
class OrchestrationCoreTest(unittest.TestCase):
 def test_parallel_safe_and_ready(self):
  p=build_plan(CONTRACT,[task("a","governance/a.py"),task("b","docs/a.md")],"o","h","main"); self.assertEqual("VALIDATED",p["plan_status"]); self.assertEqual({"a","b"},set(schedule(p)["ready"]))
 def test_conflict_and_cycle_blocked(self):
  p=build_plan(CONTRACT,[task("a","governance/a.py",["b"]),task("b","governance/a.py",["a"])],"o","h","main"); self.assertEqual("BLOCKED",p["plan_status"]); self.assertTrue(p["validation_errors"])
 def test_required_failure_blocks_aggregation(self):
  p=build_plan(CONTRACT,[task("a","governance/a.py")],"o","h","main"); r={"subtask_id":"a","orchestration_id":"o","task_id":"t1","contract_digest":p["subtasks"][0]["parent_contract_digest"],"head_sha":"h","branch":"main","workspace_fingerprint":"x","status":"FAILED"}; self.assertEqual("FAILED",aggregate(p,[r],[])["status"])
if __name__=="__main__": unittest.main()
