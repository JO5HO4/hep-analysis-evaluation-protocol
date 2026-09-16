"""Evaluator-side inclusive hadronic ttH baseline.

The baseline deliberately uses no BDT score, classifier, or agent-defined
category.  It aggregates the trusted hadronic event table into one category
and performs a binned S+B Asimov profile-likelihood calculation with a
constant continuum rate determined from observed-data sidebands.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd


BASELINE_VERSION = "inclusive-hadronic-constant-sideband/v1"
CATEGORY = "inclusive_hadronic"
MASS_EDGES_GEV = (105.0, 110.0, 115.0, 120.0, 123.0, 127.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0)
SIGNAL_WINDOW_GEV = (123.0, 127.0)
SIDEBAND_INTERVALS_GEV = ((105.0, 120.0), (130.0, 160.0))
REQUIRED_COLUMNS = {
    "m_gammagamma",
    "passes_hadronic_preselection",
    "model_component",
    "significance_model_weight_36fb",
    "is_data",
    "photon_ti",
}


def _bool(values: pd.Series) -> pd.Series:
    if values.dtype == bool:
        return values
    return values.astype(str).str.strip().str.lower().isin({"1", "true", "yes"})


def _histogram(rows: pd.DataFrame, weight: str) -> list[float]:
    weights = pd.to_numeric(rows[weight], errors="coerce").fillna(0.0)
    bins = pd.cut(pd.to_numeric(rows["m_gammagamma"], errors="coerce"), bins=MASS_EDGES_GEV, right=False)
    grouped = weights.groupby(bins, observed=False).sum()
    return [float(grouped.get(interval, 0.0)) for interval in pd.IntervalIndex.from_breaks(MASS_EDGES_GEV, closed="left")]


def _sideband_mask(mass: pd.Series) -> pd.Series:
    return ((mass >= SIDEBAND_INTERVALS_GEV[0][0]) & (mass < SIDEBAND_INTERVALS_GEV[0][1])) | ((mass >= SIDEBAND_INTERVALS_GEV[1][0]) & (mass < SIDEBAND_INTERVALS_GEV[1][1]))


def _nll(observed: list[float], signal: list[float], resonant: list[float], continuum: list[float], mu: float, beta: float) -> float:
    total = 0.0
    for n, s, r, c in zip(observed, signal, resonant, continuum, strict=True):
        expectation = mu * s + r + beta * c
        if expectation <= 0:
            return math.inf
        total += expectation - n * math.log(expectation)
    return total


def _best_continuum_scale(observed: list[float], fixed: list[float], continuum: list[float]) -> float:
    """Profile the nonnegative continuum scale with deterministic bisection."""
    if not any(continuum):
        return 0.0

    def derivative(beta: float) -> float:
        return sum(c * (1.0 - n / max(f + beta * c, 1.0e-300)) for n, f, c in zip(observed, fixed, continuum, strict=True))

    if derivative(0.0) >= 0:
        return 0.0
    high = 1.0
    while derivative(high) < 0:
        high *= 2.0
        if high > 1.0e12:
            raise ValueError("could not profile continuum normalization")
    low = 0.0
    for _ in range(100):
        middle = (low + high) / 2.0
        if derivative(middle) < 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def evaluate(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    missing = sorted(REQUIRED_COLUMNS - set(events.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    frame = events.copy()
    frame["m_gammagamma"] = pd.to_numeric(frame["m_gammagamma"], errors="coerce")
    hadronic = _bool(frame["passes_hadronic_preselection"])
    in_range = frame["m_gammagamma"].between(MASS_EDGES_GEV[0], MASS_EDGES_GEV[-1], inclusive="left")
    selected = frame.loc[hadronic & in_range].copy()
    selected["baseline_category"] = CATEGORY

    component = selected["model_component"].astype(str)
    signal = _histogram(selected.loc[component == "signal_ttH_tH"], "significance_model_weight_36fb")
    resonant = _histogram(selected.loc[component == "resonant_higgs_bkg"], "significance_model_weight_36fb")
    data_ti = selected.loc[_bool(selected["is_data"]) & _bool(selected["photon_ti"])].copy()
    sideband_data = data_ti.loc[_sideband_mask(data_ti["m_gammagamma"])]
    data_weight = "observed_data_weight" if "observed_data_weight" in sideband_data.columns else None
    if data_weight is None:
        sideband_count = float(len(sideband_data))
    else:
        sideband_count = float(pd.to_numeric(sideband_data[data_weight], errors="coerce").fillna(0.0).sum())
    sideband_width = sum(high - low for low, high in SIDEBAND_INTERVALS_GEV)
    if sideband_count <= 0:
        raise ValueError("no positive observed TI sideband yield for continuum baseline")
    rate = sideband_count / sideband_width
    continuum = [rate * (high - low) for low, high in zip(MASS_EDGES_GEV[:-1], MASS_EDGES_GEV[1:], strict=True)]
    observed = [s + r + c for s, r, c in zip(signal, resonant, continuum, strict=True)]
    fixed_mu0 = [r for r in resonant]
    beta_mu0 = _best_continuum_scale(observed, fixed_mu0, continuum)
    nll_free = _nll(observed, signal, resonant, continuum, 1.0, 1.0)
    nll_mu0 = _nll(observed, signal, resonant, continuum, 0.0, beta_mu0)
    q0 = max(0.0, 2.0 * (nll_mu0 - nll_free))
    information_mumu = sum(s * s / n for s, n in zip(signal, observed, strict=True) if n > 0)
    information_mubeta = sum(s * c / n for s, c, n in zip(signal, continuum, observed, strict=True) if n > 0)
    information_betabeta = sum(c * c / n for c, n in zip(continuum, observed, strict=True) if n > 0)
    profiled_information = information_mumu - information_mubeta * information_mubeta / information_betabeta if information_betabeta > 0 else 0.0
    signal_total = float(sum(signal))
    background_total = float(sum(resonant) + sum(continuum))
    counting_z = math.sqrt(2.0 * ((signal_total + background_total) * math.log1p(signal_total / background_total) - signal_total)) if signal_total > 0 and background_total > 0 else 0.0
    report: dict[str, Any] = {
        "schema_version": "tth-inclusive-hadronic-baseline-results/v1",
        "baseline": {
            "name": BASELINE_VERSION,
            "category": CATEGORY,
            "uses_bdt_score": False,
            "uses_agent_category": False,
            "signal_window_GeV": list(SIGNAL_WINDOW_GEV),
            "sideband_intervals_GeV": [list(interval) for interval in SIDEBAND_INTERVALS_GEV],
            "continuum_model": "constant rate fitted only to observed TI sideband yield",
        },
        "sample": {
            "input_event_count": int(len(events)),
            "inclusive_hadronic_event_count": int(len(selected)),
            "observed_ti_sideband_yield": sideband_count,
            "observed_ti_sideband_rate_per_GeV": rate,
        },
        "fit": {
            "method": "binned Poisson profile likelihood on S+B Asimov data",
            "mu_gen": 1.0,
            "mu_hat": 1.0,
            "mu_uncertainty": math.sqrt(1.0 / profiled_information) if profiled_information > 0 else None,
            "continuum_scale_hat": 1.0,
            "continuum_scale_mu0": beta_mu0,
            "q0": q0,
            "expected_Z": math.sqrt(q0),
        },
        "yields_36fb": {
            "signal_ttH_tH": signal_total,
            "resonant_higgs_background": float(sum(resonant)),
            "continuum_background": float(sum(continuum)),
            "total_background": background_total,
            "expected_counting_Z": counting_z,
        },
        "mass_bins": [
            {"low_GeV": low, "high_GeV": high, "signal": s, "resonant_higgs_background": r, "continuum_background": c, "asimov_total": n}
            for low, high, s, r, c, n in zip(MASS_EDGES_GEV[:-1], MASS_EDGES_GEV[1:], signal, resonant, continuum, observed, strict=True)
        ],
        "limitations": [
            "This is an evaluator-side development baseline, not the task verifier or an authoritative outcome scorer.",
            "The baseline requires a trusted evaluator event table; agent-produced event tables are unsuitable as the canonical evaluation input.",
            "The continuum model is intentionally a constant sideband-rate model and is not a substitute for the task's full RooFit workspace model.",
        ],
    }
    return selected, report
