# AGC-UX-EXISTING-PROJECT-ADOPTION-04D-B Remediation Report

## Scope

- Fixed only the two 04D-A P1 findings. No target project, network, credential, production, runtime-state, Git, or 04E operation was performed.
- Baseline HEAD remained `f0c4b75b40a09a9e8558d306b48834c7b8fbe6a1`; pre-existing 04C, 04D, and 04D-A reports were retained.

## P1-01: target identity binding

- Root cause: the Plan carried only the sanitized literal `<target-project>`, while export accepted an independent target-root argument.
- Fix: each Plan now contains `target_identity`: SHA-256 fingerprints of canonical real path and a controlled project-marker set, a Git-presence flag, and an aggregate identity digest. No literal target path, marker content, remote URL, or credential is emitted.
- Export recomputes this identity for `--target-project-root` before creating the output directory. Any mismatch fails with a non-sensitive error.
- Canonical symlink aliases to the same target are accepted; distinct, same-name, copied, and symlinked-different targets fail.

## P1-02: candidate-ID uniqueness

- Root cause: export converted IDs to a set for membership and then selected the first matching candidate.
- Fix: candidate IDs have Schema length/character constraints and are also normalized (NFC, trim, case-fold) before a mandatory uniqueness check. Plan build and export validation both perform this check.
- Exact duplicates and manually tampered case, whitespace, and Unicode variants fail before output. No first/last-match fallback remains.

## Atomic and safety behavior

- All Plan, confirmation, identity, and uniqueness checks finish before output-path creation or write.
- Failed different-target and duplicate-ID tests verify no output directory exists. The target remains read-only to the exporter.
- The export path has no subprocess, shell, package-manager, Git, HTTP, or socket invocation.

## Verification

- Directed export/adoption/public-assets suite: 23 tests passed.
- Full unit suite: 100 tests passed.
- Governance validation, code quality, Schema compatibility, and `git diff --check`: passed.
- Original P1 reproduction cases now pass as safety assertions: cross-target replay rejected; duplicate candidate IDs rejected.

## Remaining boundary

- This remains a draft exporter, not installation or activation. 04E was not entered; its decision depends on the accompanying R1 audit.
