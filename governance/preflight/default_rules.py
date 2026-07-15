"""Stable P1 rule identifiers and conservative keyword sets."""

C_RULES = {"architecture": "CLASS-C-ARCHITECTURE", "new module": "CLASS-C-NEW-MODULE", "cross-system": "CLASS-C-CROSS-SYSTEM", "migration": "CLASS-C-MIGRATION", "release": "CLASS-C-RELEASE"}
A_RULES = {"documentation": "CLASS-A-DOCS-ONLY", "docs": "CLASS-A-DOCS-ONLY", "test": "CLASS-A-TEST-ONLY"}
RISK_RULES = {"external": "RISK-EXTERNAL-ACCESS", "production": "RISK-PRODUCTION-WRITE", "destructive": "RISK-DESTRUCTIVE-OPERATION", "secret": "RISK-SECRET-REQUIRED", "release": "RISK-RELEASE-PUBLISH", "scope": "RISK-SCOPE-MISSING", "unknown": "RISK-UNKNOWN-FAIL-CLOSED"}
DENY_PATTERNS = (".env", ".env/**", "config/secrets/**", "secrets/**", "data/production/**")
