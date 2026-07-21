from __future__ import annotations

import io
import json
import runpy
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


def load_module() -> dict:
    return runpy.run_path(str(ROOT / "scripts/run_governance_ci.py"))


class Completed:
    returncode = 0
    stdout = "OK\n"
    stderr = ""


class P5ReleaseGate(unittest.TestCase):
    def write_config(self, root: Path, value) -> Path:
        path = root / "release_gate.yaml"
        path.write_text(
            yaml.safe_dump(
                {"schema_version": "1.0", "release_gate": {"test_timeout_seconds": value}},
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def test_gate_has_fixed_read_only_steps(self) -> None:
        module = load_module()
        names = [name for name, _ in module["GATES"]]
        self.assertEqual(
            ["governance", "schema-compatibility", "runtime-dependencies", "bootstrap", "ci-security", "tests", "quality", "syntax"],
            names,
        )

    def test_missing_config_uses_600_second_framework_default(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            policy = module["load_test_timeout_policy"](Path(temp) / "missing.yaml")
        self.assertEqual(600, policy.seconds)
        self.assertEqual("framework_default", policy.source)

    def test_legal_config_override_and_boundaries_are_accepted(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for value in (60, 900, 3600):
                with self.subTest(value=value):
                    policy = module["load_test_timeout_policy"](self.write_config(root, value))
                    self.assertEqual(value, policy.seconds)
                    self.assertEqual("framework_config", policy.source)

    def test_invalid_config_values_fail_closed(self) -> None:
        module = load_module()
        invalid_values = (59, 3601, 0, -1, 1.5, "600", "", None, True)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for value in invalid_values:
                with self.subTest(value=value):
                    with self.assertRaisesRegex(ValueError, "test_timeout_seconds"):
                        module["load_test_timeout_policy"](self.write_config(root, value))

    def test_invalid_config_shape_and_unparseable_yaml_fail_closed(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "release_gate.yaml"
            for text in (
                "",
                "release_gate: {}\n",
                "schema_version: '1.0'\nrelease_gate:\n  test_timeout_seconds: 600\n  unexpected: true\n",
                "release_gate: [\n",
            ):
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        module["load_test_timeout_policy"](path)

    def test_tests_gate_passes_effective_timeout_to_subprocess_and_audits_result(self) -> None:
        module = load_module()
        output = io.StringIO()
        with mock.patch.object(module["subprocess"], "run", return_value=Completed()) as run_mock:
            with mock.patch.object(module["time"], "monotonic", side_effect=(10.0, 14.25)):
                with redirect_stdout(output):
                    result = module["run"](
                        "tests", ["python", "-m", "unittest"], timeout_seconds=600, timeout_source="framework_default"
                    )
        self.assertTrue(result)
        self.assertEqual(600, run_mock.call_args.kwargs["timeout"])
        text = output.getvalue()
        self.assertIn("effective_timeout_seconds=600", text)
        self.assertIn("timeout_source=framework_default", text)
        self.assertIn("elapsed_seconds=4.2", text)
        self.assertIn("timeout_result=COMPLETED", text)
        self.assertIn("command=python -m unittest", text)

    def test_timeout_is_classified_as_timeout_with_auditable_fields(self) -> None:
        module = load_module()
        output = io.StringIO()
        expired = subprocess.TimeoutExpired(["python", "-m", "unittest"], 600)
        with mock.patch.object(module["subprocess"], "run", side_effect=expired):
            with mock.patch.object(module["time"], "monotonic", side_effect=(20.0, 620.5)):
                with redirect_stdout(output):
                    result = module["run"](
                        "tests", ["python", "-m", "unittest"], timeout_seconds=600, timeout_source="framework_config"
                    )
        self.assertFalse(result)
        text = output.getvalue()
        self.assertIn("tests: TIMEOUT", text)
        self.assertIn("exit_classification=TIMEOUT", text)
        self.assertIn("timeout_result=TIMEOUT", text)
        self.assertIn("effective_timeout_seconds=600", text)
        self.assertIn("timeout_source=framework_config", text)
        self.assertIn("elapsed_seconds=600.5", text)
        self.assertIn("command=python -m unittest", text)

    def test_only_tests_gate_uses_configured_test_timeout(self) -> None:
        module = load_module()
        calls = []
        globals_ = module["main"].__globals__

        def record(name, argv, *, timeout_seconds, timeout_source):
            calls.append((name, timeout_seconds, timeout_source))
            return True

        with mock.patch.dict(globals_, {"run": record}):
            self.assertEqual(0, module["main"]())
        self.assertEqual(8, len(calls))
        tests_call = next(call for call in calls if call[0] == "tests")
        self.assertEqual(("tests", 600, "framework_config"), tests_call)
        self.assertTrue(
            all(
                seconds == module["GATE_TIMEOUT_SECONDS"] and source == "gate_default"
                for name, seconds, source in calls
                if name != "tests"
            )
        )
        self.assertTrue(all(isinstance(seconds, int) and seconds > 0 for _, seconds, _ in calls))

    def test_schema_and_runtime_timeout_contract_are_consistent(self) -> None:
        module = load_module()
        schema = json.loads((ROOT / "schemas/release_gate_config.schema.json").read_text(encoding="utf-8"))
        timeout_schema = schema["properties"]["release_gate"]["properties"]["test_timeout_seconds"]
        self.assertEqual(module["MIN_TEST_TIMEOUT_SECONDS"], timeout_schema["minimum"])
        self.assertEqual(module["MAX_TEST_TIMEOUT_SECONDS"], timeout_schema["maximum"])
        self.assertEqual(module["DEFAULT_TEST_TIMEOUT_SECONDS"], timeout_schema["default"])
        config = yaml.safe_load((ROOT / "config/release_gate.yaml").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(config)

    def test_default_policy_is_platform_independent(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.yaml"
            with mock.patch.object(module["sys"], "platform", "win32"):
                windows = module["load_test_timeout_policy"](missing)
            with mock.patch.object(module["sys"], "platform", "linux"):
                wsl = module["load_test_timeout_policy"](missing)
        self.assertEqual(windows, wsl)
        self.assertEqual(600, windows.seconds)


if __name__ == "__main__":
    unittest.main()
