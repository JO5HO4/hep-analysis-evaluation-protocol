#!/usr/bin/env python3
"""Schema, link, and ledger validation for the traceability pilot."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def main() -> None:
    failures: list[str] = []
    records = sorted((OUT / "runs").glob("*.json"))
    if len(records) != 15:
        failures.append(f"expected 15 records, found {len(records)}")
    for path in records:
        item = json.loads(path.read_text())
        if item.get("schema_version") != "top-reconstruction-traceability-review/v1" or not item.get("source_inventory", {}).get("complete"):
            failures.append(f"invalid schema/inventory: {path.name}")
        ids = {entry["id"] for entry in item.get("evidence_ledger", [])}
        for claim in item.get("claims", []):
            if not claim.get("evidence_ids") or not set(claim["evidence_ids"]) <= ids:
                failures.append(f"unresolved claim ledger reference: {path.name}:{claim.get('id')}")
        answers = item.get("rubric_answers", [])
        review_reward = item.get("review_reward", {})
        if len(answers) != 31 or [answer.get("id") for answer in answers] != [f"Q{i}" for i in range(1, 32)]:
            failures.append(f"incomplete 31-question protocol: {path.name}")
        elif any(answer.get("reward") != (1 if answer.get("status") == "pass" else 0) for answer in answers):
            failures.append(f"invalid question reward: {path.name}")
        elif review_reward.get("earned") != sum(answer["reward"] for answer in answers) or review_reward.get("possible") != 31:
            failures.append(f"invalid review-reward aggregate: {path.name}")
        for answer in answers:
            if not set(answer.get("evidence_ids", [])) <= ids:
                failures.append(f"unresolved rubric ledger reference: {path.name}:{answer.get('id')}")
        for entry in item.get("evidence_ledger", []):
            source = entry.get("source")
            if source and not (ROOT / source).is_file():
                failures.append(f"unresolved ledger source: {path.name}:{source}")
        if not (path.with_suffix(".md")).is_file():
            failures.append(f"missing technical note: {path.name}")
    index = (OUT / "index.md").read_text()
    for link in re.findall(r"\]\(([^)]+)\)", index):
        if not (OUT / link).is_file():
            failures.append(f"broken portfolio link: {link}")
    if failures:
        print("traceability pilot validation failed:\n" + "\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(f"traceability pilot validation: OK ({len(records)} records, resolved claims and links)")


if __name__ == "__main__":
    main()
