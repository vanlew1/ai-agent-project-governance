# AGENTS.md

本仓库是通用 Agent 治理模板，不是具体业务项目。

## 轻量任务快车道

适用于 A 类任务：文案、注释、小 bug、局部测试、已有函数轻量调整。

A 类任务默认只读：

1. `docs/AGENT_QUICK_CONTEXT.md`
2. `README.md`
3. 与任务直接相关的源码或测试片段

A 类任务默认不要读取完整 `docs/ARCHITECTURE.md`、`docs/IMPLEMENTATION_PLAN.md`、`docs/PROJECT_BRIEF_DRAFT.md`、`agent_rules/RULES_INDEX.yaml`，除非任务涉及架构边界、模块登记、数据安全、发布、Git 操作、外部接入或用户明确要求。

## 使用原则

1. 先读 `agent_rules/RULES_INDEX.yaml`。
2. 再读 `agent_rules/00_rule_router.md`。
3. 如果项目方案尚未确认，先读 `agent_rules/15_plan_adaptation_rules.md`，判断处于 DISCOVERY、ADAPTATION 还是 EXECUTION。
4. 再读 `agent_rules/01_task_classification.md`，判断任务属于 A、B、C 哪一类。
5. 仅按当前任务需要加载规则，避免无差别全量扫描。

## 模板仓库边界

- 本模板用于复制到新项目后再启用。
- 新项目必须补齐 `agent_rules/11_project_specific_rules.md`。
- 如果项目专有规则与通用规则冲突，以项目专有规则为准。

## 每次任务开始前必须明确

轻量任务只需简短说明任务等级、修改范围和验证方式。B/C 类任务需要明确：

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
