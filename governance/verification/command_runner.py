"""Safe shell-free runner for validated local commands."""

import subprocess, time
from datetime import datetime, timezone

def _summary(value):
    lines=value.splitlines(); return "\n".join(lines[-40:]), len(lines)>40

def run(command, root):
    started=datetime.now(timezone.utc).isoformat(); tick=time.monotonic()
    try:
        done=subprocess.run(command["argv"],cwd=root,stdin=subprocess.DEVNULL,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=command["timeout_seconds"],shell=False)
        status="PASS" if done.returncode==0 else "FAIL"; out,trunc=_summary(done.stdout); err,trunc_err=_summary(done.stderr)
        code=done.returncode
    except subprocess.TimeoutExpired as exc:
        status,code,out,err,trunc="TIMEOUT",None,"",str(exc),False
    except OSError as exc:
        status,code,out,err,trunc="ERROR",None,"",str(exc),False
    return {"status":status,"exit_code":code,"duration_ms":round((time.monotonic()-tick)*1000),"stdout_summary":out,"stderr_summary":err,"truncated":trunc or trunc_err,"started_at":started,"finished_at":datetime.now(timezone.utc).isoformat()}
