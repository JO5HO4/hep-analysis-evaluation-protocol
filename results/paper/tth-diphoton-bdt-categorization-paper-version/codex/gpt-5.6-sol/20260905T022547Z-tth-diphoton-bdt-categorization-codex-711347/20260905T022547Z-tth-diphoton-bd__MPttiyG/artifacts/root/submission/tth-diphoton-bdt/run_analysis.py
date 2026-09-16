#!/usr/bin/env python3
"""Deterministic end-to-end hadronic ttH/tH diphoton BDT analysis."""

from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import platform
import sys
import time
from pathlib import Path
from typing import Any

import awkward as ak
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import uproot
import yaml
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis.top_categorization import (  # noqa: E402
    BDT_FEATURES, CATEGORY_ORDER, assign_top_category, optimize_bdt_boundaries,
    stable_partition,
)

ALLOWED_PROCESSES = ["ggH", "VBF", "WH", "ZH", "ggZH", "ttH", "tH"]
SIGNAL_PROCESSES = {"ttH", "tH"}
LUMI_FB = 36.0
LUMI_PB = 36000.0
MASS_RANGE = (105.0, 160.0)
SIGNAL_WINDOW = (123.0, 127.0)
TI_BLIND_WINDOW = (120.0, 130.0)
PARTITION_FRACTIONS = (0.60, 0.20, 0.20)
SEED = 240513


def native(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): native(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(native(payload), indent=2, sort_keys=True) + "\n")


def savefig(path_no_suffix: Path) -> None:
    path_no_suffix.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path_no_suffix.with_suffix(".png"), dpi=170)
    plt.savefig(path_no_suffix.with_suffix(".pdf"))
    plt.close()


def hist_payload(values: np.ndarray, weights: np.ndarray, edges: np.ndarray) -> dict[str, Any]:
    contents, _ = np.histogram(values, bins=edges, weights=weights)
    sumw2, _ = np.histogram(values, bins=edges, weights=weights * weights)
    return {"bin_edges": edges, "bin_contents": contents, "sumw2": sumw2,
            "total": float(np.sum(weights)), "entries": int(len(values))}


def asimov_z(s: float, b: float) -> float:
    s, b = max(float(s), 0.0), max(float(b), 0.0)
    if s <= 0 or b <= 0:
        return 0.0
    return math.sqrt(max(2 * ((s + b) * math.log1p(s / b) - s), 0.0))


def discover_inputs(input_root: Path) -> tuple[dict[str, Path], Path]:
    mc_dir, data_dir = input_root / "MC", input_root / "data"
    if not mc_dir.is_dir() or not data_dir.is_dir():
        raise FileNotFoundError(f"Expected MC/ and data/ under {input_root}")
    found: dict[str, Path] = {}
    for process in ALLOWED_PROCESSES:
        matches = sorted(mc_dir.glob(f"{process}*.root"))
        # Avoid matching ggZH when looking for ggH, and ZH when looking for ggZH.
        matches = [p for p in matches if p.stem.split("_", 1)[0] == process]
        if matches:
            found[process] = matches[0]
    data_matches = sorted(data_dir.glob("*.root"))
    if not data_matches:
        raise FileNotFoundError(f"No observed GamGam data ROOT file under {data_dir}")
    missing = [p for p in ALLOWED_PROCESSES if p not in found]
    if missing:
        raise FileNotFoundError(f"Missing required nominal Higgs samples: {missing}")
    return found, data_matches[0]


BRANCHES = [
    "eventNumber", "runNumber", "channelNumber", "num_events", "sum_of_weights", "xsec", "filteff", "kfac",
    "mcWeight", "ScaleFactor_PILEUP", "ScaleFactor_PHOTON", "ScaleFactor_BTAG",
    "ScaleFactor_JVT", "ScaleFactor_FTAG", "jet_pt", "jet_eta", "jet_phi", "jet_e",
    "jet_btag_quantile", "lep_pt", "lep_type", "photon_pt", "photon_eta", "photon_phi",
    "photon_e", "photon_isTightID", "photon_isTightIso",
]


def read_selected(path: Path, process: str, is_data: bool, max_selected: int | None) -> tuple[pd.DataFrame, dict[str, Any]]:
    tree = uproot.open(path)["analysis"]
    a = tree.arrays(BRANCHES, library="ak")
    n_input = len(a)
    ph_mask = ((a.photon_pt > 25.0) & (abs(a.photon_eta) < 2.37)
               & ~((abs(a.photon_eta) > 1.37) & (abs(a.photon_eta) < 1.52)))
    ph_order = ak.argsort(a.photon_pt[ph_mask], axis=1, ascending=False)
    ph_pt = a.photon_pt[ph_mask][ph_order]
    ph_eta = a.photon_eta[ph_mask][ph_order]
    ph_phi = a.photon_phi[ph_mask][ph_order]
    ph_e = a.photon_e[ph_mask][ph_order]
    ph_tid = a.photon_isTightID[ph_mask][ph_order]
    ph_tiso = a.photon_isTightIso[ph_mask][ph_order]
    has_two = ak.num(ph_pt, axis=1) >= 2
    px = ak.sum(ph_pt[:, :2] * np.cos(ph_phi[:, :2]), axis=1)
    py = ak.sum(ph_pt[:, :2] * np.sin(ph_phi[:, :2]), axis=1)
    pz = ak.sum(ph_pt[:, :2] * np.sinh(ph_eta[:, :2]), axis=1)
    energy = ak.sum(ph_e[:, :2], axis=1)
    mass = np.sqrt(np.maximum(np.asarray(energy * energy - px * px - py * py - pz * pz), 0.0))
    diphoton_pt = np.sqrt(np.asarray(px) ** 2 + np.asarray(py) ** 2)
    ti = np.asarray(has_two & ak.all(ph_tid[:, :2] & ph_tiso[:, :2], axis=1), dtype=bool)

    jet_mask = a.jet_pt > 25.0
    central_mask = jet_mask & (abs(a.jet_eta) <= 2.5)
    forward_mask = jet_mask & (abs(a.jet_eta) > 2.5)
    b_mask = jet_mask & (a.jet_btag_quantile >= 4)
    n_jets = np.asarray(ak.sum(jet_mask, axis=1), dtype=int)
    n_central = np.asarray(ak.sum(central_mask, axis=1), dtype=int)
    n_forward = np.asarray(ak.sum(forward_mask, axis=1), dtype=int)
    n_b = np.asarray(ak.sum(b_mask, axis=1), dtype=int)
    jet_ht = np.asarray(ak.sum(a.jet_pt[jet_mask], axis=1), dtype=float)
    jet1 = np.asarray(ak.fill_none(ak.firsts(a.jet_pt[jet_mask]), 0.0), dtype=float)
    lep_mask = (a.lep_pt > 10.0) & ((abs(a.lep_type) == 11) | (abs(a.lep_type) == 13))
    n_lep = np.asarray(ak.sum(lep_mask, axis=1), dtype=int)
    hadronic = np.asarray(has_two, dtype=bool) & (n_lep == 0) & (n_jets >= 3) & (n_b >= 1)
    in_range = (mass >= MASS_RANGE[0]) & (mass <= MASS_RANGE[1])
    selected = hadronic & in_range
    # Standard analysis blinding: observed TI data in 120--130 GeV never enters
    # an analysis row, count, histogram, score output, or category assignment.
    if is_data:
        selected &= ~(ti & (mass >= TI_BLIND_WINDOW[0]) & (mass <= TI_BLIND_WINDOW[1]))
    indices = np.flatnonzero(selected)
    uncapped_selected = len(indices)
    if max_selected is not None:
        indices = indices[:max_selected]
    def take(field: str, dtype=float) -> np.ndarray:
        return np.asarray(a[field], dtype=dtype)[indices]
    if is_data:
        mc_weight = np.ones(len(indices))
        sf_product = np.ones(len(indices))
        physical = np.zeros(len(indices))
    else:
        mc_weight = take("mcWeight")
        sf_product = (take("ScaleFactor_PILEUP") * take("ScaleFactor_PHOTON")
                      * take("ScaleFactor_BTAG") * take("ScaleFactor_JVT")
                      * take("ScaleFactor_FTAG"))
        denominator = take("sum_of_weights")
        physical = np.divide(
            LUMI_PB * take("xsec") * take("filteff") * take("kfac") * mc_weight * sf_product,
            denominator, out=np.zeros(len(indices)), where=denominator != 0,
        )
    run = take("runNumber", np.int64)
    event = take("eventNumber", np.int64)
    mc_channel = take("channelNumber", np.int64)
    ids = [f"{process}:{int(c)}:{int(r)}:{int(e)}" for c, r, e in zip(mc_channel, run, event)]
    df = pd.DataFrame({
        "event_id": ids, "mc_channel_number": mc_channel, "run_number": run, "event_number": event, "sample": process,
        "process": process, "is_data": is_data, "is_signal_process": process in SIGNAL_PROCESSES,
        "m_gammagamma": mass[indices], "diphoton_pt": diphoton_pt[indices],
        "diphoton_is_ti": ti[indices], "diphoton_is_nti": ~ti[indices],
        "n_leptons": n_lep[indices], "n_jets": n_jets[indices],
        "n_central_jets": n_central[indices], "n_forward_jets": n_forward[indices],
        "n_bjets": n_b[indices], "jet1_pt": jet1[indices], "jet_ht": jet_ht[indices],
        "hadronic_preselection": True, "leptonic_bookkeeping": False, "channel": "hadronic",
        "mc_generator_weight": mc_weight, "event_scale_factor_product": sf_product,
        "sm_normalized_mc_weight_36fb": physical,
        "observed_data_weight": np.ones(len(indices)) if is_data else np.zeros(len(indices)),
    })
    df["stable_partition"] = [stable_partition(x, SEED, PARTITION_FRACTIONS) for x in ids]
    summary = {
        "process": process, "input_entries": n_input,
        "two_kinematic_photons": int(np.count_nonzero(has_two & in_range)),
        "hadronic_preselection_unblinded_analysis_rows_before_optional_cap": uncapped_selected,
        "rows_written": len(df), "cap_applied": max_selected is not None,
        "signed_weight_sum_36fb": float(df.sm_normalized_mc_weight_36fb.sum()),
        "absolute_weight_sum_36fb": float(df.sm_normalized_mc_weight_36fb.abs().sum()),
        "negative_weight_rows": int((df.sm_normalized_mc_weight_36fb < 0).sum()),
        "observed_unit_weight_sum": float(df.observed_data_weight.sum()),
    }
    return df, summary


