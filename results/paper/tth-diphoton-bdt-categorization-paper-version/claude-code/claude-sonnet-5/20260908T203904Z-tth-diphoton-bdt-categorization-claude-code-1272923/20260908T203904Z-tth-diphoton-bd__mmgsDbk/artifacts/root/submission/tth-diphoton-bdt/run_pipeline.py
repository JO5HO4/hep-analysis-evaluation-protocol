#!/usr/bin/env python3
"""End-to-end tth-diphoton-bdt pipeline driver.

Reads the ATLAS open-data GamGam ROOT directory (TB_HYY_INPUTS or
/data/GamGam), applies the hadronic-only preselection and BDT
categorization described in the task spec, and writes every required
artifact under RESULTS_DIR (default /root/results/tth-diphoton-bdt).
"""
import json
import math
import os
import sys
import time

import joblib
import ROOT
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import data_io
from analysis.top_categorization import (
    BDT_FEATURES, CATEGORY_ORDER, LEPTONIC_BOOKKEEPING_CATEGORY,
    assign_top_category, build_jet_features, invariant_mass,
    optimize_bdt_boundaries, stable_partition,
)
from analysis import workspace as ws_mod

RUN_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.environ.get("TTH_RESULTS_DIR", "/root/results/tth-diphoton-bdt")
INPUTS_DIR = os.environ.get("TB_HYY_INPUTS", "/data/GamGam")
MAX_PER_SAMPLE_ENV = os.environ.get("TTH_MAX_SELECTED_PER_SAMPLE")
MAX_PER_SAMPLE = int(MAX_PER_SAMPLE_ENV) if MAX_PER_SAMPLE_ENV else None


def load_config():
    with open(os.path.join(HERE, "config", "config.yaml")) as f:
        return yaml.safe_load(f)


def ensure_dirs():
    for sub in [
        "", "inference", "categorization", "categorization/histograms",
        "categorization/plots", "fit", "fit/FIT1", "fit/FIT1/plots",
        "model", "optimization", "plots",
    ]:
        os.makedirs(os.path.join(RESULTS_DIR, sub), exist_ok=True)


def out(*parts):
    return os.path.join(RESULTS_DIR, *parts)


def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=_json_default, sort_keys=False)


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, pd.Series):
        return o.tolist()
    raise TypeError(f"not JSON serializable: {type(o)}")


def write_table(df, base_path_no_ext):
    """Write parquet if pyarrow is usable, else CSV; return the path used."""
    try:
        path = base_path_no_ext + ".parquet"
        df.to_parquet(path, index=False)
        return path
    except Exception:
        path = base_path_no_ext + ".csv"
        df.to_csv(path, index=False)
        return path


# ---------------------------------------------------------------------------
# Stage 1: load + preselection bookkeeping
# ---------------------------------------------------------------------------

def stage_load_and_preselect(cfg):
    t0 = time.time()
    df, cutflows_by_process, input_manifest = data_io.load_all(
        INPUTS_DIR, max_rows_per_sample=MAX_PER_SAMPLE
    )
    load_seconds = time.time() - t0

    input_data_contract = {
        "external_input_env_var": "TB_HYY_INPUTS",
        "resolved_inputs_dir": INPUTS_DIR,
        "expected_layout": {"MC": "MC/*.root", "data": "data/*.root"},
        "root_inputs_copied_into_submission": False,
        "processed_mc_processes": input_manifest["allowed_mc_processes"],
        "processed_data_samples": ["data"],
        "excluded_by_policy": [
            "Sherpa yy continuum diphoton MC",
            "any non-nominal-Higgs MC process",
        ],
        "rejected_mc_files_found_but_not_processed": input_manifest["rejected_mc_files_not_nominal_higgs"],
        "signal_processes": input_manifest["signal_processes"],
        "resonant_higgs_background_processes": input_manifest["resonant_higgs_processes"],
        "row_throttling_env_var": "TTH_MAX_SELECTED_PER_SAMPLE",
        "row_throttling_active": MAX_PER_SAMPLE is not None,
        "row_throttling_value": MAX_PER_SAMPLE,
        "load_wall_time_seconds": load_seconds,
    }
    write_json(out("input_data_contract.json"), input_data_contract)

    object_definition_record = {
        "photon": {
            "pt_min_gev": data_io.PHOTON_PT_MIN,
            "abs_eta_max": data_io.PHOTON_ETA_MAX,
            "crack_veto_abs_eta": [data_io.PHOTON_CRACK_LO, data_io.PHOTON_CRACK_HI],
            "tight_id_required_for_preselection": False,
            "tight_isolation_required_for_preselection": False,
            "note": "Photon tight-ID and photon isolation are explicitly NOT required "
                    "to build the diphoton candidate for this preselection sample; "
                    "TI/NTI are recorded as bookkeeping/control-region labels only.",
            "diphoton_candidate": "leading two photons (by pT) passing kinematic acceptance",
            "TI_definition": "both selected photons pass tight ID AND tight isolation",
            "NTI_definition": "at least one selected photon fails tight ID or tight isolation",
        },
        "lepton": {
            "pt_min_gev": data_io.LEPTON_PT_MIN,
            "id_required": False,
            "isolation_required": False,
            "types": ["electron (lep_type==11)", "muon (lep_type==13)"],
        },
        "jet": {
            "pt_min_gev": data_io.JET_PT_MIN,
            "central_abs_eta_max": data_io.CENTRAL_JET_ETA_MAX,
            "forward_abs_eta_min": data_io.CENTRAL_JET_ETA_MAX,
            "btag_definition": f"jet_btag_quantile >= {data_io.BTAG_QUANTILE_MIN}",
            "note": "This open-data sample contains no reconstructed forward jets "
                    "(max |eta| observed ~2.5), so forward-jet-dependent leptonic "
                    "top-associated categories are out of scope by construction.",
        },
        "channels": {
            "hadronic": "n_leptons==0 AND n_jets>=3 AND n_bjets>=1 (REQUIRED categorization channel)",
            "leptonic_bookkeeping": "n_leptons>=1 AND n_bjets>=1 (legacy provenance rows only, "
                                     "excluded from BDT training/optimization/categorization metrics)",
        },
    }
    write_json(out("object_definition_record.json"), object_definition_record)

    # --- preselection_summary.json: raw + weighted counts overall and by process ---
    def counts_block(frame):
        mc = frame[~frame["is_data"]]
        data = frame[frame["is_data"]]
        return {
            "n_raw": int(len(frame)),
            "n_raw_mc": int(len(mc)),
            "n_raw_data": int(len(data)),
            "sum_signed_mc_event_weight": float(mc["event_weight"].sum()) if len(mc) else 0.0,
            "sum_abs_mc_event_weight": float(mc["event_weight"].abs().sum()) if len(mc) else 0.0,
            "sum_observed_data_unit_weight": float(len(data)),
            "note": "MC weight is the SM-normalized (per 1 fb^-1) signed event weight; "
                    "observed data always carries unit weight.",
        }

    by_process = {}
    for proc, g in df.groupby("process"):
        by_process[proc] = {
            "all_preselected": counts_block(g),
            "hadronic": counts_block(g[g.channel == "hadronic"]),
            "leptonic_bookkeeping": counts_block(g[g.channel == "leptonic"]),
        }

    preselection_summary = {
        "definitions": {
            "photon_kinematic_acceptance": "pT>25 GeV, |eta|<2.37 excluding 1.37-1.52 crack, no tight-ID/iso requirement",
            "hadronic_selection": "0 selected e/mu, >=3 selected jets (pT>25 GeV), >=1 b-tagged jet (jet_btag_quantile>=4)",
            "leptonic_bookkeeping_selection": ">=1 selected e/mu (pT>10 GeV, no ID/iso) AND >=1 b-tagged jet; "
                                               "bookkeeping only, not part of the required hadronic categorization",
        },
        "overall": {
            "all_preselected": counts_block(df),
            "hadronic": counts_block(df[df.channel == "hadronic"]),
            "leptonic_bookkeeping": counts_block(df[df.channel == "leptonic"]),
        },
        "by_process": by_process,
    }
    write_json(out("preselection_summary.json"), preselection_summary)

    # --- cutflow.json ---
    cutflow = {"per_process": cutflows_by_process}
    totals = {}
    for stage in next(iter(cutflows_by_process.values())).keys():
        totals[stage] = int(sum(v[stage] for v in cutflows_by_process.values()))
    cutflow["totals"] = totals
    write_json(out("cutflow.json"), cutflow)

    return df, input_manifest


