# Offline upper-workflow mapping example

This folder is a documentation fixture, not a Superpowers installation or integration test. It shows how any upper workflow can hand a bounded task to the local governance runtime.

```text
upper-plan.md → task-contract.yaml → Guard → focused test → Verification → Closure
```

Run the reusable offline proof from the repository root:

```bash
python3 examples/demo/run_visual_proof.py
```

Expected outcomes are in `expected-output.json`. The runner creates disposable synthetic repositories and does not modify this example or contact a network service.
