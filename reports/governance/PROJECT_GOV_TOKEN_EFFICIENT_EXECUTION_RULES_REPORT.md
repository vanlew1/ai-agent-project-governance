# PROJECT-GOV-TOKEN-EFFICIENT-EXECUTION-RULES Report

## 结论

该优化建议适合当前通用 Agent 治理模板。已采用其中高价值部分，并按现有模板结构做了去重合入：主规则集中放入 `agent_rules/14_cost_aware_testing_rules.md`，路由、索引和 `AGENTS.md` 仅保留入口与触发条件。

## 实际修改

- `agent_rules/14_cost_aware_testing_rules.md`
  - 新增 Token-Efficient Execution Contract。
  - 覆盖 Gate 0、确认复用、最小读取、已有资产复用、测试分层、数据库备份时机、阻塞任务 checkpoint、输出压缩、Windows 执行、报告压缩、施工指令格式和验收要求。
- `agent_rules/00_rule_router.md`
  - 在基础顺序中加入 Gate 0 前置检查。
  - 明确成本、联网、正式写入或大规模验证任务应读取成本感知规则中的执行合同。
- `agent_rules/RULES_INDEX.yaml`
  - 新增 `execution_contracts.token_efficient_execution` 入口。
  - 明确触发读取条件与 Gate 0 必须早于代码修改、完整规则树读取、全量回归、数据库备份和真实外部请求。
- `AGENTS.md`
  - 在使用原则中增加一条简短 Gate 0 入口。
- `docs/CHANGELOG.md`
  - 新增治理变更记录。

## 适配判断

- 适合吸收：
  - Gate 0 人工前置门；
  - 已有确认复用规则；
  - 最小读取和输出压缩；
  - 已有资产复用门；
  - Level 1 -> Level 2 -> Level 3 分层测试；
  - 正式数据库备份紧邻真实写入；
  - 阻塞任务只产最小 checkpoint。
- 已做压缩：
  - 未把同一套规则复制到 `AGENTS.md`、router 和 index。
  - `AGENTS.md` 只增加入口，避免长期维护多个规则真源。

## 验收结果

- 真实 API、联网、connectivity probe、登录态和云服务任务会先触发 Gate 0。
- Gate 0 缺失时规则要求不修改代码、不运行完整测试、不备份正式数据库、不调用真实 API。
- 已确认且仍有效的人工条件允许复用，不重复询问。
- 小任务继续使用轻量入口，不默认读取完整规则树。
- 测试按 Level 1 -> Level 2 -> Level 3 逐步升级。
- 阻塞任务只生成 checkpoint，不生成完整正式施工报告。
- 其他分支或 worktree 资产需先记录 branch、commit、path、hash，再选择性同步。
- 新规则明确不得削弱数据安全、正式写入门禁、测试质量或验收要求。

## 测试与检查

- 本任务只修改治理文档，未修改业务代码。
- 已按目标文件范围完成文档级合入。

## 风险与下一步

- `docs/CHANGELOG.md` 原本不存在，本次按用户指定目标文件创建实际 changelog；模板文件保持不变。
- 后续若将本模板复制到具体项目，应在项目专属规则中补充该项目自己的 Gate 0 确认项。
