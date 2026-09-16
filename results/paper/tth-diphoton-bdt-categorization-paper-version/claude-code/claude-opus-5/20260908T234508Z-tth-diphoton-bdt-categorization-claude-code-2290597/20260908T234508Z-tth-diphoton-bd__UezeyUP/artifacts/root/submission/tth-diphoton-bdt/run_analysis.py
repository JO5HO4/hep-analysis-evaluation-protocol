#!/usr/bin/env python3
"""End-to-end driver for the top-associated H -> gamma gamma BDT categorization.

Usage
-----
    TB_HYY_INPUTS=/data/GamGam python3 run_analysis.py [--config config/config.yaml]

Deterministic and uncapped by default.  ``TTH_MAX_SELECTED_PER_SAMPLE`` limits
the number of selected rows per sample only when explicitly set.
"""

from __future__ import annotations

import os

# Single-threaded numeric backends -> bit-level reproducibility.
for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_var, "1")

import argparse  # noqa: E402
import datetime as _dt  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analysis import bdt as bdt_mod  # noqa: E402
from analysis import categorization as cat_mod  # noqa: E402
from analysis import plotting  # noqa: E402
from analysis import preselection as pre_mod  # noqa: E402
from analysis.common import (  # noqa: E402
    Paths,
    environment_record,
    load_config,
    resolve_runtime,
    write_json,
    write_yaml,
)
from analysis.inputs import EXCLUSION_STATEMENT, resolve_inputs  # noqa: E402
from analysis.top_categorization import BDT_FEATURES, CATEGORY_ORDER  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=None)
    parser.add_argument("--skip-fit", action="store_true")
    args = parser.parse_args()

    t_start = time.perf_counter()
    stage_times: dict[str, float] = {}

    def mark(name: str, t0: float) -> None:
        stage_times[name] = time.perf_counter() - t0

    cfg_raw = load_config(args.config)
    cfg = resolve_runtime(cfg_raw)
    paths = Paths(Path(cfg["run"]["results_dir"]))
    np.random.seed(int(cfg["run"]["seed"]))

    print(f"[1/12] results -> {paths.root}")
    write_yaml(paths("config_resolved.yaml"), cfg)

    # ---------------- inputs ----------------
    t0 = time.perf_counter()
    contract = resolve_inputs(cfg)
    write_json(paths("input_data_contract.json"), contract)
    if contract["missing_files"]:
        raise FileNotFoundError(f"missing input files: {contract['missing_files']}")
    mark("resolve_inputs", t0)

    object_record = pre_mod.object_definition_record(cfg)
    write_json(paths("object_definition_record.json"), object_record)

    # ---------------- preselection ----------------
    print("[2/12] preselection")
    t0 = time.perf_counter()
    frames, cutflows, checks = [], [], []
    for sample in contract["resolved_samples"]:
        df_s, cf = pre_mod.process_sample(sample, cfg)
        frames.append(df_s)
        cutflows.append(cf)
        checks.append(pre_mod.crosscheck_scalar_vs_vectorised(sample, cfg, df_s))
        print(f"       {sample['sample']:>5s}: {len(df_s):7d} selected rows")
    df = pd.concat(frames, ignore_index=True)
    mark("preselection", t0)

    write_json(
        paths("cutflow.json"),
        {
            "stage_order": pre_mod.CUTFLOW_STAGES,
            "weighted_column": "weight_mc_36fb (MC only; data rows are unweighted)",
            "signed_weight_bookkeeping": "each stage records the sum of positive "
            "weights, the sum of negative weights and the number of "
            "negative-weight events",
            "row_cap_policy": cfg["run"]["row_cap_policy"],
            "per_sample": cutflows,
        },
    )

    presel_summary = pre_mod.preselection_summary(df, cfg, object_record)
    presel_summary["scalar_vs_vectorised_crosscheck"] = checks
    write_json(paths("preselection_summary.json"), presel_summary)

    t0 = time.perf_counter()
    presel_plots = plotting.plot_preselection(df, cfg, paths("plots"))
    mark("preselection_plots", t0)

    # ---------------- NTI proxy + model weights ----------------
    print("[3/12] NTI continuum proxy normalisation")
    sf = bdt_mod.compute_nti_scale_factors(df, cfg)
    df = bdt_mod.add_model_weights(df, sf)

    # ---------------- training sample ----------------
    print("[4/12] BDT training sample")
    t0 = time.perf_counter()
    train_rows, balance = bdt_mod.build_training_sample(df, cfg, sf)
    write_json(
        paths("model", "background_mixture_and_normalization.json"),
        {
            "nti_scale_factors": sf,
            "background_mixture": balance["background_mixture"],
            "component_signed_weight_sums": balance["component_signed_weight_sums"],
            "component_raw_rows": balance["component_raw_rows"],
            "signal_definition": {
                "samples": list(bdt_mod.SIGNAL_SAMPLES),
                "selection": "TI diphoton, hadronic preselection, 125 +/- 2 GeV",
                "weight": "SM-normalised MC weight: xsec[pb] * k-factor * filter "
                "efficiency / signed generator-weight sum * generator weight * "
                "available per-event scale factors (pileup, photon, b-tag, JVT), "
                "scaled to the observed-data luminosity",
            },
            "luminosity_fb": cfg["normalization"]["luminosity_fb"],
            "scale_factor_branches": cfg["normalization"]["scale_factors"],
            "blinding": balance["blinding"],
        },
    )
    write_json(paths("model", "class_balance_check.json"), balance)
    train_rows.to_csv(paths("model", "training_sample.csv"), index=False)
    mark("training_sample", t0)

    # ---------------- training ----------------
    print("[5/12] BDT training")
    t0 = time.perf_counter()
    model, meta = bdt_mod.train_classifier(train_rows, cfg)
    mark("bdt_training", t0)
    model_path = paths("model", "bdt_model.pkl")
    with open(model_path, "wb") as handle:
        pickle.dump(model, handle)
    meta["model"]["artifact_path"] = str(model_path)
    meta["nti_scale_factors"] = {k: sf[k] for k in ("SF1", "SF2", "SF1xSF2")}
    meta["class_balance"] = {
        "before": balance["before_balancing"],
        "after": balance["after_balancing"],
    }
    write_json(paths("model", "training_metadata.json"), meta)

    # ---------------- inference ----------------
    print("[6/12] inference")
    t0 = time.perf_counter()
    features = list(cfg["bdt"]["features"])
    score, finite = bdt_mod.score_dataframe(model, df, features)
    df["bdt_score"] = score
    df["bdt_inputs_finite"] = finite
    train_ids = set(train_rows.loc[train_rows["partition"] == "train", "event_id"])
    df["used_in_bdt_training"] = df["event_id"].isin(train_ids)
    df["training_role"] = np.where(
        df["event_id"].isin(set(train_rows["event_id"])),
        "training-sample-" + df["partition"].astype(str),
        "not-in-training-sample",
    )
    mark("inference", t0)

    # ---------------- boundary optimisation ----------------
    print("[7/12] BDT boundary optimisation")
    t0 = time.perf_counter()
    opt = bdt_mod.run_boundary_optimization(df, cfg)
    thresholds = list(opt["thresholds"])
    mark("boundary_optimization", t0)
    write_json(
        paths("optimization", "thresholds.json"),
        {
            "thresholds_descending": thresholds,
            "n_boundaries": len(thresholds),
            "category_mapping": {
                f"ttH_had_BDT{i + 1}": {
                    "score_low": t,
                    "score_high": 1.0 if i == 0 else thresholds[i - 1],
                }
                for i, t in enumerate(thresholds)
            },
            "stopping_rule": "add a boundary only while the relative improvement "
            "in expected significance w.r.t. the previous iteration is >= 5%",
            "min_relative_improvement": cfg["optimization"]["min_relative_improvement"],
            "status": opt["status"],
            "best_combined_significance": opt["best_significance"],
            "weights_used": opt["weights_used"],
            "observed_ti_signal_window_used": False,
            "test_partition_crosscheck": opt["test_partition_crosscheck"],
        },
    )
    write_json(
        paths("optimization", "accepted_splits.json"),
        {
            "accepted_boundary_sequence": [
                s["candidate_boundary"] for s in opt["accepted_splits"]
            ],
            "accepted_splits": opt["accepted_splits"],
            "all_iterations_including_rejected": opt["iterations"],
            "min_relative_improvement": cfg["optimization"]["min_relative_improvement"],
            "config": opt["config"],
            "status": opt["status"],
        },
    )

    # ---------------- categorization ----------------
    print("[8/12] categorization")
    t0 = time.perf_counter()
    df, retention = cat_mod.assign_categories(df, thresholds, cfg)
    summary, cat_manifest, combined_z = cat_mod.category_summary(df, retention, cfg)
    cat_manifest["bdt_boundaries"] = thresholds
    cat_manifest["nti_scale_factors"] = {k: sf[k] for k in ("SF1", "SF2", "SF1xSF2")}
    mark("categorization", t0)

    write_json(paths("categorization", "category_retention.json"), retention)
    summary.to_csv(paths("categorization", "category_summary.csv"), index=False)
    write_json(paths("categorization", "categorization_manifest.json"), cat_manifest)
    component_yields = {
        row["category"]: {
            k: row[k]
            for k in (
                "signal_ttH_tH_yield",
                "resonant_higgs_bkg_yield",
                "nti_continuum_bkg_yield",
                "total_background_yield",
                "total_model_yield",
                "S_over_B",
                "S_over_sqrtB",
                "expected_counting_significance",
                "signal_raw_rows",
                "resonant_raw_rows",
                "nti_proxy_raw_rows",
                "observed_ti_sideband_rows",
            )
        }
        for _, row in summary.iterrows()
    }
    write_json(
        paths("categorization", "category_component_yields.json"),
        {
            "luminosity_fb": cfg["normalization"]["luminosity_fb"],
            "weight": "significance_model_weight_36fb",
            "components": {
                "signal_ttH_tH": "ttH + tH TI MC in 125 +/- 2 GeV @ 36 fb^-1",
                "resonant_higgs_bkg": "non-top Higgs TI MC in 125 +/- 2 GeV @ 36 fb^-1",
                "nti_continuum_bkg": "observed-data NTI sideband rows x SF1*SF2",
            },
            "per_category": component_yields,
            "combined_expected_counting_significance": combined_z,
        },
    )
    write_json(
        paths("category_yields_36fb.json"),
        {
            "luminosity_fb": cfg["normalization"]["luminosity_fb"],
            "weight_column": "significance_model_weight_36fb",
            "blinding": cat_manifest["blinding"],
            "categories": json.loads(summary.to_json(orient="records")),
            "combined_expected_counting_significance": combined_z,
            "kept_categories": retention["kept_categories"],
            "dropped_categories": retention["dropped_categories"],
        },
    )

    # ---------------- event-level outputs ----------------
    print("[9/12] event tables")
    t0 = time.perf_counter()
    df.to_csv(paths("preselected_events.csv"), index=False)

    pred_cols = [
        "event_id", "sample", "process", "process_role", "is_mc", "is_data",
        "channel_number", "run_number", "event_number", "m_gammagamma", "pt_gg",
        "photon_ti", "photon_nti", "mgg_region", "in_signal_window", "in_sideband",
        "passes_hadronic_preselection", "passes_leptonic_preselection",
        "preselection_channel", "partition", "training_role", "used_in_bdt_training",
        *features, "bdt_score", "bdt_inputs_finite", "category", "category_is_kept",
        "weight_mc_36fb", "significance_model_weight_36fb", "nti_continuum_weight",
        "observed_data_weight", "model_component",
    ]
    df[pred_cols].to_csv(paths("predictions.csv"), index=False)

    had = df[df["passes_hadronic_preselection"]]
    had_cols = [
        "event_id", "sample", "process", "process_role", "m_gammagamma",
        "n_electrons", "n_muons", "n_leptons", "n_jets", "n_jets_central",
        "n_jets_forward", "n_bjets", "n_bjets_central", "ht_jets", "lead_jet_pt",
        "sublead_jet_pt", "met", "pt_gg", "delta_r_gg", "photon_ti", "partition",
        "bdt_score", "category", "significance_model_weight_36fb",
    ]
    had[had_cols].to_csv(paths("hadronic_features.csv"), index=False)

    inference_cols = pred_cols + [
        "delta_r_gg", "lead_photon_pt", "sublead_photon_pt", "n_leptons", "n_jets",
        "n_jets_forward", "n_bjets_central", "lead_jet_pt", "sublead_jet_pt",
        "mc_generator_weight", "weight_sm_per_pb", "mc_model_weight_36fb",
    ]
    inference_cols = list(dict.fromkeys(inference_cols))
    df[inference_cols].to_csv(paths("inference", "events_with_bdt_scores.csv"), index=False)

    had_scored = had["bdt_score"].notna()
    scores_finite = df.loc[df["bdt_score"].notna(), "bdt_score"]
    category_codes = {name: i for i, name in enumerate(CATEGORY_ORDER)}
    write_json(
        paths("inference", "inference_manifest.json"),
        {
            "model_path": str(model_path),
            "model_kind": cfg["bdt"]["model"]["kind"],
            "feature_list": features,
            "m_gammagamma_used_as_input": False,
            "n_selected_rows": int(len(df)),
            "n_selected_hadronic_rows": int(len(had)),
            "n_selected_leptonic_bookkeeping_rows": int(
                (df["passes_leptonic_preselection"] & ~df["passes_hadronic_preselection"]).sum()
            ),
            "n_scored_rows": int(df["bdt_score"].notna().sum()),
            "n_unscored_rows": int(df["bdt_score"].isna().sum()),
            "n_hadronic_scored_rows": int(had_scored.sum()),
            "n_hadronic_unscored_rows": int((~had_scored).sum()),
            "all_hadronic_rows_with_finite_features_scored": bool(
                (~had_scored).sum() == 0
            ),
            "score_range": [float(scores_finite.min()), float(scores_finite.max())],
            "score_in_unit_interval": bool(
                (scores_finite >= 0).all() and (scores_finite <= 1).all()
            ),
            "score_all_finite": bool(np.isfinite(scores_finite.to_numpy()).all()),
            "leptonic_rows_scored": True,
            "leptonic_rows_note": "optional bookkeeping rows are also scored, but "
            "they are excluded from categorization, significance and the workspace",
            "preserved_columns": inference_cols,
            "categorical_code_maps": {
                "category": category_codes,
                "preselection_channel": {"hadronic": 0, "leptonic_bookkeeping": 1},
                "process": {
                    name: i
                    for i, name in enumerate(sorted(df["process"].unique()))
                },
                "process_role": {
                    name: i
                    for i, name in enumerate(sorted(df["process_role"].unique()))
                },
                "partition": {"train": 0, "val": 1, "test": 2},
                "model_component": {
                    name: i
                    for i, name in enumerate(sorted(df["model_component"].unique()))
                },
            },
            "code_map_note": "a ROOT inference tree may encode the string columns "
            "above as integer codes using these maps",
            "csv_path": str(paths("inference", "events_with_bdt_scores.csv")),
        },
    )
    mark("event_tables", t0)

    # ---------------- histograms + categorization plots ----------------
    print("[10/12] histograms and plots")
    t0 = time.perf_counter()
    shape_hist = cat_mod.score_shape_histograms(df, cfg)
    write_json(paths("plots", "score_by_component_histograms.json"), shape_hist)
    score_shape_plots = plotting.plot_score_shapes(
        shape_hist, paths("plots", "score_by_component_shape_bdt_v1")
    )

    model_hist = cat_mod.bdt_score_model_histograms(df, cfg, thresholds)
    write_json(
        paths("categorization", "histograms", "bdt_score_model_component_histograms.json"),
        model_hist,
    )
    mgg_hist = cat_mod.category_mgg_histograms(df, retention, sf, cfg)
    write_json(
        paths("categorization", "histograms", "category_mgg_control_histograms.json"),
        mgg_hist,
    )

    cat_plots = []
    cat_plots += plotting.plot_category_yields(
        summary, paths("categorization", "plots", "category_expected_yields_36fb_v1")
    )
    cat_plots += plotting.plot_category_significance(
        summary,
        combined_z,
        paths("categorization", "plots", "category_expected_counting_z_36fb_v1"),
    )
    cat_plots += plotting.plot_bdt_model_components(
        model_hist,
        paths("categorization", "plots", "bdt_score_model_components_36fb_v1"),
    )
    cat_plots += plotting.plot_bdt_model_components(
        model_hist,
        paths(
            "categorization", "plots", "bdt_score_model_components_with_boundaries_36fb_v1"
        ),
        boundaries=thresholds,
    )
    cat_plots += plotting.plot_category_mgg_shapes(
        mgg_hist, paths("categorization", "plots", "category_mgg_control_shapes_36fb_v1")
    )
    mark("histograms_and_plots", t0)

    # ---------------- workspace + Asimov significance ----------------
    print("[11/12] RooFit workspace and Asimov expected significance")
    t0 = time.perf_counter()
    fit_result: dict | None = None
    fit_error: str | None = None
    if not args.skip_fit:
        from analysis import fitting

        try:
            fit_result = fitting.build_workspace_and_significance(
                df, retention, sf, cfg, paths("fit", "FIT1")
            )
        except Exception as exc:  # pragma: no cover
            import traceback

            fit_error = f"{type(exc).__name__}: {exc}"
            traceback.print_exc()
    mark("workspace_fit", t0)

    fit_plots: list[str] = []
    t0 = time.perf_counter()
    if fit_result is not None:
        sideband_files = plotting.plot_sideband_fits(
            fit_result["sideband_plots"], paths("fit", "FIT1", "plots")
        )
        asimov_files, asimov_payload = plotting.plot_asimov_fit(
            fit_result, paths("fit", "FIT1", "plots")
        )
        fit_plots = (
            [f for files in sideband_files["per_category"].values() for f in files]
            + sideband_files["combined_summary"]
            + asimov_files
        )
        _write_fit_artifacts(
            paths, cfg, fit_result, sideband_files, asimov_payload, combined_z, sf
        )
    mark("workspace_fit_plots", t0)

    # ---------------- metrics + manifest + report ----------------
    print("[12/12] metrics, manifest, report")
    metrics = _build_metrics(
        df, summary, meta, opt, sf, balance, retention, combined_z, fit_result,
        fit_error, cfg, stage_times, checks,
    )
    write_json(paths("metrics.json"), metrics)

    total_wall = time.perf_counter() - t_start
    manifest = {
        "run_name": cfg["run"]["name"],
        "generated_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "total_wall_time_seconds": total_wall,
        "stage_durations_seconds": stage_times,
        "bdt_training_wall_time_seconds": meta["timing"]["training_wall_time_seconds"],
        "config_path": cfg.get("_config_path"),
        "results_dir": str(paths.root),
        "submission_dir": str(Path(__file__).resolve().parent),
        "deterministic": True,
        "seed": cfg["run"]["seed"],
        "row_cap": {
            "max_selected_per_sample": cfg["run"]["max_selected_per_sample"],
            "source": cfg["run"]["max_selected_per_sample_source"],
            "uncapped": cfg["run"]["max_selected_per_sample"] is None,
            "env_var": cfg["run"]["max_selected_per_sample_env"],
        },
        "input_scope": {
            "statement": EXCLUSION_STATEMENT,
            "nominal_higgs_signal_mc_only": True,
            "mc_samples_processed": sorted(
                df[df["is_mc"]]["process"].unique().tolist()
            ),
            "data_samples_processed": sorted(
                df[df["is_data"]]["process"].unique().tolist()
            ),
            "sherpa_yy_processed": False,
            "prompt_diphoton_continuum_mc_processed": False,
            "non_higgs_mc_processed": False,
            "inputs_copied_into_submission": False,
            "input_root": contract["input_root"],
            "input_env_var": contract["environment_variable"],
        },
        "categorization": {
            "required_categories": [c for c in CATEGORY_ORDER if c != "unassigned"],
            "kept_categories": retention["kept_categories"],
            "dropped_categories": retention["dropped_categories"],
            "hadronic_only": True,
            "leptonic_in_scope": False,
        },
        "blinding": cat_manifest["blinding"],
        "expected_significance": {
            "combined_counting": combined_z,
            "asimov_roofit_expected_Z": fit_result["expected_Z"] if fit_result else None,
            "observed": "blocked (blinded)",
        },
        "environment": environment_record(),
        "artifacts": _artifact_index(paths),
        "plots": {
            "preselection": presel_plots,
            "score_shape": score_shape_plots,
            "categorization": cat_plots,
            "fit": fit_plots,
        },
    }
    write_json(paths("run_manifest.json"), manifest)

    from analysis.report import write_report

    write_report(
        paths, cfg, contract, object_record, presel_summary, cutflows, meta, balance,
        sf, opt, thresholds, summary, retention, cat_manifest, combined_z, fit_result,
        fit_error, metrics, manifest,
    )

    print(f"done in {total_wall:.1f}s -> {paths.root}")
    return 0


