# Compatibility

| Label | Exact meaning | Does not mean |
| --- | --- | --- |
| Tested | Local automated or repeatable evidence exists. | Every version or layout works. |
| Supported by local runtime | A local adapter or command path exists. | Official third-party integration. |
| Instruction-compatible | Instructions can be copied into a workflow. | The product executes this runtime. |
| Not yet tested | No local evidence is recorded. | Known incompatibility. |
| Planned | A roadmap item. | A delivery commitment. |

| Item | Label | Evidence |
| --- | --- | --- |
| Python | Tested; supported by local runtime | Adapter acceptance coverage. |
| Node.js | Tested; supported by local runtime | Adapter acceptance coverage. |
| WeChat Mini Program | Tested; supported by local runtime | Adapter acceptance coverage. |
| Generic fallback | Tested; supported by local runtime | Adapter acceptance coverage. |
| Linux local CI | Tested | Fixed local gate. |
| Windows local smoke | Tested | Unicode-path bootstrap check. |
| Codex | Instruction-compatible | `AGENTS.md` guides a task; no product integration is claimed. |
| Claude Code | Not yet tested | No recorded end-to-end case. |
| Cursor | Not yet tested | No recorded end-to-end case. |
| GitHub Copilot | Not yet tested | No recorded end-to-end case. |

The repository has a GitHub Actions workflow named `Governance CI` and a `v1.0.0` Release. This document does not claim a live remote-CI result for the current `main` branch; any test result recorded in a Release is historical evidence for that Release.
