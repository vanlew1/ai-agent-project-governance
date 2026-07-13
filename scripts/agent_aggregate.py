from __future__ import annotations
import argparse,sys
from datetime import datetime,timezone
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.schema_loader import load_mapping,validate_mapping
from governance.orchestration.result_aggregator import aggregate
from governance.state import store

def save(base,name,value,schema):
 validate_mapping(value,schema); from governance.serialization import dump_mapping
 from governance.state.atomic_writer import write; write(base/name,dump_mapping(value,"yaml"))
def main():
 p=argparse.ArgumentParser(description="Aggregate local P6 evidence; never executes worker commands or Git actions")
 p.add_argument("action",choices=["build","verify","close"]);p.add_argument("--orchestration-id",required=True);a=p.parse_args(); base=store.orchestration_path(a.orchestration_id,"")
 if a.action=="build":
  plan=load_mapping(base/"plan.yaml"); results=[load_mapping(x) for x in (base/"results").glob("*.yaml")]; hands=[load_mapping(x) for x in (base/"handoffs").glob("*.yaml")]; out=aggregate(plan,results,hands); save(base,"orchestration_result.yaml",out,"orchestration_result.schema.json")
 elif a.action=="verify":
  result=load_mapping(base/"orchestration_result.yaml"); out={"orchestration_id":a.orchestration_id,"status":"VERIFIED" if result["status"]=="READY_FOR_VERIFICATION" else "BLOCKED","source_status":result["status"],"verified_at":datetime.now(timezone.utc).isoformat()}; from governance.serialization import dump_mapping; from governance.state.atomic_writer import write; write(base/"verification.yaml",dump_mapping(out,"yaml"))
 else:
  verification=load_mapping(base/"verification.yaml"); out={"orchestration_id":a.orchestration_id,"status":"CLOSED" if verification["status"]=="VERIFIED" else "BLOCKED","verification_status":verification["status"],"closed_at":datetime.now(timezone.utc).isoformat()}; from governance.serialization import dump_mapping; from governance.state.atomic_writer import write; write(base/"closure.yaml",dump_mapping(out,"yaml"))
 print(yaml.safe_dump(out,allow_unicode=True,sort_keys=False)); return 0 if out["status"] in {"READY_FOR_VERIFICATION","VERIFIED","CLOSED"} else 3
if __name__=="__main__": raise SystemExit(main())
