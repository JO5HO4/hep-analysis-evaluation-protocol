"""Frozen four-quantile category baseline using an agent's continuous BDT score."""
from __future__ import annotations
import math
from typing import Any
import pandas as pd
from baseline import evaluate as evaluate_inclusive

BASELINE_VERSION = "fixed-score-quantiles-4/v1"

def evaluate(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    if "bdt_score" not in events: raise ValueError("bdt_score is required for the fixed-quantile baseline")
    scores = pd.to_numeric(events["bdt_score"], errors="coerce")
    if scores.isna().any() or not scores.between(0, 1).all(): raise ValueError("bdt_score must be finite in [0, 1]")
    boundaries = [float(scores.quantile(q)) for q in (0, .25, .5, .75, 1)]
    frame = events.copy(); frame["fixed_quantile_category"] = pd.cut(scores, bins=boundaries, labels=False, include_lowest=True, duplicates="drop")
    reports=[]
    for category, rows in frame.groupby("fixed_quantile_category", observed=True):
        if rows.empty: continue
        try: _, report = evaluate_inclusive(rows)
        except ValueError: continue
        reports.append((int(category), report))
    if not reports: raise ValueError("no quantile category has a usable TI sideband")
    q0=sum(item[1]["fit"]["q0"] for item in reports); info=sum(1/item[1]["fit"]["mu_uncertainty"]**2 for item in reports if item[1]["fit"]["mu_uncertainty"])
    return frame, {"schema_version":"tth-fixed-quantile-baseline-results/v1", "baseline":{"name":BASELINE_VERSION,"category_count":len(reports),"boundaries":boundaries,"uses_agent_score":True,"uses_agent_category":False}, "fit":{"q0":q0,"expected_Z":math.sqrt(q0),"mu_uncertainty":math.sqrt(1/info) if info else None}, "categories":[{"index":i,"fit":r["fit"],"yields_36fb":r["yields_36fb"]} for i,r in reports], "limitations":["Evaluator-side development baseline; not an authoritative outcome scorer.","It holds the supplied BDT score fixed and tests only category-boundary optimization."]}
