# AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A Audit Report

## Scope and attribution

- Independent read-only audit of 04E. No 04E implementation, Schema, test, document, target project, network, or Git state was changed.
- Existing changes were attributable to 04C, 04D, 04D-A, 04D-B, 04D-A-R1, and 04E; this audit adds only this report.

## P0 findings

### P0-01 — Installation receipt can be written inside the target project

`install_approved()` rejects a receipt only when `receipt_destination.parent.resolve(...) == target`. A receipt at `<target>/reports/receipt.json` has a different parent and is accepted. The implementation then creates that directory and exclusive-creates the receipt there. This violates the new-files-only approved target-file set and the explicit requirement that receipts be outside the target project.

### P0-02 — Rollback has a check/delete TOCTOU window

`rollback_install()` first verifies every installed path and its hash, then starts a separate deletion loop. A file can be modified or replaced after the verification loop but before its `unlink()`. The code does not re-open or re-verify atomically immediately before each delete, nor use a directory descriptor based operation. It can therefore delete a user-modified file in the documented race scenario.

## Additional audit observations

- Final approval does not carry a direct Plan identity object. The installation flow validates target identity against final approval, but only compares Plan and confirmation digest strings from the export manifest; it cannot independently recompute the original Plan-target binding from the bundle. This is a P1 digest-chain gap.
- The implementation uses exclusive creation and `O_NOFOLLOW` where available, and directed tests for normal install/conflict/rollback pass. Those positive checks do not close the P0 paths above.
- Existing 04E directed suite reports 13 tests and the preceding full suite reports 103 passing tests; they do not cover the discovered receipt-inside-target or rollback race cases.

## Not executed

No real project, network, credentials, production data, candidate tests, build, package manager, Git operation, or 04F action was executed. The planned broader synthetic matrix was not expanded after the P0 findings because repair is outside this audit's authority.

## Conclusion

```text
AGC-UX-EXISTING-PROJECT-ADOPTION-04E-A
REQUIRES_REVISION
CLOSEOUT_BLOCKED
NOT_READY_FOR_04F
```

Required remediation: reject every receipt path contained by the target realpath; make rollback delete fail-closed against check/delete races; and bind/revalidate Plan target identity through the install digest chain. Re-run the complete 04E-A audit after repair.
