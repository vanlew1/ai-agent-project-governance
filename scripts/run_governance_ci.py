"""Fixed, read-only local release gate shared with GitHub Actions."""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable
GATES=(
    ("governance", [PY,"scripts/validate_governance.py"]),
    ("schema-compatibility", [PY,"scripts/check_schema_compatibility.py"]),
    ("runtime-dependencies", [PY,"scripts/check_runtime_dependencies.py"]),
    ("bootstrap", [PY,"scripts/check_template_integrity.py"]),
    ("ci-security", [PY,"scripts/check_ci_security.py"]),
    ("tests", [PY,"-m","unittest","discover","-s","tests","-p","test_*.py"]),
    ("quality", [PY,"scripts/check_code_quality.py"]),
    ("syntax", [PY,"scripts/check_python_syntax.py"]),
)
def run(name, argv):
    started=time.monotonic()
    try: result=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,encoding="utf-8",errors="replace",timeout=180)
    except (OSError,subprocess.TimeoutExpired) as exc: print(f"{name}: ERROR ({exc})"); return False
    elapsed=time.monotonic()-started; summary=(result.stdout or result.stderr).strip().splitlines()
    detail=summary[-1] if summary else "no output"
    print(f"{name}: {'PASS' if result.returncode == 0 else 'FAIL'} ({elapsed:.1f}s) {detail[:240]}")
    return result.returncode == 0
def main():
    results=[run(name,argv) for name,argv in GATES]
    status="PASS" if all(results) else "FAIL"; print(f"Governance release gate: {status} ({sum(results)}/{len(results)} gates)"); return 0 if all(results) else 2
if __name__ == "__main__": raise SystemExit(main())
