# AGC-UX-EXISTING-PROJECT-ADOPTION-04G-R1 CLI Help Remediation

Status: PASS — `CLI_HELP_SURFACE_VERIFIED`

## P1 root cause and repair

`scripts/agent_adopt.py` used separate command-specific parsers plus hand-written `sys.argv[1]` dispatch. Its top-level parser declared only `dry-run`, so the other five supported commands were hidden from `--help`.

The script now has one argparse subcommand registry (`COMMANDS`) and one handler mapping (`HANDLERS`). A defensive invariant requires their key sets to match. The previous `--project-root … dry-run` ordering remains supported, while `dry-run --help` exposes its real parameters.

## Command matrix

| Command | Parser | Dispatcher | Help | Docs | Tests |
| --- | ---: | ---: | ---: | ---: | ---: |
| `dry-run` | yes | yes | yes | yes | yes |
| `export-drafts` | yes | yes | yes | yes | yes |
| `compile-runtime-artifacts` | yes | yes | yes | yes | yes |
| `install-approved` | yes | yes | yes | yes | yes |
| `assess-rollback` | yes | yes | yes | yes | yes |
| `rollback-install` | yes | yes | yes | yes | yes |

Top-level help gives every command a one-line description. Subcommand help confirms that installation does not activate, compilation does not install, assessment is read-only, and automatic rollback is unsupported and non-destructive. An unknown subcommand exits non-zero without outputting sensitive content.

## Regression and documentation

`tests/unit/test_agent_adopt.py` now covers top-level discovery, dispatcher/help agreement, each subcommand help surface, safety wording, help exit status, and unknown-command failure. `README.md` and `docs/EXISTING_PROJECT_ADOPTION.md` now expose the complete local-only command surface.

## Validation

Executed from `/home/liyouran1997/projects/ai-agent-project-governance`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_agent_adopt tests.unit.test_agent_adopt_export tests.unit.test_agent_adopt_install tests.unit.test_public_adoption_assets  # 33 passed
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest  # 151 passed, 18.913s
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py  # PASS, 32 schemas
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py  # PASS, 155 files, no warnings
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py  # PASS, 32 schemas
git diff --check  # PASS
```

No network, real-project, production-data, or Git-write operation was executed.
