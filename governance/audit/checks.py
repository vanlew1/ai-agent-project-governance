"""Bounded, deterministic checks for local coding-agent governance adoption."""
from __future__ import annotations

import json
from pathlib import Path

from governance.adapters.detection import detect_adapters

from .models import AuditCheck, AuditResult
from .scoring import level_for, recommended_preset, score_checks

TOOL_VERSION = "1.0.0"
MAX_DOCUMENT_BYTES = 128 * 1024
MAX_DOCUMENTS = 32
BAD_TEXT_FRAGMENTS = ("\ufffd", "Ã", "Â", "â€", "ðŸ")
AGENT_ENTRY_FILES = ("AGENTS.md", "CLAUDE.md", ".cursorrules", ".github/copilot-instructions.md")
SENSITIVE_NAME_PARTS = (".env", "credential", "secret", "id_rsa")
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")


def _read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        if path.stat().st_size > MAX_DOCUMENT_BYTES:
            return None, "too large"
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError):
        return None, "unreadable or non-UTF-8"


def _governance_documents(root: Path) -> tuple[list[tuple[Path, str]], list[str]]:
    candidates = [root / "AGENTS.md", root / "README.md"]
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        candidates.extend(sorted(path for path in docs_dir.rglob("*") if path.suffix.lower() in {".md", ".txt"}))
    documents: list[tuple[Path, str]] = []
    skipped: list[str] = []
    for path in candidates[:MAX_DOCUMENTS]:
        if not path.is_file():
            continue
        text, reason = _read_text(path)
        display = str(path.relative_to(root)).replace("\\", "/")
        if text is None:
            skipped.append(f"{display} ({reason})")
        else:
            documents.append((path, text))
    return documents, skipped


