"""Frozen, mass-blind Gaussian-naive-Bayes top-candidate classifier baseline."""
from __future__ import annotations
import numpy as np
import pandas as pd

BASELINE_VERSION = "gaussian-naive-bayes-mass-blind/v1"
FEATURES = ("dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc")

def partition(event_id: pd.Series) -> pd.Series:
    bucket = pd.to_numeric(event_id, errors="raise").astype("int64") % 10
    return pd.Series(np.where(bucket < 7, "train", np.where(bucket < 8, "validation", "test")), index=event_id.index)

def _matrix(frame: pd.DataFrame) -> np.ndarray:
    missing = sorted(set(FEATURES) - set(frame.columns))
    if missing: raise ValueError(f"missing classifier features: {', '.join(missing)}")
    x = frame.loc[:, FEATURES].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    if not np.isfinite(x).all(): raise ValueError("classifier features contain non-finite values")
    return x

def fit(train: pd.DataFrame) -> dict[str, np.ndarray]:
    x, y = _matrix(train), train["is_truth"].astype(bool).to_numpy()
    if not y.any() or y.all(): raise ValueError("training partition must contain both classes")
    return {"mean0": x[~y].mean(0), "var0": x[~y].var(0).clip(1e-12), "mean1": x[y].mean(0), "var1": x[y].var(0).clip(1e-12)}

def score(frame: pd.DataFrame, model: dict[str, np.ndarray]) -> np.ndarray:
    x = _matrix(frame)
    def logp(label: str) -> np.ndarray:
        variance, mean = model[f"var{label}"], model[f"mean{label}"]
        return -0.5 * (np.log(2 * np.pi * variance) + (x - mean) ** 2 / variance).sum(1)
    difference = np.clip(logp("1") - logp("0"), -700, 700)
    return 1 / (1 + np.exp(-difference))

def auc(y: np.ndarray, scores: np.ndarray) -> float:
    if y.min() == y.max(): raise ValueError("AUC requires both classes")
    order = np.argsort(scores, kind="mergesort"); ranks = np.empty(len(scores), float); ranks[order] = np.arange(1, len(scores)+1)
    for value in np.unique(scores):
        tied = scores == value
        if tied.sum() > 1: ranks[tied] = ranks[tied].mean()
    positives = y.astype(bool); npos, nneg = positives.sum(), (~positives).sum()
    return float((ranks[positives].sum() - npos*(npos+1)/2) / (npos*nneg))

def evaluate(frame: pd.DataFrame) -> dict[str, object]:
    if "event_id" not in frame or "is_truth" not in frame: raise ValueError("event_id and is_truth are required")
    parts = partition(frame["event_id"]); train, test = frame.loc[parts == "train"], frame.loc[parts == "test"]
    model = fit(train); test_scores = score(test, model)
    return {"schema_version": "top-classifier-baseline-results/v1", "baseline": {"name": BASELINE_VERSION, "features": list(FEATURES), "mass_blind": True, "partition": "event_id modulo 10: train 0-6, validation 7, test 8-9"}, "sample": {"train_candidates": int(len(train)), "test_candidates": int(len(test))}, "test": {"roc_auc": auc(test["is_truth"].to_numpy(), test_scores)}}
