<!-- encoding: UTF-8 -->

# CASE-001 Cross-Platform Validation Report

## Windows native

- Runtime: CPython 3.13 at the local Windows installation.
- Direct full suite: 163 tests executed; the one initial failure was a test-fixture scope error that included a non-formal Windows CRLF file, then corrected and revalidated.
- Final fixed release gate: `PASS (8/8 gates)`.
- Embedded final full suite: `PASS`, 163 tests, 2 expected platform skips, no failures or errors.
- Tests gate duration: approximately 219 seconds; the fixed per-gate timeout is now 300 seconds for cross-platform parity.

## WSL authority

- The two exact local commits were transferred to an independent WSL worktree without push.
- `python3 -m unittest discover tests`: PASS.
- `python3 scripts/run_governance_ci.py`: PASS, 8/8 gates.
- The Chinese/space-path, CRLF raw/normalized digest, C0, and temporary demo-output cases are included in the accepted suite.

## Interpretation

Windows and WSL results exercise the same repository content. The fallback for a WSL process reading a Windows `.git` pointer is conditional on that precise pointer form and verifies a repository snapshot; it is not an unconditional skip.
