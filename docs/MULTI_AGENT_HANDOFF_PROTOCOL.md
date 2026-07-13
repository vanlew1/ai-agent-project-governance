# Multi-Agent Handoff Protocol

A handoff binds task, orchestration, contract digest, HEAD, branch, workspace fingerprint and changed files. Any mismatch is stale and blocks dependent work.


V1 status: isolated CLI acceptance verified a fresh structured handoff through `VERIFIED` to `CLOSED`; stale identity/fingerprint evidence remains a blocking condition.
