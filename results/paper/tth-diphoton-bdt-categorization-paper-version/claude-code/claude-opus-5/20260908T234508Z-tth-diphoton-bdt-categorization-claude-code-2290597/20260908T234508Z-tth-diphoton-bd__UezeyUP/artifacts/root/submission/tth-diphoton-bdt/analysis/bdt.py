"""Hadronic BDT: background mixture, class balancing, training and boundaries."""

from __future__ import annotations

import time
from typing import Any, Mapping

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

from .top_categorization import BDT_FEATURES, optimize_bdt_boundaries

SIGNAL_SAMPLES = ("ttH", "tH")
RESONANT_TRAINING_SAMPLES = ("ggH",)


# --------------------------------------------------------------------------
# NTI continuum proxy normalisation
# --------------------------------------------------------------------------


def compute_nti_scale_factors(df: pd.DataFrame, cfg: Mapping[str, Any]) -> dict[str, Any]:
    """SF1, SF2 and SF1*SF2 from the hadronic data control sample.

    ``SF1 = TI_sideband_yield / NTI_sideband_yield``
    ``SF2 = NTI_(125 +/- 2 GeV)_yield / NTI_sideband_yield``

    The product ``SF1*SF2`` transports an NTI *sideband* event into an expected
    TI *signal-window* continuum yield, and is the per-event weight of the NTI
    continuum proxy.
    """
    data = df[df["is_data"] & df["passes_hadronic_preselection"]]
    ti = data[data["photon_ti"]]
    nti = data[data["photon_nti"]]

    ti_sb = int(ti["in_sideband"].sum())
    nti_sb = int(nti["in_sideband"].sum())
    nti_win = int(nti["in_signal_window"].sum())

    sf1 = float(ti_sb) / nti_sb if nti_sb else float("nan")
    sf2 = float(nti_win) / nti_sb if nti_sb else float("nan")

    inclusive = df[df["is_data"]]
    inc_ti = inclusive[inclusive["photon_ti"]]
    inc_nti = inclusive[inclusive["photon_nti"]]

    return {
        "region": "hadronic preselection, observed GamGam data",
        "definitions": {
            "TI": "both photons pass tight ID AND tight isolation",
            "NTI": "at least one photon fails tight ID or fails tight isolation",
            "sidebands_gev": [
                cfg["selection"]["sideband_low_gev"],
                cfg["selection"]["sideband_high_gev"],
            ],
            "signal_window_gev": cfg["selection"]["signal_window_gev"],
            "SF1": "TI_sideband_yield / NTI_sideband_yield",
            "SF2": "NTI_(125 +/- 2 GeV)_yield / NTI_sideband_yield",
            "SF1xSF2": "per-event weight of an NTI sideband event used as the "
            "continuum proxy in the 125 +/- 2 GeV signal window",
        },
        "counts": {
            "TI_sideband_yield": ti_sb,
            "NTI_sideband_yield": nti_sb,
            "NTI_signal_window_yield": nti_win,
            "TI_signal_window_yield": "BLINDED (observed TI data in 125 +/- 2 GeV "
            "is never inspected)",
        },
        "SF1": sf1,
        "SF2": sf2,
        "SF1xSF2": sf1 * sf2,
        "implied_continuum_yield_in_signal_window": sf1 * sf2 * nti_sb,
        "inclusive_crosscheck": {
            "TI_sideband_yield": int(inc_ti["in_sideband"].sum()),
            "NTI_sideband_yield": int(inc_nti["in_sideband"].sum()),
            "NTI_signal_window_yield": int(inc_nti["in_signal_window"].sum()),
        },
        "nti_control_shape_policy": (
            "NTI control-shape distributions retain entries in 120-130 GeV. The "
            "120-130 GeV blinding/removal policy applies ONLY to observed TI data."
        ),
    }


# --------------------------------------------------------------------------
# Model weights
# --------------------------------------------------------------------------


