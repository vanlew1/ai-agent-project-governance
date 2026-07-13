import subprocess,sys,tempfile,unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
class OrchestrationCliFlowTest(unittest.TestCase):
 def execute(self,cwd,*args):
  return subprocess.run([sys.executable,*args],cwd=cwd,text=True,capture_output=True,encoding="utf-8")
 def test_isolated_cli_lifecycle(self):
  with tempfile.TemporaryDirectory(prefix="p6-") as tmp:
   cwd=Path(tmp); payload={"contract":{"task_id":"p6-cli","write_scope":{"allow":["src/*"],"deny":[]}},"subtasks":[{"subtask_id":"a","title":"implement","role":"IMPLEMENTER","required":True,"depends_on":[],"read_scope":[],"write_scope":["src/a.py"],"required_command_ids":[],"required_artifacts":[],"workspace_assignment_id":"w"}]}; source=cwd/"input.yaml"; source.write_text(yaml.safe_dump(payload),encoding="utf-8")
   self.assertEqual(0,self.execute(cwd,str(ROOT/"scripts/agent_orchestrate.py"),"plan","--input",str(source),"--orchestration-id","o","--head-sha","h","--branch","b").returncode)
   plan=cwd/".agent_state/orchestration/o/plan.yaml"; self.assertEqual(0,self.execute(cwd,str(ROOT/"scripts/agent_orchestrate.py"),"validate","--plan",str(plan)).returncode); self.assertEqual(0,self.execute(cwd,str(ROOT/"scripts/agent_orchestrate.py"),"ready","--orchestration-id","o").returncode)
   saved=yaml.safe_load(plan.read_text(encoding="utf-8")); sub=saved["subtasks"][0]; result={"schema_version":"1.0","orchestration_id":"o","task_id":"p6-cli","subtask_id":"a","role":"IMPLEMENTER","status":"SUCCEEDED","contract_digest":sub["parent_contract_digest"],"head_sha":"h","branch":"b","workspace_fingerprint":"fp","changed_files":["src/a.py"],"commands_run":[],"test_results":[],"artifacts":[],"risks":[],"unresolved_items":[],"started_at":"2026-01-01T00:00:00Z","finished_at":"2026-01-01T00:01:00Z"}; d=cwd/".agent_state/orchestration/o/results";d.mkdir(parents=True); rp=d/"a.yaml";rp.write_text(yaml.safe_dump(result),encoding="utf-8")
   hand=self.execute(cwd,str(ROOT/"scripts/agent_handoff.py"),"create","--result",str(rp)); self.assertEqual(0,hand.returncode,hand.stderr); hd=cwd/".agent_state/orchestration/o/handoffs";hd.mkdir();(hd/"a.yaml").write_text(hand.stdout,encoding="utf-8")
   for action in ("build","verify","close"): self.assertEqual(0,self.execute(cwd,str(ROOT/"scripts/agent_aggregate.py"),action,"--orchestration-id","o").returncode)
   self.assertEqual("CLOSED",yaml.safe_load((cwd/".agent_state/orchestration/o/closure.yaml").read_text(encoding="utf-8"))["status"])
