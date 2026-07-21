# Governance Runtime CI Guide

Run `python scripts/run_governance_ci.py` before release-oriented changes. It is read-only and uses fixed Python argv: governance and reference validation, schema compatibility, dependency direction, isolated bootstrap, CI security, tests, and quality checks. Each gate has a 300-second cross-platform timeout so the complete Windows suite is not rejected by the faster Linux-oriented limit. GitHub Actions calls the same script on Linux; its Windows smoke separately covers Unicode bootstrap and compilation. The workflow uses only `contents: read`, no secrets, and no write or publish operations.


## V1 release preparation

A local PASS verifies the eight fixed gates only. It does not prove a remote GitHub Actions run; commit, push, and remote-run observation require explicit user authorization.