def _contains_boundary(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    boundary_words = ("must", "must not", "forbid", "forbidden", "do not", "only", "不得", "禁止", "仅")
    return any(term in lowered for term in terms) and any(word in lowered for word in boundary_words)


def _check(check_id: str, passed: bool, summary: str, evidence: tuple[str, ...], recommendation: str) -> AuditCheck:
    return AuditCheck(check_id, "PASS" if passed else "WARN", summary, evidence, recommendation)


def _test_command_check(root: Path) -> AuditCheck:
    markers: list[str] = []
    if (root / "pyproject.toml").is_file() or (root / "pytest.ini").is_file() or (root / "tox.ini").is_file():
        markers.append("Python test configuration")
    package_json = root / "package.json"
    if package_json.is_file():
        text, _ = _read_text(package_json)
        try:
            scripts = json.loads(text or "{}").get("scripts", {})
            if isinstance(scripts, dict) and "test" in scripts:
                markers.append("package.json:scripts.test")
        except json.JSONDecodeError:
            markers.append("package.json")
    if (root / "tests").is_dir() or (root / "test").is_dir():
        markers.append("test directory")
    return _check(
        "test_command", bool(markers), "Recognizable local test configuration was found." if markers else "No recognizable local test configuration was found.",
        tuple(markers), "Document one local test command before relying on coding agents.",
    )


def _sensitive_file_check(root: Path) -> AuditCheck:
    risky: list[str] = []
    ignored = False
    ignore_file = root / ".gitignore"
    if ignore_file.is_file():
        ignore_text, _ = _read_text(ignore_file)
        ignored = bool(ignore_text and any(token in ignore_text for token in (".env", "*.pem", "*.key")))
    try:
        paths = (path for path in root.rglob("*") if ".git" not in path.parts and path.is_file())
        for path in paths:
            name = path.name.lower()
            if any(part in name for part in SENSITIVE_NAME_PARTS) or name.endswith(SENSITIVE_SUFFIXES):
                risky.append(str(path.relative_to(root)).replace("\\", "/"))
                if len(risky) == 8:
                    break
    except OSError:
        return AuditCheck("sensitive_commit_risk", "SKIPPED", "File-name scan could not be completed.", (), "Review ignore rules and local state manually.")
    if risky:
        return AuditCheck("sensitive_commit_risk", "WARN", "Potential sensitive or local-state filenames are present.", tuple(risky), "Keep these files untracked and add explicit ignore rules.")
    return _check("sensitive_commit_risk", ignored, "Ignore rules cover common secret file patterns." if ignored else "No common secret-file ignore patterns were found.",
                  (".gitignore",) if ignored else (), "Add ignore rules for .env, private keys, and local generated state.")


def run_audit(project_root: Path) -> AuditResult:
    root = project_root.expanduser().resolve()
    documents, skipped = _governance_documents(root)
    combined = "\n".join(text for _, text in documents)
    doc_paths = tuple(str(path.relative_to(root)).replace("\\", "/") for path, _ in documents)
    entry_files = tuple(name for name in AGENT_ENTRY_FILES if (root / name).is_file())
    adapter = detect_adapters(root)
    checks = (
        _check("agent_entry", bool(entry_files), "Coding-agent entry instructions were found." if entry_files else "No supported coding-agent entry file was found.", entry_files,
               "Add AGENTS.md with concise local instructions."),
        _test_command_check(root),
        _check("change_scope", _contains_boundary(combined, ("allow", "scope", "write scope", "允许修改", "修改范围")), "Change-scope guidance was found." if _contains_boundary(combined, ("allow", "scope", "write scope", "允许修改", "修改范围")) else "No explicit allowed change scope was found.", doc_paths,
               "Define allowed and forbidden paths for each task."),
        _check("risk_tiering", _contains_boundary(combined, ("risk", "high-risk", "task level", "高风险", "任务等级")), "Task risk guidance was found." if _contains_boundary(combined, ("risk", "high-risk", "task level", "高风险", "任务等级")) else "No small-task versus high-risk-task distinction was found.", doc_paths,
               "Document how high-risk work receives stronger review and tests."),
        _check("external_boundaries", _contains_boundary(combined, ("api", "network", "credential", "production", "外部", "网络", "凭据", "生产")), "External-access safeguards were found." if _contains_boundary(combined, ("api", "network", "credential", "production", "外部", "网络", "凭据", "生产")) else "No clear external-access or credential boundary was found.", doc_paths,
               "State limits for network, credentials, external APIs, and production systems."),
        _check("git_boundaries", _contains_boundary(combined, ("git", "commit", "push", "rollback", "提交", "推送", "回滚")), "Git safety guidance was found." if _contains_boundary(combined, ("git", "commit", "push", "rollback", "提交", "推送", "回滚")) else "No Git save, rollback, or publish boundary was found.", doc_paths,
               "Document when agents may commit, push, or roll back work."),
        _check("verification_closure", _contains_boundary(combined, ("test", "verification", "close", "report", "测试", "验证", "收口", "报告")), "Verification or closure guidance was found." if _contains_boundary(combined, ("test", "verification", "close", "report", "测试", "验证", "收口", "报告")) else "No verification or closure requirement was found.", doc_paths,
               "Require a targeted test and a concise completion report."),
        AuditCheck("document_encoding", "WARN" if skipped else "PASS" if not any(fragment in combined for fragment in BAD_TEXT_FRAGMENTS) else "FAIL",
                   "Public governance documents are readable UTF-8." if not skipped and not any(fragment in combined for fragment in BAD_TEXT_FRAGMENTS) else "Some public governance documents were skipped or contain encoding damage.",
                   tuple(skipped) if skipped else doc_paths, "Save public documentation as UTF-8 and remove replacement characters or mojibake."),
        AuditCheck("adapter_signal", "PASS" if adapter.status == "DETECTED" else "WARN", f"Adapter detector selected {adapter.primary_adapter} ({adapter.status}).",
                   (f"adapter:{adapter.primary_adapter}", f"status:{adapter.status}"), "Add standard project markers or review the detected adapter."),
        _sensitive_file_check(root),
    )
    score = score_checks(checks)
    return AuditResult("1.0", TOOL_VERSION, root.name or ".", score, level_for(score), recommended_preset(checks, combined), checks)
