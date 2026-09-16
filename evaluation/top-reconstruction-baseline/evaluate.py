#!/usr/bin/env python3
"""Evaluate the mass-only baseline on a labeled or unlabeled candidate table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from baseline_selector import MAX_SELECTED_PER_EVENT, SELECTOR_VERSION, TOP_MASS_GEV, select_mass_greedy


def mass_summary(values: pd.Series) -> dict[str, float | int] | None:
    if values.empty:
        return None
    return {
        "count": int(values.size),
        "mean_GeV": float(values.mean()),
        "median_GeV": float(values.median()),
        "stddev_GeV": float(values.std(ddof=0)),
    }


def evaluate(candidates: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    selected = select_mass_greedy(candidates)
    report: dict[str, Any] = {
        "schema_version": "top-reconstruction-baseline-results/v1",
        "selector": {
            "name": SELECTOR_VERSION,
            "top_mass_reference_GeV": TOP_MASS_GEV,
            "ranking": "ascending abs(triplet_mass - 172.5 GeV)",
            "tie_break": "ascending canonical sorted jet-index triplet",
            "jet_disjoint": True,
            "maximum_selected_per_event": MAX_SELECTED_PER_EVENT,
            "uses_candidate_score": False,
            "uses_truth_labels": False,
        },
        "sample": {
            "candidate_count": int(len(candidates)),
            "event_count": int(candidates["event_id"].nunique()),
            "selected_candidate_count": int(len(selected)),
            "selected_event_count": int(selected["event_id"].nunique()),
        },
        "metrics": None,
        "limitations": [
            "Results are valid only for the input sample and are not a hidden-test score.",
            "The candidate table has no b-quark matching fields; b-jet inclusion is not evaluated.",
        ],
    }
    if "is_truth" not in candidates.columns:
        return selected, report

    # Task exports may encode this label as Boolean or numeric 0/1.
    truth_mask = candidates["is_truth"].fillna(False).astype(bool)
    selected_truth_mask = selected["is_truth"].fillna(False).astype(bool)
    truth_total = int(truth_mask.sum())
    true_selected = selected[selected_truth_mask]
    fake_selected = selected[~selected_truth_mask]
    selected_total = int(len(selected))
    report["metrics"] = {
        "definition": {
            "reconstruction_efficiency": "selected truth-matched triplets / all truth-matched input triplets",
            "purity": "selected truth-matched triplets / all selected triplets",
            "fake_to_true_ratio": "selected non-truth triplets / selected truth-matched triplets",
            "mass_resolution": "population standard deviation of triplet_mass for selected truth-matched triplets",
        },
        "truth_candidate_count": truth_total,
        "true_selected_count": int(len(true_selected)),
        "fake_selected_count": int(len(fake_selected)),
        "reconstruction_efficiency": float(len(true_selected) / truth_total) if truth_total else None,
        "purity": float(len(true_selected) / selected_total) if selected_total else None,
        "fake_to_true_ratio": float(len(fake_selected) / len(true_selected)) if len(true_selected) else None,
        "truth_matched_selected_mass": mass_summary(true_selected["triplet_mass"]),
        "fake_selected_mass": mass_summary(fake_selected["triplet_mass"]),
    }
    return selected, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--selected-output", type=Path)
    args = parser.parse_args()

    candidates = pd.read_parquet(args.input)
    # Preserved task artifacts use ``m123`` while evaluator inputs use the
    # rubric's canonical ``triplet_mass`` name.
    if "triplet_mass" not in candidates.columns and "m123" in candidates.columns:
        candidates = candidates.rename(columns={"m123": "triplet_mass"})
    selected, report = evaluate(candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.selected_output:
        args.selected_output.parent.mkdir(parents=True, exist_ok=True)
        selected.to_parquet(args.selected_output, index=False)


if __name__ == "__main__":
    main()
