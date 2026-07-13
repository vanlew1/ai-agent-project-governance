from pathlib import Path
import sys,argparse,uuid
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.schema_loader import load_mapping
from governance.state import approval_store
p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
a=s.add_parser("add");a.add_argument("--task-id",required=True);a.add_argument("--type",required=True);a.add_argument("--scope-file",type=Path,required=True);a.add_argument("--approved-by",required=True);a.add_argument("--expires-at")
s.add_parser("list");e=s.add_parser("expire");e.add_argument("--approval-id",required=True);v=s.add_parser("validate");v.add_argument("--approval-id",required=True)
x=p.parse_args()
try:
 if x.cmd=="list": print(approval_store.load())
 elif x.cmd=="add":
  scope=load_mapping(x.scope_file)
  if any(k in str(scope).casefold() for k in ("token","password","secret","cookie","authorization")): raise ValueError("secret-like approval scope is forbidden")
  approval_store.add({"schema_version":"1.0","approval_id":str(uuid.uuid4()),"task_id":x.task_id,"approval_type":x.type,"status":"approved","scope":scope,"environment_fingerprint":{},"approved_by":x.approved_by,"approved_at":datetime.now(timezone.utc).isoformat(),"expires_when":["task_changes"],"expires_at":x.expires_at})
 elif x.cmd=="expire": approval_store.expire(x.approval_id)
 else:
  item=next((a for a in approval_store.load() if a["approval_id"]==x.approval_id),None)
  if not item: raise ValueError("approval not found")
  print(item["status"]); raise SystemExit(0 if item["status"]=="approved" else 3)
except Exception as exc: print(f"approval error: {exc}",file=sys.stderr);raise SystemExit(1)
