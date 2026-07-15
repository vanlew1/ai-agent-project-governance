from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from governance.adoption.lifecycle import run_adoption_test_plan, transition_project_state
from governance.security.output_sanitizer import sanitize_output


class AdoptionRemediationSecurityTest(unittest.TestCase):
    def state_path(self, root: Path) -> Path:
        value = {"schema_version":"1.0","project_mode":"EXECUTION","architecture_status":"confirmed","implementation_plan_status":"confirmed","repository_root":".","adapter":"generic","high_risk_paths":[],"default_forbidden_operations":[],"status":"ACTIVATED_NOT_PREFLIGHTED","activated":True,"activation_status":"ACTIVATED_NOT_PREFLIGHTED","activation_approval_digest":"a" * 64,"activation_receipt_digest":"b" * 64,"lifecycle_stage":"ACTIVATED_NOT_PREFLIGHTED","lifecycle_evidence":[]}
        path = root / "project_state.yaml"; path.write_text(yaml.safe_dump(value), encoding="utf-8"); return path

    def evidence(self, root: Path, state: Path, evidence_type: str = "PreflightEvidence", status: str = "PASS") -> Path:
        path = root / "evidence.json"
        path.write_text(json.dumps({"schema_version":"1.0","evidence_type":evidence_type,"status":status,"target_identity_digest":"a" * 64,"previous_state_digest":hashlib.sha256(state.read_bytes()).hexdigest(),"upstream_evidence_digests":[],"payload":{}}), encoding="utf-8")
        return path

    def test_sensitive_output_is_redacted_and_raw_digest_is_preserved(self) -> None:
        raw = b"TOKEN=AGC_SYNTHETIC_CANARY_SECRET\nAuthorization: Bearer abc.def\n"
        output = sanitize_output(raw)
        self.assertNotIn("AGC_SYNTHETIC_CANARY_SECRET", output.text)
        self.assertNotIn("abc.def", output.text)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), output.raw_digest)
        self.assertGreaterEqual(output.redaction_count, 2)

    def test_runner_output_contract_drops_unsafe_mocked_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plan = {"status":"READY","context_digest":"a" * 64,"guard_evidence_digest":"b" * 64,"selected":[{"candidate_id":"x","command_digest":"c" * 64,"argv":["python","-c","pass"],"cwd":".","timeout_seconds":1,"required":True}]}
            from governance.adoption.installer import digest
            plan["test_plan_digest"] = digest(plan)
            with patch("governance.adoption.lifecycle.run_command", return_value={"status":"FAIL","stdout_summary":"TOKEN=AGC_SYNTHETIC_CANARY_SECRET"}):
                record = run_adoption_test_plan(root, plan)
            self.assertEqual("FAIL", record["overall_status"])
            self.assertNotIn("AGC_SYNTHETIC_CANARY_SECRET", json.dumps(record))

    def test_state_transition_rejects_wrong_evidence_and_modified_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); state = self.state_path(root); evidence = self.evidence(root, state, "GuardEvidence")
            current = hashlib.sha256(state.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                transition_project_state(state, expected_current_stage="ACTIVATED_NOT_PREFLIGHTED", expected_current_state_digest=current, evidence_path=evidence, requested_next_stage="PREFLIGHT_PASSED", target_identity_digest="a" * 64)
            evidence = self.evidence(root, state)
            transition_project_state(state, expected_current_stage="ACTIVATED_NOT_PREFLIGHTED", expected_current_state_digest=current, evidence_path=evidence, requested_next_stage="PREFLIGHT_PASSED", target_identity_digest="a" * 64)
            evidence.write_text(evidence.read_text(encoding="utf-8") + " ", encoding="utf-8")
            guard = self.evidence(root, state, "GuardEvidence", "PASS")
            with self.assertRaises(ValueError):
                transition_project_state(state, expected_current_stage="PREFLIGHT_PASSED", expected_current_state_digest=hashlib.sha256(state.read_bytes()).hexdigest(), evidence_path=guard, requested_next_stage="GUARDED", target_identity_digest="a" * 64)


if __name__ == "__main__":
    unittest.main()
