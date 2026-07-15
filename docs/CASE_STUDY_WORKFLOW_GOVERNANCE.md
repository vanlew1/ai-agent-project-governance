# Reproducible case: a plan is not a closure

This synthetic case uses the repository's [local visual proof](DEMO.md), not a third-party customer project.

An upper workflow produces a narrow plan: change one allowed source file and run one focused test. The corresponding [TaskContract](../examples/superpowers_compat/task-contract.yaml) denies `restricted-change.txt`.

| Event | Runtime outcome | Why it matters |
| --- | --- | --- |
| An agent changes the denied file | `BLOCKED` (exit 3) | A written plan is checked against the actual diff. |
| The focused test passes, then the workspace changes | `BLOCKED` (exit 3) | Old verification cannot justify current work. |
| The allowed change and focused test remain fresh | `CLOSED` (exit 0) | Closure is backed by scope and evidence. |

Reproduce it with `python3 examples/demo/run_visual_proof.py`. This is not evidence of customer deployment, production use, or third-party workflow certification.
