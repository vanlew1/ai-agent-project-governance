# AGC-UX-EXISTING-PROJECT-ADOPTION-04F-R2 End-to-End Acceptance

Status: PASS — `END_TO_END_ADOPTION_VERIFIED`

## Scope and safety boundary

This acceptance used only synthetic projects below `/tmp/agc-adoption-04f-r2/`-style temporary roots. No real project, network request, credential, production data, Git write, release, or deployment was used. The baseline was the already-authorized dirty governance-runtime worktree at `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1`.

## Successful lifecycle matrix

| Synthetic target | Confirmed local candidate | Result |
| --- | --- | --- |
| Python | `python3 -m unittest discover -s tests` | `CLOSED` |
| Node | `npm test` (argv, `shell=False`) | `CLOSED` |
| Generic / non-Git | `python3 -c pass` | `CLOSED` |
| Chinese path | `python3 -c pass` | `CLOSED` |
| Path with spaces | `python3 -c pass` | `CLOSED` |

Each chain exercised dry-run planning, draft export, immutable Runtime-artifact compilation, final approval binding, new-files-only installation, approved activation, formal preflight, scope guard, digest-bound candidate selection, exact command run, verification, and closure. `CLOSED` records `production_ready=false`, `released=false`, and `deployed=false`.

## Security and failure-closed evidence

- State edges are CAS-bound to the exact preceding state digest and registered evidence type; skip/reverse requests are rejected.
- Lifecycle context reconstructs target, Runtime manifest, final approval, install/activation receipt, confirmation, and command-registry provenance to reject replay or identity changes.
- Guard rejects denied/unmatched paths; test planning accepts only confirmed candidates with an exact registry digest.
- Verification returns failed, incomplete, or stale results without allowing Closure; Closure rechecks workspace, state, provenance, blocker, and denied-scope freshness.
- Runner output retains raw SHA-256 digests and bounded sanitized tails only. The canary suite covers secret assignments, bearer values, credentialed URLs, private-key headers, mocked unsafe runner output, and sanitizer failure closure.
- Node `npm test` is allowed as a local argv invocation. Package-resolution and download operations (`npm install/ci/add/update`, `npx`, `pip`, `curl`, `wget`) remain ineligible.

## Reproducible verification

Executed from `/home/liyouran1997/projects/ai-agent-project-governance`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_code_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_schema_compatibility.py
git diff --check
```

Results: `147 tests OK`; governance validation passed for 32 schemas; quality gate passed with 155 Python files scanned; schema compatibility passed; whitespace check passed.

## Remaining risk and next step

This is synthetic, local-only evidence. It does not authorize a real-project installation, network access, package installation, Git writes, production readiness, release, or deployment. Independent read-only review is recommended and recorded separately.
