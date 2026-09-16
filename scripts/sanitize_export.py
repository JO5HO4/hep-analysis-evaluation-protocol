#!/usr/bin/env python3
"""Redact source-machine paths from text evidence in this standalone export."""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH_PATTERNS = (
    (re.compile(r"/global/(?:cfs|homes)/[^\s\"'`<>]+"), "<host-path>"),
    (re.compile(r"/pscratch/[^\s\"'`<>]+"), "<host-path>"),
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
)


def is_text(path: Path) -> bool:
    if path.is_symlink() or ".git" in path.parts:
        return False
    try:
        with path.open("rb") as handle:
            return b"\0" not in handle.read(8192)
    except OSError:
        return False


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if path == Path(__file__) or not path.is_file() or not is_text(path):
            continue
        raw = path.read_bytes()
        raw_redacted = raw
        for prefix in (b"/global/cfs", b"/global/homes", b"/pscratch"):
            raw_redacted = raw_redacted.replace(prefix, b"<host-path>")
            raw_redacted = raw_redacted.replace(b"\\" + prefix, b"\\<host-path>")
        if raw_redacted != raw:
            path.write_bytes(raw_redacted)
            changed += 1
        try:
            text = raw_redacted.decode()
        except UnicodeDecodeError:
            continue
        redacted = text
        for pattern, replacement in PATH_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        redacted = redacted.replace("\\/global/", "\\/<host-path>/")
        for pattern in SECRET_PATTERNS:
            redacted = pattern.sub("<redacted-secret>", redacted)
        if redacted != text:
            path.write_text(redacted)
            if raw_redacted == raw:
                changed += 1
    print(f"redacted host paths in {changed} text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
