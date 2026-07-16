# AGC-OSS-GROWTH-05-R1 — upstream baseline validation

## Conclusion

`BASELINE_RED_CANDIDATE_DELTA_CLEAN`

The target's contribution policy requires its generation and verification workflow, but does not explicitly require a wholly green repository baseline or prohibit a transparently disclosed baseline-red submission. No PR template or repository CI workflow was present at revalidation. Recent closed contribution examples also show that contributors have not uniformly run the complete verifier. This is an evidence-based policy interpretation, not a maintainer endorsement.

## Fixed inputs

| Input | Value |
| --- | --- |
| Target | `Picrew/awesome-agent-harness` |
| Upstream branch / SHA | `main` / `85d6410079854334e50b2de8e8961b4ac09de1e7` |
| Candidate branch / SHA | `add-coding-agent-governance` / `47c9e1a736b5d361a85589598fe49bb7f9d1548f` |
| Baseline worktree | `/tmp/awesome-agent-harness-baseline` |
| Candidate worktree | `/home/liyouran1997/projects/awesome-agent-harness-submission` |

## Same-command comparison

Both worktrees used Python 3 with `PYTHONDONTWRITEBYTECODE=1` and the target-prescribed commands:

```text
python3 scripts/sync_github_metadata.py
python3 scripts/render_readme.py
python3 scripts/verify_catalog.py
```

Metadata synchronization and README generation completed successfully for both. The full verifier exited nonzero for both because of pre-existing catalog failures.

| Set | Verifier result | Failure count |
| --- | --- | ---: |
| Baseline | nonzero | 86 |
| Candidate | nonzero | 2 |
| Candidate minus baseline | empty | 0 |

The failure-set JSON artifacts were written locally, not committed to the target repository:

```text
/tmp/baseline_failures.json
/tmp/candidate_failures.json
/tmp/failure_comparison.json
/tmp/targeted_entry_validation.json
```

## Baseline and candidate failures

The candidate's only two failure identities are already contained in the upstream baseline:

1. `AGENT.md` (`https://github.com/agentmd/agent.md`) has `updated_at: 2025-07-10`, older than the verifier's 12-month threshold.
2. `https://code.claude.com/docs/en/agent-sdk/overview` returns HTTP 404.

The baseline had the same stale entry and URL failure plus additional external-link reachability failures. Those broader failures are not attributed to the candidate. The comparison criterion is therefore satisfied: `C ⊆ B` and the candidate introduces no new failure identity.

## Candidate-specific validation

All 14 directed checks passed:

- YAML parses and contains required fields, including the synchronized MIT license field.
- Category is `Guardrails, Security & Governance`.
- Tags, GitHub URL, summary length, Chinese summary, and duplicate check pass.
- Current public metadata is preserved: 2 stars and `2026-07-16` update date.
- Both generated README files contain the entry.
- The entry order follows the target's category sort rule.

## Scope and policy result

- Only `data/projects.yaml`, generated `README.md`, generated `README_zh.md`, and the generated verification report are part of the candidate commit.
- No unrelated entry, including `AGENT.md` or the Claude Agent SDK overview, was modified.
- The author disclosure and baseline-red explanation are included in the PR body.
- No second target, Issue, Discussion, comment, or PR #39 resubmission was made.

`POLICY_ALLOWS_BASELINE_EXCEPTION`
