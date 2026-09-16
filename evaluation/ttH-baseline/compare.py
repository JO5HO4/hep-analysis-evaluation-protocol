#!/usr/bin/env python3
"""Compare an agent's saved ttH fit result with the inclusive baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from evaluate import read_table
from baseline import BASELINE_VERSION, evaluate


def agent_metric(payload: dict[str, Any], keys: tuple[str, ...], name: str, *, positive: bool = False) -> float:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, (int, float)) and value >= 0 and (not positive or value > 0):
            return float(value)
    qualifier = "positive" if positive else "nonnegative"
    raise ValueError(f"agent fit JSON has no {qualifier} {name} field")


def comparison(name: str, agent: float, baseline: float, direction: str, unit: str) -> dict[str, Any]:
    delta = agent - baseline
    no_worse = agent >= baseline if direction == "higher_is_better" else agent <= baseline
    relative = None if baseline == 0 else 100.0 * (delta if direction == "higher_is_better" else -delta) / abs(baseline)
    return {
        "direction": direction,
        "unit": unit,
        "agent": agent,
        "baseline": baseline,
        "delta_agent_minus_baseline": delta,
        "relative_improvement_percent": relative,
        "agent_no_worse_than_baseline": no_worse,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, type=Path, help="Trusted evaluator-side event table")
    parser.add_argument("--agent-fit", required=True, type=Path, help="Agent significance_asimov.json artifact")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    _, baseline = evaluate(read_table(args.events))
    agent_payload = json.loads(args.agent_fit.read_text())
    agent_z = agent_metric(agent_payload, ("expected_Z", "expected_significance", "z_discovery"), "expected significance")
    agent_q0 = agent_metric(agent_payload, ("q0",), "q0")
    agent_uncertainty = agent_metric(agent_payload, ("mu_uncertainty",), "mu uncertainty", positive=True)
    baseline_fit = baseline["fit"]
    z_comparison = comparison("expected_Z", agent_z, float(baseline_fit["expected_Z"]), "higher_is_better", "sigma")
    q0_comparison = comparison("q0", agent_q0, float(baseline_fit["q0"]), "higher_is_better", "dimensionless")
    uncertainty_comparison = comparison("mu_uncertainty", agent_uncertainty, float(baseline_fit["mu_uncertainty"]), "lower_is_better", "dimensionless")
    pareto = all(item["agent_no_worse_than_baseline"] for item in (z_comparison, uncertainty_comparison)) and any(
        item["agent"] != item["baseline"] for item in (z_comparison, uncertainty_comparison)
    )
    comparison = {
        "schema_version": "tth-inclusive-hadronic-baseline-comparison/v1",
        "comparison_owner": "evaluator",
        "baseline": {"name": BASELINE_VERSION, "fit": baseline_fit},
        "agent": {"expected_Z": agent_z, "q0": agent_q0, "mu_uncertainty": agent_uncertainty},
        "metric_comparisons": {"expected_Z": z_comparison, "q0": q0_comparison, "mu_uncertainty": uncertainty_comparison},
        "pareto_improvement": pareto,
        "pareto_definition": "expected Z no lower, mu uncertainty no greater, with at least one strict improvement; q0 is supporting evidence only",
        "limitations": [
            "The agent fit must be evaluated on the same trusted event sample and common fit assumptions as the baseline.",
            "This comparison is evaluator-owned development evidence and is not an authoritative outcome grade.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
