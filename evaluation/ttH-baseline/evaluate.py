#!/usr/bin/env python3
"""Write the inclusive hadronic baseline result for an evaluator event table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from baseline import evaluate


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError("input must be a .csv or .parquet table")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Trusted evaluator-side event table")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--selected-output", type=Path)
    parser.add_argument(
        "--input-role",
        choices=("trusted-evaluator", "development-proxy"),
        default="trusted-evaluator",
        help="Whether the input is the canonical evaluator sample or a non-authoritative development proxy",
    )
    args = parser.parse_args()
    selected, report = evaluate(read_table(args.input))
    report["input_provenance"] = {"path": str(args.input), "role": args.input_role}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.selected_output:
        args.selected_output.parent.mkdir(parents=True, exist_ok=True)
        selected.to_parquet(args.selected_output, index=False)


if __name__ == "__main__":
    main()
