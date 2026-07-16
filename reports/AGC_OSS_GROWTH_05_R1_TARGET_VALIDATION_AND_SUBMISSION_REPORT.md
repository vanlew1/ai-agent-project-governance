# AGC-OSS-GROWTH-05-R1 — targeted submission report

## Outcome

`ONE_TRANSPARENT_EXTERNAL_PR_SUBMITTED`

- Target: `Picrew/awesome-agent-harness`
- External PR: https://github.com/Picrew/awesome-agent-harness/pull/45
- Base: `main` at `85d6410079854334e50b2de8e8961b4ac09de1e7`
- Head: `vanlew1:add-coding-agent-governance` at `47c9e1a736b5d361a85589598fe49bb7f9d1548f`
- Changed files: `data/projects.yaml`, `README.md`, `README_zh.md`, and `reports/verification/2026-07-17.md`.
- Current target PR checks: none reported by GitHub at creation time.

## Disclosure and validation

The PR explicitly discloses that its author submitted Coding Agent Governance, that its acceptance evidence is offline and synthetic-only, and that `CLOSED != PRODUCTION_READY`.

It also states that the target's full verifier remains red only for failures already present in the upstream baseline: stale `AGENT.md` metadata and the Claude Agent SDK overview HTTP 404. It does not claim that all checks pass, and it does not ask maintainers to repair those unrelated entries.

The baseline-versus-candidate evidence is recorded in [the upstream baseline validation report](AGC_OSS_GROWTH_05_R1_UPSTREAM_BASELINE_VALIDATION.md). The candidate-specific checks passed and the failure delta is empty.

## Safety boundaries

- PR #6 was already merged by merge commit `d4770b4`.
- Exactly one third-party PR was created.
- No second target, Issue, Discussion, maintainer ping, comment, or automatic follow-up was created.
- The previously declined `brandonhimpfen/awesome-ai-coding-agents#39` was not reopened or resubmitted.
- No runtime, schema, CLI, state-machine, production, tag, release, deployment, force-push, or unrelated-upstream change occurred.

## Next review

Review PR #45 no earlier than 2026-07-24. Until then, leave the external PR unchanged unless maintainers request changes.
