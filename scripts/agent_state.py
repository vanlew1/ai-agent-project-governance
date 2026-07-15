"""Local Runtime state commands, including bounded adoption activation."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from governance.adoption.activation import activate_approved
from governance.state import store, layout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage local Runtime state")
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init"); init.add_argument("--project-state-file", type=Path, required=True); init.add_argument("--force", action="store_true")
    legacy = sub.add_parser("activate", help="Legacy active-task command; cannot activate Existing Project Adoption state")
    legacy.add_argument("--contract-file", type=Path, required=True)
    sub.add_parser("deactivate"); sub.add_parser("show")
    reset = sub.add_parser("reset"); reset.add_argument("--confirm-reset", action="store_true")
    approved = sub.add_parser("activate-approved", help="Activate an installed adoption Runtime without running lifecycle steps")
    approved.add_argument("--target-project-root", type=Path, required=True)
    approved.add_argument("--task-contract", type=Path, required=True)
    approved.add_argument("--project-state", type=Path, required=True)
    approved.add_argument("--runtime-artifact-manifest", type=Path, required=True)
    approved.add_argument("--final-install-approval", type=Path, required=True)
    approved.add_argument("--installation-receipt", type=Path, required=True)
    approved.add_argument("--activation-approval", type=Path, required=True)
    approved.add_argument("--activation-receipt-output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.cmd == "init": store.init(args.project_state_file, args.force)
        elif args.cmd == "activate": store.activate(args.contract_file)
        elif args.cmd == "deactivate": store.deactivate()
        elif args.cmd == "show": print({"project_mode": store.load_project()["project_mode"], "active_task": store.active().get("task_id") if layout.ACTIVE.exists() else None})
        elif args.cmd == "reset":
            if not args.confirm_reset: raise ValueError("--confirm-reset required")
            import shutil; shutil.rmtree(layout.STATE_DIR)
        elif args.cmd == "activate-approved":
            activate_approved(args.target_project_root, args.task_contract, args.project_state, args.runtime_artifact_manifest, args.final_install_approval, args.installation_receipt, args.activation_approval, args.activation_receipt_output)
    except Exception as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
