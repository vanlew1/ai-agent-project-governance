# Share kit

## Message spine

Upper workflows help an AI coding agent plan and build. Agent Governance independently checks whether the work stayed in scope, whether its evidence is still fresh, and whether it can close.

## Proof points

- Scope Guard checks actual changes against an explicit TaskContract.
- Verification records task-relevant evidence.
- Closure blocks stale validation after a workspace change.
- Handoff and single-writer checks make multi-agent ownership explicit.
- The [Demo](DEMO.md) is offline, reproducible, and synthetic.

## Use only with these qualifiers

- “documented offline mapping” for Superpowers or other upper workflows;
- “local evidence” for adapter and demo claims;
- “synthetic” for the case study and visual proof.

## Do not claim

- official integration, endorsement, plugin, or Marketplace availability;
- end-to-end third-party compatibility;
- customer adoption, production proof, user count, or performance metrics;
- that Closure means production readiness or deployment.

## 30-second demo script

1. Show the README's one-line positioning and run `python3 examples/demo/run_visual_proof.py`.
2. Show the `BLOCKED` out-of-scope result and the named denied path.
3. Show the focused test passing, then the stale-closure `BLOCKED` result.
4. Show the fresh `CLOSED` result and point to the machine-readable JSON.
5. Close with: “Use any planning workflow above it; this layer proves the bounded task below it.”

## Screenshot/GIF checklist

- README first screen and Demo command;
- all three terminal statuses with exit codes;
- `visual-proof-summary.json` with local paths removed;
- the workflow-to-TaskContract diagram in [Workflow integration](WORKFLOW_INTEGRATION.md).

Do not record usernames, local paths, tokens, private repositories, or third-party account screens.

## Pre-publication fact check

- [ ] The linked commit has passed the local release gate.
- [ ] The Demo command and three stated outcomes were rerun locally.
- [ ] “Documented offline mapping only” appears with every Superpowers reference.
- [ ] No text implies official integration, production proof, users, stars, or performance metrics.
- [ ] Repository description, homepage, and topics match [GitHub metadata](GITHUB_TOPICS.md).
- [ ] Screenshots and posts contain no credentials, local paths, private data, or unreviewed third-party claims.
