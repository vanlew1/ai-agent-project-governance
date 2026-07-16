# AGC-OSS-GROWTH-05-R5 — determinism capability audit

## Conclusion

`MAINTAINER_CLARIFICATION_REQUIRED`

The target repository has no documented or implemented official way to produce a deterministic, scoped single-entry contribution while complying with its required live metadata sync. R5 therefore did not create a new submission PR.

## Evidence

- Fixed upstream examined: `85d6410079854334e50b2de8e8961b4ac09de1e7`.
- R4 ran `sync_github_metadata.py` and `render_readme.py` from that same commit in isolated baseline and candidate worktrees.
- The candidate added one target entry but also modified 10 existing entries because live GitHub star values changed between the two runs. The two generated README files carried the same unrelated changes.
- The source contribution guide requires all contributors to run metadata sync, README rendering, and verification, then commit generated files together.

## Official capability matrix

| Capability | Present | Official | Safe | Usable |
| --- | ---: | ---: | ---: | ---: |
| Offline mode | No | No | N/A | No |
| Metadata snapshot | No | No | N/A | No |
| Cache file | No | No | N/A | No |
| Single-entry sync | No | No | N/A | No |
| Changed-only mode | No | No | N/A | No |
| Skip metadata refresh | No | No | N/A | No |
| Fixed timestamp | No | No | N/A | No |
| Deterministic test fixture | No | No | N/A | No |

`sync_github_metadata.py` accepts no CLI mode arguments and always fetches every GitHub entry, refreshes fields, sorts entries, and updates `last_verified`. `render_readme.py` also accepts no CLI mode arguments. `verify_catalog.py` supports only `--skip-links`, which affects URL reachability checks rather than metadata generation.

## Precedent review

| PR | Submitted files | Sync claimed | Maintainer response | Result / interpretation |
| --- | --- | --- | --- | --- |
| [#45](https://github.com/Picrew/awesome-agent-harness/pull/45) | README mirrors, YAML, verification report | Yes | None | Existing `vanlew1` PR; R5 did not modify it. |
| [#26](https://github.com/Picrew/awesome-agent-harness/pull/26) | README mirrors, YAML, verification report | Explicitly skipped | None | Contributor statement only; no maintainer authorization. |
| [#25](https://github.com/Picrew/awesome-agent-harness/pull/25) | YAML only | Explicitly skipped | None | Contributor comment says daily regeneration handles mirrors; not maintainer guidance. |
| [#19](https://github.com/Picrew/awesome-agent-harness/pull/19) | README mirrors, YAML, verification report | Explicitly skipped | None | Contributor statement only; no maintainer authorization. |

No reviewed example supplies an explicit maintainer-approved minimal-submission workflow. The target repository has Issues enabled and Discussions disabled.

## Official-mode experiment

No experiment was run beyond the isolated R4 generation already recorded: no official snapshot, cache, offline, single-entry, changed-only, or skip-sync feature exists to test. R5 did not alter target scripts, inject mock GitHub responses, or fabricate metadata.

## Next step

Wait until at least 2026-07-24 for a maintainer response to issue #46. Do not open a new submission PR, comment again, or pursue a second target in the meantime.
