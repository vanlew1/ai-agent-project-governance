# 00 Rule Router

## 目标

本文件定义 Agent 在新项目中的最小读取顺序，避免为了形式合规而无差别加载全部规则。

## 基础顺序

1. 读取 `RULES_INDEX.yaml`。
2. 如果项目方案未确认，读取 `15_plan_adaptation_rules.md`，先判断 DISCOVERY、ADAPTATION 或 EXECUTION。
3. 读取 `01_task_classification.md`。
4. 根据任务等级与触发条件，补充读取对应规则。
5. 如任务涉及项目专有边界，补充读取 `11_project_specific_rules.md`。

## 路由原则

- 默认按 B 类任务处理不明确需求。
- 未确认施工方案前，默认按 DISCOVERY 或 ADAPTATION 处理，不得直接进入 EXECUTION。
- 风险可以升级，修改范围不得自动扩大。
- 只在触发条件满足时加载附加规则。
- 规则读取应服务于当前任务，而不是覆盖式浏览仓库。
