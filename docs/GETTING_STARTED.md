# Getting started in five minutes

This template is local-first. It does not upload project content, start agents, contact a network service, or change a Git remote.

1. Run a read-only assessment of an existing repository:

   ```bash
   python scripts/agent_audit.py --project-root .
   ```

2. Use the recommended preset when creating a new governed project:

   ```bash
   python scripts/init_new_project.py --preset lightweight
   ```

3. Fill in the first-focus items in `config/governance_preset.yaml`, then run the documented local test command.

On Windows, open PowerShell in the repository before running these commands. On macOS or Linux, use a terminal in the repository. If `python` refers to Python 2 on your system, use `python3` instead.

The initializer only creates a new folder. To undo it, delete that newly created folder with your normal file manager or shell command; it never changes the source template or an existing project.

See [the audit reference](ADOPTION_AUDIT.md), [preset guide](PRESETS.md), and [synthetic examples](examples/README.md).
