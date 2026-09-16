#!/usr/bin/env python3
"""Evaluator-side comparison of an agent selection with mass-greedy/v2-n-top-2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from baseline_selector import TOP_MASS_GEV, select_mass_greedy
from evaluate import mass_summary


KEY_COLUMNS = ["event_id", "i", "j", "k"]
MAX_SELECTED_PER_EVENT = 2
# Fixed, versioned, unweighted histogram specification.  It is deliberately
# independent of an agent selection so all compared modes have identical bins.
FAKE_MASS_HISTOGRAM = {
    "version": "fixed-unweighted-0-400-GeV-40-bin/v1",
    "range_GeV": [0.0, 400.0],
    "bin_count": 40,
}


def fake_mass_sculpting(unbiased_fakes: pd.Series, selected_fakes: pd.Series) -> dict[str, Any] | None:
    """Describe fake-mass sculpting relative to all pre-selection fakes.

    The mode is the center of the first highest-count fixed histogram bin;
    this deterministic tie convention is part of the record schema.
    """
    reference = pd.to_numeric(unbiased_fakes, errors="coerce").dropna().to_numpy(dtype=float)
    selected = pd.to_numeric(selected_fakes, errors="coerce").dropna().to_numpy(dtype=float)
    if not len(reference) or not len(selected):
        return None
    lower, upper = FAKE_MASS_HISTOGRAM["range_GeV"]
    bins = FAKE_MASS_HISTOGRAM["bin_count"]
    ref_counts, edges = np.histogram(reference, bins=bins, range=(lower, upper))
    selected_counts, _ = np.histogram(selected, bins=bins, range=(lower, upper))
    if not ref_counts.sum() or not selected_counts.sum():
        return None
    centers = (edges[:-1] + edges[1:]) / 2
    reference_mode = float(centers[int(np.argmax(ref_counts))])
    selected_mode = float(centers[int(np.argmax(selected_counts))])
    reference_width = float(np.std(reference, ddof=0))
    selected_width = float(np.std(selected, ddof=0))
    return {
        "histogram": FAKE_MASS_HISTOGRAM,
        "unbiased_fake_count": int(len(reference)),
        "selected_fake_count": int(len(selected)),
        "unbiased_fake_modal_bin_center_GeV": reference_mode,
        "selected_fake_modal_bin_center_GeV": selected_mode,
        "selected_fake_modal_bin_center_shift_GeV": abs(selected_mode - reference_mode),
        "unbiased_fake_population_stddev_GeV": reference_width,
        "selected_fake_population_stddev_GeV": selected_width,
        "selected_fake_width_retention": None if reference_width == 0 else selected_width / reference_width,
    }


def selected_metrics(candidates: pd.DataFrame, selected: pd.DataFrame) -> dict[str, Any]:
    """Calculate labeled metrics after proving selections came from candidates."""
    missing = sorted(set(KEY_COLUMNS) - set(selected.columns))
    if missing:
        raise ValueError(f"selected output is missing key columns: {', '.join(missing)}")
    if "is_truth" not in candidates.columns:
        raise ValueError("comparison input must contain is_truth labels")
    if candidates.duplicated(KEY_COLUMNS).any():
        raise ValueError("candidate table has duplicate candidate keys")
    if selected.duplicated(KEY_COLUMNS).any():
        raise ValueError("selected output contains duplicate candidate keys")
    for event_id, event in selected.groupby("event_id", sort=False):
        if len(event) > MAX_SELECTED_PER_EVENT:
            raise ValueError(f"event {event_id} exceeds {MAX_SELECTED_PER_EVENT} selected candidates")
        jets = event[["i", "j", "k"]].to_numpy().ravel()
        if len(jets) != len(set(int(jet) for jet in jets)):
            raise ValueError(f"event {event_id} contains overlapping selected triplets")

    truth = candidates[KEY_COLUMNS + ["is_truth", "triplet_mass"]]
    labeled = selected[KEY_COLUMNS].merge(truth, on=KEY_COLUMNS, how="left", validate="one_to_one")
    if labeled["is_truth"].isna().any():
        raise ValueError("selected output contains candidates absent from the input table")

    # Input artifacts encode the truth label as either bool or 0/1 integer.
    # Boolean indexing must be explicit: ``frame[integer_series]`` selects
    # columns named 0 and 1 rather than rows on current pandas releases.
    selected_truth_mask = labeled["is_truth"].astype(bool)
    true_selected = labeled[selected_truth_mask]
    fake_selected = labeled[~selected_truth_mask]
    unbiased_fakes = candidates[~candidates["is_truth"].astype(bool)]
    candidate_total = int(len(candidates))
    truth_total = int(candidates["is_truth"].sum())
    selected_total = int(len(labeled))
    true_positive = int(len(true_selected))
    false_positive = int(len(fake_selected))
    false_negative = truth_total - true_positive
    true_negative = candidate_total - true_positive - false_positive - false_negative
    efficiency = float(true_positive / truth_total) if truth_total else None
    purity = float(true_positive / selected_total) if selected_total else None
    specificity = float(true_negative / (true_negative + false_positive)) if true_negative + false_positive else None
    mass = mass_summary(true_selected["triplet_mass"])
    return {
        "candidate_count": candidate_total,
        "truth_candidate_count": truth_total,
        "selected_candidate_count": selected_total,
        "true_selected_count": true_positive,
        "fake_selected_count": false_positive,
        "confusion_matrix": {"true_positive": true_positive, "false_positive": false_positive, "true_negative": true_negative, "false_negative": false_negative},
        "reconstruction_efficiency": efficiency,
        "purity": purity,
        "fake_to_true_ratio": float(false_positive / true_positive) if true_positive else None,
        "f1": float(2 * purity * efficiency / (purity + efficiency)) if purity is not None and efficiency is not None and purity + efficiency else None,
        "selection_accuracy": float((true_positive + true_negative) / candidate_total) if candidate_total else None,
        "balanced_selection_accuracy": float((efficiency + specificity) / 2) if efficiency is not None and specificity is not None else None,
        "truth_matched_selected_mass": mass,
        "truth_matched_selected_mass_bias_GeV": abs(float(mass["median_GeV"]) - TOP_MASS_GEV) if mass else None,
        "fake_mass_sculpting": fake_mass_sculpting(unbiased_fakes["triplet_mass"], fake_selected["triplet_mass"]),
    }


def pareto_improvement(agent: dict[str, Any], baseline: dict[str, Any]) -> bool:
    agent_efficiency = agent["reconstruction_efficiency"]
    baseline_efficiency = baseline["reconstruction_efficiency"]
    agent_fake_ratio = agent["fake_to_true_ratio"]
    baseline_fake_ratio = baseline["fake_to_true_ratio"]
    if None in (agent_efficiency, baseline_efficiency, agent_fake_ratio, baseline_fake_ratio):
        return False
    return bool(
        agent_efficiency >= baseline_efficiency
        and agent_fake_ratio <= baseline_fake_ratio
        and (agent_efficiency > baseline_efficiency or agent_fake_ratio < baseline_fake_ratio)
    )


def compare_metrics(agent: dict[str, Any], baseline: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return evaluator-owned, directional comparisons for every supported metric."""
    definitions = {
        "reconstruction_efficiency": ("higher_is_better", "fraction"),
        "purity": ("higher_is_better", "fraction"),
        "fake_to_true_ratio": ("lower_is_better", "ratio"),
        "f1": ("higher_is_better", "fraction"),
        "selection_accuracy": ("higher_is_better", "fraction"),
        "balanced_selection_accuracy": ("higher_is_better", "fraction"),
        "truth_matched_selected_mass_bias_GeV": ("lower_is_better", "GeV"),
    }
    comparisons: dict[str, dict[str, Any]] = {}
    for name, (direction, unit) in definitions.items():
        agent_value, baseline_value = agent[name], baseline[name]
        passes = None if None in (agent_value, baseline_value) else (agent_value >= baseline_value if direction == "higher_is_better" else agent_value <= baseline_value)
        relative_improvement = None
        if None not in (agent_value, baseline_value) and baseline_value != 0:
            numerator = agent_value - baseline_value if direction == "higher_is_better" else baseline_value - agent_value
            relative_improvement = 100 * numerator / abs(baseline_value)
        comparisons[name] = {
            "direction": direction,
            "unit": unit,
            "agent": agent_value,
            "baseline": baseline_value,
            "delta_agent_minus_baseline": None if None in (agent_value, baseline_value) else agent_value - baseline_value,
            "relative_improvement_percent": relative_improvement,
            "agent_no_worse_than_baseline": passes,
        }
    for name in ("stddev_GeV",):
        agent_mass, baseline_mass = agent["truth_matched_selected_mass"], baseline["truth_matched_selected_mass"]
        agent_value = agent_mass[name] if agent_mass else None
        baseline_value = baseline_mass[name] if baseline_mass else None
        comparisons["truth_matched_selected_mass_resolution_GeV"] = {
            "direction": "lower_is_better",
            "unit": "GeV",
            "agent": agent_value,
            "baseline": baseline_value,
            "delta_agent_minus_baseline": None if None in (agent_value, baseline_value) else agent_value - baseline_value,
            "relative_improvement_percent": None if None in (agent_value, baseline_value) or baseline_value == 0 else 100 * (baseline_value - agent_value) / abs(baseline_value),
            "agent_no_worse_than_baseline": None if None in (agent_value, baseline_value) else agent_value <= baseline_value,
        }
    return comparisons


