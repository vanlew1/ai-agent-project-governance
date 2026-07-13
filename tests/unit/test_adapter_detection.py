from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from governance.adapters.detection import detect_adapters


class AdapterDetectionTest(unittest.TestCase):
    def test_python_and_node_are_mixed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
            (root / "package.json").write_text('{"scripts":{"test":"node test.js"}}', encoding="utf-8")
            result = detect_adapters(root)
            self.assertEqual("MIXED", result.status)
            self.assertEqual(("python", "node"), result.detected_adapters)

    def test_miniprogram_is_primary_with_node_auxiliary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "project.config.json").write_text("{}", encoding="utf-8")
            (root / "package.json").write_text("{}", encoding="utf-8")
            result = detect_adapters(root)
            self.assertEqual("wechat_miniprogram", result.primary_adapter)
            self.assertEqual(("node",), result.auxiliary_adapters)

    def test_empty_repository_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = detect_adapters(Path(temporary))
            self.assertEqual(("generic",), result.detected_adapters)
            self.assertEqual("FALLBACK", result.status)
