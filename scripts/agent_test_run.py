from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.verification.command_validator import validate
from governance.verification.command_runner import run
state=Path.cwd()/'.agent_state'; plan=yaml.safe_load((state/'test_plan.yaml').read_text(encoding='utf-8'))
if plan['status']=='BLOCKED': raise SystemExit(3)
results=[]
for cmd in plan['selected_commands']:
 ok,_=validate(cmd)
 if not ok: raise SystemExit(3)
 result=run(cmd,Path.cwd());result.update({'schema_version':'1.0','task_id':plan['task_id'],'plan_id':plan['plan_id'],'command_id':cmd['command_id'],'level':cmd['level'],'required':cmd['required']});results.append(result)
(state/'test_results.yaml').write_text(yaml.safe_dump(results,sort_keys=False),encoding='utf-8');raise SystemExit(0 if all(r['status']=='PASS' for r in results) else 4)
