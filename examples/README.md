# Examples

All examples are offline, minimal, and free of secrets, production configuration, build output, and downloaded dependencies.

| Example | Marker | Expected adapter | Passing check | Blocking idea |
| --- | --- | --- | --- | --- |
| [Python](python-small/README.md) | `pyproject.toml` | `python` | `python -m unittest discover -s tests` | `secrets/**` is denied. |
| [Node.js](node-small/README.md) | `package.json` | `node` | `npm test` | `node_modules/**` is generated. |
| [WeChat Mini Program](wechat-miniprogram/README.md) | `project.config.json` | `wechat_miniprogram` | `npm test` | `project.private.config.json` is sensitive. |

```powershell
python scripts/agent_detect_adapter.py --root examples/python-small detect
python scripts/agent_detect_adapter.py --root examples/node-small detect
python scripts/agent_detect_adapter.py --root examples/wechat-miniprogram detect
```
