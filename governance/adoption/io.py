"""Cross-platform byte-stable writers for formal adoption artifacts."""
from __future__ import annotations

import hashlib
import json
import os
import secrets
from pathlib import Path
from typing import Any

import yaml


def lf_text(value: str) -> str:
    """Normalize text to LF without changing any other Unicode content."""
    return value.replace("\r\n", "\n").replace("\r", "\n")


def text_bytes(value: str) -> bytes:
    normalized = lf_text(value)
    illegal = sorted({ord(character) for character in normalized if ord(character) < 32 and character not in "\t\n"})
    if illegal:
        rendered = ", ".join(f"0x{code:02x}" for code in illegal)
        raise ValueError(f"formal artifact contains illegal C0 control characters: {rendered}")
    return normalized.encode("utf-8")


def raw_and_normalized_digests(value: bytes) -> dict[str, str]:
    """Return byte identity and an explicitly labelled normalized-text identity."""
    text = value.decode("utf-8")
    return {
        "raw_sha256": hashlib.sha256(value).hexdigest(),
        "normalized_text_sha256": hashlib.sha256(text_bytes(text)).hexdigest(),
    }


def _open_flags(*, exclusive: bool) -> int:
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    return flags


def _write_descriptor(path: Path, value: bytes, *, exclusive: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, _open_flags(exclusive=exclusive), 0o600)
    try:
        view = memoryview(value)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("formal artifact write made no progress")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_bytes_exclusive(path: Path, value: bytes) -> None:
    _write_descriptor(path, value, exclusive=True)


def write_text_exclusive(path: Path, value: str) -> None:
    write_bytes_exclusive(path, text_bytes(value))


def write_json_exclusive(path: Path, value: Any) -> None:
    write_text_exclusive(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_yaml_exclusive(path: Path, value: Any) -> None:
    write_text_exclusive(path, yaml.safe_dump(value, allow_unicode=True, sort_keys=False))


def write_bytes_atomic(path: Path, value: bytes) -> None:
    """Replace one formal artifact atomically after a durable temporary write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.adoption.{os.getpid()}.{secrets.token_hex(8)}.tmp")
    write_bytes_exclusive(temporary, value)
    try:
        os.replace(temporary, path)
        if os.name != "nt":
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def write_text_atomic(path: Path, value: str) -> None:
    write_bytes_atomic(path, text_bytes(value))