def add_model_weights(df: pd.DataFrame, sf: Mapping[str, Any]) -> pd.DataFrame:
    """Attach the yield/significance weights used downstream.

    * ``nti_continuum_weight`` -- SF1*SF2 for NTI data sideband rows, else 0.
    * ``significance_model_weight_36fb`` -- TI MC normalised to 36 fb^-1 in the
      125 +/- 2 GeV signal window PLUS the scaled NTI continuum proxy.
    * ``observed_data_weight`` -- unit weight for observed data, kept separate.
    """
    out = df.copy()
    sf12 = float(sf["SF1xSF2"])

    is_nti_proxy = out["is_data"] & out["photon_nti"] & out["in_sideband"]
    out["is_nti_continuum_proxy"] = is_nti_proxy
    out["nti_continuum_weight"] = np.where(is_nti_proxy, sf12, 0.0)

    mc_signal_window_ti = out["is_mc"] & out["photon_ti"] & out["in_signal_window"]
    out["is_mc_model_row"] = mc_signal_window_ti
    out["mc_model_weight_36fb"] = np.where(
        mc_signal_window_ti, out["weight_mc_36fb"], 0.0
    )
    out["significance_model_weight_36fb"] = (
        out["mc_model_weight_36fb"] + out["nti_continuum_weight"]
    )

    role = out["process_role"].to_numpy()
    out["model_component"] = np.select(
        [
            mc_signal_window_ti.to_numpy() & (role == "signal_top"),
            mc_signal_window_ti.to_numpy() & (role == "resonant_higgs"),
            is_nti_proxy.to_numpy(),
        ],
        ["signal_ttH_tH", "resonant_higgs_bkg", "nti_continuum_bkg"],
        default="not_in_model",
    )
    return out


# --------------------------------------------------------------------------
# Training sample
# --------------------------------------------------------------------------