def make_preselection_outputs(df: pd.DataFrame, summaries: list[dict[str, Any]], out: Path) -> None:
    by_process = {x["process"]: x for x in summaries}
    payload = {
        "photon_selection": "at least two photons with pT > 25 GeV, |eta| < 2.37, excluding 1.37 < |eta| < 1.52; no tight-ID or isolation requirement",
        "hadronic_selection": "zero selected e/mu, at least three selected jets, at least one b-tagged selected jet",
        "leptonic_bookkeeping_selection": "not retained in this run (if retained: >=1 selected e/mu and >=1 selected b-jet; bookkeeping only)",
        "mass_bookkeeping_range_GeV": list(MASS_RANGE), "channel_rows": "hadronic only",
        "raw_and_weighted_counts_by_process": by_process,
        "overall_input_entries": int(sum(x["input_entries"] for x in summaries)),
        "overall_two_kinematic_photon_rows_in_mass_range": int(sum(x["two_kinematic_photons"] for x in summaries)),
        "overall_rows_written": int(len(df)),
        "overall_signed_mc_yield_36fb": float(df.sm_normalized_mc_weight_36fb.sum()),
        "overall_observed_unit_weight": float(df.observed_data_weight.sum()),
        "signed_weight_bookkeeping": True,
    }
    write_json(out / "preselection_summary.json", payload)
    write_json(out / "cutflow.json", {
        "by_process": {p: {k: v for k, v in x.items() if k in ["input_entries", "two_kinematic_photons", "hadronic_preselection_unblinded_analysis_rows_before_optional_cap", "rows_written"]} for p, x in by_process.items()},
        "notes": "Observed TI data in 120-130 GeV are blinded before analysis-row counting; no blinded count is recorded.",
    })
    bins = np.linspace(105, 160, 56)
    plt.figure(figsize=(8, 5))
    for label, mask in [("Higgs MC", ~df.is_data), ("NTI data", df.is_data & df.diphoton_is_nti), ("TI sideband data", df.is_data & df.diphoton_is_ti)]:
        plt.hist(df.loc[mask, "m_gammagamma"], bins=bins, histtype="step", label=label)
    plt.axvspan(120, 130, color="gray", alpha=.18, label="TI data blinded")
    plt.xlabel(r"$m_{\gamma\gamma}$ [GeV]"); plt.ylabel("Analysis rows"); plt.legend()
    savefig(out / "plots" / "preselection_mass")
    plt.figure(figsize=(6, 4)); plt.bar(["hadronic"], [len(df)]); plt.ylabel("Analysis rows")
    savefig(out / "plots" / "preselection_channels")
    counts = df.groupby("process").size().reindex(ALLOWED_PROCESSES + ["data"], fill_value=0)
    plt.figure(figsize=(8, 4)); plt.bar(counts.index, counts.values); plt.yscale("log"); plt.ylabel("Analysis rows")
    savefig(out / "plots" / "preselection_processes")


def construct_training(df: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, dict[str, float]]:
    data_had = df[df.is_data]
    sideband = ((data_had.m_gammagamma >= 105) & (data_had.m_gammagamma < 120)) | ((data_had.m_gammagamma > 130) & (data_had.m_gammagamma <= 160))
    window = (data_had.m_gammagamma >= 123) & (data_had.m_gammagamma <= 127)
    ti_sb = float((data_had.diphoton_is_ti & sideband).sum())
    nti_sb = float((data_had.diphoton_is_nti & sideband).sum())
    nti_sw = float((data_had.diphoton_is_nti & window).sum())
    sf1 = ti_sb / nti_sb if nti_sb else 0.0
    sf2 = nti_sw / nti_sb if nti_sb else 0.0
    factors = {"SF1": sf1, "SF2": sf2, "SF1_times_SF2": sf1 * sf2,
               "TI_sideband_yield": ti_sb, "NTI_sideband_yield": nti_sb,
               "NTI_125_plusminus_2_yield": nti_sw}
    df["nti_continuum_proxy_weight"] = np.where(df.is_data & df.diphoton_is_nti & sideband, sf1 * sf2, 0.0)
    # A separate all-mass NTI control-shape weight deliberately retains the
    # 120--130 GeV NTI entries. It is never substituted for the sideband-only
    # expected-yield proxy above.
    df["nti_control_shape_weight"] = np.where(df.is_data & df.diphoton_is_nti, sf1 * sf2, 0.0)
    df["significance_model_weight_36fb"] = np.where(~df.is_data, df.sm_normalized_mc_weight_36fb, df.nti_continuum_proxy_weight)
    signal = df[(~df.is_data) & df.process.isin(SIGNAL_PROCESSES)]
    ggh = df[(df.process == "ggH") & df.diphoton_is_ti & window]
    nti = df[df.is_data & df.diphoton_is_nti & sideband]
    parts = []
    for role, sub, is_signal in [("ttH_tH_signal", signal, True), ("ggH_resonant_background", ggh, False), ("NTI_continuum_background", nti, False)]:
        x = sub.copy()
        x["training_role"] = role
        x["is_signal"] = is_signal
        if role == "NTI_continuum_background":
            x["bdt_physical_weight_signed"] = x.nti_continuum_proxy_weight
        else:
            x["bdt_physical_weight_signed"] = x.sm_normalized_mc_weight_36fb
        parts.append(x)
    train = pd.concat(parts, ignore_index=True)
    train["bdt_base_fit_weight"] = train.bdt_physical_weight_signed.clip(lower=0.0)
    fit_mask = train.stable_partition == "train"
    before = train.loc[fit_mask].groupby("is_signal").bdt_base_fit_weight.sum().to_dict()
    sig_sum, bkg_sum = float(before.get(True, 0.0)), float(before.get(False, 0.0))
    target = 0.5 * (sig_sum + bkg_sum)
    sig_factor = target / sig_sum if sig_sum > 0 else 0.0
    bkg_factor = target / bkg_sum if bkg_sum > 0 else 0.0
    train["class_balance_factor"] = np.where(train.is_signal, sig_factor, bkg_factor)
    train["bdt_fit_weight"] = train.bdt_base_fit_weight * train.class_balance_factor
    after = train.loc[fit_mask].groupby("is_signal").bdt_fit_weight.sum().to_dict()
    write_json(out / "model" / "background_mixture_and_normalization.json", {
        "signal": "ttH+tH hadronic MC, SM-normalized per event", "background": "TI ggH MC in 123-127 GeV plus NTI observed-data sidebands",
        "nti_definition": "at least one of the two kinematic photons fails tight ID or tight isolation",
        "ti_definition": "both kinematic photons pass tight ID and tight isolation",
        "sidebands_GeV": [[105, 120], [130, 160]], "signal_window_GeV": [123, 127], **factors,
        "nti_sideband_per_event_proxy_weight": sf1 * sf2,
    })
    write_json(out / "model" / "class_balance_check.json", {
        "applied_after_physical_mixture_construction": True,
        "nonpositive_signed_mc_events_receive_zero_classifier_fit_weight": True,
        "signed_weights_remain_available_for_yields": True,
        "training_partition_class_sums_before_balancing": {"signal": sig_sum, "background": bkg_sum},
        "training_partition_signed_physical_sums_before_balancing": {
            "signal": float(train.loc[fit_mask & train.is_signal, "bdt_physical_weight_signed"].sum()),
            "background": float(train.loc[fit_mask & ~train.is_signal, "bdt_physical_weight_signed"].sum()),
        },
        "balance_factors": {"signal": sig_factor, "background": bkg_factor},
        "training_partition_class_sums_after_balancing": {"signal": float(after.get(True, 0.0)), "background": float(after.get(False, 0.0))},
    })
    return train, factors


