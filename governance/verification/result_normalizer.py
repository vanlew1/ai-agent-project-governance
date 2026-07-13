def status(exit_code=None, timeout=False, error=False, blocked=False, skipped=False):
    if blocked:return "BLOCKED"
    if skipped:return "SKIPPED"
    if timeout:return "TIMEOUT"
    if error:return "ERROR"
    return "PASS" if exit_code==0 else "FAIL"