def build_training_sample(
    df: pd.DataFrame, cfg: Mapping[str, Any], sf: Mapping[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Assemble the ``ttH+tH`` vs ``ggH + NTI`` training sample."""
    had = df[df["passes_hadronic_preselection"]].copy()

    sig_mask = (
        had["process"].isin(SIGNAL_SAMPLES)
        & had["is_mc"]
        & had["photon_ti"]
        & had["in_signal_window"]
    )
    res_mask = (
        had["process"].isin(RESONANT_TRAINING_SAMPLES)
        & had["is_mc"]
        & had["photon_ti"]
        & had["in_signal_window"]
    )
    nti_mask = had["is_data"] & had["photon_nti"] & had["in_sideband"]

    lumi_pb = float(cfg["normalization"]["luminosity_fb"]) * 1000.0
    sf12 = float(sf["SF1xSF2"])

    rows = had[sig_mask | res_mask | nti_mask].copy()
    rows["train_component"] = np.select(
        [sig_mask.loc[rows.index], res_mask.loc[rows.index], nti_mask.loc[rows.index]],
        ["signal_ttH_tH", "background_ggH_resonant", "background_nti_continuum"],
        default="unused",
    )
    rows["bdt_class"] = (rows["train_component"] == "signal_ttH_tH").astype(int)

    # Physical weight of every training row.  MC rows use the SM-normalised MC
    # weight (xsec * k-factor * filter-eff / signed sum-of-weights * generator
    # weight * scale factors), scaled to the luminosity of the observed data so
    # that the ggH + NTI background mixture is physically meaningful.  NTI rows
    # carry the SF1*SF2 sideband-to-signal-window transport factor.
    physical = np.where(
        rows["is_mc"].to_numpy(),
        rows["weight_sm_per_pb"].to_numpy() * lumi_pb,
        sf12,
    )
    rows["bdt_physical_weight"] = physical

    # Classifier fit weights must be non-negative; the signed generator weights
    # are preserved in `bdt_physical_weight` and in the bookkeeping below.
    rows["bdt_fit_weight_unbalanced"] = np.abs(physical)

    sig = rows["bdt_class"] == 1
    bkg = ~sig
    sum_sig_before = float(rows.loc[sig, "bdt_fit_weight_unbalanced"].sum())
    sum_bkg_before = float(rows.loc[bkg, "bdt_fit_weight_unbalanced"].sum())

    target = 0.5 * (sum_sig_before + sum_bkg_before)
    scale_sig = target / sum_sig_before if sum_sig_before > 0 else 0.0
    scale_bkg = target / sum_bkg_before if sum_bkg_before > 0 else 0.0
    rows["bdt_fit_weight"] = rows["bdt_fit_weight_unbalanced"] * np.where(
        sig, scale_sig, scale_bkg
    )

    sums_signed = {
        component: float(
            rows.loc[rows["train_component"] == component, "bdt_physical_weight"].sum()
        )
        for component in sorted(rows["train_component"].unique())
    }

    balance = {
        "order_of_operations": [
            "1. SM-normalised MC weights for ttH+tH signal (xsec, filter eff, "
            "k-factor, signed generator weight sum, generator weight, per-event "
            "scale factors), scaled to the data luminosity",
            "2. ggH resonant MC (same normalisation) + NTI data sideband proxy "
            "weighted by SF1*SF2 form the background mixture",
            "3. ONLY THEN class balancing is applied",
        ],
        "negative_weight_handling": {
            "policy": "classifier fit weights use |w|; signed weights preserved "
            "in bdt_physical_weight and in every yield/significance weight",
            "n_negative_weight_rows": int((physical < 0).sum()),
            "sum_signed_weights": float(physical.sum()),
            "sum_abs_weights": float(np.abs(physical).sum()),
        },
        "before_balancing": {
            "signal_class_weight_sum": sum_sig_before,
            "background_class_weight_sum": sum_bkg_before,
            "signal_raw_rows": int(sig.sum()),
            "background_raw_rows": int(bkg.sum()),
            "ratio_signal_over_background": (
                sum_sig_before / sum_bkg_before if sum_bkg_before else None
            ),
        },
        "balancing": {
            "applied": True,
            "target_per_class_weight_sum": target,
            "signal_scale_factor": scale_sig,
            "background_scale_factor": scale_bkg,
        },
        "after_balancing": {
            "signal_class_weight_sum": float(rows.loc[sig, "bdt_fit_weight"].sum()),
            "background_class_weight_sum": float(rows.loc[bkg, "bdt_fit_weight"].sum()),
            "ratio_signal_over_background": float(
                rows.loc[sig, "bdt_fit_weight"].sum()
                / max(rows.loc[bkg, "bdt_fit_weight"].sum(), 1e-30)
            ),
        },
        "component_signed_weight_sums": sums_signed,
        "component_raw_rows": {
            component: int((rows["train_component"] == component).sum())
            for component in sorted(rows["train_component"].unique())
        },
        "background_mixture": {
            "resonant": "ggH TI MC in 125 +/- 2 GeV",
            "continuum": "NTI observed-data sidebands 105-120 and 130-160 GeV, "
            "weighted by SF1*SF2",
            "SF1": sf["SF1"],
            "SF2": sf["SF2"],
            "SF1xSF2": sf["SF1xSF2"],
        },
        "blinding": {
            "nominal_TI_observed_data_in_signal_window_used_for_training": False,
            "nominal_TI_observed_data_in_signal_window_used_for_thresholds": False,
        },
    }
    return rows.reset_index(drop=True), balance


# --------------------------------------------------------------------------
# Training
# --------------------------------------------------------------------------


def train_classifier(
    rows: pd.DataFrame, cfg: Mapping[str, Any]
) -> tuple[HistGradientBoostingClassifier, dict[str, Any]]:
    features = list(cfg["bdt"]["features"])
    if tuple(features) != tuple(BDT_FEATURES):
        raise ValueError(
            f"config BDT features {features} do not match BDT_FEATURES {list(BDT_FEATURES)}"
        )

    finite = np.isfinite(rows[features].to_numpy()).all(axis=1)
    usable = rows[finite].copy()

    train = usable[usable["partition"] == "train"]
    val = usable[usable["partition"] == "val"]
    test = usable[usable["partition"] == "test"]

    params = dict(cfg["bdt"]["model"]["params"])
    model = HistGradientBoostingClassifier(**params)

    start = time.perf_counter()
    model.fit(
        train[features].to_numpy(dtype=np.float64),
        train["bdt_class"].to_numpy(dtype=np.int32),
        sample_weight=train["bdt_fit_weight"].to_numpy(dtype=np.float64),
    )
    wall = time.perf_counter() - start

    def auc(sub: pd.DataFrame) -> float | None:
        if sub.empty or sub["bdt_class"].nunique() < 2:
            return None
        score = model.predict_proba(sub[features].to_numpy(dtype=np.float64))[:, 1]
        return float(
            roc_auc_score(
                sub["bdt_class"].to_numpy(),
                score,
                sample_weight=sub["bdt_fit_weight"].to_numpy(),
            )
        )

    metadata = {
        "model": {
            "kind": cfg["bdt"]["model"]["kind"],
            "library": "scikit-learn",
            "hyperparameters": params,
            "deterministic": True,
            "determinism_note": "fixed random_state, early_stopping disabled, "
            "single-threaded numeric backends (OMP_NUM_THREADS=1)",
            "n_iter_": int(model.n_iter_),
        },
        "features": features,
        "feature_count": len(features),
        "m_gammagamma_used_as_input": False,
        "signal_class": {
            "definition": "ttH + tH TI MC in 125 +/- 2 GeV, hadronic preselection",
            "samples": list(SIGNAL_SAMPLES),
        },
        "background_class": {
            "definition": "ggH TI MC in 125 +/- 2 GeV  +  NTI observed-data "
            "sidebands scaled by SF1*SF2",
            "resonant_samples": list(RESONANT_TRAINING_SAMPLES),
            "continuum": "NTI data sidebands",
        },
        "rows": {
            "total": int(len(rows)),
            "with_finite_features": int(len(usable)),
            "dropped_non_finite_features": int(len(rows) - len(usable)),
            "train": int(len(train)),
            "val": int(len(val)),
            "test": int(len(test)),
            "train_signal": int((train["bdt_class"] == 1).sum()),
            "train_background": int((train["bdt_class"] == 0).sum()),
        },
        "partitioning": {
            "identifier": "event_id (stable)",
            "seed": cfg["partition"]["seed"],
            "fractions": cfg["partition"]["fractions"],
            "fit_partition": "train",
        },
        "performance": {
            "weighted_auc_train": auc(train),
            "weighted_auc_val": auc(val),
            "weighted_auc_test": auc(test),
        },
        "timing": {
            "training_wall_time_seconds": wall,
            "stage": "bdt_training",
        },
    }
    return model, metadata


def score_dataframe(
    model: HistGradientBoostingClassifier, df: pd.DataFrame, features: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    """Return ``(score, scored_mask)`` with NaN where inputs are not finite."""
    values = df[features].to_numpy(dtype=np.float64)
    finite = np.isfinite(values).all(axis=1)
    score = np.full(len(df), np.nan)
    if finite.any():
        score[finite] = model.predict_proba(values[finite])[:, 1]
    return score, finite


# --------------------------------------------------------------------------
# Boundary optimisation
# --------------------------------------------------------------------------


def run_boundary_optimization(
    df: pd.DataFrame, cfg: Mapping[str, Any]
) -> dict[str, Any]:
    """Optimise the hadronic BDT boundaries on the 36 fb^-1 expected-yield model."""
    model_rows = df[
        df["passes_hadronic_preselection"]
        & df["bdt_score"].notna()
        & df["model_component"].isin(
            ["signal_ttH_tH", "resonant_higgs_bkg", "nti_continuum_bkg"]
        )
    ]

    payload = pd.DataFrame(
        {
            "score": model_rows["bdt_score"].to_numpy(dtype=float),
            "is_signal": (model_rows["model_component"] == "signal_ttH_tH").to_numpy(),
            "weight": model_rows["significance_model_weight_36fb"].to_numpy(dtype=float),
        }
    )
    result = optimize_bdt_boundaries(payload, cfg["optimization"])

    # Robustness cross-check on the held-out test partition, scaled up by the
    # inverse test fraction.
    test = model_rows[model_rows["partition"] == "test"]
    frac = float(cfg["partition"]["fractions"]["test"])
    if len(test) > 0 and frac > 0:
        payload_test = pd.DataFrame(
            {
                "score": test["bdt_score"].to_numpy(dtype=float),
                "is_signal": (test["model_component"] == "signal_ttH_tH").to_numpy(),
                "weight": test["significance_model_weight_36fb"].to_numpy(dtype=float)
                / frac,
            }
        )
        cross = optimize_bdt_boundaries(payload_test, cfg["optimization"])
    else:
        cross = {"status": "unavailable"}

    result["weights_used"] = (
        "significance_model_weight_36fb (physical 36 fb^-1 yields); the "
        "class-balanced bdt_fit_weight is NEVER used for yields or significance"
    )
    result["rows_used"] = int(len(model_rows))
    result["observed_ti_signal_window_used"] = False
    result["test_partition_crosscheck"] = {
        "thresholds": cross.get("thresholds"),
        "best_significance": cross.get("best_significance"),
        "status": cross.get("status"),
        "note": "test-partition-only optimisation with weights scaled by "
        "1/test-fraction; diagnostic only, not used for the final boundaries",
    }
    return result
