# Adoption audit

`python scripts/agent_audit.py --project-root <path>` is a deterministic local configuration-completeness check. It is not a security audit or certification.

The command is read-only by default: it does not write reports, inspect Git object content, read environment-variable values, open credential files, call a network service, or start a coding agent. It reads bounded UTF-8 text only from `AGENTS.md`, `README.md`, and Markdown/text files under `docs`; files that are too large, binary, unreadable, or inaccessible are reported as skipped or warnings.

```bash
python scripts/agent_audit.py --project-root .
python scripts/agent_audit.py --project-root . --format json
python scripts/agent_audit.py --project-root . --output reports/adoption-audit.txt
```

`--output` is optional and is resolved below `--project-root`; parent directories are created only after the audit succeeds. `--strict` returns `4` when a check has status `FAIL`. Normal completed audits return `0` even when they contain `WARN` or `FAIL`, invalid paths return `2`, and tool or output errors return `3`.

The fixed checks cover agent entry instructions, test signals, modification scope, risk tiers, external and credential boundaries, Git boundaries, verification and reporting, public-document encoding, adapter signals, and sensitive filename/ignore-rule risk. Every check includes only safe evidence such as paths, configuration keys, or command names.

JSON output is stable and includes `schema_version`, `tool_version`, `project_root_display`, `score`, `level`, `recommended_preset`, and `checks`. Each check has `check_id`, `status`, `summary`, `safe_evidence`, `recommendation`, and a fixed `weight`.

Scores use fixed 10-point checks: `PASS` earns 10, `WARN` earns 5, and `FAIL` or `SKIPPED` earns 0. `NOT_APPLICABLE` is excluded from the denominator. `READY` is 80–100, `PARTIAL` is 50–79, and `NEEDS_GUARDRAILS` is below 50.

```json
{
  "schema_version": "1.0",
  "tool_version": "1.0.0",
  "project_root_display": "demo",
  "score": 65,
  "level": "PARTIAL",
  "recommended_preset": "standard",
  "checks": [{"check_id": "agent_entry", "status": "WARN"}]
}
```