def _write_fit_artifacts(paths, cfg, fit, sideband_files, asimov_payload, combined_z, sf):
    out = lambda *p: paths("fit", "FIT1", *p)  # noqa: E731
    backend = {
        "backend": "ROOT/PyROOT/RooFit",
        "root_version": environment_record()["packages"]["ROOT"],
        "workspace_class": "RooWorkspace",
        "model_class": "RooSimultaneous over RooAddPdf per category",
        "minimizer": "Minuit2/migrad + hesse (RooMinimizer)",
        "likelihood": "RooAddition of per-category extended NLLs (shared mu)",
        "combined_asimov_dataset_written": fit["combined_asimov_dataset"],
        "hs3_json_export": fit["hs3_export_ok"],
        "hs3_json_export_error": fit["hs3_export_error"],
    }
    write_json(out("backend.json"), backend)

    results = {
        "categories": fit["categories"],
        "mu_hat": fit["mu_hat"],
        "mu_uncertainty": fit["mu_uncertainty"],
        "free_mu_fit": fit["free_fit"],
        "mu0_fit": fit["conditional_fit"],
        "q0": fit["q0"],
        "expected_Z": fit["expected_Z"],
        "mu_gen": fit["mu_gen"],
        "per_category": fit["per_category"],
        "fit_statuses": {
            "free_mu": fit["free_fit"]["fit_status"],
            "mu0": fit["conditional_fit"]["fit_status"],
        },
        "covariance_qualities": {
            "free_mu": fit["free_fit"]["cov_quality"],
            "mu0": fit["conditional_fit"]["cov_quality"],
        },
        "observed_significance": "blocked (observed TI data in 125 +/- 2 GeV is blinded)",
    }
    write_json(out("results.json"), results)
    write_json(
        out("significance_asimov.json"),
        {
            "method": "asymptotic likelihood-ratio discovery test statistic on "
            "signal+background Asimov data",
            "mu_gen": fit["mu_gen"],
            "mu_hat": fit["mu_hat"],
            "mu_uncertainty": fit["mu_uncertainty"],
            "q0": fit["q0"],
            "expected_Z": fit["expected_Z"],
            "shared_signal_strength": True,
            "categories": fit["categories"],
            "observed_Z": None,
            "observed_blocked": True,
        },
    )
    write_json(
        out("significance.json"),
        {
            "expected_asimov_Z_roofit": fit["expected_Z"],
            "expected_combined_counting_Z": combined_z,
            "observed_Z": None,
            "observed_status": "blocked - observed TI data in the 125 +/- 2 GeV "
            "signal window is blinded; an explicit unblinding step is required",
            "q0": fit["q0"],
            "mu_hat": fit["mu_hat"],
            "mu_uncertainty": fit["mu_uncertainty"],
        },
    )
    write_json(
        out("significance_asimov_construction.json"),
        {
            "strategy": [
                "1. per category: model = mu*(ttH+tH signal) + fixed resonant-Higgs "
                "background + floating smooth continuum background",
                "2. the continuum PDF and its normalisation are determined from "
                "OBSERVED TI DATA SIDEBANDS ONLY (105-120, 130-160 GeV) and "
                "extrapolated over the full 105-160 GeV fit range",
                "3. S+B Asimov pseudo-data generated with mu_gen = 1",
                "4. free-mu fit -> mu_hat, NLL_min; mu = 0 fit -> NLL_0",
                "5. q0 = 2*(NLL_0 - NLL_min); expected Z = sqrt(q0)",
            ],
            "shared_mu": "one signal-strength parameter multiplies the ttH+tH "
            "component in every hadronic category",
            "signal_template": "ttH + tH TI MC (shape and normalisation)",
            "resonant_background_template": "non-top Higgs TI MC (fixed)",
            "continuum_template": "observed TI data sidebands (floating normalisation "
            "and floating shape parameters)",
            "distinct_from_nti_proxy": "the NTI proxy is used for BDT training and "
            "categorization control estimates; the workspace continuum is taken "
            "from observed TI data sidebands only",
            "luminosity_fb": cfg["normalization"]["luminosity_fb"],
            "fit_range_gev": fit["mgg_range"],
            "sidebands_gev": fit["sidebands"],
            "binning": fit["binning"],
            "per_category": fit["per_category"],
            "nti_scale_factors_for_reference": {
                k: sf[k] for k in ("SF1", "SF2", "SF1xSF2")
            },
            "blinding": "observed TI data in 125 +/- 2 GeV never read",
        },
    )
    write_json(out("significance_asimov_plot_payload.json"), asimov_payload)
    write_json(
        out("sideband_fit_plots.json"),
        {
            "description": "per-category observed-TI-sideband continuum fit "
            "diagnostics: observed sideband data, fitted PDF, blinded window and "
            "explicit m_gammagamma binning",
            "plot_files": sideband_files,
            "per_category_payload": fit["sideband_plots"],
        },
    )
    write_json(
        out("background_pdf_scan.json"),
        {
            "criterion": "minimum AIC = 2k + 2*NLL among converged candidates",
            "candidates": list(cfg["fit"]["background_pdf_candidates"]),
            "fit_ranges": "SBLO (105-120 GeV) + SBHI (130-160 GeV), observed TI data only",
            "per_category": fit["background_pdf_scan"],
        },
    )
    write_json(
        out("background_pdf_choice.json"),
        {
            "per_category_choice": {
                c: fit["background_pdf_scan"][c]["selected"] for c in fit["categories"]
            },
            "criterion": "minimum AIC",
            "source_of_continuum": "observed TI data sidebands only",
            "normalisation": "sideband count / PDF sideband fraction, extrapolated "
            "to the full 105-160 GeV range; the yield floats in the fit",
        },
    )
    write_json(
        out("background_template_selection.json"),
        {
            "continuum_background": {
                "source": "observed TI data sidebands (105-120, 130-160 GeV)",
                "not_used": "NTI proxy is NOT used in the statistical workspace",
                "per_category_pdf": {
                    c: fit["background_pdf_scan"][c]["selected"] for c in fit["categories"]
                },
                "per_category_sideband_events": {
                    c: fit["background_pdf_scan"][c]["n_ti_sideband_events"]
                    for c in fit["categories"]
                },
            },
            "resonant_higgs_background": {
                "source": "non-top Higgs TI MC (ggH, VBF, WH, ZH, ggZH), normalisation fixed",
                "per_category_yield_36fb": {
                    c: fit["resonant_pdf"][c]["expected_yield_36fb_full_range"]
                    for c in fit["categories"]
                },
            },
            "signal": {
                "source": "ttH + tH TI MC",
                "per_category_yield_36fb": {
                    c: fit["signal_pdf"][c]["expected_yield_36fb_full_range"]
                    for c in fit["categories"]
                },
            },
        },
    )
    write_json(out("signal_pdf.json"), {
        "pdf": "RooGaussian", "template": "ttH + tH TI MC",
        "fit_note": "fitted to the weighted m_gammagamma template histogram; "
        "shape parameters are frozen in the workspace",
        "per_category": fit["signal_pdf"],
    })
    write_json(out("resonant_higgs_pdf.json"), {
        "pdf": "RooGaussian",
        "template": "non-top Higgs TI MC (ggH, VBF, WH, ZH, ggZH)",
        "normalisation": "fixed to the SM expectation at 36 fb^-1",
        "per_category": fit["resonant_pdf"],
    })
    write_json(
        paths("workspace_manifest.json"),
        {
            "backend": "ROOT/PyROOT/RooFit",
            "workspace_name": "tth_hyy_hadronic",
            "workspace_root": str(paths("fit", "FIT1", "workspace.root")),
            "workspace_json": str(paths("fit", "workspace.json")),
            "hs3_export_ok": fit["hs3_export_ok"],
            "categories": fit["categories"],
            "leptonic_rows_excluded": True,
            "observable": {"name": "m_yy", "range_gev": fit["mgg_range"],
                           "bins": fit["binning"]["n_bins"]},
            "parameters_of_interest": ["mu"],
            "shared_mu": True,
            "model": "mu*(ttH+tH) + fixed resonant Higgs + floating smooth continuum",
            "continuum_source": "observed TI data sidebands only",
            "mu_gen": fit["mu_gen"],
            "mu_hat": fit["mu_hat"],
            "mu_uncertainty": fit["mu_uncertainty"],
            "fit_statuses": results["fit_statuses"],
            "covariance_qualities": results["covariance_qualities"],
            "q0": fit["q0"],
            "expected_Z": fit["expected_Z"],
            "observed_significance": "blocked (blinded)",
            "per_category": fit["per_category"],
        },
    )
    if not fit["hs3_export_ok"]:
        write_json(
            paths("fit", "workspace.json"),
            {
                "format": "custom workspace description (HS3 export unavailable: "
                f"{fit['hs3_export_error']})",
                "backend": "ROOT/PyROOT/RooFit",
                "workspace_name": "tth_hyy_hadronic",
                "root_file": str(paths("fit", "FIT1", "workspace.root")),
                "observable": {"name": "m_yy", "range_gev": fit["mgg_range"],
                               "bins": fit["binning"]["n_bins"]},
                "parameters_of_interest": {"mu": {"value": fit["mu_hat"],
                                                  "error": fit["mu_uncertainty"],
                                                  "shared_across_categories": True}},
                "categories": {
                    c: {
                        "pdf": "RooAddPdf(mu*nsig*signal + nres*resonant + nbkg*continuum)",
                        "signal": fit["signal_pdf"][c],
                        "resonant": fit["resonant_pdf"][c],
                        "continuum_pdf": fit["background_pdf_scan"][c]["selected"],
                        "continuum_yield_extrapolated": fit["sideband_plots"][c][
                            "fitted_full_range_yield"
                        ],
                        "n_ti_sideband_events": fit["sideband_plots"][c][
                            "n_ti_sideband_events"
                        ],
                        "asimov_dataset": f"asimov_{c}",
                    }
                    for c in fit["categories"]
                },
                "asimov": {"mu_gen": fit["mu_gen"],
                           "combined_dataset": fit["combined_asimov_dataset"]},
            },
        )


