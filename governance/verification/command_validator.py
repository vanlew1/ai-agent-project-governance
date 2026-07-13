"""Reject anything outside the closed argv registry."""

from .command_registry import get

FORBIDDEN = (";", "&&", "||", "|", "$", "`", "http://", "https://", "git", "curl", "wget", "pip", "npm", "rm", "del", "remove-item")

def validate(command):
    spec=get(command.get("command_id"))
    if not spec or command.get("argv") != spec["argv"]: return False, "command_not_registered"
    if command.get("working_directory", ".") != spec["cwd"] or ".." in command.get("working_directory", "."): return False, "invalid_working_directory"
    if command.get("timeout_seconds") != spec["timeout"]: return False, "invalid_timeout"
    joined=" ".join(command["argv"]).casefold()
    if any(marker in joined for marker in FORBIDDEN): return False, "forbidden_argv"
    return True, "valid"
