"""Category assignment, retention, expected yields and machine-readable histograms."""

from __future__ import annotations

import math
from typing import Any, Mapping

import numpy as np
import pandas as pd

from .top_categorization import (
    CATEGORY_ORDER,
    CUTBASED_HADRONIC_CATEGORIES,
    HADRONIC_BDT_CATEGORIES,
    assign_top_category,
    counting_significance,
)

MODEL_COMPONENTS = ("signal_ttH_tH", "resonant_higgs_bkg", "nti_continuum_bkg")


def _assign(df: pd.DataFrame, thresholds: list[float], allowed: set[str] | None) -> np.ndarray:
    n_lep = df["n_leptons"].to_numpy()
    n_jets = df["n_jets"].to_numpy()
    n_cent = df["n_jets_central"].to_numpy()
    n_b = df["n_bjets"].to_numpy()
    had = df["passes_hadronic_preselection"].to_numpy()
    score = df["bdt_score"].to_numpy(dtype=float)

    out = np.empty(len(df), dtype=object)
    for i in range(len(df)):
        if not had[i]:
            out[i] = "unassigned"
            continue
        event = {
            "n_leptons": int(n_lep[i]),
            "n_jets": int(n_jets[i]),
            "n_jets_central": int(n_cent[i]),
            "n_bjets": int(n_b[i]),
        }
        if allowed is not None:
            event["allowed_categories"] = allowed
        s = score[i]
        out[i] = assign_top_category(
            event, score=None if not math.isfinite(s) else float(s), thresholds=thresholds
        )
    return out


def _component_yields(sub: pd.DataFrame) -> dict[str, float]:
    w = sub["significance_model_weight_36fb"].to_numpy(dtype=float)
    comp = sub["model_component"].to_numpy()
    out = {}
    for name in MODEL_COMPONENTS:
        mask = comp == name
        out[name] = float(w[mask].sum())
        out[name + "_raw_rows"] = int(mask.sum())
        out[name + "_sumw2"] = float((w[mask] ** 2).sum())
    return out