def _build_metrics(
    df, summary, meta, opt, sf, balance, retention, combined_z, fit_result, fit_error,
    cfg, stage_times, checks,
):
    had = df[df["passes_hadronic_preselection"]]
    return {
        "counts": {
            "selected_rows": int(len(df)),
            "hadronic_rows": int(len(had)),
            "leptonic_bookkeeping_rows": int(
                (df["passes_leptonic_preselection"] & ~df["passes_hadronic_preselection"]).sum()
            ),
            "scored_rows": int(df["bdt_score"].notna().sum()),
            "hadronic_scored_rows": int(had["bdt_score"].notna().sum()),
            "by_process": {k: int(v) for k, v in df["process"].value_counts().items()},
            "by_category": {k: int(v) for k, v in df["category"].value_counts().items()},
        },
        "weighted_yields_36fb": {
            "mc_all_selected": float(df["weight_mc_36fb"].sum()),
            "signal_window_model": float(df["significance_model_weight_36fb"].sum()),
            "signed_weight_bookkeeping": {
                "n_negative_weight_mc_rows": int((df["weight_mc_36fb"] < 0).sum()),
                "sum_positive": float(df.loc[df["weight_mc_36fb"] > 0, "weight_mc_36fb"].sum()),
                "sum_negative": float(df.loc[df["weight_mc_36fb"] < 0, "weight_mc_36fb"].sum()),
            },
        },
        "nti_scale_factors": {k: sf[k] for k in ("SF1", "SF2", "SF1xSF2")},
        "bdt": {
            "features": list(BDT_FEATURES),
            "hyperparameters": meta["model"]["hyperparameters"],
            "weighted_auc": meta["performance"],
            "training_wall_time_seconds": meta["timing"]["training_wall_time_seconds"],
            "class_balance_before": balance["before_balancing"],
            "class_balance_after": balance["after_balancing"],
            "score_range": [
                float(df["bdt_score"].min()),
                float(df["bdt_score"].max()),
            ],
        },
        "optimization": {
            "thresholds": opt["thresholds"],
            "status": opt["status"],
            "best_combined_significance": opt["best_significance"],
            "relative_improvements": [
                s["relative_improvement"] for s in opt["accepted_splits"]
            ],
        },
        "categorization": {
            "kept_categories": retention["kept_categories"],
            "dropped_categories": retention["dropped_categories"],
            "combined_expected_counting_significance": combined_z,
            "per_category": json.loads(summary.to_json(orient="records")),
        },
        "statistical_interpretation": (
            {
                "backend": "ROOT/PyROOT/RooFit",
                "mu_hat": fit_result["mu_hat"],
                "mu_uncertainty": fit_result["mu_uncertainty"],
                "q0": fit_result["q0"],
                "expected_Z": fit_result["expected_Z"],
                "observed": "blocked (blinded)",
            }
            if fit_result
            else {"status": "unavailable", "error": fit_error}
        ),
        "validation": {
            "scalar_vs_vectorised_crosscheck": checks,
            "all_hadronic_rows_scored": bool(had["bdt_score"].notna().all()),
            "bdt_score_within_unit_interval": bool(
                df["bdt_score"].dropna().between(0.0, 1.0).all()
            ),
            "m_gammagamma_excluded_from_features": "m_gammagamma" not in list(BDT_FEATURES),
        },
        "timing_seconds": stage_times,
        "row_cap": {
            "max_selected_per_sample": cfg["run"]["max_selected_per_sample"],
            "uncapped": cfg["run"]["max_selected_per_sample"] is None,
        },
    }


def _artifact_index(paths) -> list[str]:
    root = paths.root
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