def fake_mass_sculpting_comparison(agent: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any] | None:
    """Compare raw sculpting values; this is a diagnostic, not a score."""
    agent_metrics = agent["fake_mass_sculpting"]
    baseline_metrics = baseline["fake_mass_sculpting"]
    if agent_metrics is None or baseline_metrics is None:
        return None
    shift_agent = agent_metrics["selected_fake_modal_bin_center_shift_GeV"]
    shift_baseline = baseline_metrics["selected_fake_modal_bin_center_shift_GeV"]
    width_agent = agent_metrics["selected_fake_width_retention"]
    width_baseline = baseline_metrics["selected_fake_width_retention"]
    better = None if None in (shift_agent, shift_baseline, width_agent, width_baseline) else bool(
        shift_agent <= shift_baseline
        and width_agent >= width_baseline
        and (shift_agent < shift_baseline or width_agent > width_baseline)
    )
    return {
        "definition": "agent mode shift <= baseline mode shift and agent width retention >= baseline width retention, with at least one strict improvement",
        "agent_better_than_baseline": better,
        "agent": agent_metrics,
        "baseline": baseline_metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True, type=Path, help="Labeled evaluator-side candidate Parquet")
    parser.add_argument("--agent-selection", required=True, type=Path, help="Agent output Parquet")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    candidates = pd.read_parquet(args.candidates)
    agent_selection = pd.read_parquet(args.agent_selection)
    baseline_selection = select_mass_greedy(candidates)
    agent = selected_metrics(candidates, agent_selection)
    baseline = selected_metrics(candidates, baseline_selection)
    report = {
        "schema_version": "top-reconstruction-baseline-comparison/v2",
        "comparison_owner": "evaluator",
        "agent": agent,
        "baseline": {"selector": "mass-greedy/v2-n-top-2", "metrics": baseline},
        "metric_comparisons": compare_metrics(agent, baseline),
        "fake_mass_sculpting_comparison": fake_mass_sculpting_comparison(agent, baseline),
        "pareto_improvement": pareto_improvement(agent, baseline),
        "definition": "agent efficiency >= baseline efficiency and agent fake-to-true ratio <= baseline ratio, with at least one strict improvement",
        "unavailable_metrics": {
            "roc_auc": "The task artifact records only selected candidates, not an agent-produced continuous score for every candidate.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
