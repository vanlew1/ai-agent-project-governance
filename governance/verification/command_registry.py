"""Closed registry of local, non-network governance validation commands."""

COMMANDS = {
    "unit_tests": {"argv": ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], "level": 3, "timeout": 120, "cwd": "."},
    "governance_validate": {"argv": ["python", "scripts/validate_governance.py"], "level": 2, "timeout": 60, "cwd": "."},
    "quality_gate": {"argv": ["python", "scripts/check_code_quality.py"], "level": 2, "timeout": 60, "cwd": "."},
    "python-unittest-discover": {"argv": ["python", "-m", "unittest", "discover"], "level": 1, "timeout": 120, "cwd": "."},
    "python-pytest": {"argv": ["python", "-m", "pytest"], "level": 1, "timeout": 120, "cwd": "."},
    "python-py-compile": {"argv": ["python", "-m", "py_compile"], "level": 1, "timeout": 60, "cwd": "."},
    "node-npm-test": {"argv": ["npm", "run", "test"], "level": 1, "timeout": 120, "cwd": "."},
    "node-npm-lint": {"argv": ["npm", "run", "lint"], "level": 2, "timeout": 120, "cwd": "."},
    "node-npm-typecheck": {"argv": ["npm", "run", "typecheck"], "level": 2, "timeout": 120, "cwd": "."},
}

def get(command_id): return COMMANDS.get(command_id)