def assign_categories(
    df: pd.DataFrame, thresholds: list[float], cfg: Mapping[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Assign categories and apply the >= 0.8-background retention requirement."""
    min_b = float(cfg["categorization"]["min_background_yield_signal_window"])
    physics_categories = [c for c in CATEGORY_ORDER if c != "unassigned"]
    allowed: set[str] = set(physics_categories)

    history: list[dict[str, Any]] = []
    for iteration in range(1, len(physics_categories) + 2):
        cats = _assign(df, thresholds, allowed)
        dropped_this_round: list[str] = []
        snapshot: dict[str, Any] = {}
        for name in physics_categories:
            if name not in allowed:
                snapshot[name] = {"kept": False, "reason": "dropped in an earlier iteration"}
                continue
            sub = df[cats == name]
            comp = _component_yields(sub)
            total_bkg = comp["resonant_higgs_bkg"] + comp["nti_continuum_bkg"]
            keep = total_bkg >= min_b
            snapshot[name] = {
                "kept": bool(keep),
                "total_expected_background_signal_window": total_bkg,
                "resonant_higgs_bkg": comp["resonant_higgs_bkg"],
                "nti_continuum_bkg": comp["nti_continuum_bkg"],
                "signal_ttH_tH": comp["signal_ttH_tH"],
                "threshold": min_b,
            }
            if not keep:
                dropped_this_round.append(name)
        history.append({"iteration": iteration, "categories": snapshot})
        if not dropped_this_round:
            break
        allowed -= set(dropped_this_round)

    cats = _assign(df, thresholds, allowed)
    out = df.copy()
    out["category"] = cats
    out["category_is_kept"] = np.isin(cats, list(allowed))

    retention = {
        "requirement": (
            "A non-catch-all physics category is kept only if its TOTAL expected "
            f"background yield in the 125 +/- 2 GeV signal window is >= {min_b} "
            "events, after applying the resonant Higgs normalisation and the "
            "scaled NTI continuum normalisation."
        ),
        "min_background_yield": min_b,
        "weight_used": "significance_model_weight_36fb",
        "iterations": history,
        "kept_categories": [c for c in physics_categories if c in allowed],
        "dropped_categories": [c for c in physics_categories if c not in allowed],
        "dropped_policy": "events of a dropped category fall through to the next "
        "priority category and ultimately to `unassigned`; dropped categories are "
        "excluded from final yields, significances, plots and the workspace",
        "catch_all_category": "unassigned",
    }
    return out, retention


def category_summary(
    df: pd.DataFrame, retention: Mapping[str, Any], cfg: Mapping[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any], float]:
    """Per-category expected yields, S/B, S/sqrt(B) and counting significance."""
    kept = list(retention["kept_categories"])
    ordered = [c for c in CATEGORY_ORDER if c in kept] + ["unassigned"]

    records: list[dict[str, Any]] = []
    z2 = 0.0
    for name in ordered:
        sub = df[df["category"] == name]
        comp = _component_yields(sub)
        s = comp["signal_ttH_tH"]
        b_res = comp["resonant_higgs_bkg"]
        b_cont = comp["nti_continuum_bkg"]
        b = b_res + b_cont
        z = counting_significance(s, b)
        if name != "unassigned":
            z2 += z * z
        had = sub[sub["passes_hadronic_preselection"]]
        ti_sb = int(
            (sub["is_data"] & sub["photon_ti"] & sub["in_sideband"]).sum()
        )
        records.append(
            {
                "category": name,
                "kept": name != "unassigned",
                "is_catch_all": name == "unassigned",
                "n_hadronic_rows": int(len(had)),
                "signal_ttH_tH_yield": s,
                "resonant_higgs_bkg_yield": b_res,
                "nti_continuum_bkg_yield": b_cont,
                "total_background_yield": b,
                "total_model_yield": s + b,
                "S_over_B": (s / b) if b > 0 else float("nan"),
                "S_over_sqrtB": (s / math.sqrt(b)) if b > 0 else float("nan"),
                "expected_counting_significance": z,
                "signal_raw_rows": comp["signal_ttH_tH_raw_rows"],
                "resonant_raw_rows": comp["resonant_higgs_bkg_raw_rows"],
                "nti_proxy_raw_rows": comp["nti_continuum_bkg_raw_rows"],
                "observed_ti_sideband_rows": ti_sb,
                "observed_ti_signal_window": "BLINDED",
            }
        )

    summary = pd.DataFrame.from_records(records)
    combined = math.sqrt(z2)

    manifest = {
        "luminosity_fb": cfg["normalization"]["luminosity_fb"],
        "weight_used_for_yields": "significance_model_weight_36fb",
        "weight_definition": (
            "TI MC events in 125 +/- 2 GeV normalised to 36 fb^-1 "
            "(xsec * k-factor * filter-eff / signed sum-of-weights * generator "
            "weight * scale factors * 36000 pb^-1) PLUS observed-data NTI "
            "sideband events weighted by SF1*SF2"
        ),
        "classifier_fit_weight_used_for_yields": False,
        "classifier_fit_weight_note": (
            "bdt_fit_weight is class-balanced and is used ONLY to fit the "
            "classifier; it never enters yields or significances"
        ),
        "observed_data_weight_column": "observed_data_weight",
        "nti_continuum_weight_column": "nti_continuum_weight",
        "category_order": list(CATEGORY_ORDER),
        "hadronic_bdt_categories": list(HADRONIC_BDT_CATEGORIES),
        "cut_based_hadronic_categories": {
            "categories": list(CUTBASED_HADRONIC_CATEGORIES),
            "priority": "evaluated only after the event fails every hadronic BDT category",
            "requirements": {
                "tH_had_4j1b": "N_leptons == 0 AND exactly 4 CENTRAL jets AND exactly 1 b-tag",
                "tH_had_4j2b": "N_leptons == 0 AND exactly 4 CENTRAL jets AND >= 2 b-tags",
            },
            "jet_counter": "n_jets_central (central-jet count, NOT total jet multiplicity)",
        },
        "leptonic_categories": {
            "in_scope": False,
            "reason": "no reconstructed forward jets in the current open-data inputs",
            "leptonic_rows": "retained as bookkeeping only; excluded from "
            "categorization, significance and the workspace",
        },
        "kept_categories": kept,
        "dropped_categories": list(retention["dropped_categories"]),
        "combined_expected_counting_significance": combined,
        "blinding": {
            "observed_ti_signal_window_blinded": True,
            "blinded_range_gev": cfg["blinding"]["blinded_range_gev"],
            "signal_window_gev": cfg["selection"]["signal_window_gev"],
            "statement": "Observed TI data in the 125 +/- 2 GeV signal window is "
            "never inspected, counted, plotted or reported.",
            "nti_control_shapes_blinded": False,
            "nti_policy": "NTI control-shape distributions retain 120-130 GeV "
            "entries; the removal policy applies only to observed TI data.",
            "observed_significance": "blocked",
        },
        "expected_yield_model": (
            "signal window model: TI MC events in 125 +/- 2 GeV plus observed "
            "data NTI sideband events scaled by SF1*SF2"
        ),
    }
    return summary, manifest, combined


# --------------------------------------------------------------------------
# Histograms
# --------------------------------------------------------------------------


def _hist(values: np.ndarray, weights: np.ndarray, edges: np.ndarray) -> dict[str, Any]:
    contents, _ = np.histogram(values, bins=edges, weights=weights)
    sumw2, _ = np.histogram(values, bins=edges, weights=weights**2)
    raw, _ = np.histogram(values, bins=edges)
    return {
        "contents": contents.tolist(),
        "sumw2": sumw2.tolist(),
        "raw_entries": raw.tolist(),
        "integral": float(contents.sum()),
        "raw_total": int(raw.sum()),
    }


def bdt_score_model_histograms(
    df: pd.DataFrame, cfg: Mapping[str, Any], thresholds: list[float]
) -> dict[str, Any]:
    spec = cfg["bdt"]["score_bins"]
    edges = np.linspace(float(spec["low"]), float(spec["high"]), int(spec["n"]) + 1)
    had = df[df["passes_hadronic_preselection"] & df["bdt_score"].notna()]

    components: dict[str, Any] = {}
    for name in MODEL_COMPONENTS:
        sub = had[had["model_component"] == name]
        components[name] = _hist(
            sub["bdt_score"].to_numpy(dtype=float),
            sub["significance_model_weight_36fb"].to_numpy(dtype=float),
            edges,
        )
    return {
        "variable": "bdt_score",
        "binning": {
            "n_bins": int(spec["n"]),
            "low": float(spec["low"]),
            "high": float(spec["high"]),
            "edges": edges.tolist(),
            "explicit": True,
        },
        "weight": "significance_model_weight_36fb",
        "luminosity_fb": cfg["normalization"]["luminosity_fb"],
        "category_boundaries": list(thresholds),
        "components": components,
        "observed_ti_signal_window_included": False,
    }


def category_mgg_histograms(
    df: pd.DataFrame, retention: Mapping[str, Any], sf: Mapping[str, Any], cfg: Mapping[str, Any]
) -> dict[str, Any]:
    spec = cfg["categorization"]["mgg_hist"]
    edges = np.linspace(float(spec["low"]), float(spec["high"]), int(spec["n"]) + 1)
    blind_lo, blind_hi = cfg["blinding"]["blinded_range_gev"]
    sf1 = float(sf["SF1"])

    kept = [c for c in CATEGORY_ORDER if c in retention["kept_categories"]]
    out_categories: dict[str, Any] = {}
    for name in kept:
        sub = df[(df["category"] == name) & df["passes_hadronic_preselection"]]
        mc = sub[sub["is_mc"] & sub["photon_ti"]]
        sig = mc[mc["process_role"] == "signal_top"]
        res = mc[mc["process_role"] == "resonant_higgs"]
        nti = sub[sub["is_data"] & sub["photon_nti"]]
        ti_data = sub[sub["is_data"] & sub["photon_ti"]]
        ti_unblinded = ti_data[
            (ti_data["m_gammagamma"] < blind_lo) | (ti_data["m_gammagamma"] > blind_hi)
        ]
        out_categories[name] = {
            "signal_ttH_tH_ti_mc_36fb": _hist(
                sig["m_gammagamma"].to_numpy(dtype=float),
                sig["weight_mc_36fb"].to_numpy(dtype=float),
                edges,
            ),
            "resonant_higgs_ti_mc_36fb": _hist(
                res["m_gammagamma"].to_numpy(dtype=float),
                res["weight_mc_36fb"].to_numpy(dtype=float),
                edges,
            ),
            "nti_continuum_control_shape_scaled_by_SF1": _hist(
                nti["m_gammagamma"].to_numpy(dtype=float),
                np.full(len(nti), sf1),
                edges,
            ),
            "observed_ti_data_sidebands_only": _hist(
                ti_unblinded["m_gammagamma"].to_numpy(dtype=float),
                np.ones(len(ti_unblinded)),
                edges,
            ),
        }

    return {
        "variable": "m_gammagamma",
        "units": "GeV",
        "binning": {
            "n_bins": int(spec["n"]),
            "low": float(spec["low"]),
            "high": float(spec["high"]),
            "edges": edges.tolist(),
            "explicit": True,
        },
        "luminosity_fb": cfg["normalization"]["luminosity_fb"],
        "components": {
            "signal_ttH_tH_ti_mc_36fb": "ttH + tH TI MC, weight_mc_36fb, full mass range",
            "resonant_higgs_ti_mc_36fb": "non-top Higgs TI MC (ggH, VBF, WH, ZH, ggZH)",
            "nti_continuum_control_shape_scaled_by_SF1": (
                f"NTI observed-data control shape over the FULL 105-160 GeV range "
                f"(120-130 GeV entries retained), scaled by SF1 = {sf1:.6g}"
            ),
            "observed_ti_data_sidebands_only": (
                f"observed TI data with {blind_lo}-{blind_hi} GeV REMOVED (blinded)"
            ),
        },
        "blinding": {
            "observed_ti_blinded_range_gev": [blind_lo, blind_hi],
            "nti_blinded": False,
            "nti_note": "NTI data are not the signal-enriched TI sample; no "
            "120-130 GeV removal is applied to them",
        },
        "categories": out_categories,
    }


def score_shape_histograms(
    df: pd.DataFrame, cfg: Mapping[str, Any]
) -> dict[str, Any]:
    """Equal-area (shape) BDT-score comparison of the three model components."""
    spec = cfg["bdt"]["score_bins"]
    edges = np.linspace(float(spec["low"]), float(spec["high"]), int(spec["n"]) + 1)
    had = df[df["passes_hadronic_preselection"] & df["bdt_score"].notna()]

    components: dict[str, Any] = {}
    for name in MODEL_COMPONENTS:
        sub = had[had["model_component"] == name]
        weights = sub["significance_model_weight_36fb"].to_numpy(dtype=float)
        values = sub["bdt_score"].to_numpy(dtype=float)
        raw = _hist(values, weights, edges)
        total = raw["integral"]
        norm = np.array(raw["contents"], dtype=float)
        normalized = (norm / total).tolist() if total > 0 else norm.tolist()
        components[name] = {
            "total_before_shape_normalization": total,
            "sumw2": raw["sumw2"],
            "raw_entries": raw["raw_entries"],
            "raw_total": raw["raw_total"],
            "contents_before_normalization": raw["contents"],
            "normalized_contents": normalized,
            "normalized_integral": float(np.sum(normalized)),
        }
    return {
        "variable": "bdt_score",
        "normalization": "each component histogram normalised to unit area "
        "(same area for every component)",
        "binning": {
            "n_bins": int(spec["n"]),
            "low": float(spec["low"]),
            "high": float(spec["high"]),
            "edges": edges.tolist(),
            "explicit": True,
            "range": [0.0, 1.0],
        },
        "weight_before_normalization": "significance_model_weight_36fb",
        "components": components,
        "component_labels": {
            "signal_ttH_tH": "ttH + tH signal",
            "resonant_higgs_bkg": "resonant ggH background (125 +/- 2 GeV)",
            "nti_continuum_bkg": "NTI continuum background (data sidebands)",
        },
    }