def stage_partition(df, cfg):
    seed = cfg["partitioning"]["seed"]
    fr = cfg["partitioning"]["fractions"]
    fractions = (fr["train"], fr["val"], fr["test"])
    df = df.copy()
    df["partition"] = [stable_partition(eid, seed=seed, fractions=fractions) for eid in df["event_id"]]
    return df


def stage_write_preselected_table_and_plots(df):
    cols = [
        "event_id", "eventNumber", "runNumber", "process", "is_data",
        "is_signal_class", "is_resonant_higgs_class", "channel", "partition",
        "m_gammagamma", "diphoton_class",
        "photon_lead_tightID", "photon_lead_tightIso",
        "photon_sublead_tightID", "photon_sublead_tightIso",
        "n_leptons", "n_jets", "n_jets_central", "n_jets_forward", "n_bjets",
        "jet_ht", "leading_jet_pt", "dijet_mass_leading",
        "raw_weight", "mc_weight_per_fb", "event_weight",
    ]
    path = write_table(df[cols], out("preselected_events"))

    # preselection_mass.png : m_gammagamma by channel (hadronic vs leptonic bookkeeping)
    fig, ax = plt.subplots(figsize=(7, 5))
    bins = np.linspace(105, 160, 56)
    for ch, color in [("hadronic", "tab:blue"), ("leptonic", "tab:orange")]:
        sub = df[(df.channel == ch) & df.m_gammagamma.between(105, 160)]
        ax.hist(sub.m_gammagamma, bins=bins, histtype="step", label=f"{ch} (n={len(sub)})",
                color=color, linewidth=1.5)
    ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
    ax.set_ylabel("Events (raw, preselection)")
    ax.set_title("Preselection diphoton mass by channel")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out("plots", "preselection_mass.png"), dpi=150)
    plt.close(fig)

    # preselection_channels.png
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df.channel.value_counts()
    ax.bar(counts.index.astype(str), counts.values, color=["tab:blue", "tab:orange"])
    ax.set_ylabel("Raw preselected events")
    ax.set_title("Preselection channel counts")
    fig.tight_layout()
    fig.savefig(out("plots", "preselection_channels.png"), dpi=150)
    plt.close(fig)

    # preselection_processes.png
    fig, ax = plt.subplots(figsize=(8, 4))
    counts = df.process.value_counts()
    ax.bar(counts.index.astype(str), counts.values, color="tab:green")
    ax.set_ylabel("Raw preselected events")
    ax.set_title("Preselection process counts")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(out("plots", "preselection_processes.png"), dpi=150)
    plt.close(fig)

    return path


def stage_build_hadronic_features(df):
    had = df[df.channel == "hadronic"].copy()
    finite_mask = np.all(np.isfinite(had[BDT_FEATURES].to_numpy(dtype=float)), axis=1)
    had["bdt_inputs_finite"] = finite_mask
    cols = [
        "event_id", "process", "is_data", "is_signal_class", "is_resonant_higgs_class",
        "partition", "m_gammagamma", "diphoton_class", "event_weight", "mc_weight_per_fb",
        "n_leptons", "n_jets", "n_jets_forward",
        "bdt_inputs_finite",
    ] + BDT_FEATURES
    path = write_table(had[cols], out("hadronic_features"))
    return had, path


def compute_sideband_scale_factors(had_df, cfg):
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    (sb1_lo, sb1_hi) = cfg["mass_windows"]["sideband_low_gev"]
    (sb2_lo, sb2_hi) = cfg["mass_windows"]["sideband_high_gev"]

    def in_sideband(m):
        return ((m >= sb1_lo) & (m < sb1_hi)) | ((m >= sb2_lo) & (m <= sb2_hi))

    def in_window(m):
        return (m >= lo) & (m <= hi)

    data = had_df[had_df.is_data]
    ti_data = data[data.diphoton_class == "TI"]
    nti_data = data[data.diphoton_class == "NTI"]

    ti_sideband_yield = float(ti_data.loc[in_sideband(ti_data.m_gammagamma), "event_weight"].sum())
    nti_sideband_yield = float(nti_data.loc[in_sideband(nti_data.m_gammagamma), "event_weight"].sum())
    nti_window_yield = float(nti_data.loc[in_window(nti_data.m_gammagamma), "event_weight"].sum())
    # Observed TI data in the signal window is never touched: not counted,
    # not summed, not plotted. Blinding is enforced by construction here.

    sf1 = ti_sideband_yield / nti_sideband_yield if nti_sideband_yield > 0 else float("nan")
    sf2 = nti_window_yield / nti_sideband_yield if nti_sideband_yield > 0 else float("nan")

    return {
        "signal_window_gev": [lo, hi],
        "sideband_low_gev": [sb1_lo, sb1_hi],
        "sideband_high_gev": [sb2_lo, sb2_hi],
        "TI_sideband_yield": ti_sideband_yield,
        "NTI_sideband_yield": nti_sideband_yield,
        "NTI_window_yield": nti_window_yield,
        "SF1": sf1,
        "SF2": sf2,
        "SF1_times_SF2": sf1 * sf2,
        "blinded_region_gev": [lo, hi],
        "blinding_note": "Observed TI data in the 125+/-2 GeV window is never inspected, counted, "
                          "summed, or plotted anywhere in this pipeline.",
        "computed_on": "full hadronic-channel observed data (all partitions), a fixed data-driven calibration constant",
    }


def _labeled_bdt_rows(finite, cfg, sf_record, partition):
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    sf1sf2 = sf_record["SF1_times_SF2"]

    sig_rows = finite[finite.is_signal_class & (finite.partition == partition)].copy()
    sig_rows["bdt_fit_weight_prebalance"] = sig_rows["event_weight"]
    sig_rows["training_role"] = "signal_ttH_tH"

    bkg_ggh = finite[
        (finite.process == "ggH") & (finite.diphoton_class == "TI")
        & finite.m_gammagamma.between(lo, hi) & (finite.partition == partition)
    ].copy()
    bkg_ggh["bdt_fit_weight_prebalance"] = bkg_ggh["event_weight"]
    bkg_ggh["training_role"] = "background_ggH_resonant"

    in_sideband = ((finite.m_gammagamma >= sb1_lo) & (finite.m_gammagamma < sb1_hi)) | (
        (finite.m_gammagamma >= sb2_lo) & (finite.m_gammagamma <= sb2_hi)
    )
    bkg_nti = finite[
        finite.is_data & (finite.diphoton_class == "NTI") & in_sideband & (finite.partition == partition)
    ].copy()
    bkg_nti["bdt_fit_weight_prebalance"] = sf1sf2
    bkg_nti["training_role"] = "background_NTI_continuum_proxy"

    return sig_rows, bkg_ggh, bkg_nti


