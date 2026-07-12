# AGENTS.md

本仓库是通用 Agent 治理模板，不是具体业务项目。

## 轻量任务快车道

轻量入口仅适用于 A 类任务：

- 文案修改
- README 小修
- 注释修改
- 局部格式修复
- 已有函数内极小调整
- 单个测试补充
- 不涉及数据写入、不涉及架构、不涉及 Git、不涉及外部 API 的小任务

A 类任务必须同时满足：

1. 修改范围小。
2. 影响面清晰。
3. 可快速验证。
4. 不涉及生产数据或敏感资产。
5. 不引入新模块。
6. 不改变架构边界。
7. 不触发 Git、外部 API、LLM API、联网抓取或大规模测试。

A 类任务默认只读：

1. `docs/AGENT_QUICK_CONTEXT.md`
2. `README.md`
3. 与任务直接相关的源码或测试片段

A 类任务默认不要读取完整 `docs/ARCHITECTURE.md`、`docs/IMPLEMENTATION_PLAN.md`、`docs/PROJECT_BRIEF_DRAFT.md`、`agent_rules/RULES_INDEX.yaml`，除非任务涉及架构边界、模块登记、数据安全、发布、Git 操作、外部接入或用户明确要求。

如任务涉及以下任一项，必须退出轻量入口并读取完整规则树：

- 新增文件或模块
- 修改架构边界
- 修改数据库、缓存、production、正式证据库
- 修改 Git 存档、push、remote
- 调用 LLM API、外部 API、联网抓取
- 全量扫描、大规模测试、成本较高任务
- 安全、隐私、密钥、token
- 跨模块改动
- 任务范围不明确

如果 Agent 在执行轻量任务过程中发现任一升级条件，应立即停止继续施工，并输出：

当前任务已触发升级条件，不能继续按轻量入口执行。
需要切换到完整治理规则树后重新确认任务类型、允许范围、禁止范围和验证方式。

## 使用原则

1. 先读 `agent_rules/RULES_INDEX.yaml`。
2. 再读 `agent_rules/00_rule_router.md`。
3. 涉及真实外部 API、正式数据写入、网络/VPN 状态、用户授权、不可逆或高成本操作时，先按 `agent_rules/14_cost_aware_testing_rules.md` 执行 Gate 0。
4. 如果项目方案尚未确认，先读 `agent_rules/15_plan_adaptation_rules.md`，判断处于 DISCOVERY、ADAPTATION 还是 EXECUTION。
5. 再读 `agent_rules/01_task_classification.md`，判断任务属于 A、B、C 哪一类。
6. 仅按当前任务需要加载规则，避免无差别全量扫描。

## 模板仓库边界

- 本模板用于复制到新项目后再启用。
- 新项目必须补齐 `agent_rules/11_project_specific_rules.md`。
- 如果项目专有规则与通用规则冲突，以项目专有规则为准。

## 每次任务开始前必须明确

轻量任务仍需保留最低报告闭环：

- 修改文件
- 核心改动
- 测试/检查
- 未触碰范围
- 是否需要升级

`docs/AGENT_QUICK_CONTEXT.md` 只是轻量入口，不是规则真源；如与 `AGENTS.md`、`agent_rules/RULES_INDEX.yaml` 或 `agent_rules/` 下完整规则冲突，以完整规则树为准。

B/C 类任务需要明确：

1. 当前项目模式：DISCOVERY、ADAPTATION 或 EXECUTION。
2. 当前任务等级。
3. 本次读取了哪些规则文件。
4. 允许修改哪些目录或文件。
5. 禁止修改哪些目录或文件。

## 节省上下文要求

1. 不要全文读取大文件，先用 `rg` 定位。
2. 只查看相关函数、相关 UI block 或相关测试附近代码。
3. 修改后只总结改动点，不回显完整 diff。
4. 测试输出只保留通过/失败摘要和失败原因。
5. 施工报告只写修改文件、核心改动、测试结果和风险。
6. 不重复粘贴大段源码、测试文件或历史背景。

## 全局红线

- 未经授权不得写入生产环境。
- 未经授权不得修改数据库结构或批量覆盖数据。
- 审计任务默认只读。
- 外部建议必须适配当前项目上下文，不得直接照抄。
- 未经验证不得宣称任务完成。
- 施工方案未确认前，不得把探索性对话固化为正式架构、模块表、任务表或变更日志。
