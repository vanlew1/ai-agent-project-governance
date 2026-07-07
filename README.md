# Agent Governance Template

通用 Agent 治理模板，适用于需要使用 Codex、Antigravity 或多 Agent 协作完成开发、评审、留档与发布控制的软件项目。

## 这个模板用于什么

本仓库提供一套可复制的治理骨架，用于约束 Agent 在新项目中的读取范围、改动边界、测试策略、留档方式和 Git 存档流程。

## 适合哪些项目

- AI 辅助开发项目
- 多 Agent 协作项目
- 需要审计与任务留痕的工程项目
- 希望把规则、模板和项目专有红线分离管理的代码仓库

## 如何复制到新项目

1. 复制 `AGENTS.md`、`agent_rules/`、`docs/`、`scripts/` 到新项目根目录。
2. 运行 `python scripts/init_new_project.py`，或手动将所有 `*.template.*` 文件改为正式文件名。
3. 在新项目中补齐项目专有规则、架构说明、模块登记和任务登记。
4. 新项目应在独立 Git 仓库中维护自己的任务、变更与版本记录。

## 新项目必须填写的模板文件

- `agent_rules/11_project_specific_rules.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_REGISTRY.yaml`
- `docs/TASK_REGISTRY.yaml`
- `docs/CHANGELOG.md`

## 核心文件作用

- `AGENTS.md`：Agent 入口说明，规定最小必要读取和基础路由顺序。
- `agent_rules/RULES_INDEX.yaml`：机器可读规则索引，用于任务分类与规则装载。
- `agent_rules/task_cards/`：按任务等级提供执行检查清单。

## 如何使用 TASK / CHG / CHANGELOG

- `TASK`：登记任务目标、范围、负责人、状态与验证方式。
- `CHG`：记录单次施工变更、受影响模块、风险和回滚信息。
- `CHANGELOG`：记录对外可见的阶段性版本变化。
- 推荐做法：先登记 `TASK`，施工中补充 `CHG`，收口时更新 `CHANGELOG`。

## Git 本地存档规则

- 需要可回滚的阶段性成果时，应优先做本地 commit。
- 提交前只添加本次任务相关文件，不使用无差别全量加入。
- 推送远程仓库前，应再次确认忽略规则、敏感文件排除和变更范围。

## 成本感知测试规则

- 对高成本任务优先选择 smoke test、样本验证、局部回归和 dry-run。
- 只有在风险等级要求时，才执行更重的完整回归。
- 不能用低成本验证冒充高置信度结论。

## 边界说明

本仓库只包含通用治理模板，不包含任何具体业务规则、业务代码、数据资产或项目私有配置。
