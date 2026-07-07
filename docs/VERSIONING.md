# Versioning

## 推荐做法

- 任务推进使用 `TASK` 管理范围与状态。
- 单次施工使用 `CHG` 记录改动、风险与验证。
- 对外可见阶段结果使用 `CHANGELOG` 记录。

## 最小流程

1. 确认项目已经进入 EXECUTION，且执行确认字段完整。
2. 建立或更新 `TASK`。
3. 实施改动并记录必要 `CHG`。
4. 收口时更新 `CHANGELOG`。
5. 如需发布，再补充标签或版本号。

## 方案未确认时

如果项目仍处于 DISCOVERY 或 ADAPTATION，不要把草稿写成正式 `TASK`、`CHG` 或 `CHANGELOG`。先使用 `PROJECT_BRIEF_DRAFT`、`OPEN_QUESTIONS`、`BOOTSTRAP_DECISION` 和 `IMPLEMENTATION_PLAN` 收敛方案。

验证记录应区分：

- `automated_tests`：可重复自动测试。
- `repeatable_smoke`：可重复的轻量链路验证。
- `manual_one_off_checks`：一次性人工检查或临时命令。

不要把一次性人工检查写成自动化验证。

## 版本号建议

- `v0.x`：规则仍在快速演进。
- `v1.0.0`：模板结构稳定，适合更广泛复用。
- 后续遵循语义化版本或团队约定版本号。
