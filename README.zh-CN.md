# Agent Governance Runtime

> 面向 AI 编码 Agent 的本地确定性治理运行时。

[![Python](https://img.shields.io/badge/runtime-Python-blue)](requirements-governance.txt)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)

[English](README.md) | [简体中文](README.zh-CN.md)

它不是提示词集合：它检查范围、必跑测试、验证、收口和多 Agent 写入归属。

> 公开仓库当前没有已发布 Release 或 Actions workflow，因此不展示虚假的 Release 或 CI 通过徽章。请查看 [仓库设置清单](docs/GITHUB_REPOSITORY_SETTINGS_CHECKLIST.md)。

## 它能阻止什么

- TaskContract 之外的文件修改。
- 未跑必跑测试就声称完成。
- Verification 后工作区变化却沿用旧验证收口。
- 多个 Agent 无单写者保护地并行写同一文件。

## 五分钟开始

```powershell
git clone https://github.com/vanlew1/ai-agent-project-governance.git
cd ai-agent-project-governance
python -m pip install -r requirements-governance.txt
python scripts/run_governance_ci.py
```

## 如何工作

![治理运行时架构](docs/assets/architecture-overview.svg)

| 静态 Agent 说明 | Governance Runtime |
| --- | --- |
| 告诉 Agent 不要越界 | Guard 检查实际范围 |
| 要求 Agent 跑测试 | TestPlan 选择已登记命令 |
| 依赖完成声明 | Verification 与 Closure 决定完成 |
| 自然语言交接 | 结构化 Handoff |
| 人工协调 | DAG 与单写者保护 |
| 可复用旧验证 | 工作区变化阻止 Closure |

[Quickstart](docs/QUICKSTART.md) · [Demo](docs/DEMO.md) · [示例](examples/README.md) · [接入已有项目](docs/EXISTING_PROJECT_ADOPTION.md) · [兼容性](docs/COMPATIBILITY.md)

运行时不会自动启动 Agent、创建 worktree、访问远端 API、安装依赖、提交、推送、部署或发布。

## 社区

[贡献](CONTRIBUTING.md) · [安全](SECURITY.md) · [支持](SUPPORT.md) · [路线图](docs/OPEN_SOURCE_ROADMAP.md)

## 许可证

MIT，见 [LICENSE](LICENSE)。
