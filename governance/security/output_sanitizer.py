"""Fail-closed redaction for untrusted local command output."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


RULE_VERSION = "1.0"
_REDACTED = "[REDACTED]"
_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.DOTALL)),
    ("credentialed_url", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@[^\s]+", re.IGNORECASE)),
    ("bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)),
    ("assignment", re.compile(r"\b(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD|PASSWD|ACCESS[_-]?KEY|AWS_SECRET_ACCESS_KEY)\b\s*(?:=|:)\s*[^\s'\"]+", re.IGNORECASE)),
    ("cloud_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("synthetic_canary", re.compile(r"\bAGC[_-]?(?:SYNTHETIC[_-]?)?CANARY[_-]?(?:SECRET|TOKEN)[A-Za-z0-9._-]*\b", re.IGNORECASE)),
)


class OutputSanitizationError(RuntimeError):
    """Raised when untrusted output cannot be represented safely."""


@dataclass(frozen=True)
class SanitizedOutput:
    text: str
    raw_digest: str
    redaction_count: int
    rule_version: str = RULE_VERSION


def sanitize_output(raw: bytes, *, tail_lines: int = 40) -> SanitizedOutput:
    """Return a bounded redacted summary and a digest of the original bytes.

    Raw bytes are intentionally never returned or retained by this interface.
    """
    if not isinstance(raw, bytes) or tail_lines < 1:
        raise OutputSanitizationError("invalid command-output input")
    try:
        text = raw.decode("utf-8", errors="replace")
        count = 0
        for _, pattern in _RULES:
            text, replacements = pattern.subn(_REDACTED, text)
            count += replacements
        return SanitizedOutput(
            text="\n".join(text.splitlines()[-tail_lines:]),
            raw_digest=hashlib.sha256(raw).hexdigest(),
            redaction_count=count,
        )
    except Exception as exc:  # pragma: no cover - defensive fail-closed boundary
        raise OutputSanitizationError("command output could not be sanitized") from exc
