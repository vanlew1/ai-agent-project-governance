from datetime import datetime, timezone
def close(verification, stale=False):
    status={"VERIFIED":"CLOSED","PARTIAL":"PARTIAL","BLOCKED":"BLOCKED","FAILED":"FAILED"}[verification["completion_status"]]
    reasons=["verification_stale_after_workspace_change"] if stale else []
    if stale: status="BLOCKED"
    return {"schema_version":"1.0","task_id":verification["task_id"],"status":status,"guard_status":verification["guard_status"],"verification_status":verification["completion_status"],"report_path":"","reasons":reasons,"remaining_risks":verification["remaining_risks"],"closed_at":datetime.now(timezone.utc).isoformat()}
