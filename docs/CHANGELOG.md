# Changelog

## Unreleased

### Added

- Added a provenance-bound adoption lifecycle foundation: formal Preflight bridging, CAS ProjectState transitions, confirmed-candidate test selection, workspace snapshots, fresh-evidence verification, and non-production closure semantics.

- Added provenance-bound `activate-approved` for Existing Project Adoption. It can only transition an installed Runtime to `ACTIVATED_NOT_PREFLIGHTED`; it does not run Preflight, tests, verification, closure, network, Git, or production operations.

- Added public-facing README files, Quickstart, adoption and demo guides, examples, community files, Issue/PR templates, compatibility evidence, and repository-settings checklist for GOV-OSS-GROWTH-01.

- Added P2 local-state, approval-freshness, Guard baseline and acceptance tests; approval-to-Guard enforcement remains incomplete.
- Added deterministic TaskRequest/ProjectState to TaskContract Preflight models, CLI, fixtures, and tests; persistence, guards, test execution, and automatic closure remain unimplemented.
- Added the governance runtime target architecture, module registry, core Schema contracts, baseline validator, and baseline tests. Runtime behavior remains disabled in P0.
- 鍦?`agent_rules/14_cost_aware_testing_rules.md` 澧炲姞 Token-Efficient Execution Contract锛岃鐩?Gate 0銆佺‘璁ゅ鐢ㄣ€佹渶灏忚鍙栥€佽祫浜у鐢ㄣ€佸垎灞傛祴璇曘€佸浠芥椂鏈恒€侀樆濉?checkpoint銆佽緭鍑哄帇缂╁拰鎶ュ憡鍘嬬缉銆?
- 鍦?`agent_rules/RULES_INDEX.yaml` 澧炲姞 token-efficient execution 鍚堝悓鍏ュ彛锛屾槑纭Е鍙戞潯浠跺拰 Gate 0 鍓嶇疆浜嬮」銆?

### Changed

- 鏇存柊 `agent_rules/00_rule_router.md` 鍜?`AGENTS.md`锛屽皢楂樻垚鏈€佽仈缃戙€佹寮忓啓鍏ャ€佷笉鍙€嗘搷浣滅瓑浠诲姟鐨勪汉宸ュ墠缃棬鍓嶇Щ鍒版墿灞曡鍙栧拰鏂藉伐涔嬪墠銆?

### Fixed

-
- Added P3 allowlisted verification, closure, isolated CLI acceptance, and compact reporting; adapters, CI, and multi-agent remain disabled.

## GOV-RUNTIME-P5
- Added self-validation, schema compatibility, isolated bootstrap checks, a fixed local release gate, and least-privilege GitHub Actions CI.

## GOV-RUNTIME-P4
- Added deterministic generic, Python, Node and WeChat Mini Program adapters, adapter detection, bootstrap configuration, adapter-aware test planning and guard classification.


## GOV-RUNTIME-P6
- Added deterministic local multi-agent orchestration, handoff freshness, ownership checks and CLI entry points.


## [1.0.0] - 2026-07-13

### Added

- Deterministic governance runtime V1: Preflight, local state/approval/guard, allowlisted verification/closure, adapters/bootstrap, read-only CI gate, and local multi-agent orchestration contracts.

### Security

- Runtime and CI remain local/read-only by default: no remote Agent/API invocation, automatic worktree, Git write, Secret use, deployment, or publishing.

### Known limits

- Prompt bundles are manually distributed to Agent threads. GitHub Actions configuration is locally validated only; V1 has not been committed, pushed, tagged, or remotely executed from this checkout.