def train_and_score(df: pd.DataFrame, training: pd.DataFrame, out: Path) -> tuple[Any, dict[str, Any]]:
    started = time.perf_counter()
    fit = training[(training.stable_partition == "train") & (training.bdt_fit_weight > 0)].copy()
    model = HistGradientBoostingClassifier(
        learning_rate=0.055, max_iter=180, max_leaf_nodes=15, max_depth=4,
        min_samples_leaf=20, l2_regularization=1.0, random_state=SEED,
    )
    model.fit(fit[BDT_FEATURES], fit.is_signal.astype(int), sample_weight=fit.bdt_fit_weight)
    duration = time.perf_counter() - started
    finite = np.isfinite(df[BDT_FEATURES]).all(axis=1)
    df["bdt_score"] = np.nan
    df.loc[finite, "bdt_score"] = model.predict_proba(df.loc[finite, BDT_FEATURES])[:, 1]
    df["bdt_score"] = df.bdt_score.clip(0.0, 1.0)
    # Score the role-specific table directly. Exact duplicate source identifiers
    # remain in the same stable partition, while each physical row keeps its own
    # feature-derived score without introducing a row-order identifier.
    training["bdt_score"] = model.predict_proba(training[BDT_FEATURES])[:, 1]
    eval_rows = training[(training.stable_partition == "test") & training.bdt_score.notna() & (training.bdt_base_fit_weight > 0)]
    auc = None
    if eval_rows.is_signal.nunique() == 2:
        auc = roc_auc_score(eval_rows.is_signal.astype(int), eval_rows.bdt_score, sample_weight=eval_rows.bdt_base_fit_weight)
    model_dir = out / "model"; model_dir.mkdir(parents=True, exist_ok=True)
    with (model_dir / "bdt_model.pkl").open("wb") as handle:
        pickle.dump(model, handle)
    metadata = {
        "classifier": "sklearn.ensemble.HistGradientBoostingClassifier",
        "deterministic_seed": SEED, "features": BDT_FEATURES,
        "mass_used_as_input": False, "hyperparameters": model.get_params(),
        "training_partition": "train", "evaluation_partition": "test",
        "training_rows_with_positive_fit_weight": len(fit), "test_weighted_roc_auc": auc,
        "training_stage_duration_seconds": duration, "model_path": "model/bdt_model.pkl",
        "negative_weight_policy_for_fit": "nonpositive signed physical weights get zero bdt_fit_weight; signed values are retained for yields",
    }
    write_json(model_dir / "training_metadata.json", metadata)
    training.to_csv(model_dir / "training_sample.csv", index=False)
    return model, metadata


def optimize_and_assign(df: pd.DataFrame, training: pd.DataFrame, out: Path) -> dict[str, Any]:
    opt = training[(training.stable_partition == "validation") & training.bdt_score.notna()].copy()
    # Undo the validation sampling fraction so optimizer yields represent the full analysis sample.
    opt["optimization_weight"] = opt.bdt_physical_weight_signed / PARTITION_FRACTIONS[1]
    thresholds = optimize_bdt_boundaries(opt, {
        "minimum_relative_improvement": 0.05, "max_categories": 4,
        "minimum_background": 0.8, "candidate_quantiles": 100,
    })
    (out / "optimization").mkdir(parents=True, exist_ok=True)
    write_json(out / "optimization" / "thresholds.json", thresholds)
    write_json(out / "optimization" / "accepted_splits.json", {
        "accepted_boundary_sequence": thresholds["accepted_splits"],
        "stopping_rule": "accept an added boundary only for relative expected-significance improvement >= 5%",
        "stop_reason": thresholds["stop_reason"],
    })
    df["assigned_category_pre_retention"] = [assign_top_category(row, row.bdt_score, thresholds) for row in df.itertuples(index=False)]
    return thresholds


def component_masks(df: pd.DataFrame) -> dict[str, pd.Series]:
    sw = df.m_gammagamma.between(*SIGNAL_WINDOW, inclusive="both")
    sb = df.m_gammagamma.between(105, 120, inclusive="left") | df.m_gammagamma.between(130, 160, inclusive="right")
    ti_mc = (~df.is_data) & df.diphoton_is_ti
    return {
        "ttH_tH_signal": ti_mc & df.process.isin(SIGNAL_PROCESSES) & sw,
        "resonant_Higgs_background": ti_mc & ~df.process.isin(SIGNAL_PROCESSES) & sw,
        "NTI_continuum_proxy": df.is_data & df.diphoton_is_nti & sb,
    }


