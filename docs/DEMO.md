# Demo

Three isolated temporary-directory scenarios demonstrate deterministic blocks:

1. Contract allows `src/` only; `secrets/token.txt` makes Guard `BLOCKED`.
2. A workspace change after `VERIFIED` makes Closure `BLOCKED` with `verification_stale_after_workspace_change`.
3. Two parallel subtasks claiming `src/shared.py` make OrchestrationPlan `BLOCKED`.

See [assets/demo-terminal.txt](assets/demo-terminal.txt).

## Record a 30–60 second GIF

1. Open an empty temporary directory and enlarge terminal text.
2. Run the three scenarios from `assets/demo-terminal.txt`, pausing after each `BLOCKED`.
3. Record only fictional paths; never show credentials or unrelated output.
4. Trim to 30–60 seconds and export an optimized GIF.
5. Check for local paths and sensitive material before saving under `docs/assets/`.
