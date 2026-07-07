# AGENTS.md

本仓库是通用 Agent 治理模板，不是具体业务项目。

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

1. 当前项目模式：DISCOVERY、ADAPTATION 或 EXECUTION。
2. 当前任务等级。
3. 本次读取了哪些规则文件。
4. 允许修改哪些目录或文件。
5. 禁止修改哪些目录或文件。

## 全局红线

- 未经授权不得写入生产环境。
- 未经授权不得修改数据库结构或批量覆盖数据。
- 审计任务默认只读。
- 外部建议必须适配当前项目上下文，不得直接照抄。
- 未经验证不得宣称任务完成。
- 施工方案未确认前，不得把探索性对话固化为正式架构、模块表、任务表或变更日志。
