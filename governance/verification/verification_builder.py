from datetime import datetime, timezone
def build(contract, guard, plan, results, orchestration=None):
    if guard["status"] in {"BLOCKED","ERROR"} or plan["status"]=="BLOCKED": outcome="BLOCKED"
    elif any(r["status"] in {"ERROR","TIMEOUT"} or (r.get("required") and r["status"]=="FAIL") for r in results): outcome="FAILED"
    elif guard["status"]=="WARN" or any(not r.get("required") and r["status"]!="PASS" for r in results): outcome="PARTIAL"
    else: outcome="VERIFIED"
    value={"schema_version":"1.0","task_id":contract["task_id"],"scope_check":"PASS" if guard["status"]=="PASS" else "FAIL", "forbidden_operation_check":"PASS", "guard_status":guard["status"],"test_plan_status":plan["status"],"tests":results,"required_tests_passed":outcome=="VERIFIED","optional_tests_passed":outcome=="VERIFIED","completion_status":outcome,"remaining_risks":[] if outcome=="VERIFIED" else [outcome.lower()],"verified_at":datetime.now(timezone.utc).isoformat()}
    if orchestration:
        value["orchestration_id"]=orchestration["orchestration_id"]
        if orchestration.get("status") != "READY_FOR_VERIFICATION": value["completion_status"]="BLOCKED"; value["remaining_risks"]=["orchestration_not_ready"]
    return value
