# 11 Project Specific Rules

> 复制到新项目后，请改名为 `11_project_specific_rules.md` 并补齐内容。

## 项目专有红线

### Confirmed Red Lines

只有 owner 明确确认后，才把规则写到这里。

- 在这里写明禁止触碰的目录、数据、服务和环境。
- 在这里写明哪些命令必须人工确认后才能执行。

### Draft Red Lines

ADAPTATION 阶段的候选规则写在这里。草案规则可以用于评审，但不能当作 EXECUTION 施工许可。

- Draft rule:

## 项目专有约束

### Confirmed Constraints

只有 owner 明确确认后，才把约束写到这里。

- 在这里写明命名规范、模块边界、发布流程或审计要求。
- 在这里写明哪些测试是强制项，哪些只是建议项。

### Draft Constraints

- Draft constraint:

## 外部系统与数据接入

如果项目涉及外部平台、网站、API、登录态、爬虫、浏览器自动化、Webhook、云服务、生产系统、数据导入或数据导出，必须先明确：

- 允许的接入方式：
- 允许的频率或规模：
- 可存储的数据：
- 存储位置：
- 失败兜底方式：
- 明确禁止的行为：
- owner 批准或接受的风险：

## 项目专有背景

- 在这里说明仓库用途、关键模块、运行方式和常见风险。
