# Reproducible Test Evidence

Record one evidence block per test run. Keep environment variable names only; never record values, credentials, or private paths.

| Field | Value |
| --- | --- |
| Command | |
| Working directory | |
| Test nodes / directory | |
| Marker / include / exclude | |
| Environment variable names | |
| Project dependency versions | |
| Basetemp / temporary directory | |
| Collected / passed / failed / skipped / warning | |
| Failed nodes | |
| JUnit or machine-readable summary path | |
| Baseline HEAD | |

If a historical numeric summary lacks its command and scope, label it `not fully reproducible`; do not infer or invent a command.
