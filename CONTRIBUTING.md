# Contributing

1. Describe the user-facing goal and the smallest change scope.
2. Do not add remote API calls, automatic agent startup, worktree creation, Git writes, secret handling, deployment, or publishing without explicit review.
3. Keep fixtures offline and free of credentials and production data.
4. Run focused checks, then the local release gate for runtime-facing changes:

```powershell
python scripts/run_governance_ci.py
```

5. Update docs and compatibility evidence when behavior changes.

Report failures with a minimal sanitized reproduction; never include secrets, complete environment variables, or private logs.
