from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.state import store, layout
from governance.verification.verification_builder import build
s=Path.cwd()/'.agent_state'; guard=yaml.safe_load((s/'last_guard_result.yaml').read_text(encoding='utf-8'));plan=yaml.safe_load((s/'test_plan.yaml').read_text(encoding='utf-8'));results=yaml.safe_load((s/'test_results.yaml').read_text(encoding='utf-8'))
v=build(store.active(),guard,plan,results);store.save_p3(layout.VERIFICATION, v, 'verification_result.schema.json');print(yaml.safe_dump(v,sort_keys=False));raise SystemExit({'VERIFIED':0,'PARTIAL':2,'BLOCKED':3,'FAILED':4}[v['completion_status']])
