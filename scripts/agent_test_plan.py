from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.state import store, layout
from governance.verification.test_planner import create
state=Path.cwd()/'.agent_state'; guard=state/'last_guard_result.yaml'; plan=state/'test_plan.yaml'
if len(sys.argv)<2 or sys.argv[1] not in ('create','show'): raise SystemExit(1)
if sys.argv[1]=='show': print(plan.read_text(encoding='utf-8'));raise SystemExit(0)
if not guard.exists(): raise SystemExit(1)
value=create(store.active(),yaml.safe_load(guard.read_text(encoding='utf-8')));store.save_p3(layout.TEST_PLAN, value, 'test_plan.schema.json');print(yaml.safe_dump(value,sort_keys=False));raise SystemExit({'READY':0,'DRAFT':2,'BLOCKED':3}[value['status']])
