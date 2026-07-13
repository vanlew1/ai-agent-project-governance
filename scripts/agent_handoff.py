from __future__ import annotations
import argparse,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from governance.schema_loader import load_mapping,validate_mapping
from governance.orchestration.handoff import create_handoff
def main():
 p=argparse.ArgumentParser();q=p.add_subparsers(dest="action",required=True);
 for x in ("create","validate"): q.add_parser(x).add_argument("--result" if x=="create" else "--handoff",required=True,type=Path)
 a=p.parse_args(); value=create_handoff(load_mapping(a.result),[]) if a.action=="create" else load_mapping(a.handoff); validate_mapping(value,"agent_handoff.schema.json"); print(yaml.safe_dump(value,allow_unicode=True,sort_keys=False)); return 0
if __name__=="__main__": raise SystemExit(main())
