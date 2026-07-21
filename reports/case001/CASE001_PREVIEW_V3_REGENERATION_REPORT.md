<!-- encoding: UTF-8 -->

# CASE-001 Preview v3 Regeneration Report

## Result

The final `adoption-preview-v3` is generated only after implementation commits and Windows/WSL gates pass. It uses `scripts/agent_adopt.py`, the public CLI, and `case001_replay_phase1_scope.yaml`; Preview v2 is not reused or overwritten.

## Expected and verified contents

- copied formal scope input
- `adoption-plan.json`
- standalone `ADOPTION_PROVENANCE_RECEIPT.json`
- pending `adoption-confirmations.yaml`
- `drafts/`
- `runtime/` with task/state artifacts and `RUNTIME_ARTIFACT_MANIFEST.json`
- `runtime/INSTALL_WRITESET.json`
- `runtime/PRE_INSTALL_HASHES.json`
- `runtime/ROLLBACK_MANIFEST.json`
- unapproved `adoption-approval-candidate.yaml`

## Safety assertions

- `confirmed_by_user=false`
- `install_approved=false`
- `activate_approved=false`
- `Replay target writes=0`
- `task.yaml` absent in Replay
- `project_state.yaml` absent in Replay
- formal output is UTF-8/LF and contains no illegal C0 characters
- provenance target branch/HEAD and framework commit match generation-time Git state

No install or activation command is part of regeneration.
