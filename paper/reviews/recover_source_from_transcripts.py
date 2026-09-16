#!/usr/bin/env python3
"""Materialize source files safely recoverable from retained agent transcripts.

The evaluator owns these derived artifacts.  They are exact, unexecuted payloads
from shell heredocs which wrote a source file during a preserved run.  They are
kept separately from copied workspace files and each payload has a provenance
manifest.  This accepts arbitrary solver layouts; it never requires a solver
submission schema.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "results" / "paper"
SOURCE_SUFFIXES = {".py", ".sh", ".ipynb", ".r", ".jl", ".c", ".cc", ".cpp", ".h", ".hpp"}

# Both common spellings are accepted:
#   cat > path.py <<'PY'     and     cat <<'PY' > path.py
HEREDOC_BEFORE = re.compile(
    r"(?:cat|tee)\s+<<-?\s*['\"]?(?P<marker>[A-Za-z_][A-Za-z0-9_]*)['\"]?\s*"
    r">\s*(?P<path>[^\s;&|]+)",
    re.MULTILINE,
)
HEREDOC_AFTER = re.compile(
    r"(?:cat|tee)\s+>?\s*(?P<path>[^\s;&|]+)\s+<<-?\s*['\"]?(?P<marker>[A-Za-z_][A-Za-z0-9_]*)['\"]?",
    re.MULTILINE,
)


def text_values(value: Any) -> Iterator[str]:
    """Yield string leaves from JSON telemetry without depending on its schema."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from text_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from text_values(child)


def transcript_strings(path: Path) -> Iterator[str]:
    """Read text directly and additionally decode JSON/JSONL payload strings."""
    try:
        raw = path.read_text(errors="ignore")
    except OSError:
        return
    yield raw
    if path.suffix not in {".json", ".jsonl"}:
        return
    entries: list[Any] = []
    if path.suffix == ".json":
        try:
            entries.append(json.loads(raw))
        except json.JSONDecodeError:
            return
    else:
        for line in raw.splitlines():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    for entry in entries:
        yield from text_values(entry)


def safe_destination(original: str) -> Path | None:
    """Map a runtime source path to a relative, non-traversing evidence path."""
    candidate = Path(original.strip("'\""))
    if candidate.suffix.lower() not in SOURCE_SUFFIXES:
        return None
    pieces = [part for part in candidate.parts if part not in {"/", ".", ".."}]
    if not pieces:
        return None
    return Path(*pieces)


def extract_heredocs(text: str) -> list[tuple[str, str]]:
    """Return (runtime path, exact body) for completed source-writing heredocs."""
    found: list[tuple[str, str]] = []
    for match in (*HEREDOC_BEFORE.finditer(text), *HEREDOC_AFTER.finditer(text)):
        destination = safe_destination(match.group("path"))
        if destination is None:
            continue
        body_start = text.find("\n", match.end())
        if body_start < 0:
            continue
        marker = match.group("marker")
        end = re.search(rf"(?m)^[ \t]*{re.escape(marker)}[ \t]*$", text[body_start + 1 :])
        if end is None:
            continue
        body = text[body_start + 1 : body_start + 1 + end.start()]
        if body.strip():
            found.append((match.group("path").strip("'\""), body))
    return found


def evidence_transcripts(run: Path) -> Iterator[Path]:
    for path in run.rglob("*"):
        if not path.is_file() or path.suffix not in {".txt", ".json", ".jsonl", ".log", ".cast", ".pane"}:
            continue
        rel = path.relative_to(run).as_posix().lower()
        if rel.startswith("agent/") or path.name in {"trial.log", "job.log"}:
            yield path


def recover_run(run: Path) -> list[dict[str, str | int]]:
    recovered: dict[Path, tuple[str, Path, str]] = {}
    for transcript in evidence_transcripts(run):
        for text in transcript_strings(transcript):
            for original, body in extract_heredocs(text):
                destination = safe_destination(original)
                if destination is not None:
                    # Preserve one deterministic representative when telemetry
                    # repeats a write.  The manifest deliberately does not
                    # call it a final workspace snapshot.
                    recovered[destination] = (original, transcript, body)
    output = run / "recovered-source"
    if not recovered:
        return []
    records: list[dict[str, str | int]] = []
    for destination, (original, transcript, body) in sorted(recovered.items()):
        target = output / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)
        records.append({
            "recovered_path": target.relative_to(run).as_posix(),
            "runtime_path": original,
            "source_transcript": transcript.relative_to(run).as_posix(),
            "extraction": "shell-heredoc",
            "sha256": hashlib.sha256(body.encode()).hexdigest(),
            "bytes": len(body.encode()),
            "executed": False,
        })
    (output / "manifest.json").write_text(json.dumps({
        "schema_version": 1,
        "description": "Evaluator-generated, unexecuted source recovered exactly from retained shell-heredoc payloads; not a copied workspace snapshot or an assertion of final runtime state.",
        "files": records,
    }, indent=2, sort_keys=True) + "\n")
    return records


def main() -> None:
    runs = sorted({path.parent for path in PAPER.rglob("result.json") if "__" in path.parent.name})
    written = 0
    recovered_runs = 0
    for run in runs:
        records = recover_run(run)
        if records:
            recovered_runs += 1
            written += len(records)
    print(f"recovered {written} source files across {recovered_runs} of {len(runs)} retained runs")


if __name__ == "__main__":
    main()
