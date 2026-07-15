# Synthetic examples

These are repeatable demonstration fixtures, not real adoption stories or user projects.

- [Python minimal](python-minimal/README.md) is exercised by the audit test suite. Its initial state has a Python test signal but no agent instructions, so the audit recommends `standard`.
- [Node minimal](node-minimal/README.md) is a static fixture showing the equivalent project markers and command shape.

The intended first-use path is: inspect the initial fixture with `agent_audit.py`, use the recommended preset when creating a new project, then add the minimal boundaries described by that preset.
