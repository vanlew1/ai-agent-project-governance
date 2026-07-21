"""Scan text files for illegal C0 control characters."""
from __future__ import annotations

from pathlib import Path


# C0 control characters: ASCII 0-31, but TAB(9), LF(10), CR(13) are allowed.
ILLEGAL_C0 = set(range(32)) - {9, 10, 13}


def scan_file_for_c0(path: Path) -> list[str]:
    """Scan a file for illegal C0 characters. Returns a list of error messages."""
    errors = []
    try:
        content_bytes = path.read_bytes()
    except OSError as error:
        return [f"Could not read {path}: {error}"]

    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        return [f"File {path} is not valid UTF-8: {error}"]

    for i, char in enumerate(content):
        code = ord(char)
        if code in ILLEGAL_C0:
            line_num = content[:i].count("\n") + 1
            errors.append(f"Illegal C0 control character '\\x{code:02x}' found in {path} at line {line_num}")

    return errors


def scan_directory_for_c0(directory: Path, extensions: set[str] | None = None) -> list[str]:
    """Scan all matching files in a directory for C0 characters."""
    if extensions is None:
        extensions = {".md", ".json", ".yaml", ".yml", ".txt"}
        
    all_errors: list[str] = []
    if not directory.exists() or not directory.is_dir():
        return all_errors

    for p in directory.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            all_errors.extend(scan_file_for_c0(p))
            
    return all_errors
