"""Safe shell-free runner for validated local commands."""
from __future__ import annotations

import subprocess
import time
from datetime import datetime, timezone

from governance.security.output_sanitizer import OutputSanitizationError, sanitize_output


def _safe_output(raw: bytes) -> dict[str, object]:
    value = sanitize_output(raw)
    return {
        "tail": value.text,
        "digest": value.raw_digest,
        "redaction_count": value.redaction_count,
        "redaction_rule_version": value.rule_version,
    }


def run(command, root):
    started = datetime.now(timezone.utc).isoformat(); tick = time.monotonic()
    try:
        done = subprocess.run(command["argv"], cwd=root, stdin=subprocess.DEVNULL, capture_output=True,
                              timeout=command["timeout_seconds"], shell=False)
        stdout, stderr = _safe_output(done.stdout), _safe_output(done.stderr)
        status, code = ("PASS" if done.returncode == 0 else "FAIL"), done.returncode
    except subprocess.TimeoutExpired as exc:
        status, code = "TIMEOUT", None
        stdout, stderr = _safe_output(exc.stdout or b""), _safe_output(exc.stderr or b"")
    except (OSError, OutputSanitizationError):
        # Never include exception text: it may contain an unsafe command argument.
        status, code = "ERROR", None
        stdout = {"tail": "", "digest": None, "redaction_count": 0, "redaction_rule_version": "1.0"}
        stderr = {"tail": "command output sanitization failed", "digest": None, "redaction_count": 0, "redaction_rule_version": "1.0"}
    return {
        "status": status, "exit_code": code, "duration_ms": round((time.monotonic() - tick) * 1000),
        "sanitized_stdout_tail": stdout["tail"], "sanitized_stderr_tail": stderr["tail"],
        "stdout_digest": stdout["digest"], "stderr_digest": stderr["digest"],
        "redaction_count": stdout["redaction_count"] + stderr["redaction_count"],
        "redaction_rule_version": stdout["redaction_rule_version"], "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
