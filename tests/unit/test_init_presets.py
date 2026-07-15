from __future__ import annotations

import shutil
from contextlib import redirect_stdout
from io import StringIO
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.init_new_project import PRESETS, main, parse_args, write_preset_config

ROOT = Path(__file__).resolve().parents[2]


class InitPresetTest(unittest.TestCase):
    def test_all_presets_are_centrally_defined_and_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "template"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", ".agent_state"))
            focuses = set()
            for preset in PRESETS:
                data = write_preset_config(target, preset)
                saved = yaml.safe_load((target / "config" / "governance_preset.yaml").read_text(encoding="utf-8"))
                self.assertEqual(preset, data["preset"])
                self.assertEqual(data, saved)
                focuses.add(tuple(data["initial_focus"]))
            self.assertEqual(3, len(focuses))

    def test_default_cli_preset_preserves_the_existing_baseline(self) -> None:
        with patch("sys.argv", ["init_new_project.py"]):
            self.assertEqual("standard", parse_args().preset)

    def test_existing_target_is_not_silently_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "already-there"
            target.mkdir()
            args = Namespace(adapter="auto", output_dir=base, preset="standard")
            with patch("scripts.init_new_project.parse_args", return_value=args), \
                 patch("scripts.init_new_project.prompt_text", side_effect=["already-there", "demo", "owner", "summary"]), \
                 patch("scripts.init_new_project.prompt_yes_no", return_value=False), \
                 redirect_stdout(StringIO()):
                self.assertEqual(1, main())
            self.assertEqual([], list(target.iterdir()))

    def test_invalid_preset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "template"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", ".agent_state"))
            with self.assertRaises(ValueError):
                write_preset_config(target, "unsupported")


if __name__ == "__main__":
    unittest.main()
