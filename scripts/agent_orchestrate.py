from __future__ import annotations
import argparse,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.schema_loader import load_mapping,validate_mapping
from governance.orchestration.planner import build_plan,validate_plan
from governance.orchestration.scheduler import schedule
from governance.state import store
def main():
 p=argparse.ArgumentParser(description="Local deterministic P6 planning; never starts agents or Git actions"); q=p.add_subparsers(dest="action",required=True)
 a=q.add_parser("plan");a.add_argument("--input",required=True,type=Path);a.add_argument("--orchestration-id",required=True);a.add_argument("--head-sha",default="LOCAL");a.add_argument("--branch",default="LOCAL")
 a=q.add_parser("validate");a.add_argument("--plan",required=True,type=Path)
 a=q.add_parser("ready");a.add_argument("--orchestration-id",required=True)
 a=q.add_parser("status");a.add_argument("--orchestration-id",required=True)
 args=p.parse_args()
 if args.action=="plan":
  value=load_mapping(args.input); contract=value.get("contract",value); subtasks=value.get("subtasks",[]); out=build_plan(contract,subtasks,args.orchestration_id,args.head_sha,args.branch); validate_mapping(out,"orchestration_plan.schema.json"); store.save_orchestration(args.orchestration_id,"plan.yaml",out,"orchestration_plan.schema.json")
 elif args.action=="validate":
  plan=load_mapping(args.plan); contract={"write_scope":{"allow":sum((x.get("write_scope",[]) for x in plan["subtasks"]),[]),"deny":[]}}; out=validate_plan(plan,contract)
 else:
  plan=load_mapping(store.orchestration_path(args.orchestration_id,"plan.yaml")); out=schedule(plan) if args.action=="ready" else {"plan_status":plan["plan_status"],"queue":schedule(plan)}
 print(yaml.safe_dump(out,allow_unicode=True,sort_keys=False)); return 0 if out.get("plan_status","VALIDATED")!="BLOCKED" else 3
if __name__=="__main__": raise SystemExit(main())
