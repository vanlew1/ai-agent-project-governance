"""Static least-privilege validation for the governance workflow."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
FORBIDDEN = ("pull_request_target", "contents: write", "pull-requests: write", "issues: write", "id-token: write", "secrets.", "curl ", "wget ", "invoke-webrequest", "git push", "npm publish", "twine upload", "eval ", "shell=True")
def parse_args():
    parser=argparse.ArgumentParser(description="Check governance CI security")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); return parser.parse_args()
def main():
    path=parse_args().root.resolve()/".github/workflows/governance-ci.yml"; errors=[]
    try: data=yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError,yaml.YAMLError) as exc: print(f"CI security: ERROR ({exc})"); return 1
    text=path.read_text(encoding="utf-8").lower()
    for token in FORBIDDEN:
        if token in text: errors.append(f"Forbidden CI token: {token.strip()}")
    if data.get("permissions") != {"contents":"read"}: errors.append("Workflow permissions must be exactly contents: read")
    jobs=data.get("jobs", {})
    if not jobs: errors.append("Workflow has no jobs")
    for name, job in jobs.items():
        if not isinstance(job,dict) or not job.get("timeout-minutes"): errors.append(f"Job missing timeout: {name}")
    if "python scripts/run_governance_ci.py" not in text: errors.append("Workflow does not call the fixed local gate")
    if errors: print(f"CI security: FAIL ({len(errors)} issue(s))"); print("\n".join(f"- {e}" for e in errors)); return 2
    print("CI security: PASS (read-only, fixed local gate)"); return 0
if __name__ == "__main__": raise SystemExit(main())