def stage_train_bdt(had, cfg, sf_record):
    from sklearn.ensemble import GradientBoostingClassifier

    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    sf1sf2 = sf_record["SF1_times_SF2"]

    finite = had[had.bdt_inputs_finite]
    sig_rows, bkg_ggh, bkg_nti = _labeled_bdt_rows(finite, cfg, sf_record, "train")
    bkg_rows = pd.concat([bkg_ggh, bkg_nti], ignore_index=True)

    sum_sig_before = float(sig_rows["bdt_fit_weight_prebalance"].sum())
    sum_bkg_before = float(bkg_rows["bdt_fit_weight_prebalance"].sum())
    balance_factor = sum_bkg_before / sum_sig_before if sum_sig_before > 0 else 1.0

    sig_rows["bdt_fit_weight"] = sig_rows["bdt_fit_weight_prebalance"] * balance_factor
    bkg_rows["bdt_fit_weight"] = bkg_rows["bdt_fit_weight_prebalance"]

    sum_sig_after = float(sig_rows["bdt_fit_weight"].sum())
    sum_bkg_after = float(bkg_rows["bdt_fit_weight"].sum())

    sig_rows["label"] = 1
    bkg_rows["label"] = 0
    train_df = pd.concat([sig_rows, bkg_rows], ignore_index=True)
    # Deterministic row order independent of upstream concatenation order.
    train_df = train_df.sort_values("event_id").reset_index(drop=True)

    hp = cfg["bdt"]["hyperparameters"]
    clf = GradientBoostingClassifier(
        n_estimators=hp["n_estimators"], max_depth=hp["max_depth"],
        learning_rate=hp["learning_rate"], subsample=hp["subsample"],
        random_state=hp["random_state"],
    )
    t0 = time.time()
    X = train_df[BDT_FEATURES].to_numpy(dtype=float)
    y = train_df["label"].to_numpy()
    w = train_df["bdt_fit_weight"].clip(lower=0).to_numpy()
    clf.fit(X, y, sample_weight=w)
    train_seconds = time.time() - t0

    class_balance_check = {
        "signal_weight_sum_before_balancing": sum_sig_before,
        "background_weight_sum_before_balancing": sum_bkg_before,
        "balance_factor_applied_to_signal": balance_factor,
        "signal_weight_sum_after_balancing": sum_sig_after,
        "background_weight_sum_after_balancing": sum_bkg_after,
        "n_signal_rows": int(len(sig_rows)),
        "n_background_rows_ggH": int(len(bkg_ggh)),
        "n_background_rows_NTI": int(len(bkg_nti)),
        "note": "bdt_fit_weight is a classifier-fit-only quantity; category yields and "
                "significance never use it. Negative SM-normalized weights are clipped "
                "at 0 for the classifier sample_weight but retained unmodified elsewhere.",
    }

    training_metadata = {
        "features": BDT_FEATURES,
        "excluded_input": "m_gammagamma",
        "algorithm": cfg["bdt"]["algorithm"],
        "hyperparameters": hp,
        "signal_definition": cfg["bdt"]["signal_definition"],
        "background_definition": cfg["bdt"]["background_definition"],
        "training_partition": "train",
        "excluded_from_training": cfg["bdt"]["exclude_from_training"],
        "n_training_rows": int(len(train_df)),
        "train_wall_time_seconds": train_seconds,
        "random_state": hp["random_state"],
    }

    background_mixture_and_normalization = {
        "sideband_scale_factors": sf_record,
        "ggH_resonant_component": {
            "selection": f"process==ggH, diphoton_class==TI, m_gammagamma in [{lo},{hi}]",
            "n_rows_train_partition": int(len(bkg_ggh)),
            "sum_weight_prebalance": float(bkg_ggh["bdt_fit_weight_prebalance"].sum()),
        },
        "NTI_continuum_component": {
            "selection": f"is_data, diphoton_class==NTI, m_gammagamma in sidebands [{sb1_lo},{sb1_hi}] U [{sb2_lo},{sb2_hi}]",
            "n_rows_train_partition": int(len(bkg_nti)),
            "per_event_weight": sf1sf2,
            "sum_weight_prebalance": float(bkg_nti["bdt_fit_weight_prebalance"].sum()),
        },
    }

    write_json(out("model", "training_metadata.json"), training_metadata)
    write_json(out("model", "background_mixture_and_normalization.json"), background_mixture_and_normalization)
    write_json(out("model", "class_balance_check.json"), class_balance_check)
    write_table(
        train_df[["event_id", "process", "label", "training_role", "partition",
                  "m_gammagamma", "diphoton_class",
                  "bdt_fit_weight_prebalance", "bdt_fit_weight"] + BDT_FEATURES],
        out("model", "training_sample"),
    )

    return clf, train_df, training_metadata


def stage_score_all(clf, frame, cfg):
    X_all = frame[BDT_FEATURES].to_numpy(dtype=float)
    scores = np.full(len(frame), np.nan)
    finite = frame["bdt_inputs_finite"].to_numpy()
    if finite.any():
        scores[finite] = clf.predict_proba(X_all[finite])[:, 1]
    frame = frame.copy()
    frame["bdt_score"] = scores
    return frame


def stage_build_scoring_universe(df):
    """Hadronic (required) + leptonic-bookkeeping (optional) rows eligible
    for BDT scoring, sharing the same feature columns computed in data_io."""
    uni = df[df.channel.isin(["hadronic", "leptonic"])].copy()
    finite_mask = np.all(np.isfinite(uni[BDT_FEATURES].to_numpy(dtype=float)), axis=1)
    uni["bdt_inputs_finite"] = finite_mask
    return uni


def stage_optimize_boundaries(had_scored, cfg, sf_record):
    """Optimize boundaries on the validation partition using 36fb-normalized
    expected signal/background model yields in the 125+/-2 GeV window
    (never observed TI data)."""
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    lumi = cfg["luminosities"]["categorization_significance_ifb"]
    sf1sf2 = sf_record["SF1_times_SF2"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]

    val = had_scored[(had_scored.partition == "val") & had_scored.bdt_score.notna()]

    sig_val = val[val.is_signal_class & val.m_gammagamma.between(lo, hi)]
    ggh_val = val[(val.process == "ggH") & (val.diphoton_class == "TI") & val.m_gammagamma.between(lo, hi)]
    in_sideband = ((val.m_gammagamma >= sb1_lo) & (val.m_gammagamma < sb1_hi)) | (
        (val.m_gammagamma >= sb2_lo) & (val.m_gammagamma <= sb2_hi)
    )
    nti_val = val[val.is_data & (val.diphoton_class == "NTI") & in_sideband]

    rows = []
    for _, r in sig_val.iterrows():
        rows.append({"bdt_score": r.bdt_score, "signal_weight": r.event_weight * lumi, "background_weight": 0.0})
    for _, r in ggh_val.iterrows():
        rows.append({"bdt_score": r.bdt_score, "signal_weight": 0.0, "background_weight": r.event_weight * lumi})
    for _, r in nti_val.iterrows():
        rows.append({"bdt_score": r.bdt_score, "signal_weight": 0.0, "background_weight": sf1sf2})

    opt_cfg = {
        "min_relative_improvement": cfg["boundary_optimization"]["min_relative_improvement"],
        "max_boundaries": cfg["boundary_optimization"]["max_boundaries"],
        "grid": [round(x * cfg["boundary_optimization"]["grid_step"], 4)
                 for x in range(1, int(1 / cfg["boundary_optimization"]["grid_step"]))],
    }
    result = optimize_bdt_boundaries(rows, config=opt_cfg)
    result["partition_used"] = "val"
    result["lumi_ifb"] = lumi
    result["n_signal_rows_val"] = int(len(sig_val))
    result["n_ggH_rows_val"] = int(len(ggh_val))
    result["n_NTI_rows_val"] = int(len(nti_val))

    write_json(out("optimization", "thresholds.json"), {
        "boundaries_descending": result["boundaries"],
        "n_categories_from_bdt": result["n_categories"],
        "final_expected_significance": result["final_significance"],
        "min_relative_improvement": result["min_relative_improvement"],
    })
    write_json(out("optimization", "accepted_splits.json"), {
        "iterations": result["iterations"],
        "rejected_next_candidate": result["rejected"],
    })
    return result


def _asimov_z(s, b):
    if b <= 0 or s < 0:
        return 0.0
    return float(np.sqrt(2.0 * ((s + b) * np.log(1.0 + s / b) - s)))


