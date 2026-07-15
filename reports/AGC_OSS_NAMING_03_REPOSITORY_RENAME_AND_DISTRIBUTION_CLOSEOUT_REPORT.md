# AGC-OSS-NAMING-03 — repository naming and distribution closeout

## Final status

`PARTIAL` — the public product presentation now uses **Coding Agent Governance**. The repository slug, GitHub metadata, PR, merge, awesome-list update, and direct-user distribution were not changed because the configured GitHub CLI authentication is invalid. No credential refresh, credential inspection, or authentication workaround was attempted.

## Naming decision

| Candidate | Clarity | Distinctiveness | Search terms | Confusion risk | Extension room | Migration cost | Total / 30 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `coding-agent-governance` | 5 | 4 | 5 | 4 | 4 | 4 | 26 |
| `coding-agent-governance-runtime` | 4 | 4 | 4 | 4 | 5 | 3 | 24 |
| `agent-governance-runtime` | 2 | 2 | 3 | 2 | 4 | 3 | 16 |
| `ai-agent-project-governance` | 2 | 3 | 3 | 2 | 3 | 5 | 18 |

Selected public title: **Coding Agent Governance**.

Selected future slug, subject to an authenticated GitHub availability check: `coding-agent-governance`.

Decision: `DISPLAY_NAME_ONLY` until the rename gate can be completed. The live slug remains `ai-agent-project-governance`, so all clone, security, homepage, and launch links deliberately remain live and unchanged.

## Rename-gate evidence

- Public remote check: `git ls-remote https://github.com/vanlew1/ai-agent-project-governance.git HEAD` returned `2b6a553a79beb30146bb3217f4e3a4307cd01c10`.
- Target public remote check returned `Repository not found` for `vanlew1/coding-agent-governance`. This supports public availability but cannot exclude a private collision, so it is not sufficient to rename without a valid authenticated owner session.
- Repository search found no external GitHub Action reference, raw GitHub URL, GitHub API URL, GitHub Pages URL, package coordinate, container configuration, or action manifest tied to the old slug.
- Compatibility-facing schema `$id` values retain the old GitHub Pages namespace. They are part of existing data contracts and were intentionally not changed.
- Existing awesome-list submission is recorded as `brandonhimpfen/awesome-ai-coding-agents#39`; no remote update was attempted.
- Rollback is straightforward: no remote rename or metadata write occurred, and the repository's current live links remain the old slug.

## Baseline and Git state

- Initial local branch / HEAD: `codex/superpowers-release-closeout` / `e3d2a4b9dffd3a3a7a501450601c78b8e44bdb8b`.
- Remote baseline after read-only fetch: `origin/main` / `2b6a553a79beb30146bb3217f4e3a4307cd01c10`.
- Task branch: `codex/repository-rename-distribution` based on `origin/main`.
- Current remote: `https://github.com/vanlew1/ai-agent-project-governance.git` for fetch and push.
- Local commits:
  - `cffeae4` — `docs(project): clarify naming and prepare repository rename`
  - `68d40a3` — `docs(project): keep live URLs pending repository rename`
- No push, PR, merge, remote rename, release mutation, tag mutation, or remote metadata update occurred.

## Local changes

- Updated English and Chinese README titles to Coding Agent Governance and made the pending slug migration explicit.
- Updated current Share Kit and launch wording to the selected public title.
- Updated the Changelog with the correct pending-rename status.
- Preserved current clone commands, homepage, security, and launch URLs so public links stay valid.
- Did not modify `governance/`, `schemas/`, `scripts/`, `config/`, core runtime semantics, CLI contracts, state-machine behavior, or historical reports.

## Verification

Executed from `/home/liyouran1997/projects/ai-agent-project-governance`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q tests.unit.test_public_adoption_assets tests.unit.test_demo_visual_proof
Result: PASS (12 tests)

PYTHONDONTWRITEBYTECODE=1 python3 examples/demo/run_visual_proof.py
Result: PASS; generated a temporary synthetic visual proof

PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_governance_ci.py
Result: PASS (8/8 gates; full suite passed)

git diff --check
Result: PASS
```

The final full governance gate was run after the live-link correction. No test-network access, dependency installation, production-data write, or destructive Git operation was used.

## External distribution and blockers

- `gh auth status` reported the active `vanlew1` token as invalid.
- This is a hard blocker under `GOV-BLOCKER-001` for GitHub writes; authentication refresh requires owner action and was not attempted.
- X, Reddit, and Hacker News were not posted. No browser automation, login bypass, CAPTCHA handling, or credential handling was attempted.
- External distribution status therefore remains `PARTIAL`, not `COMPLETE`.

## Safe continuation

1. Owner re-authenticates GitHub with a normal approved flow.
2. Recheck target-slug availability in the authenticated repository settings.
3. Rename the repository to `coding-agent-governance`, then update `origin` and verify redirect, fetch, push, Actions, tags, releases, and metadata.
4. Replace the intentionally preserved old live URLs, push this branch, open and merge the PR, and update the existing awesome-list submission.
5. Attempt one direct-user channel only through an existing safe login session; otherwise preserve `PARTIAL` and use the vetted launch copy for manual posting.
