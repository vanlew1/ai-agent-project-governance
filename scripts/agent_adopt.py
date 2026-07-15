"""Create and operate bounded, local existing-project adoption artifacts."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from governance.adoption import assess_rollback, build_plan, compile_runtime_bundle, export_drafts, install_approved, rollback_install, render_json, render_markdown  # noqa: E402


COMMANDS = {
    "dry-run": "Analyze an existing project without writing to the target.",
    "export-drafts": "Export adoption drafts and confirmation artifacts outside the target.",
    "compile-runtime-artifacts": "Compile approved drafts into external Runtime preview artifacts.",
    "install-approved": "Install exact approved Runtime artifact bytes without activation.",
    "assess-rollback": "Produce a read-only manual recovery assessment.",
    "rollback-install": "Reject automatic rollback and explain the manual-only boundary.",
}


def _add_dry_run_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", type=Path, default=argparse.SUPPRESS, help="Existing local project to inspect (required)")
    parser.add_argument("--format", choices=("markdown", "json"), default=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, default=argparse.SUPPRESS, help="Explicit output path outside --project-root; stdout by default")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use bounded local Existing Project Adoption commands.",
        epilog="All commands are local-only. They do not authorize network, Git writes, production actions, or deployment.",
    )
    # Keep the original `--project-root ... dry-run` ordering compatible while
    # also showing the dry-run parameters in subcommand help.
    _add_dry_run_arguments(parser)
    subcommands = parser.add_subparsers(dest="command", required=True, title="commands")
    dry_run = subcommands.add_parser("dry-run", help=COMMANDS["dry-run"], description=COMMANDS["dry-run"])
    _add_dry_run_arguments(dry_run)

    export = subcommands.add_parser("export-drafts", help=COMMANDS["export-drafts"], description=COMMANDS["export-drafts"])
    export.add_argument("--plan", type=Path, required=True)
    export.add_argument("--confirmations", type=Path, required=True)
    export.add_argument("--output-dir", type=Path, required=True)
    export.add_argument("--target-project-root", type=Path, required=True, help="Used only to reject target-project output paths")

    compile_artifacts = subcommands.add_parser("compile-runtime-artifacts", help=COMMANDS["compile-runtime-artifacts"], description=COMMANDS["compile-runtime-artifacts"])
    compile_artifacts.add_argument("--plan", type=Path, required=True)
    compile_artifacts.add_argument("--confirmations", type=Path, required=True)
    compile_artifacts.add_argument("--draft-bundle", type=Path, required=True)
    compile_artifacts.add_argument("--output-dir", type=Path, required=True)
    compile_artifacts.add_argument("--target-project-root", type=Path, required=True, help="Used only to reject target-project output paths")

    install = subcommands.add_parser("install-approved", help=COMMANDS["install-approved"], description="Install exact approved Runtime artifact bytes. It does not activate state or run lifecycle steps.")
    install.add_argument("--target-project-root", type=Path, required=True)
    install.add_argument("--draft-bundle", type=Path, required=True)
    install.add_argument("--runtime-artifact-bundle", type=Path, required=True)
    install.add_argument("--final-approval", type=Path, required=True)
    install.add_argument("--receipt-output", type=Path, required=True)
    install.add_argument("--plan", type=Path, required=True)
    install.add_argument("--confirmations", type=Path, required=True)

    assessment = subcommands.add_parser("assess-rollback", help=COMMANDS["assess-rollback"], description="Produce a read-only manual recovery assessment; it never deletes target files.")
    assessment.add_argument("--target-project-root", type=Path, required=True)
    assessment.add_argument("--installation-receipt", type=Path, required=True)
    assessment.add_argument("--output", type=Path, required=True)

    rollback = subcommands.add_parser("rollback-install", help=COMMANDS["rollback-install"], description="Automatic rollback is unsupported; this command never deletes target files.")
    rollback.add_argument("--target-project-root", type=Path, required=True)
    rollback.add_argument("--installation-receipt", type=Path, required=True)
    rollback.add_argument("--rollback-approval", type=Path, required=True)
    return parser


def _output_path(root: Path, output: Path) -> Path:
    destination = output.expanduser().resolve()
    try:
        destination.relative_to(root)
    except ValueError:
        return destination
    raise ValueError("--output must be outside --project-root; target-project writes are forbidden")


def _dry_run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not getattr(args, "project_root", None):
        parser.error("dry-run requires --project-root")
    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"--project-root must be an existing directory: {args.project_root}")
    plan = build_plan(root)
    rendered = render_markdown(plan) if getattr(args, "format", "markdown") == "markdown" else render_json(plan)
    if getattr(args, "output", None):
        destination = _output_path(root, args.output)
        if destination.exists():
            raise ValueError("--output already exists; refusing to overwrite it")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def _export_drafts(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    export_drafts(args.plan, args.confirmations, args.output_dir, args.target_project_root)


def _compile_runtime_artifacts(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    compile_runtime_bundle(args.plan, args.confirmations, args.draft_bundle, args.output_dir, args.target_project_root)


def _install_approved(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    install_approved(args.target_project_root, args.draft_bundle, args.runtime_artifact_bundle, args.final_approval, args.receipt_output, args.plan, args.confirmations)


def _assess_rollback(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    assess_rollback(args.target_project_root, args.installation_receipt, args.output)


def _rollback_install(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    rollback_install(args.target_project_root, args.installation_receipt, args.rollback_approval)


HANDLERS = {
    "dry-run": _dry_run,
    "export-drafts": _export_drafts,
    "compile-runtime-artifacts": _compile_runtime_artifacts,
    "install-approved": _install_approved,
    "assess-rollback": _assess_rollback,
    "rollback-install": _rollback_install,
}


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if set(COMMANDS) != set(HANDLERS):  # defensive invariant for future edits
        raise RuntimeError("parser command registry and dispatcher differ")
    try:
        HANDLERS[args.command](args, parser)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] Adoption command could not complete: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