def stage_predictions_and_inference(uni_scored, train_df, boundary_result, cfg, model_path):
    thresholds = boundary_result["boundaries"]

    role_map = train_df.set_index("event_id")["training_role"].to_dict()
    uni_scored = uni_scored.copy()
    uni_scored["training_role"] = uni_scored["event_id"].map(role_map).fillna("not_used_in_training")

    def cat_for_row(r):
        ev = {
            "channel": r.channel, "n_leptons": r.n_leptons,
            "n_jets_central": r.n_jets_central, "n_bjets": r.n_bjets,
        }
        return assign_top_category(ev, score=r.bdt_score if pd.notna(r.bdt_score) else None,
                                    thresholds=thresholds)

    uni_scored["category_initial"] = uni_scored.apply(cat_for_row, axis=1)

    n_hadronic = int((uni_scored.channel == "hadronic").sum())
    n_hadronic_scored = int(((uni_scored.channel == "hadronic") & uni_scored.bdt_score.notna()).sum())
    n_leptonic = int((uni_scored.channel == "leptonic").sum())
    n_leptonic_scored = int(((uni_scored.channel == "leptonic") & uni_scored.bdt_score.notna()).sum())

    pred_cols = [
        "event_id", "process", "is_data", "is_signal_class", "is_resonant_higgs_class",
        "channel", "partition", "m_gammagamma", "diphoton_class",
        "n_leptons", "n_jets", "n_jets_forward",
    ] + BDT_FEATURES + [
        "bdt_score", "bdt_inputs_finite", "training_role", "category_initial",
        "event_weight", "mc_weight_per_fb",
    ]
    predictions_path = write_table(uni_scored[pred_cols], out("predictions"))
    inference_path = write_table(uni_scored[pred_cols], out("inference", "events_with_bdt_scores"))

    category_codes = {c: i for i, c in enumerate(CATEGORY_ORDER + [LEPTONIC_BOOKKEEPING_CATEGORY])}
    process_codes = {p: i for i, p in enumerate(sorted(uni_scored.process.unique()))}
    channel_codes = {c: i for i, c in enumerate(sorted(uni_scored.channel.unique()))}
    partition_codes = {p: i for i, p in enumerate(sorted(uni_scored.partition.unique()))}
    diphoton_class_codes = {d: i for i, d in enumerate(sorted(uni_scored.diphoton_class.unique()))}

    finite_scores = uni_scored.loc[uni_scored.bdt_score.notna(), "bdt_score"]
    manifest = {
        "n_selected_rows": int(len(uni_scored)),
        "n_hadronic_rows": n_hadronic,
        "n_hadronic_scored": n_hadronic_scored,
        "n_hadronic_unscored": n_hadronic - n_hadronic_scored,
        "n_leptonic_bookkeeping_rows": n_leptonic,
        "n_leptonic_bookkeeping_scored": n_leptonic_scored,
        "score_min": float(finite_scores.min()) if len(finite_scores) else None,
        "score_max": float(finite_scores.max()) if len(finite_scores) else None,
        "features": BDT_FEATURES,
        "model_path": model_path,
        "bdt_boundaries_descending": thresholds,
        "code_maps": {
            "category": category_codes,
            "process": process_codes,
            "channel": channel_codes,
            "partition": partition_codes,
            "diphoton_class": diphoton_class_codes,
        },
        "predictions_table": predictions_path,
        "inference_table": inference_path,
    }
    write_json(out("inference", "inference_manifest.json"), manifest)
    return uni_scored, manifest


def hist1d(values, weights, edges):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    ok = np.isfinite(values) & np.isfinite(weights)
    counts, _ = np.histogram(values[ok], bins=edges, weights=weights[ok])
    sumw2, _ = np.histogram(values[ok], bins=edges, weights=weights[ok] ** 2)
    return counts, sumw2


MGG_EDGES = np.linspace(105.0, 160.0, 56)
BDT_EDGES = np.linspace(0.0, 1.0, 21)
BLIND_DISPLAY_WINDOW = (120.0, 130.0)


def stage_categorize(uni_scored, sf_record, boundary_result, cfg):
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    lumi = cfg["luminosities"]["categorization_significance_ifb"]
    sf1sf2 = sf_record["SF1_times_SF2"]
    retention_threshold = cfg["category_retention"]["min_expected_background_signal_window"]

    had = uni_scored[uni_scored.channel == "hadronic"].copy()

    def in_sideband(m):
        return ((m >= sb1_lo) & (m < sb1_hi)) | ((m >= sb2_lo) & (m <= sb2_hi))

    def in_window(m):
        return (m >= lo) & (m <= hi)

    mc_mask = ~had.is_data
    had["significance_model_weight_36fb"] = 0.0
    had.loc[mc_mask, "significance_model_weight_36fb"] = had.loc[mc_mask, "mc_weight_per_fb"] * lumi

    nti_sideband_mask = had.is_data & (had.diphoton_class == "NTI") & in_sideband(had.m_gammagamma)
    had["NTI_continuum_proxy_weight"] = 0.0
    had.loc[nti_sideband_mask, "NTI_continuum_proxy_weight"] = sf1sf2
    had.loc[nti_sideband_mask, "significance_model_weight_36fb"] = sf1sf2

    had["observed_data_weight"] = 0.0
    had.loc[had.is_data, "observed_data_weight"] = 1.0

    ti_mask = had.diphoton_class == "TI"
    window_mask = in_window(had.m_gammagamma)

    signal_rows = had[mc_mask & ti_mask & window_mask & had.is_signal_class]
    resonant_rows = had[mc_mask & ti_mask & window_mask & had.is_resonant_higgs_class]
    nti_rows = had[nti_sideband_mask]

    def by_cat(frame, col="category_initial"):
        return frame.groupby(col)["significance_model_weight_36fb"].sum()

    sig_by_cat = by_cat(signal_rows)
    res_by_cat = by_cat(resonant_rows)
    nti_by_cat = by_cat(nti_rows)
    total_bkg_initial = res_by_cat.add(nti_by_cat, fill_value=0.0)

    physics_categories = [c for c in CATEGORY_ORDER if c != "unassigned"]
    kept = [c for c in physics_categories if total_bkg_initial.get(c, 0.0) >= retention_threshold]
    merged = [c for c in physics_categories if c not in kept]

    had["category_final"] = had["category_initial"].apply(lambda c: c if (c in kept or c == "unassigned") else "unassigned")
    signal_rows = signal_rows.assign(category_final=had.loc[signal_rows.index, "category_final"])
    resonant_rows = resonant_rows.assign(category_final=had.loc[resonant_rows.index, "category_final"])
    nti_rows = nti_rows.assign(category_final=had.loc[nti_rows.index, "category_final"])

    sig_final = by_cat(signal_rows, "category_final")
    res_final = by_cat(resonant_rows, "category_final")
    nti_final = by_cat(nti_rows, "category_final")

    report_categories = kept + ["unassigned"]
    summary_rows = []
    z_list = []
    for cat in report_categories:
        s = float(sig_final.get(cat, 0.0))
        bres = float(res_final.get(cat, 0.0))
        bnti = float(nti_final.get(cat, 0.0))
        b = bres + bnti
        s_over_b = s / b if b > 0 else float("nan")
        s_over_sqrtb = s / math.sqrt(b) if b > 0 else float("nan")
        z = _asimov_z(s, b)
        if cat != "unassigned":
            z_list.append(z)
        summary_rows.append({
            "category": cat,
            "kept": cat in kept,
            "ttH_tH_signal_yield_36fb": s,
            "resonant_higgs_background_yield_36fb": bres,
            "NTI_continuum_proxy_yield_36fb": bnti,
            "total_background_yield_36fb": b,
            "total_model_yield_36fb": s + b,
            "S_over_B": s_over_b,
            "S_over_sqrtB": s_over_sqrtb,
            "expected_counting_significance_Z": z,
        })

    combined_z = float(np.sqrt(np.sum(np.square(z_list)))) if z_list else 0.0

    category_summary_df = pd.DataFrame(summary_rows)
    category_summary_df.to_csv(out("categorization", "category_summary.csv"), index=False)
    write_json(out("category_yields_36fb.json"), {
        "lumi_ifb": lumi,
        "categories": summary_rows,
        "combined_expected_counting_significance": combined_z,
        "blinding_flag_signal_window_TI_data": True,
        "signal_window_gev": [lo, hi],
    })

    # per-process component breakdown for kept + unassigned categories
    component_yields = {}
    for cat in report_categories:
        comp = {}
        for proc in sorted(had.process.unique()):
            if proc == "data":
                continue
            proc_rows = had[mc_mask & ti_mask & window_mask & (had.process == proc) & (had.category_final == cat)]
            comp[proc] = float(proc_rows["significance_model_weight_36fb"].sum())
        comp["NTI_continuum_proxy"] = float(nti_final.get(cat, 0.0))
        component_yields[cat] = comp
    write_json(out("categorization", "category_component_yields.json"), component_yields)

    write_json(out("categorization", "category_retention.json"), {
        "threshold_min_background_yield_36fb": retention_threshold,
        "total_background_yield_36fb_before_retention": {k: float(v) for k, v in total_bkg_initial.items()},
        "kept_categories": kept,
        "merged_to_unassigned": merged,
        "note": "Categories with total (resonant-Higgs + NTI-continuum) expected background "
                "below threshold in the 125+/-2 GeV window are merged into 'unassigned' "
                "before any yields, significances or plots are produced.",
    })

    write_json(out("categorization", "categorization_manifest.json"), {
        "category_order": CATEGORY_ORDER,
        "bdt_boundaries_descending": boundary_result["boundaries"],
        "lumi_ifb": lumi,
        "sideband_scale_factors": sf_record,
        "retention_threshold": retention_threshold,
        "kept_categories": kept,
        "merged_categories": merged,
        "n_hadronic_events_categorized": int(len(had)),
        "blinding": {
            "signal_window_gev": [lo, hi],
            "observed_TI_data_in_signal_window_used": False,
            "note": "Observed TI data in the 125+/-2 GeV window is never inspected, counted or "
                    "reported anywhere in this pipeline; only TI *MC* and NTI *data* enter the "
                    "signal-window model.",
        },
        "cut_based_categories": cfg["cut_based_categories"],
    })

    return had, {
        "kept": kept, "merged": merged, "combined_z": combined_z,
        "summary_rows": summary_rows,
    }


