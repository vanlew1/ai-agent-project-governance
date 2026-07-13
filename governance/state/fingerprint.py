from __future__ import annotations
import hashlib, subprocess
from pathlib import Path
def git(root:Path,args:list[str])->str:
    return subprocess.run(['git',*args],cwd=root,text=True,capture_output=True,check=False).stdout.strip()
def build(root:Path,task_id:str,contract:dict)->dict:
    digest=hashlib.sha256(repr(sorted(contract.items())).encode()).hexdigest()
    return {'repository_root':str(root.resolve()),'current_branch':git(root,['branch','--show-current']),'head_commit':git(root,['rev-parse','HEAD']),'task_id':task_id,'contract_digest':digest}
