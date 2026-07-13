from __future__ import annotations
import subprocess
from pathlib import Path
def changed_paths(root:Path)->list[str]:
    out=subprocess.run(['git','status','--porcelain=v1','-z'],cwd=root,capture_output=True,check=False).stdout
    if not out: return []
    values=[]
    for record in out.split(b'\0'):
        if not record: continue
        path=record[3:].decode('utf-8','surrogateescape').replace('\\','/')
        values.append(path)
    return sorted(set(values))