def stage_score_shape_plots(had_scored, sf_record, cfg):
    """Top-level required BDT score plots: area-normalized shape comparison
    of ttH+tH signal vs resonant ggH background vs NTI continuum background,
    built from the full hadronic sample (all partitions) for plotting stats."""
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    sf1sf2 = sf_record["SF1_times_SF2"]

    scored = had_scored[had_scored.bdt_score.notna()]
    sig = scored[scored.is_signal_class]
    ggh = scored[(scored.process == "ggH") & (scored.diphoton_class == "TI") & scored.m_gammagamma.between(lo, hi)]
    in_sb = ((scored.m_gammagamma >= sb1_lo) & (scored.m_gammagamma < sb1_hi)) | (
        (scored.m_gammagamma >= sb2_lo) & (scored.m_gammagamma <= sb2_hi))
    nti = scored[scored.is_data & (scored.diphoton_class == "NTI") & in_sb]

    components = {
        "ttH_tH_signal": (sig.bdt_score.to_numpy(), sig.event_weight.to_numpy()),
        "ggH_resonant_background": (ggh.bdt_score.to_numpy(), ggh.event_weight.to_numpy()),
        "NTI_continuum_background": (nti.bdt_score.to_numpy(), np.full(len(nti), sf1sf2)),
    }

    hist_json = {"bin_edges": BDT_EDGES.tolist(), "components": {}}
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = {"ttH_tH_signal": "crimson", "ggH_resonant_background": "steelblue",
              "NTI_continuum_background": "seagreen"}
    for name, (vals, w) in components.items():
        counts, sumw2 = hist1d(vals, w, BDT_EDGES)
        total_before = float(counts.sum())
        norm_counts = counts / total_before if total_before > 0 else counts
        hist_json["components"][name] = {
            "raw_bin_contents": counts.tolist(),
            "sumw2": sumw2.tolist(),
            "total_before_normalization": total_before,
            "area_normalized_bin_contents": norm_counts.tolist(),
        }
        centers = 0.5 * (BDT_EDGES[:-1] + BDT_EDGES[1:])
        ax.step(centers, norm_counts, where="mid", label=name, color=colors[name], linewidth=1.8)
    ax.set_xlabel("BDT score")
    ax.set_ylabel("Area-normalized events / bin")
    ax.set_title("BDT-score shape comparison (area-normalized)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out("plots", "score_by_component_shape_bdt_v1.png"), dpi=150)
    fig.savefig(out("plots", "score_by_component_shape_bdt_v1.pdf"))
    plt.close(fig)

    write_json(out("plots", "score_by_component_histograms.json"), hist_json)
    return hist_json


def stage_categorization_histograms_and_plots(had_categorized, sf_record, boundary_result, cfg):
    lo, hi = cfg["mass_windows"]["signal_window_gev"]
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    sf1sf2 = sf_record["SF1_times_SF2"]
    blind_lo, blind_hi = BLIND_DISPLAY_WINDOW

    with open(out("categorization", "category_summary.csv")) as f:
        summary_df = pd.read_csv(f)
    kept = summary_df.loc[summary_df.kept, "category"].tolist()
    report_categories = kept + ["unassigned"]

    had = had_categorized
    scored = had[had.bdt_score.notna()]

    # --- bdt_score_model_component_histograms.json (36fb-weighted, not shape-normalized) ---
    window_mask = scored.m_gammagamma.between(lo, hi)
    in_sb = ((scored.m_gammagamma >= sb1_lo) & (scored.m_gammagamma < sb1_hi)) | (
        (scored.m_gammagamma >= sb2_lo) & (scored.m_gammagamma <= sb2_hi))
    sig = scored[(~scored.is_data) & (scored.diphoton_class == "TI") & window_mask & scored.is_signal_class]
    res = scored[(~scored.is_data) & (scored.diphoton_class == "TI") & window_mask & scored.is_resonant_higgs_class]
    nti = scored[scored.is_data & (scored.diphoton_class == "NTI") & in_sb]

    bdt_hist = {"bin_edges": BDT_EDGES.tolist(), "lumi_ifb": cfg["luminosities"]["categorization_significance_ifb"],
                "components": {}}
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, frame, w, color in [
        ("ttH_tH_signal_36fb", sig, sig["significance_model_weight_36fb"], "crimson"),
        ("resonant_higgs_background_36fb", res, res["significance_model_weight_36fb"], "steelblue"),
        ("NTI_continuum_background_36fb", nti, pd.Series(np.full(len(nti), sf1sf2), index=nti.index), "seagreen"),
    ]:
        counts, sumw2 = hist1d(frame.bdt_score.to_numpy(), w.to_numpy(), BDT_EDGES)
        bdt_hist["components"][name] = {"bin_contents": counts.tolist(), "sumw2": sumw2.tolist(),
                                         "total": float(counts.sum())}
        centers = 0.5 * (BDT_EDGES[:-1] + BDT_EDGES[1:])
        ax.step(centers, counts, where="mid", label=name, color=color, linewidth=1.8)
    ax.set_xlabel("BDT score")
    ax.set_ylabel("Expected events / bin (36 fb$^{-1}$)")
    ax.set_title("BDT-score model components (36 fb$^{-1}$)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out("categorization", "plots", "bdt_score_model_components_36fb_v1.png"), dpi=150)
    fig.savefig(out("categorization", "plots", "bdt_score_model_components_36fb_v1.pdf"))
    for b in boundary_result["boundaries"]:
        ax.axvline(b, color="black", linestyle="--", linewidth=1.0)
    ax.set_title("BDT-score model components (36 fb$^{-1}$) with category boundaries")
    fig.tight_layout()
    fig.savefig(out("categorization", "plots", "bdt_score_model_components_with_boundaries_36fb_v1.png"), dpi=150)
    fig.savefig(out("categorization", "plots", "bdt_score_model_components_with_boundaries_36fb_v1.pdf"))
    plt.close(fig)
    write_json(out("categorization", "histograms", "bdt_score_model_component_histograms.json"), bdt_hist)

    # --- category_mgg_control_histograms.json + control-shape plot ---
    mgg_hist = {"bin_edges": MGG_EDGES.tolist(), "blind_display_window_gev": list(BLIND_DISPLAY_WINDOW),
                "categories": {}}
    ncat = max(len(report_categories), 1)
    fig, axes = plt.subplots(1, ncat, figsize=(4.5 * ncat, 4), squeeze=False)
    for i, cat in enumerate(report_categories):
        axc = axes[0][i]
        cat_had = had[had.category_final == cat]
        ti = cat_had[cat_had.is_data & (cat_had.diphoton_class == "TI")]
        ti_display = ti[~ti.m_gammagamma.between(blind_lo, blind_hi)]
        nti_c = cat_had[cat_had.is_data & (cat_had.diphoton_class == "NTI")]
        res_mc = cat_had[(~cat_had.is_data) & (cat_had.diphoton_class == "TI") & cat_had.is_resonant_higgs_class]

        ti_counts, ti_sumw2 = hist1d(ti_display.m_gammagamma, np.ones(len(ti_display)), MGG_EDGES)
        nti_counts, nti_sumw2 = hist1d(nti_c.m_gammagamma, np.ones(len(nti_c)), MGG_EDGES)
        res_counts, res_sumw2 = hist1d(res_mc.m_gammagamma, res_mc.event_weight.to_numpy(), MGG_EDGES)

        mgg_hist["categories"][cat] = {
            "TI_data_blinded_120_130": {"bin_contents": ti_counts.tolist(), "sumw2": ti_sumw2.tolist()},
            "NTI_data_unblinded": {"bin_contents": nti_counts.tolist(), "sumw2": nti_sumw2.tolist()},
            "resonant_higgs_MC_TI": {"bin_contents": res_counts.tolist(), "sumw2": res_sumw2.tolist()},
        }
        centers = 0.5 * (MGG_EDGES[:-1] + MGG_EDGES[1:])
        axc.step(centers, ti_counts, where="mid", label="TI data (blinded 120-130)", color="black")
        axc.step(centers, nti_counts, where="mid", label="NTI data", color="seagreen")
        axc.step(centers, res_counts, where="mid", label="resonant Higgs MC (TI)", color="steelblue")
        axc.axvspan(blind_lo, blind_hi, color="grey", alpha=0.2)
        axc.set_title(cat)
        axc.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
        if i == 0:
            axc.set_ylabel("Events")
            axc.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out("categorization", "plots", "category_mgg_control_shapes_36fb_v1.png"), dpi=150)
    fig.savefig(out("categorization", "plots", "category_mgg_control_shapes_36fb_v1.pdf"))
    plt.close(fig)
    write_json(out("categorization", "histograms", "category_mgg_control_histograms.json"), mgg_hist)

    # --- category expected yields & significance bar plots ---
    plot_df = summary_df[summary_df.category.isin(report_categories)]
    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(plot_df))
    ax.bar(x - 0.2, plot_df.ttH_tH_signal_yield_36fb, width=0.4, label="S (ttH+tH)", color="crimson")
    ax.bar(x + 0.2, plot_df.total_background_yield_36fb, width=0.4, label="B (resonant Higgs + NTI)", color="steelblue")
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df.category, rotation=30, ha="right")
    ax.set_ylabel("Expected yield (36 fb$^{-1}$)")
    ax.set_title("Category expected yields")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out("categorization", "plots", "category_expected_yields_36fb_v1.png"), dpi=150)
    fig.savefig(out("categorization", "plots", "category_expected_yields_36fb_v1.pdf"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(x, plot_df.expected_counting_significance_Z, color="purple")
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df.category, rotation=30, ha="right")
    ax.set_ylabel("Expected counting significance Z")
    ax.set_title("Category expected counting significance (36 fb$^{-1}$)")
    fig.tight_layout()
    fig.savefig(out("categorization", "plots", "category_expected_counting_z_36fb_v1.png"), dpi=150)
    fig.savefig(out("categorization", "plots", "category_expected_counting_z_36fb_v1.pdf"))
    plt.close(fig)


def stage_workspace_and_fit(had_categorized, cat_info, sf_record, cfg):
    """Per-category RooFit background/signal modelling and Asimov
    discovery-significance estimation for every retained hadronic category,
    combined via a quadrature sum of independent per-category Z values
    (see analysis/workspace.py docstring for why a single RooSimultaneous
    fit is not used in this ROOT build)."""
    sb1_lo, sb1_hi = cfg["mass_windows"]["sideband_low_gev"]
    sb2_lo, sb2_hi = cfg["mass_windows"]["sideband_high_gev"]
    fit_lo, fit_hi = sb1_lo, sb2_hi

    had = had_categorized
    kept = cat_info["kept"]

    def in_sideband(m):
        return ((m >= sb1_lo) & (m < sb1_hi)) | ((m >= sb2_lo) & (m <= sb2_hi))

    ws = ROOT.RooWorkspace("tth_hadronic_workspace", "tth_hadronic_workspace")

    per_category = {}
    for cat in kept:
        cat_had = had[had.category_final == cat]
        cat_mc_mask = ~cat_had.is_data
        cat_ti_mask = cat_had.diphoton_class == "TI"
        sig_rows = cat_had[cat_mc_mask & cat_ti_mask & cat_had.is_signal_class]
        res_rows = cat_had[cat_mc_mask & cat_ti_mask & cat_had.is_resonant_higgs_class]
        data_ti = cat_had[cat_had.is_data & (cat_had.diphoton_class == "TI")]
        sb_rows = data_ti[in_sideband(data_ti.m_gammagamma)]

        result = ws_mod.build_and_fit_category(
            category=cat,
            signal_vals=sig_rows.m_gammagamma.to_numpy(),
            signal_w=sig_rows.significance_model_weight_36fb.to_numpy(),
            resonant_vals=res_rows.m_gammagamma.to_numpy(),
            resonant_w=res_rows.significance_model_weight_36fb.to_numpy(),
            sideband_vals=sb_rows.m_gammagamma.to_numpy(),
            sb_low=(sb1_lo, sb1_hi), sb_high=(sb2_lo, sb2_hi),
            fit_lo=fit_lo, fit_hi=fit_hi, workspace=ws,
        )
        per_category[cat] = result
        print(f"  fit[{cat}]: bkg={result['background_pdf_choice']['chosen_model']} "
              f"mu_hat={result['fit_results']['mu_hat']:.3f}+-{result['fit_results']['mu_hat_err']:.3f} "
              f"Z={result['significance']['Z_asimov']:.3f}")

    z_values = [per_category[c]["significance"]["Z_asimov"] for c in kept]
    combined_z = math.sqrt(sum(z * z for z in z_values))

    ws_path = out("fit", "FIT1", "workspace.root")
    ws.writeToFile(ws_path)

    write_json(out("fit", "FIT1", "backend.json"), {
        "backend": "PyROOT/RooFit",
        "root_version": ROOT.gROOT.GetVersion(),
        "minimizer": "Minuit2 via RooMinimizer (migrad + hesse)",
        "asimov_construction": "analytic deterministic construction at mu=1 (no Poisson generation)",
        "combination_method": "quadrature sum of independent per-category Asimov Z "
                               "(mu_<category> fit separately per category)",
        "known_issue": "RooSimultaneous combination of the per-category RooAddPdf models "
                       "segfaults in this ROOT build (6.38.00) inside "
                       "RooSimultaneous::compileForNormSet / RooAddPdf::clone during "
                       "createNLL; independent per-category fits are used instead.",
    })
    write_json(out("fit", "FIT1", "background_pdf_scan.json"),
               {c: per_category[c]["background_pdf_scan"] for c in kept})
    write_json(out("fit", "FIT1", "background_pdf_choice.json"),
               {c: per_category[c]["background_pdf_choice"] for c in kept})
    write_json(out("fit", "FIT1", "background_template_selection.json"), {
        "strategy": "data-driven analytic sideband template (no simulated continuum template available)",
        "reason": "Event-level continuum MC (Sherpa gamma-gamma and any other non-nominal-Higgs MC) "
                  "is excluded from this analysis (see input_data_contract.json), so no simulated "
                  "background template exists; the continuum background is instead estimated purely "
                  "from observed TI sideband data (105-120, 130-160 GeV) using the AIC-selected "
                  "analytic shape recorded per category in background_pdf_choice.json.",
        "per_category_chosen_template": {c: per_category[c]["background_pdf_choice"]["chosen_model"] for c in kept},
    })
    write_json(out("fit", "FIT1", "signal_pdf.json"),
               {c: per_category[c]["signal_pdf"] for c in kept})
    write_json(out("fit", "FIT1", "resonant_higgs_pdf.json"),
               {c: per_category[c]["resonant_higgs_pdf"] for c in kept})
    write_json(out("fit", "FIT1", "results.json"), {
        "categories": {c: {"model": per_category[c]["model"],
                            "fit_results": per_category[c]["fit_results"],
                            "significance": per_category[c]["significance"]} for c in kept},
        "combined": {"Z_combined_asimov": combined_z, "categories_used": kept},
    })
    write_json(out("fit", "FIT1", "significance_asimov.json"), {
        "per_category": {c: per_category[c]["significance"] for c in kept},
        "combined_Z_asimov": combined_z,
        "lumi_ifb": cfg["luminosities"]["categorization_significance_ifb"],
    })
    write_json(out("fit", "FIT1", "significance_asimov_construction.json"),
               {c: per_category[c]["asimov_construction"] for c in kept})
    write_json(out("fit", "FIT1", "significance.json"), {
        "method": "q0 = 2*(NLL(mu=0) - NLL(mu_hat)), Z = sqrt(max(q0,0)); "
                  "combined Z = sqrt(sum(Z_i^2)) across independent hadronic categories",
        "lumi_ifb": cfg["luminosities"]["categorization_significance_ifb"],
        "per_category_Z": {c: per_category[c]["significance"]["Z_asimov"] for c in kept},
        "combined_expected_significance_asimov": combined_z,
    })

    # --- sideband background fit plot + payload ---
    ncat = max(len(kept), 1)
    fig, axes = plt.subplots(1, ncat, figsize=(4.5 * ncat, 4), squeeze=False)
    sideband_plot_payload = {}
    for i, cat in enumerate(kept):
        axc = axes[0][i]
        r = per_category[cat]
        cat_had = had[had.category_final == cat]
        data_ti = cat_had[cat_had.is_data & (cat_had.diphoton_class == "TI")]
        sb_rows = data_ti[in_sideband(data_ti.m_gammagamma)]
        counts, _ = hist1d(sb_rows.m_gammagamma.to_numpy(), np.ones(len(sb_rows)), MGG_EDGES)
        centers = 0.5 * (MGG_EDGES[:-1] + MGG_EDGES[1:])
        in_sb_mask = in_sideband(centers)
        axc.step(centers[in_sb_mask], counts[in_sb_mask], where="mid", color="black", label="TI data (sidebands)")

        edges = np.array(r["asimov_construction"]["bin_edges_gev"])
        fine_centers = 0.5 * (edges[:-1] + edges[1:])
        n_bkg0 = r["model"]["n_bkg0_init_from_sideband_extrapolation"]
        bkg_curve = np.array(r["asimov_construction"]["continuum_background_component_mu1_truth"])
        axc.plot(fine_centers, bkg_curve, color="crimson", linestyle="--", linewidth=1.3,
                 label="fitted continuum background\n(extrapolated across blinded 120-130 GeV)")
        axc.axvspan(*BLIND_DISPLAY_WINDOW, color="grey", alpha=0.25)
        axc.set_title(f"{cat}\nbkg={r['background_pdf_choice']['chosen_model']}")
        axc.set_xlabel("m_{gg} [GeV]")
        axc.set_ylabel("Events / bin")
        axc.legend(fontsize=7)
        sideband_plot_payload[cat] = {
            "sideband_bin_centers_gev": centers[in_sb_mask].tolist(),
            "sideband_data_counts": counts[in_sb_mask].tolist(),
            "model_curve_bin_centers_gev": fine_centers.tolist(),
            "model_curve_mu1_truth": bkg_curve.tolist(),
            "n_bkg0_full_range_estimate": n_bkg0,
        }
    fig.tight_layout()
    fig.savefig(out("fit", "FIT1", "plots", "sidebands_background_fit.png"), dpi=150)
    fig.savefig(out("fit", "FIT1", "plots", "sidebands_background_fit.pdf"))
    plt.close(fig)
    write_json(out("fit", "FIT1", "sideband_fit_plots.json"), sideband_plot_payload)

    # --- Asimov S+B fit plot + payload ---
    fig, axes = plt.subplots(1, ncat, figsize=(4.5 * ncat, 4), squeeze=False)
    asimov_plot_payload = {}
    for i, cat in enumerate(kept):
        axc = axes[0][i]
        r = per_category[cat]
        edges = np.array(r["asimov_construction"]["bin_edges_gev"])
        centers = 0.5 * (edges[:-1] + edges[1:])
        content = np.array(r["asimov_construction"]["bin_contents_mu1_truth"])
        axc.step(centers, content, where="mid", color="black", label="Asimov data (mu=1 truth)")

        mu_hat = r["fit_results"]["mu_hat"]
        n_bkg_hat = r["fit_results"]["n_bkg_hat"]
        n_bkg0 = r["model"]["n_bkg0_init_from_sideband_extrapolation"]
        bkg_scale = n_bkg_hat / n_bkg0 if n_bkg0 > 0 else 1.0
        sig_comp = np.array(r["asimov_construction"]["signal_component_mu1_truth"])
        res_comp = np.array(r["asimov_construction"]["resonant_higgs_component_fixed"])
        bkg_comp = np.array(r["asimov_construction"]["continuum_background_component_mu1_truth"])
        fitted_curve = mu_hat * sig_comp + res_comp + bkg_scale * bkg_comp
        axc.plot(centers, fitted_curve, color="crimson", linewidth=1.3,
                  label=f"post-fit model (mu_hat={mu_hat:.2f})")
        axc.set_title(f"{cat}\nmu_hat={mu_hat:.2f} Z={r['significance']['Z_asimov']:.2f}")
        axc.set_xlabel("m_{gg} [GeV]")
        axc.set_ylabel("Events / bin (Asimov)")
        axc.legend(fontsize=7)
        asimov_plot_payload[cat] = {
            "bin_centers_gev": centers.tolist(),
            "asimov_bin_contents": content.tolist(),
            "post_fit_model_curve": fitted_curve.tolist(),
            "mu_hat": mu_hat,
            "n_bkg_hat": n_bkg_hat,
            "Z_asimov": r["significance"]["Z_asimov"],
        }
    fig.tight_layout()
    fig.savefig(out("fit", "FIT1", "plots", "asimov_sb_fit.png"), dpi=150)
    fig.savefig(out("fit", "FIT1", "plots", "asimov_sb_fit.pdf"))
    plt.close(fig)
    write_json(out("fit", "FIT1", "significance_asimov_plot_payload.json"), asimov_plot_payload)

    write_json(out("fit", "workspace.json"), {
        "workspace_name": "tth_hadronic_workspace",
        "workspace_file": os.path.relpath(ws_path, RESULTS_DIR),
        "categories": kept,
        "fit_name": "FIT1",
        "observable": "m_gammagamma [105,160] GeV, 55 bins",
        "per_category_parameters": {
            c: [f"mu_{c}", f"n_bkg_{c}", f"n_res_{c} (fixed)", f"n_sig0_{c} (fixed)"] for c in kept
        },
    })
    write_json(out("workspace_manifest.json"), {
        "workspace_root_file": os.path.relpath(ws_path, RESULTS_DIR),
        "fit_directory": "fit/FIT1",
        "categories_fit": kept,
        "combined_expected_significance_asimov_Z": combined_z,
        "backend": "PyROOT/RooFit",
    })

    return per_category, combined_z


def stage_metrics(clf, had, cfg, sf_record, cat_info, boundary_result, fit_combined_z):
    from sklearn.metrics import roc_auc_score

    finite = had[had.bdt_inputs_finite]
    bdt_auc_by_partition = {}
    for partition in ("train", "val", "test"):
        sig_rows, bkg_ggh, bkg_nti = _labeled_bdt_rows(finite, cfg, sf_record, partition)
        bkg_rows = pd.concat([bkg_ggh, bkg_nti], ignore_index=True)
        if len(sig_rows) == 0 or len(bkg_rows) == 0:
            bdt_auc_by_partition[partition] = None
            continue
        y = np.concatenate([np.ones(len(sig_rows)), np.zeros(len(bkg_rows))])
        w = np.concatenate([sig_rows["bdt_fit_weight_prebalance"].clip(lower=0).to_numpy(),
                             bkg_rows["bdt_fit_weight_prebalance"].clip(lower=0).to_numpy()])
        X = np.concatenate([sig_rows[BDT_FEATURES].to_numpy(dtype=float),
                             bkg_rows[BDT_FEATURES].to_numpy(dtype=float)])
        scores = clf.predict_proba(X)[:, 1]
        try:
            bdt_auc_by_partition[partition] = float(roc_auc_score(y, scores, sample_weight=w))
        except ValueError:
            bdt_auc_by_partition[partition] = None

    metrics = {
        "bdt_weighted_roc_auc_by_partition": bdt_auc_by_partition,
        "bdt_boundaries_accepted": boundary_result["boundaries"],
        "n_categories_kept": len(cat_info["kept"]),
        "n_categories_merged_to_unassigned": len(cat_info["merged"]),
        "combined_expected_counting_significance_Z_36fb": cat_info["combined_z"],
        "combined_expected_asimov_significance_Z_36fb": fit_combined_z,
        "sideband_scale_factors": {"SF1": sf_record["SF1"], "SF2": sf_record["SF2"],
                                    "SF1_times_SF2": sf_record["SF1_times_SF2"]},
    }
    write_json(out("metrics.json"), metrics)
    return metrics


def stage_write_report_and_manifest(cfg, input_manifest, sf_record, training_metadata,
                                     boundary_result, inf_manifest, cat_info, fit_combined_z,
                                     elapsed_seconds):
    run_manifest = {
        "pipeline": "tth-diphoton-bdt",
        "results_dir": RESULTS_DIR,
        "inputs_dir": INPUTS_DIR,
        "max_selected_per_sample_throttle": MAX_PER_SAMPLE,
        "data_scope": "Nominal Higgs signal MC (ggH, VBF, WH, ZH, ggZH, ttH, tH) and data only; "
                      "Sherpa diphoton continuum MC and any other non-nominal-Higgs MC samples "
                      "are excluded from this analysis (see input_data_contract.json).",
        "allowed_mc_processes": input_manifest["allowed_mc_processes"],
        "signal_processes": input_manifest["signal_processes"],
        "resonant_higgs_processes": input_manifest["resonant_higgs_processes"],
        "rejected_mc_files_not_nominal_higgs": input_manifest["rejected_mc_files_not_nominal_higgs"],
        "sideband_scale_factors": {"SF1": sf_record["SF1"], "SF2": sf_record["SF2"],
                                    "SF1_times_SF2": sf_record["SF1_times_SF2"]},
        "bdt_boundaries_accepted": boundary_result["boundaries"],
        "categories_kept": cat_info["kept"],
        "categories_merged_to_unassigned": cat_info["merged"],
        "combined_expected_counting_significance_Z_36fb": cat_info["combined_z"],
        "combined_expected_asimov_significance_Z_36fb": fit_combined_z,
        "blinding_policy": "Observed TI data in the 125+/-2 GeV signal window is never inspected, "
                            "counted, summed, or plotted anywhere in this pipeline. A wider 120-130 GeV "
                            "display-blind window is additionally applied to TI data in control-shape "
                            "plots only; NTI data is never blinded.",
        "elapsed_seconds": elapsed_seconds,
    }
    write_json(out("run_manifest.json"), run_manifest)

    report = f"""# ttH/tH diphoton hadronic-category BDT analysis report

## Scope

Nominal Higgs signal MC ({', '.join(input_manifest['allowed_mc_processes'])}) and observed data only.
Sherpa gamma-gamma continuum MC and any other non-nominal-Higgs MC files present under the inputs
directory are excluded (see `input_data_contract.json`, `rejected_mc_files_not_nominal_higgs`).
Photon tight-ID and isolation are **not** required in the preselection (see `object_definition_record.json`).

## Blinding

Observed TI (tight-tight, both photons pass tight ID + isolation) data in the 125 +/- 2 GeV signal
window is never inspected, counted, summed, or plotted anywhere in this pipeline. A wider 120-130 GeV
display-blind window is additionally applied to TI data in control-shape plots only. NTI data is never
blinded and is used as the continuum-background proxy (ABCD method, SF1={sf_record['SF1']:.4g},
SF2={sf_record['SF2']:.4g}, SF1*SF2={sf_record['SF1_times_SF2']:.4g}).

## BDT

Features: {BDT_FEATURES}. Deterministic `GradientBoostingClassifier` trained on the stable-hashed
train partition (ttH+tH signal vs. ggH-TI + NTI-sideband background). Boundaries optimized greedily
on the validation partition, accepting a new boundary only when quadrature-summed Asimov significance
improves by >= {cfg['boundary_optimization']['min_relative_improvement'] * 100:.0f}%.
Accepted boundaries: {boundary_result['boundaries']}.

## Categorization (36 fb^-1 re-normalized)

Categories kept after the >= {cfg['category_retention']['min_expected_background_signal_window']} expected
background event retention threshold: {cat_info['kept']}.
Categories merged into `unassigned`: {cat_info['merged']}.
Combined expected counting significance Z (36 fb^-1): {cat_info['combined_z']:.4f}.

## RooFit background/signal modelling and Asimov significance

Per retained category: TI-sideband (105-120, 130-160 GeV) background shape scan
(exponential / Chebychev order 1 / order 2, AIC-selected), extrapolated into the full 105-160 GeV
fit range; fixed-shape Gaussian signal (ttH+tH TI MC) and fixed-shape, fixed-normalization Gaussian
resonant-Higgs background (non-top Higgs TI MC); combined into a RooFit extended model and fit to a
deterministic analytic Asimov dataset (mu floating, then mu=0 fixed) to obtain the discovery test
statistic q0 and Z = sqrt(q0). See `fit/FIT1/` for full per-category results; categories are combined
via quadrature sum of Z (see `fit/FIT1/backend.json` for why a single RooSimultaneous fit is not used
in this ROOT build).

Combined expected Asimov significance Z (36 fb^-1): {fit_combined_z:.4f}.

## Artifacts

See `run_manifest.json` for the full run configuration and `workspace_manifest.json` /
`fit/workspace.json` for the RooFit workspace contents.
"""
    with open(out("report.md"), "w") as f:
        f.write(report)
    return run_manifest


if __name__ == "__main__":
    cfg = load_config()
    ensure_dirs()
    with open(out("config_resolved.yaml"), "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    df, input_manifest = stage_load_and_preselect(cfg)
    df = stage_partition(df, cfg)
    path = stage_write_preselected_table_and_plots(df)
    print("preselected_events written to", path, "rows=", len(df))

    had, had_path = stage_build_hadronic_features(df)
    print("hadronic_features written to", had_path, "rows=", len(had))

    sf_record = compute_sideband_scale_factors(had, cfg)
    print("SF1, SF2, SF1*SF2 =", sf_record["SF1"], sf_record["SF2"], sf_record["SF1_times_SF2"])

    clf, train_df, training_metadata = stage_train_bdt(had, cfg, sf_record)
    print("BDT trained on", len(train_df), "rows in",
          training_metadata["train_wall_time_seconds"], "s")

    uni = stage_build_scoring_universe(df)
    uni_scored = stage_score_all(clf, uni, cfg)
    had_scored = uni_scored[uni_scored.channel == "hadronic"]
    print("scored", had_scored.bdt_score.notna().sum(), "/", len(had_scored), "hadronic rows")

    boundary_result = stage_optimize_boundaries(had_scored, cfg, sf_record)
    print("accepted boundaries:", boundary_result["boundaries"])

    model_path = out("model", "bdt_model.joblib")
    joblib.dump(clf, model_path)

    uni_scored, inf_manifest = stage_predictions_and_inference(
        uni_scored, train_df, boundary_result, cfg, model_path
    )
    print("inference rows:", inf_manifest["n_selected_rows"],
          "hadronic scored:", inf_manifest["n_hadronic_scored"])

    had_categorized, cat_info = stage_categorize(uni_scored, sf_record, boundary_result, cfg)
    print("kept categories:", cat_info["kept"], "merged:", cat_info["merged"])
    print("combined Z:", cat_info["combined_z"])

    stage_score_shape_plots(had_scored, sf_record, cfg)
    stage_categorization_histograms_and_plots(had_categorized, sf_record, boundary_result, cfg)
    print("categorization plots + histograms written")

    per_category_fit, fit_combined_z = stage_workspace_and_fit(had_categorized, cat_info, sf_record, cfg)
    print("RooFit workspace + Asimov significance written, combined Z =", fit_combined_z)

    stage_metrics(clf, had, cfg, sf_record, cat_info, boundary_result, fit_combined_z)
    print("metrics.json written")

    elapsed = time.time() - RUN_START
    stage_write_report_and_manifest(cfg, input_manifest, sf_record, training_metadata,
                                     boundary_result, inf_manifest, cat_info, fit_combined_z, elapsed)
    print("report.md + run_manifest.json written")
    print("elapsed", elapsed)
