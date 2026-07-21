<!-- encoding: UTF-8 -->
# CASE-001 Windows Line-Ending Compatibility Audit

## Result

The activation helper changes are locally sound for LF output, fsync, exclusive create, and atomic replace, but the end-to-end Windows Preview is not LF-stable and WSL compatibility regressed. The compatibility acceptance criterion is not met.

## Source review

### Activation helpers

- `_exclusive_json`: adds `O_BINARY`, `newline="\n"`, flush, and fsync; retains `O_EXCL`.
- `_finalize_json`: adds `O_BINARY`, `newline="\n"`, flush, and fsync; retains `O_NOFOLLOW` where available.
- `_replace_mapping`: adds `O_BINARY` and `newline="\n"`; writes/fsyncs a new temp file and uses `os.replace`; cleanup remains on exception.

With a binary descriptor plus `TextIOWrapper(newline="\n")`, Windows CRT and text-layer newline translation are both disabled. The branch also works when `O_BINARY` is absent on POSIX.

### Remaining non-LF writers

- `scripts/agent_adopt.py` uses `os.open` + `os.fdopen(..., newline=None)` and no `O_BINARY` for dry-run output.
- `generate_preview.py` uses `Path.write_text(..., newline=None)` for plan and confirmation.
- `runtime_artifact_compiler.py` uses `write_text(..., newline=None)` for `RUNTIME_ARTIFACT_MANIFEST.json`.
- Installer receipts and sidecars use text mode without explicit LF; sidecars also use truncating writes rather than exclusive create.

Actual Windows-generated Preview evidence confirms CRLF in plan, confirmation, and runtime manifest while draft/runtime YAML files use LF.

## Tests

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 /tmp/case001_independent_checks.py
```

Relevant results:

```text
PASS lf_roundtrip_chinese_path_o_binary_branch
PASS existing_file_fail_closed
PASS preview_internal_digest_chain
```

The independent test exercised `_exclusive_json`, `_finalize_json`, and `_replace_mapping` under a Chinese/space path, forced the `O_BINARY` branch with value zero on POSIX, verified no CRLF, verified no leaked temp file, and verified exclusive-create refusal.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q \
  tests.unit.test_agent_adopt.AgentAdoptTest.test_manifest_reports_create_same_and_different_without_copying
```

Result: 1 failure. Reading a CRLF source as text and writing it on Linux creates LF bytes; planner compares raw hashes and reports `EXISTS_DIFFERENT` instead of `EXISTS_SAME`.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_governance_ci.py
```

Result: 6/8 gates; tests and schema compatibility failed.

Windows-native execution was attempted through PowerShell but no `python`, `python3`, or `py` launcher is installed. Therefore the required native Windows unit test is unverified. The already-generated Windows Preview supplies direct file-byte evidence that stable LF currently fails.

## Digest portability

- Canonical JSON digests are stable because they hash parsed mappings with sorted compact JSON.
- Draft hashes and runtime artifact hashes are stable where code writes explicit LF or bytes.
- Raw file hashes for plan/confirmation/manifests differ by checkout/writer platform when newline policy is unspecified.
- Asset equality uses raw bytes; semantically identical LF/CRLF files can be classified as conflicts.

## Required remediation

1. centralize UTF-8 LF atomic/exclusive writers and use them for every formal JSON/YAML/Markdown artifact;
2. decide whether asset equality is byte identity or normalized text identity and test both explicitly;
3. add a Windows CI job that runs the CASE-001 line-ending, Chinese-path, digest, and existing-file tests, not only syntax/template smoke checks;
4. add a Linux/WSL job against a CRLF checkout fixture;
5. bind and validate all sidecar artifacts before target writes.
