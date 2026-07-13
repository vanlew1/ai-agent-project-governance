from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import argparse
from governance.state import store,layout
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True); i=sub.add_parser('init');i.add_argument('--project-state-file',type=Path,required=True);i.add_argument('--force',action='store_true');a=sub.add_parser('activate');a.add_argument('--contract-file',type=Path,required=True);sub.add_parser('show');sub.add_parser('deactivate');r=sub.add_parser('reset');r.add_argument('--confirm-reset',action='store_true');x=p.parse_args()
try:
 if x.cmd=='init': store.init(x.project_state_file,x.force)
 elif x.cmd=='activate': store.activate(x.contract_file)
 elif x.cmd=='deactivate': store.deactivate()
 elif x.cmd=='show': print({'project_mode':store.load_project()['project_mode'],'active_task':store.active().get('task_id') if layout.ACTIVE.exists() else None})
 elif x.cmd=='reset':
  if not x.confirm_reset: raise ValueError('--confirm-reset required')
  import shutil; shutil.rmtree(layout.STATE_DIR)
except Exception as e: print(f'state error: {e}',file=sys.stderr);raise SystemExit(1)
