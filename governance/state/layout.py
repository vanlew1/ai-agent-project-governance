from pathlib import Path
STATE_DIR=Path('.agent_state')
PROJECT=STATE_DIR/'project_state.yaml'; ACTIVE=STATE_DIR/'active_task.yaml'; APPROVALS=STATE_DIR/'approvals.yaml'; EVENTS=STATE_DIR/'events.jsonl'; LAST_GUARD=STATE_DIR/'last_guard_result.yaml'
