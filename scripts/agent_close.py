from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.verification.closure_evaluator import close
from governance.state import store, layout
from governance.verification.report_builder import write
s=Path.cwd()/'.agent_state';v=yaml.safe_load((s/'verification_result.yaml').read_text(encoding='utf-8'));c=close(v);c['report_path']=write(Path.cwd(),v['task_id'],v,c);store.save_p3(layout.CLOSURE, c, 'closure_result.schema.json');print(yaml.safe_dump(c,sort_keys=False));raise SystemExit({'CLOSED':0,'PARTIAL':2,'BLOCKED':3,'FAILED':4}[c['status']])
