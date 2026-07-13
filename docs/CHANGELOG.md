# Changelog

## Unreleased

### Added

- Added P2 local-state, approval-freshness, Guard baseline and acceptance tests; approval-to-Guard enforcement remains incomplete.
- Added deterministic TaskRequest/ProjectState to TaskContract Preflight models, CLI, fixtures, and tests; persistence, guards, test execution, and automatic closure remain unimplemented.
- Added the governance runtime target architecture, module registry, core Schema contracts, baseline validator, and baseline tests. Runtime behavior remains disabled in P0.
- 在 `agent_rules/14_cost_aware_testing_rules.md` 增加 Token-Efficient Execution Contract，覆盖 Gate 0、确认复用、最小读取、资产复用、分层测试、备份时机、阻塞 checkpoint、输出压缩和报告压缩。
- 在 `agent_rules/RULES_INDEX.yaml` 增加 token-efficient execution 合同入口，明确触发条件和 Gate 0 前置事项。

### Changed

- 更新 `agent_rules/00_rule_router.md` 和 `AGENTS.md`，将高成本、联网、正式写入、不可逆操作等任务的人工前置门前移到扩展读取和施工之前。

### Fixed

-