def summarize_categories(df: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    masks = component_masks(df)
    all_names = CATEGORY_ORDER + ["unassigned"]
    pre = df.assigned_category_pre_retention
    retention: dict[str, Any] = {}
    for cat in CATEGORY_ORDER:
        b_res = float(df.loc[(pre == cat) & masks["resonant_Higgs_background"], "sm_normalized_mc_weight_36fb"].sum())
        b_nti = float(df.loc[(pre == cat) & masks["NTI_continuum_proxy"], "nti_continuum_proxy_weight"].sum())
        background = b_res + b_nti
        keep = background >= 0.8
        retention[cat] = {"background_36fb": background, "minimum_required": 0.8,
                          "kept": keep, "action": "kept" if keep else "merged_into_unassigned"}
    df["assigned_category"] = pre
    for cat, info in retention.items():
        if not info["kept"]:
            df.loc[df.assigned_category == cat, "assigned_category"] = "unassigned"
    rows = []
    component_json: dict[str, Any] = {}
    for cat in all_names:
        cm = df.assigned_category == cat
        s = float(df.loc[cm & masks["ttH_tH_signal"], "sm_normalized_mc_weight_36fb"].sum())
        r = float(df.loc[cm & masks["resonant_Higgs_background"], "sm_normalized_mc_weight_36fb"].sum())
        n = float(df.loc[cm & masks["NTI_continuum_proxy"], "nti_continuum_proxy_weight"].sum())
        b = r + n
        z = asimov_z(s, b)
        row = {"category": cat, "kept": cat == "unassigned" or retention.get(cat, {}).get("kept", False),
               "signal_ttH_tH": s, "resonant_higgs_background": r, "nti_continuum_proxy": n,
               "total_background": b, "total_model_yield": s + b,
               "S_over_B": s / b if b > 0 else None, "S_over_sqrt_B": s / math.sqrt(b) if b > 0 else None,
               "expected_counting_significance": z}
        rows.append(row); component_json[cat] = row
    summary = pd.DataFrame(rows)
    kept_physics = [c for c in CATEGORY_ORDER if retention[c]["kept"]]
    combined_z = math.sqrt(sum(float(summary.loc[summary.category == c, "expected_counting_significance"].iloc[0]) ** 2 for c in kept_physics))
    cat_dir = out / "categorization"; cat_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(cat_dir / "category_summary.csv", index=False)
    write_json(cat_dir / "category_component_yields.json", {"categories": component_json, "combined_expected_counting_significance_kept_physics_categories": combined_z})
    write_json(cat_dir / "category_retention.json", {"rule": "retain non-catch-all physics category only if expected background >= 0.8 in 123-127 GeV", "categories": retention})
    write_json(out / "category_yields_36fb.json", {"integrated_luminosity_fb": LUMI_FB, "weight_column": "significance_model_weight_36fb", "categories": component_json, "combined_expected_counting_significance": combined_z})
    write_json(cat_dir / "categorization_manifest.json", {
        "priority_order": CATEGORY_ORDER, "final_category_order": all_names,
        "kept_workspace_categories": kept_physics, "unassigned_is_catch_all": True,
        "th_categories_evaluated_after_bdt_failure": True,
        "th_cut": "N_leptons=0, exactly 4 central jets, exactly 1 or >=2 b-tags",
        "signal_window_GeV": list(SIGNAL_WINDOW), "integrated_luminosity_fb": LUMI_FB,
        "classifier_fit_weight_used_for_yields": False,
    })
    return summary, {"retention": retention, "kept_physics": kept_physics, "combined_counting_z": combined_z}


def shape_comparison(training: pd.DataFrame, out: Path) -> None:
    edges = np.linspace(0.0, 1.0, 21)
    components = {
        "ttH_tH_signal": training.training_role == "ttH_tH_signal",
        "ggH_resonant_background": training.training_role == "ggH_resonant_background",
        "NTI_continuum_background": training.training_role == "NTI_continuum_background",
    }
    payload = {"bin_edges": edges, "normalization": "each component normalized to unit area", "components": {}}
    plt.figure(figsize=(8, 5))
    for name, mask in components.items():
        x = training[mask & (training.stable_partition == "test") & training.bdt_score.notna()]
        w = x.bdt_physical_weight_signed.to_numpy(float)
        # Shape normalization uses nonnegative display weights; signed totals are recorded separately.
        w_display = np.clip(w, 0, None)
        raw, _ = np.histogram(x.bdt_score, bins=edges, weights=w_display)
        norm = raw / raw.sum() if raw.sum() > 0 else raw
        payload["components"][name] = {"normalized_bin_contents": norm, "component_total_before_shape_normalization": float(w_display.sum()), "signed_component_total": float(w.sum()), "entries": len(x)}
        plt.stairs(norm, edges, label=name, linewidth=1.8)
    plt.xlabel("BDT score"); plt.ylabel("Unit-area bin content"); plt.xlim(0, 1); plt.legend(fontsize=8)
    savefig(out / "plots" / "score_by_component_shape_bdt_v1")
    write_json(out / "plots" / "score_by_component_histograms.json", payload)


def categorization_histograms_and_plots(df: pd.DataFrame, summary: pd.DataFrame, thresholds: dict[str, Any], out: Path) -> None:
    cat_dir = out / "categorization"; plot_dir = cat_dir / "plots"; hist_dir = cat_dir / "histograms"
    plot_dir.mkdir(parents=True, exist_ok=True); hist_dir.mkdir(parents=True, exist_ok=True)
    masks = component_masks(df)
    score_edges = np.linspace(0, 1, 21)
    score_payload = {"binning": "explicit", "components": {}}
    colors = {"ttH_tH_signal": "tab:red", "resonant_Higgs_background": "tab:blue", "NTI_continuum_proxy": "tab:green"}
    plt.figure(figsize=(8, 5))
    for name, mask in masks.items():
        x = df[mask & df.bdt_score.notna()]
        weight_col = "nti_continuum_proxy_weight" if name == "NTI_continuum_proxy" else "sm_normalized_mc_weight_36fb"
        payload = hist_payload(x.bdt_score.to_numpy(), x[weight_col].to_numpy(), score_edges)
        score_payload["components"][name] = payload
        plt.stairs(payload["bin_contents"], score_edges, label=name, color=colors[name], linewidth=1.8)
    plt.xlabel("BDT score"); plt.ylabel("Expected yield / bin (36 fb$^{-1}$ model)"); plt.legend(fontsize=8)
    savefig(plot_dir / "bdt_score_model_components_36fb_v1")
    plt.figure(figsize=(8, 5))
    for name, payload in score_payload["components"].items():
        plt.stairs(payload["bin_contents"], score_edges, label=name, color=colors[name], linewidth=1.8)
    boundaries = [thresholds["minimum"]] + thresholds["split_boundaries_desc"]
    for boundary in boundaries:
        plt.axvline(boundary, color="black", linestyle="--", linewidth=1)
    plt.xlabel("BDT score"); plt.ylabel("Expected yield / bin (36 fb$^{-1}$ model)"); plt.legend(fontsize=8)
    savefig(plot_dir / "bdt_score_model_components_with_boundaries_36fb_v1")
    score_payload["category_boundaries"] = boundaries
    write_json(hist_dir / "bdt_score_model_component_histograms.json", score_payload)

    plot_summary = summary[summary.category != "unassigned"]
    x = np.arange(len(plot_summary))
    plt.figure(figsize=(10, 5)); plt.bar(x, plot_summary.total_background, label="background"); plt.bar(x, plot_summary.signal_ttH_tH, bottom=plot_summary.total_background, label="ttH+tH")
    plt.xticks(x, plot_summary.category, rotation=30, ha="right"); plt.ylabel("Expected yield (36 fb$^{-1}$)"); plt.legend()
    savefig(plot_dir / "category_expected_yields_36fb_v1")
    plt.figure(figsize=(10, 5)); plt.bar(x, plot_summary.expected_counting_significance); plt.xticks(x, plot_summary.category, rotation=30, ha="right"); plt.ylabel("Expected counting Z")
    savefig(plot_dir / "category_expected_counting_z_36fb_v1")

    mgg_edges = np.arange(105.0, 161.0, 1.0)
    categories = CATEGORY_ORDER + ["unassigned"]
    mgg_payload: dict[str, Any] = {"bin_edges": mgg_edges, "categories": {}, "observed_TI_signal_window_included": False}
    fig, axes = plt.subplots(4, 2, figsize=(13, 14), sharex=True)
    for ax, cat in zip(axes.flat, categories):
        mgg_payload["categories"][cat] = {}
        for name in ["ttH_tH_signal", "resonant_Higgs_background", "NTI_continuum_proxy"]:
            if name == "NTI_continuum_proxy":
                base = df.is_data & df.diphoton_is_nti
                weight_col = "nti_control_shape_weight"
            elif name == "ttH_tH_signal":
                base = (~df.is_data) & df.diphoton_is_ti & df.process.isin(SIGNAL_PROCESSES)
                weight_col = "sm_normalized_mc_weight_36fb"
            else:
                base = (~df.is_data) & df.diphoton_is_ti & ~df.process.isin(SIGNAL_PROCESSES)
                weight_col = "sm_normalized_mc_weight_36fb"
            sub = df[(df.assigned_category == cat) & base]
            hp = hist_payload(sub.m_gammagamma.to_numpy(), sub[weight_col].to_numpy(), mgg_edges)
            if name == "NTI_continuum_proxy":
                hp["control_shape_policy"] = "all NTI masses retained, including 120-130 GeV; scaled by SF1*SF2"
            mgg_payload["categories"][cat][name] = hp
            ax.stairs(hp["bin_contents"], mgg_edges, label=name, color=colors[name], linewidth=1.2)
        ax.set_title(cat); ax.set_ylabel("model yield"); ax.axvspan(123, 127, color="gray", alpha=.12)
    axes.flat[-1].axis("off"); axes.flat[0].legend(fontsize=7); axes.flat[-2].set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
    savefig(plot_dir / "category_mgg_control_shapes_36fb_v1")
    write_json(hist_dir / "category_mgg_control_histograms.json", mgg_payload)


def weighted_gaussian_parameters(frame: pd.DataFrame, weight_col: str) -> tuple[float, float]:
    if frame.empty:
        return 125.0, 1.8
    x = frame.m_gammagamma.to_numpy(float)
    w = np.clip(frame[weight_col].to_numpy(float), 0, None)
    if w.sum() <= 0:
        w = np.ones_like(x)
    mean = float(np.average(x, weights=w))
    sigma = float(np.sqrt(max(np.average((x - mean) ** 2, weights=w), 0.25)))
    return float(np.clip(mean, 123.5, 126.5)), float(np.clip(sigma, 0.7, 3.5))


def gaussian_probs(edges: np.ndarray, mean: float, sigma: float) -> np.ndarray:
    from math import erf, sqrt
    cdf = np.asarray([0.5 * (1 + erf((x - mean) / (sigma * sqrt(2)))) for x in edges])
    p = np.diff(cdf)
    return p / p.sum() if p.sum() > 0 else np.ones(len(edges) - 1) / (len(edges) - 1)


def exponential_probs(edges: np.ndarray, tau: float) -> np.ndarray:
    if abs(tau) < 1e-10:
        p = np.diff(edges)
    else:
        p = np.diff(np.exp(tau * edges))
        if tau < 0:
            p = -p
    p = np.clip(p, 0, None)
    return p / p.sum() if p.sum() > 0 else np.ones(len(edges) - 1) / (len(edges) - 1)


def sideband_fraction(tau: float) -> float:
    edges_full = np.linspace(105, 160, 1101)
    p = exponential_probs(edges_full, tau)
    centers = 0.5 * (edges_full[:-1] + edges_full[1:])
    return float(p[(centers < 120) | (centers > 130)].sum())


def build_roofit_workspace(df: pd.DataFrame, kept_categories: list[str], out: Path) -> dict[str, Any]:
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
    fit_dir = out / "fit" / "FIT1"; plot_dir = fit_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    root_path = fit_dir / "workspace.root"
    m = ROOT.RooRealVar("m_gammagamma", "m_{#gamma#gamma}", 105.0, 160.0, "GeV")
    m.setRange("lowSB", 105.0, 120.0); m.setRange("highSB", 130.0, 160.0)
    channel = ROOT.RooCategory("hadronic_category", "hadronic_category")
    for cat in kept_categories:
        channel.defineType(cat)
    mu = ROOT.RooRealVar("mu", "shared ttH+tH signal strength", 1.0, 0.0, 8.0)
    sim = ROOT.RooSimultaneous("combined_model", "combined hadronic model", channel)
    refs: list[Any] = [m, channel, mu, sim]
    category_info: dict[str, Any] = {}
    model_refs: dict[str, Any] = {}
    sideband_plot_map: dict[str, Any] = {}
    fig_comb, axes_comb = plt.subplots(max(1, math.ceil(len(kept_categories) / 2)), 2, figsize=(12, 4 * max(1, math.ceil(len(kept_categories) / 2))), squeeze=False)
    mass_edges = np.linspace(105, 160, 56)
    centers = 0.5 * (mass_edges[:-1] + mass_edges[1:])
    for ax, cat in zip(axes_comb.flat, kept_categories):
        cat_mask = df.assigned_category == cat
        ti_sb = df[cat_mask & df.is_data & df.diphoton_is_ti & (((df.m_gammagamma >= 105) & (df.m_gammagamma < 120)) | ((df.m_gammagamma > 130) & (df.m_gammagamma <= 160)))]
        h = ROOT.TH1D(f"h_sideband_{cat}", "", 55, 105, 160)
        h.SetDirectory(0)
        for value in ti_sb.m_gammagamma:
            h.Fill(float(value))
        dh = ROOT.RooDataHist(f"sideband_data_{cat}", f"TI sideband data {cat}", ROOT.RooArgList(m), h)
        tau = ROOT.RooRealVar(f"tau_{cat}", f"continuum slope {cat}", -0.02, -0.20, 0.05)
        continuum = ROOT.RooExponential(f"continuum_pdf_{cat}", f"continuum {cat}", m, tau)
        sb_result = continuum.fitTo(dh, ROOT.RooFit.Range("lowSB,highSB"), ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.SumW2Error(False))
        tau_value = float(tau.getVal())
        fraction = max(sideband_fraction(tau_value), 1e-6)
        full_continuum = float(len(ti_sb) / fraction)

        signal_shape = df[cat_mask & (~df.is_data) & df.diphoton_is_ti & df.process.isin(SIGNAL_PROCESSES)]
        resonant_shape = df[cat_mask & (~df.is_data) & df.diphoton_is_ti & ~df.process.isin(SIGNAL_PROCESSES)]
        sw = df.m_gammagamma.between(*SIGNAL_WINDOW, inclusive="both")
        # RooFit covers the full 105--160 GeV range, so its Gaussian component
        # normalizations are the full-range TI MC yields (the category counting
        # summary separately and intentionally uses the 123--127 GeV model).
        signal_yield = max(float(signal_shape.sm_normalized_mc_weight_36fb.sum()), 0.0)
        resonant_yield = max(float(resonant_shape.sm_normalized_mc_weight_36fb.sum()), 0.0)
        sig_mean_v, sig_sigma_v = weighted_gaussian_parameters(signal_shape, "sm_normalized_mc_weight_36fb")
        res_mean_v, res_sigma_v = weighted_gaussian_parameters(resonant_shape, "sm_normalized_mc_weight_36fb")
        sig_mean = ROOT.RooRealVar(f"signal_mean_{cat}", "", sig_mean_v); sig_mean.setConstant(True)
        sig_sigma = ROOT.RooRealVar(f"signal_sigma_{cat}", "", sig_sigma_v, 0.1, 10.0); sig_sigma.setConstant(True)
        res_mean = ROOT.RooRealVar(f"resonant_mean_{cat}", "", res_mean_v); res_mean.setConstant(True)
        res_sigma = ROOT.RooRealVar(f"resonant_sigma_{cat}", "", res_sigma_v, 0.1, 10.0); res_sigma.setConstant(True)
        sig_pdf = ROOT.RooGaussian(f"signal_pdf_{cat}", "ttH+tH signal", m, sig_mean, sig_sigma)
        res_pdf = ROOT.RooGaussian(f"resonant_higgs_pdf_{cat}", "fixed non-top Higgs", m, res_mean, res_sigma)
        sig_nom = ROOT.RooRealVar(f"signal_yield_nominal_{cat}", "", signal_yield); sig_nom.setConstant(True)
        sig_yield_formula = ROOT.RooFormulaVar(f"signal_yield_{cat}", "@0*@1", ROOT.RooArgList(mu, sig_nom))
        res_norm = ROOT.RooRealVar(f"resonant_yield_{cat}", "", resonant_yield); res_norm.setConstant(True)
        cont_norm = ROOT.RooRealVar(f"continuum_yield_{cat}", "", max(full_continuum, 0.01), 0.0, max(10 * full_continuum + 20, 50.0))
        model = ROOT.RooAddPdf(f"model_{cat}", f"model {cat}", ROOT.RooArgList(sig_pdf, res_pdf, continuum), ROOT.RooArgList(sig_yield_formula, res_norm, cont_norm))
        sim.addPdf(model, cat)
        refs.extend([h, dh, tau, continuum, sb_result, sig_mean, sig_sigma, res_mean, res_sigma, sig_pdf, res_pdf, sig_nom, sig_yield_formula, res_norm, cont_norm, model])
        model_refs[cat] = {"tau": tau, "cont_norm": cont_norm, "model": model, "signal_yield": signal_yield,
                           "resonant_yield": resonant_yield, "sig_pars": (sig_mean_v, sig_sigma_v), "res_pars": (res_mean_v, res_sigma_v)}
        category_info[cat] = {
            "observed_TI_sideband_entries": len(ti_sb), "observed_TI_signal_window_entries": "BLINDED_NOT_COUNTED",
            "sideband_fit_status": int(sb_result.status()), "sideband_fit_covariance_quality": int(sb_result.covQual()),
            "continuum_tau": tau_value, "continuum_tau_error": float(tau.getError()),
            "sideband_fraction_of_full_range": fraction, "fitted_full_range_continuum_yield": full_continuum,
            "signal_yield_36fb_in_105_160": signal_yield, "resonant_higgs_yield_36fb_in_105_160": resonant_yield,
            "signal_shape": {"pdf": "Gaussian", "mean": sig_mean_v, "sigma": sig_sigma_v},
            "resonant_shape": {"pdf": "Gaussian", "mean": res_mean_v, "sigma": res_sigma_v},
        }
        counts, _ = np.histogram(ti_sb.m_gammagamma, bins=mass_edges)
        curve = full_continuum * exponential_probs(mass_edges, tau_value)
        for target_ax in [ax]:
            target_ax.errorbar(centers, counts, yerr=np.sqrt(counts), fmt="o", ms=3, label="observed TI sidebands")
            target_ax.plot(centers, curve, label="fitted continuum PDF")
            target_ax.axvspan(123, 127, color="gray", alpha=.3, label="blinded 125±2 GeV")
            target_ax.set_title(cat); target_ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]"); target_ax.set_ylabel("events / 1 GeV")
        fig_one, ax_one = plt.subplots(figsize=(8, 5))
        ax_one.errorbar(centers, counts, yerr=np.sqrt(counts), fmt="o", ms=3, label="observed TI sidebands")
        ax_one.plot(centers, curve, label="fitted continuum PDF"); ax_one.axvspan(123, 127, color="gray", alpha=.3, label="blinded signal window")
        ax_one.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]"); ax_one.set_ylabel("events / 1 GeV"); ax_one.set_title(cat); ax_one.legend()
        one_base = plot_dir / f"sideband_background_fit_{cat}"
        fig_one.tight_layout(); fig_one.savefig(one_base.with_suffix(".png"), dpi=170); fig_one.savefig(one_base.with_suffix(".pdf")); plt.close(fig_one)
        sideband_plot_map[cat] = {"png": str(one_base.relative_to(out).with_suffix(".png")), "pdf": str(one_base.relative_to(out).with_suffix(".pdf")), "explicit_mass_bin_edges": mass_edges}
    for ax in list(axes_comb.flat)[len(kept_categories):]:
        ax.axis("off")
    if kept_categories:
        axes_comb.flat[0].legend(fontsize=7)
    fig_comb.tight_layout(); fig_comb.savefig(plot_dir / "sidebands_background_fit.png", dpi=170); fig_comb.savefig(plot_dir / "sidebands_background_fit.pdf"); plt.close(fig_comb)

    weight_var = ROOT.RooRealVar("asimov_weight", "asimov_weight", 0.0, 1e9)
    obs = ROOT.RooArgSet(m, channel, weight_var)
    asimov = ROOT.RooDataSet("asimov_sb_mu1", "S+B Asimov data, mu_gen=1", obs, ROOT.RooFit.WeightVar(weight_var))
    expected_by_cat: dict[str, np.ndarray] = {}
    for cat in kept_categories:
        info = model_refs[cat]
        sig = info["signal_yield"] * gaussian_probs(mass_edges, *info["sig_pars"])
        res = info["resonant_yield"] * gaussian_probs(mass_edges, *info["res_pars"])
        cont = float(info["cont_norm"].getVal()) * exponential_probs(mass_edges, float(info["tau"].getVal()))
        expected = sig + res + cont
        expected_by_cat[cat] = expected
        channel.setLabel(cat)
        for center, value in zip(centers, expected):
            m.setVal(float(center)); weight_var.setVal(float(value)); asimov.add(obs, float(value))
    refs.extend([weight_var, obs, asimov])
    mu.setVal(1.0); mu.setConstant(False)
    fit_free = sim.fitTo(asimov, ROOT.RooFit.Save(True), ROOT.RooFit.Extended(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.SumW2Error(False))
    free = {"mu_hat": float(mu.getVal()), "mu_uncertainty": float(mu.getError()), "status": int(fit_free.status()), "covariance_quality": int(fit_free.covQual()), "min_nll": float(fit_free.minNll())}
    free_nuisance_values = {cat: {"tau": float(model_refs[cat]["tau"].getVal()), "continuum_yield": float(model_refs[cat]["cont_norm"].getVal())} for cat in kept_categories}
    mu_hat_for_q0 = free["mu_hat"]
    mu.setVal(0.0); mu.setConstant(True)
    fit_null = sim.fitTo(asimov, ROOT.RooFit.Save(True), ROOT.RooFit.Extended(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.SumW2Error(False))
    null = {"mu": 0.0, "status": int(fit_null.status()), "covariance_quality": int(fit_null.covQual()), "min_nll": float(fit_null.minNll())}
    q0 = max(2 * (null["min_nll"] - free["min_nll"]), 0.0) if mu_hat_for_q0 >= 0 else 0.0
    expected_z = math.sqrt(q0)
    mu.setConstant(False); mu.setVal(free["mu_hat"])
    for cat in kept_categories:
        model_refs[cat]["tau"].setVal(free_nuisance_values[cat]["tau"])
        model_refs[cat]["cont_norm"].setVal(free_nuisance_values[cat]["continuum_yield"])
    refs.extend([fit_free, fit_null])
    ws = ROOT.RooWorkspace("tth_diphoton_combined", "combined hadronic ttH/tH diphoton workspace")
    importer = getattr(ws, "import")
    importer(sim); importer(asimov); importer(fit_free, "fit_result_free_mu"); importer(fit_null, "fit_result_mu0")
    ws.writeToFile(str(root_path), True)

    # Full-range aggregate Asimov plot with the post-fit free-mu model expectation.
    plt.figure(figsize=(9, 5))
    aggregate = sum(expected_by_cat.values()) if expected_by_cat else np.zeros(len(centers))
    plt.errorbar(centers, aggregate, yerr=np.sqrt(np.maximum(aggregate, 0)), fmt="o", ms=3, label=r"S+B Asimov data, $\mu_{gen}=1$")
    postfit = np.zeros_like(aggregate)
    for cat in kept_categories:
        info = model_refs[cat]
        postfit += (free["mu_hat"] * info["signal_yield"] * gaussian_probs(mass_edges, *info["sig_pars"])
                    + info["resonant_yield"] * gaussian_probs(mass_edges, *info["res_pars"])
                    + float(info["cont_norm"].getVal()) * exponential_probs(mass_edges, float(info["tau"].getVal())))
    plt.step(mass_edges[:-1], postfit, where="post", label=r"free-$\mu$ simultaneous fit")
    plt.xlabel(r"$m_{\gamma\gamma}$ [GeV]"); plt.ylabel("Combined expected events / 1 GeV"); plt.legend()
    savefig(plot_dir / "asimov_sb_fit")

    backend = {"backend": "ROOT/PyROOT/RooFit", "ROOT_version": ROOT.gROOT.GetVersion(), "workspace": "fit/FIT1/workspace.root"}
    significance = {"kind": "expected_discovery_significance", "asimov_mu_gen": 1.0, "observed_significance": "BLOCKED_BLINDED",
                    "free_mu_fit": free, "mu0_fit": null, "q0": q0, "expected_Z": expected_z}
    construction = {"strategy": "signal-plus-background Asimov; free-mu and mu=0 extended simultaneous fits",
                    "shared_parameter": "mu", "categories": kept_categories,
                    "signal": "ttH+tH TI MC full-range shape and 36 fb^-1 normalization",
                    "fixed_resonant_background": "non-top Higgs TI MC",
                    "floating_continuum": "per-category exponential shape and normalization initialized by observed TI sidebands",
                    "continuum_generation": "fitted TI-sideband PDF extrapolated to 105-160 GeV", "category_details": category_info}
    write_json(fit_dir / "backend.json", backend)
    write_json(fit_dir / "results.json", {"fits": {"free_mu": free, "mu0": null}, "categories": category_info})
    write_json(fit_dir / "significance_asimov.json", significance)
    write_json(fit_dir / "significance.json", significance)
    write_json(fit_dir / "significance_asimov_construction.json", construction)
    write_json(fit_dir / "significance_asimov_plot_payload.json", {"bin_edges": mass_edges, "asimov_combined_bin_contents": aggregate, "postfit_combined_bin_contents": postfit})
    write_json(fit_dir / "sideband_fit_plots.json", {"per_category": sideband_plot_map, "combined": {"png": "fit/FIT1/plots/sidebands_background_fit.png", "pdf": "fit/FIT1/plots/sidebands_background_fit.pdf"}})
    write_json(fit_dir / "background_pdf_choice.json", {"selected": "RooExponential", "reason": "deterministic smooth one-parameter continuum model fit to TI data sidebands per category"})
    write_json(fit_dir / "background_pdf_scan.json", {"candidates": [{"pdf": "RooExponential", "selected": True}], "category_fit_results": category_info})
    write_json(fit_dir / "background_template_selection.json", {"source": "observed TI GamGam data sidebands only", "ranges_GeV": [[105, 120], [130, 160]], "NTI_proxy_used": False})
    write_json(fit_dir / "signal_pdf.json", {c: category_info[c]["signal_shape"] for c in kept_categories})
    write_json(fit_dir / "resonant_higgs_pdf.json", {c: category_info[c]["resonant_shape"] for c in kept_categories})
    workspace_manifest = {**backend, "categories": kept_categories, "leptonic_categories_excluded": True,
                          "shared_signal_strength": "mu", "observed_TI_125_plusminus_2_blinded": True,
                          "expected_Z": expected_z, "q0": q0}
    write_json(out / "workspace_manifest.json", workspace_manifest)
    write_json(out / "fit" / "workspace.json", construction)
    return {"backend": backend, "significance": significance, "construction": construction}


def write_tables_and_manifests(df: pd.DataFrame, training: pd.DataFrame, model_metadata: dict[str, Any], out: Path) -> None:
    sideband = ((df.m_gammagamma >= 105) & (df.m_gammagamma < 120)) | ((df.m_gammagamma > 130) & (df.m_gammagamma <= 160))
    window = df.m_gammagamma.between(*SIGNAL_WINDOW, inclusive="both")
    signal_role = (~df.is_data) & df.process.isin(SIGNAL_PROCESSES)
    ggh_role = (df.process == "ggH") & df.diphoton_is_ti & window
    nti_role = df.is_data & df.diphoton_is_nti & sideband
    df["training_role"] = "inference_only"
    df.loc[signal_role, "training_role"] = "ttH_tH_signal"
    df.loc[ggh_role, "training_role"] = "ggH_resonant_background"
    df.loc[nti_role, "training_role"] = "NTI_continuum_background"
    df["bdt_physical_weight_signed"] = 0.0
    df.loc[signal_role | ggh_role, "bdt_physical_weight_signed"] = df.loc[signal_role | ggh_role, "sm_normalized_mc_weight_36fb"]
    df.loc[nti_role, "bdt_physical_weight_signed"] = df.loc[nti_role, "nti_continuum_proxy_weight"]
    signal_factor = float(training.loc[training.is_signal, "class_balance_factor"].iloc[0])
    background_factor = float(training.loc[~training.is_signal, "class_balance_factor"].iloc[0])
    df["bdt_fit_weight"] = df.bdt_physical_weight_signed.clip(lower=0.0) * np.where(signal_role, signal_factor, background_factor)
    df.loc[df.training_role == "inference_only", "bdt_fit_weight"] = 0.0
    df["observed_ti_signal_window_blinded"] = False
    df["observed_ti_125_plusminus2_blinding_policy"] = True
    export = df.sort_values("event_id").reset_index(drop=True)
    export.to_csv(out / "preselected_events.csv", index=False)
    export.to_csv(out / "predictions.csv", index=False)
    feature_columns = ["event_id", "process", "stable_partition", *BDT_FEATURES, "m_gammagamma", "bdt_score", "assigned_category"]
    export[feature_columns].to_csv(out / "hadronic_features.csv", index=False)
    inference_dir = out / "inference"; inference_dir.mkdir(parents=True, exist_ok=True)
    export.to_csv(inference_dir / "events_with_bdt_scores.csv", index=False)
    finite = np.isfinite(export.bdt_score)
    manifest = {
        "selected_rows": len(export), "hadronic_selected_rows": int(export.hadronic_preselection.sum()),
        "scored_rows": int(finite.sum()), "unscored_rows": int((~finite).sum()),
        "score_range": [float(export.loc[finite, "bdt_score"].min()), float(export.loc[finite, "bdt_score"].max())] if finite.any() else None,
        "score_contract": "finite [0,1] for every exported hadronic row", "features": BDT_FEATURES,
        "model_path": model_metadata["model_path"], "event_identifier": "process:channelNumber:runNumber:eventNumber",
        "stable_partition": {"algorithm": "SHA-256", "seed": SEED, "fractions": dict(zip(["train", "validation", "test"], PARTITION_FRACTIONS))},
        "categorical_code_maps": {}, "table": "inference/events_with_bdt_scores.csv",
        "blinding": "observed TI data in 120-130 GeV are omitted before analysis-row construction and are not counted",
    }
    write_json(inference_dir / "inference_manifest.json", manifest)


def write_report(out: Path, config: dict[str, Any], summaries: list[dict[str, Any]], factors: dict[str, float],
                 model_metadata: dict[str, Any], thresholds: dict[str, Any], summary: pd.DataFrame,
                 category_info: dict[str, Any], workspace: dict[str, Any]) -> None:
    count_table = "\n".join(
        f"| {x['process']} | {x['input_entries']} | {x['rows_written']} | {x['signed_weight_sum_36fb']:.4g} |"
        for x in summaries
    )
    category_table = "\n".join(
        f"| {r.category} | {'yes' if r.kept else 'no'} | {r.signal_ttH_tH:.4g} | {r.total_background:.4g} | {r.expected_counting_significance:.3g} |"
        for r in summary.itertuples(index=False)
    )
    sideband_images = "\n".join(
        f"![{cat} TI sideband fit](fit/FIT1/plots/sideband_background_fit_{cat}.png)" for cat in category_info["kept_physics"]
    )
    accepted = ", ".join(
        f"{x['boundary']:.5f}" + (" (initial minimum)" if x["kind"] == "minimum_score" else f" ({100*x['relative_improvement']:.1f}% improvement)")
        for x in thresholds["accepted_splits"]
    )
    report = rf"""# Hadronic top-associated diphoton BDT categorization

## Introduction

This is an end-to-end, blinded starting point for hadronic top-associated $H\to\gamma\gamma$ categorization. It trains a deterministic five-variable BDT, constructs a 36 fb$^{{-1}}$ expected-yield model, and builds a combined PyROOT/RooFit workspace. Leptonic categories are out of scope because reconstructed forward jets are unavailable.

## Data and Monte Carlo Samples

The run reads the external GamGam directory `{config['input_root']}` through the `TB_HYY_INPUTS` contract (with `/data/GamGam` as the resolved fallback). Inputs are not copied. Only nominal Higgs MC (`ggH`, `VBF`, `WH`, `ZH`, `ggZH`, `ttH`, `tH`) and observed data are processed. Sherpa `yy`, prompt-diphoton continuum MC, and all other non-Higgs MC are excluded. The run was **{config['row_policy']}**.

| process | input entries | selected analysis rows | signed MC yield at 36 fb$^{{-1}}$ |
|---|---:|---:|---:|
{count_table}

## Object Definition and Event Selection

Photons require $p_T>25$ GeV and $|\eta|<2.37$, excluding $1.37<|\eta|<1.52$. Tight ID and isolation are deliberately **not** required for preselection. The two leading accepted photons form the candidate and $m_{{\gamma\gamma}}$ is retained only for bookkeeping. Electrons and muons require $p_T>10$ GeV with no ID or isolation cut. Jets require $p_T>25$ GeV; central means $|\eta|\le2.5$, forward means $|\eta|>2.5$, and b-tagged means `jet_btag_quantile >= 4`.

The required channel has zero selected leptons, at least three selected jets, and at least one b-jet. No leptonic bookkeeping rows are retained. Stable SHA-256 event identifiers define 60/20/20 train/validation/test partitions.

![Preselection mass](plots/preselection_mass.png)

## Overview of the Analysis Strategy

The BDT uses exactly `{', '.join(BDT_FEATURES)}`. It never uses $m_{{\gamma\gamma}}$. The classifier is `{model_metadata['classifier']}` with learning rate 0.055, 180 boosting iterations, at most 15 leaves, depth 4, minimum 20 samples per leaf, L2 regularization 1, and seed {SEED}. Training took {model_metadata['training_stage_duration_seconds']:.3f} s.

Signal is SM-normalized `ttH+tH`. Background is resonant TI `ggH` in 123–127 GeV plus NTI data from 105–120 and 130–160 GeV. TI means both photons pass tight ID and tight isolation; NTI means at least one fails either condition. Class balancing is applied only after physical signal and background mixture weights are constructed. Nonpositive signed MC weights retain their signed yield value and receive zero nonnegative classifier-fit weight.

![Equal-area BDT component shapes](plots/score_by_component_shape_bdt_v1.png)

## Signal and Control Regions

The NTI normalization is `SF1 = TI_sideband/NTI_sideband = {factors['SF1']:.6g}`, `SF2 = NTI_123-127/NTI_sideband = {factors['SF2']:.6g}`, and `SF1*SF2 = {factors['SF1_times_SF2']:.6g}`. Nominal observed TI data in 120–130 GeV are removed before analysis-row creation, never counted or scored in exported tables, and remain blinded. NTI entries in 120–130 GeV remain available for control-shape distributions. Observed TI sideband counts are kept separate from expected model yields.

## Cut Flow

Raw and weighted cut-flow details, including signed and absolute MC weights, are in [cutflow.json](cutflow.json) and [preselection_summary.json](preselection_summary.json).

![Preselection channels](plots/preselection_channels.png)

## Distributions in Signal and Control Regions

The category model uses TI Higgs MC in 123–127 GeV plus the scaled NTI sideband proxy. MC is normalized to 36 fb$^{{-1}}$. Class-balanced `bdt_fit_weight` is never used for yields or significances; `significance_model_weight_36fb`, `nti_continuum_proxy_weight`, and `observed_data_weight` remain separate.

![BDT model components](categorization/plots/bdt_score_model_components_36fb_v1.png)

![Category mass controls](categorization/plots/category_mgg_control_shapes_36fb_v1.png)

## Categorization

The accepted boundary sequence is {accepted or 'none'}; stopping reason: `{thresholds['stop_reason']}`. A new split is retained only for at least 5% relative significance improvement. BDT regions have priority. The `tH_had_4j1b` and `tH_had_4j2b` cuts are evaluated only below the BDT minimum and require exactly four **central** jets and respectively one or at least two b-tags. Any non-catch-all category with expected background below 0.8 events is merged into `unassigned` before final summaries.

| category | kept | ttH+tH | total background | counting Z |
|---|---:|---:|---:|---:|
{category_table}

Combined quadrature counting significance over kept physics categories: **{category_info['combined_counting_z']:.4g}**.

![Expected category yields](categorization/plots/category_expected_yields_36fb_v1.png)

![Expected category significance](categorization/plots/category_expected_counting_z_36fb_v1.png)

## Systematic Uncertainties

This starting-point workspace contains no nuisance-parameter model. Signed generator weights and available pileup, photon, b-tag/JVT, and flavor-tag scale factors are propagated in nominal MC yields. Experimental and theory variations, continuum functional-form uncertainty, and finite-template uncertainties must be added before physics interpretation.

## Statistical Interpretation

The backend is ROOT/PyROOT/RooFit. A shared `mu` multiplies `ttH+tH` across all kept hadronic categories. TI top-Higgs MC defines signal; TI non-top-Higgs MC is fixed resonant background. Each category's smooth continuum is fit exclusively to observed TI 105–120 and 130–160 GeV sidebands and extrapolated across 105–160 GeV. This is distinct from the NTI categorization proxy. Signal-plus-background Asimov data use $\mu_{{gen}}=1$; a free-$\mu$ fit and $\mu=0$ fit give $\hat\mu={workspace['significance']['free_mu_fit']['mu_hat']:.4g}\pm{workspace['significance']['free_mu_fit']['mu_uncertainty']:.3g}$, $q_0={workspace['significance']['q0']:.4g}$, and expected $Z={workspace['significance']['expected_Z']:.4g}$. Observed significance is blocked unless a separate explicit unblinding step is added.

{sideband_images}

![Full-range S+B Asimov fit](fit/FIT1/plots/asimov_sb_fit.png)

## Artifact Checklist

Machine-readable selection, weighting, training, optimization, inference, category-yield, histogram, RooFit workspace, fit-result, and manifest artifacts are present under this result directory. PNG and PDF versions are supplied for every requested final plot. [run_manifest.json](run_manifest.json) records the complete artifact validation.

## Summary

The repaired pipeline completed deterministically with hadronic-only categorization, strict input scoping, uncoupled classifier/yield weights, 36 fb$^{{-1}}$ physical normalization, background-based category retention, and blinded expected RooFit significance. No observed TI signal-window count or observed significance is reported.
"""
    (out / "report.md").write_text(report)


def required_artifacts() -> list[str]:
    return [
        "config_resolved.yaml", "input_data_contract.json", "object_definition_record.json", "preselection_summary.json", "cutflow.json", "metrics.json",
        "preselected_events.csv", "predictions.csv", "hadronic_features.csv", "inference/inference_manifest.json", "inference/events_with_bdt_scores.csv",
        "category_yields_36fb.json", "categorization/categorization_manifest.json", "categorization/category_summary.csv", "categorization/category_component_yields.json",
        "categorization/category_retention.json", "categorization/histograms/category_mgg_control_histograms.json", "categorization/histograms/bdt_score_model_component_histograms.json",
        "categorization/plots/category_expected_yields_36fb_v1.png", "categorization/plots/category_expected_yields_36fb_v1.pdf",
        "categorization/plots/category_expected_counting_z_36fb_v1.png", "categorization/plots/category_expected_counting_z_36fb_v1.pdf",
        "categorization/plots/bdt_score_model_components_36fb_v1.png", "categorization/plots/bdt_score_model_components_36fb_v1.pdf",
        "categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png", "categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf",
        "categorization/plots/category_mgg_control_shapes_36fb_v1.png", "categorization/plots/category_mgg_control_shapes_36fb_v1.pdf",
        "workspace_manifest.json", "fit/workspace.json", "fit/FIT1/workspace.root", "fit/FIT1/results.json", "fit/FIT1/significance_asimov.json",
        "fit/FIT1/significance_asimov_construction.json", "fit/FIT1/significance_asimov_plot_payload.json", "fit/FIT1/sideband_fit_plots.json", "fit/FIT1/significance.json",
        "fit/FIT1/backend.json", "fit/FIT1/background_pdf_choice.json", "fit/FIT1/background_pdf_scan.json", "fit/FIT1/background_template_selection.json",
        "fit/FIT1/signal_pdf.json", "fit/FIT1/resonant_higgs_pdf.json", "fit/FIT1/plots/sidebands_background_fit.png", "fit/FIT1/plots/sidebands_background_fit.pdf",
        "fit/FIT1/plots/asimov_sb_fit.png", "fit/FIT1/plots/asimov_sb_fit.pdf", "model/training_metadata.json", "model/background_mixture_and_normalization.json",
        "model/class_balance_check.json", "model/training_sample.csv", "optimization/thresholds.json", "optimization/accepted_splits.json",
        "plots/score_by_component_shape_bdt_v1.png", "plots/score_by_component_shape_bdt_v1.pdf", "plots/score_by_component_histograms.json",
        "plots/preselection_mass.png", "plots/preselection_channels.png", "plots/preselection_processes.png", "report.md",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/root/results/tth-diphoton-bdt"))
    args = parser.parse_args()
    started = time.time(); out = args.output.resolve(); out.mkdir(parents=True, exist_ok=True)
    input_env = os.environ.get("TB_HYY_INPUTS")
    input_root = Path(input_env).resolve() if input_env else Path("/data/GamGam")
    max_text = os.environ.get("TTH_MAX_SELECTED_PER_SAMPLE")
    max_selected = int(max_text) if max_text else None
    mc_files, data_file = discover_inputs(input_root)
    config = {
        "input_root": str(input_root), "input_source": "TB_HYY_INPUTS" if input_env else "default_fallback",
        "output_root": str(out), "allowed_mc_processes": ALLOWED_PROCESSES, "observed_data": str(data_file),
        "integrated_luminosity_fb": LUMI_FB, "random_seed": SEED, "partition_fractions": dict(zip(["train", "validation", "test"], PARTITION_FRACTIONS)),
        "max_selected_per_sample": max_selected, "row_policy": f"capped at {max_selected} selected rows per sample by explicit TTH_MAX_SELECTED_PER_SAMPLE" if max_selected is not None else "uncapped (default)",
        "bdt_features": BDT_FEATURES, "blinding": "observed TI data 120-130 GeV omitted before analysis row construction",
    }
    (out / "config_resolved.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
    write_json(out / "input_data_contract.json", {
        "contract": "TB_HYY_INPUTS points to an ATLAS open-data GamGam directory containing MC/ and data/",
        "resolved_input_root": str(input_root), "environment_variable_was_set": input_env is not None,
        "root_inputs_copied_into_submission": False,
        "processed_mc": {p: str(f) for p, f in mc_files.items()}, "processed_data": [str(data_file)],
        "scope": "nominal Higgs MC and observed GamGam data only", "Sherpa_yy_excluded": True,
        "prompt_diphoton_continuum_mc_excluded": True, "other_non_Higgs_mc_excluded": True,
    })
    write_json(out / "object_definition_record.json", {
        "units": "GeV", "photons": {"pt_min": 25, "abs_eta_max": 2.37, "excluded_crack": [1.37, 1.52],
        "tight_ID_required_for_preselection": False, "isolation_required_for_preselection": False,
        "explicit_statement": "Photon tight-ID and photon isolation are not required for this preselection sample."},
        "electrons_and_muons": {"pt_min": 10, "ID_required": False, "isolation_required": False},
        "jets": {"pt_min": 25, "central": "|eta| <= 2.5", "forward": "|eta| > 2.5"},
        "b_tag": "jet_btag_quantile >= 4", "hadronic_channel": "N_leptons=0, N_jets>=3, N_bjets>=1",
        "forward_jet_note": "No reconstructed forward jets are available in the current open-data inputs; no forward-jet-dependent leptonic categorization is performed.",
    })
    frames, summaries = [], []
    for process in ALLOWED_PROCESSES:
        frame, item = read_selected(mc_files[process], process, False, max_selected); frames.append(frame); summaries.append(item)
    frame, item = read_selected(data_file, "data", True, max_selected); frames.append(frame); summaries.append(item)
    df = pd.concat(frames, ignore_index=True)
    make_preselection_outputs(df, summaries, out)
    training, factors = construct_training(df, out)
    _, model_metadata = train_and_score(df, training, out)
    thresholds = optimize_and_assign(df, training, out)
    summary, category_info = summarize_categories(df, out)
    shape_comparison(training, out)
    categorization_histograms_and_plots(df, summary, thresholds, out)
    workspace = build_roofit_workspace(df, category_info["kept_physics"], out)
    write_tables_and_manifests(df, training, model_metadata, out)
    metrics = {
        "rows": len(df), "hadronic_rows": int(df.hadronic_preselection.sum()), "all_hadronic_scores_finite": bool(np.isfinite(df.bdt_score).all()),
        "score_min": float(df.bdt_score.min()), "score_max": float(df.bdt_score.max()), "nti_scale_factors": factors,
        "training": model_metadata, "optimization": thresholds, "combined_counting_Z": category_info["combined_counting_z"],
        "roofit_expected_Z": workspace["significance"]["expected_Z"], "roofit_q0": workspace["significance"]["q0"],
        "observed_significance": "BLOCKED_BLINDED", "signed_weight_bookkeeping": True,
    }
    write_json(out / "metrics.json", metrics)
    write_report(out, config, summaries, factors, model_metadata, thresholds, summary, category_info, workspace)
    missing = [p for p in required_artifacts() if not (out / p).is_file()]
    manifest = {
        "status": "complete" if not missing else "incomplete", "started_unix": started, "finished_unix": time.time(),
        "duration_seconds": time.time() - started, "deterministic_seed": SEED, "row_policy": config["row_policy"],
        "input_scope": "nominal Higgs MC and observed data only; Sherpa yy and other continuum/non-Higgs MC excluded",
        "input_files_external": True, "required_artifacts_checked": len(required_artifacts()), "missing_required_artifacts": missing,
        "blinding": {"observed_TI_125_plusminus_2": True, "observed_significance_blocked": True, "no_blinded_count_reported": True},
        "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "uproot": uproot.__version__},
    }
    write_json(out / "run_manifest.json", manifest)
    if missing:
        raise RuntimeError(f"Missing required artifacts: {missing}")
    print(json.dumps({"status": "complete", "output": str(out), "rows": len(df), "expected_Z": workspace["significance"]["expected_Z"]}, indent=2))


if __name__ == "__main__":
    main()
