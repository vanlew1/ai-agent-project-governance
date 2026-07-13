from pathlib import Path
STATE_DIR=Path('.agent_state')
PROJECT=STATE_DIR/'project_state.yaml'; ACTIVE=STATE_DIR/'active_task.yaml'; APPROVALS=STATE_DIR/'approvals.yaml'; EVENTS=STATE_DIR/'events.jsonl'; LAST_GUARD=STATE_DIR/'last_guard_result.yaml'

TEST_PLAN=STATE_DIR/"test_plan.yaml"
TEST_RESULTS=STATE_DIR/"test_results.yaml"
VERIFICATION=STATE_DIR/"verification_result.yaml"
CLOSURE=STATE_DIR/"closure_result.yaml"

ORCHESTRATION=STATE_DIR/"orchestration"
