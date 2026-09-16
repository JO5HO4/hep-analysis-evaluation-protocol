"""Generate ``report.md`` at the result-directory root."""

from __future__ import annotations

from typing import Any

import pandas as pd

SECTIONS = [
    "Introduction",
    "Data and Monte Carlo Samples",
    "Object Definition and Event Selection",
    "Overview of the Analysis Strategy",
    "Signal and Control Regions",
    "Cut Flow",
    "Distributions in Signal and Control Regions",
    "Categorization",
    "Systematic Uncertainties",
    "Statistical Interpretation",
    "Artifact Checklist",
    "Summary",
]

REQUIRED_ARTIFACTS = [
    "config_resolved.yaml",
    "input_data_contract.json",
    "object_definition_record.json",
    "preselection_summary.json",
    "cutflow.json",
    "metrics.json",
    "preselected_events.csv",
    "predictions.csv",
    "hadronic_features.csv",
    "inference/inference_manifest.json",
    "inference/events_with_bdt_scores.csv",
    "category_yields_36fb.json",
    "categorization/categorization_manifest.json",
    "categorization/category_summary.csv",
    "categorization/category_component_yields.json",
    "categorization/category_retention.json",
    "categorization/histograms/category_mgg_control_histograms.json",
    "categorization/histograms/bdt_score_model_component_histograms.json",
    "categorization/plots/category_expected_yields_36fb_v1.png",
    "categorization/plots/category_expected_yields_36fb_v1.pdf",
    "categorization/plots/category_expected_counting_z_36fb_v1.png",
    "categorization/plots/category_expected_counting_z_36fb_v1.pdf",
    "categorization/plots/bdt_score_model_components_36fb_v1.png",
    "categorization/plots/bdt_score_model_components_36fb_v1.pdf",
    "categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png",
    "categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf",
    "categorization/plots/category_mgg_control_shapes_36fb_v1.png",
    "categorization/plots/category_mgg_control_shapes_36fb_v1.pdf",
    "workspace_manifest.json",
    "fit/workspace.json",
    "fit/FIT1/workspace.root",
    "fit/FIT1/results.json",
    "fit/FIT1/significance_asimov.json",
    "fit/FIT1/significance_asimov_construction.json",
    "fit/FIT1/significance_asimov_plot_payload.json",
    "fit/FIT1/sideband_fit_plots.json",
    "fit/FIT1/significance.json",
    "fit/FIT1/backend.json",
    "fit/FIT1/background_pdf_choice.json",
    "fit/FIT1/background_pdf_scan.json",
    "fit/FIT1/background_template_selection.json",
    "fit/FIT1/signal_pdf.json",
    "fit/FIT1/resonant_higgs_pdf.json",
    "fit/FIT1/plots/sidebands_background_fit.png",
    "fit/FIT1/plots/sidebands_background_fit.pdf",
    "fit/FIT1/plots/asimov_sb_fit.png",
    "fit/FIT1/plots/asimov_sb_fit.pdf",
    "model/training_metadata.json",
    "model/background_mixture_and_normalization.json",
    "model/class_balance_check.json",
    "model/training_sample.csv",
    "optimization/thresholds.json",
    "optimization/accepted_splits.json",
    "plots/score_by_component_shape_bdt_v1.png",
    "plots/score_by_component_shape_bdt_v1.pdf",
    "plots/score_by_component_histograms.json",
    "plots/preselection_mass.png",
    "plots/preselection_channels.png",
    "plots/preselection_processes.png",
    "report.md",
    "run_manifest.json",
]


def _fmt(x: Any, nd: int = 4) -> str:
    if x is None:
        return "n/a"
    if isinstance(x, float):
        if x != x:
            return "n/a"
        return f"{x:.{nd}g}"
    return str(x)


def _table(rows: list[list[Any]], header: list[str]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def write_report(
    paths, cfg, contract, object_record, presel, cutflows, meta, balance, sf, opt,
    thresholds, summary: pd.DataFrame, retention, cat_manifest, combined_z, fit,
    fit_error, metrics, manifest,
) -> str:
    lumi = cfg["normalization"]["luminosity_fb"]
    had = presel["hadronic"]
    lep = presel["leptonic_bookkeeping_only"]
    md: list[str] = []
    A = md.append

    A("# Top-associated $H \\to \\gamma\\gamma$ hadronic BDT categorization\n")
    A(f"*Generated {manifest['generated_utc']} — run `{cfg['run']['name']}`, "
      f"total wall time {manifest['total_wall_time_seconds']:.1f} s.*\n")

    # ------------------------------------------------------------------
    A("## Introduction\n")
    A(
        "This report documents an end-to-end preselection and **hadronic** "
        "top-associated ($ttH$ / $tH$) $H \\to \\gamma\\gamma$ BDT "
        "categorization built on the ATLAS open-data `GamGam` ntuples. The "
        "pipeline selects a diphoton Higgs candidate without photon tight-ID or "
        "isolation requirements, defines a hadronic top-enriched channel, trains "
        "a deterministic five-variable gradient-boosted classifier to separate "
        "$ttH+tH$ from a mixture of resonant $ggH$ and a data-driven continuum "
        "proxy, optimises BDT category boundaries iteratively, assigns the six "
        "hadronic categories, and finally builds a combined ROOT/RooFit "
        "workspace from which an Asimov expected discovery significance is "
        "extracted.\n"
    )
    A(
        "**Scope note.** The categorization required here is hadronic-only. The "
        "current open-data ROOT inputs contain *no reconstructed forward jets* "
        f"(`n_jets_forward == 0` for all {metrics['counts']['selected_rows']} "
        "selected rows), so leptonic top-associated categories are out of scope "
        "for the BDT optimisation, the category assignment, the significance "
        "summaries and the final plots. Leptonic preselection rows are still "
        "written for provenance and are clearly labelled "
        "(`preselection_channel == \"leptonic_bookkeeping\"`); they are excluded "
        "from training, boundary optimisation, categorization metrics and the "
        "statistical workspace.\n"
    )
    A(
        "**Blinding.** Observed tight-ID + tight-isolation (TI) data in the "
        "$125 \\pm 2$ GeV signal window is never inspected, counted, plotted or "
        "reported. The observed significance is **blocked** unless an explicit "
        "unblinding step is added. The 120–130 GeV removal policy applies *only* "
        "to observed TI data: the NTI control sample retains its 120–130 GeV "
        "entries because it is not the signal-enriched sample.\n"
    )

    # ------------------------------------------------------------------
    A("## Data and Monte Carlo Samples\n")
    A(
        f"Inputs are read in place from `{contract['input_root']}` "
        f"(resolved from `${contract['environment_variable']}`, the same external "
        "input contract as `tb-hyy`), with the expected `MC/` and `data/` layout. "
        "**No ROOT input is copied into the submission directory.**\n"
    )
    A(f"> {contract['scope']['statement']}\n")
    rows = []
    for s in contract["resolved_samples"]:
        proc = presel["by_process"].get(s["sample"], {})
        allsel = proc.get("all_selected", {})
        rows.append([
            f"`{s['sample']}`", s["role"], s["kind"],
            f"{s['size_bytes'] / 1e6:.1f} MB",
            allsel.get("raw_events", 0),
            _fmt(allsel.get("weighted_events_36fb")),
        ])
    A(_table(rows, ["sample", "role", "kind", "file size",
                    "selected rows", f"weighted yield @ {lumi} fb$^{{-1}}$"]) + "\n")
    A(
        "MC events are normalised with the SM-normalised weight\n\n"
        "```\n"
        "w = L * sigma[pb] * k-factor * filter_eff / sum_of_signed_generator_weights\n"
        "      * mcWeight * SF_PILEUP * SF_PHOTON * SF_BTAG * SF_JVT\n"
        "```\n\n"
        f"with the absolute MC integrated luminosity set to **{lumi} fb$^{{-1}}$** "
        "for all expected yields and significances. Signed generator weights are "
        "kept explicit throughout: "
        f"{metrics['weighted_yields_36fb']['signed_weight_bookkeeping']['n_negative_weight_mc_rows']} "
        "selected MC rows carry a negative weight "
        f"(sum of positive weights "
        f"{_fmt(metrics['weighted_yields_36fb']['signed_weight_bookkeeping']['sum_positive'])}, "
        f"sum of negative weights "
        f"{_fmt(metrics['weighted_yields_36fb']['signed_weight_bookkeeping']['sum_negative'])}).\n"
    )
    cap = manifest["row_cap"]
    A(
        f"**Row policy.** The run is **{'uncapped' if cap['uncapped'] else 'capped'}** "
        f"by default (`max_selected_per_sample = {cap['max_selected_per_sample']}`, "
        f"source: {cap['source']}). `{cap['env_var']}` limits the number of "
        "*selected* rows per sample only when explicitly set for development "
        "throttling; when set, rows are taken deterministically in `event_id` order.\n"
    )

    # ------------------------------------------------------------------
    A("## Object Definition and Event Selection\n")
    ph = object_record["photons"]
    A(
        f"**Photons.** $p_T > {ph['pt_min_gev']}$ GeV, "
        f"$|\\eta| < {ph['abs_eta_max']}$ excluding the calorimeter crack "
        f"{ph['crack_veto_abs_eta']}, plus the relative-$p_T$ cuts "
        f"$p_T^{{lead}}/m_{{\\gamma\\gamma}} > "
        f"{cfg['objects']['photons']['lead_pt_over_mgg_min']}$ and "
        f"$p_T^{{sublead}}/m_{{\\gamma\\gamma}} > "
        f"{cfg['objects']['photons']['sublead_pt_over_mgg_min']}$. "
        "**Photon tight ID is NOT required and photon isolation is NOT "
        "required** for this preselection sample — this is recorded explicitly in "
        "`object_definition_record.json`. The tight-ID/tight-isolation flags are "
        "read only to define the TI/NTI control categories.\n"
    )
    A(
        "* **TI** diphoton: *both* photons pass tight ID *and* tight isolation.\n"
        "* **NTI** diphoton: *at least one* photon fails tight ID or fails tight "
        "isolation.\n"
    )
    A(
        "$m_{\\gamma\\gamma}$ is retained for bookkeeping and later validation "
        "(mass windows, control shapes, workspace) and is **never** a classifier "
        "input.\n"
    )
    A(
        f"**Electrons and muons.** $p_T > {cfg['objects']['leptons']['pt_min_gev']}$ "
        "GeV; no lepton ID and no lepton isolation requirement.\n"
    )
    A(
        f"**Jets.** $p_T > {cfg['objects']['jets']['pt_min_gev']}$ GeV; central "
        f"jets $|\\eta| \\le {cfg['objects']['jets']['central_abs_eta_max']}$, "
        f"forward jets $|\\eta| > {cfg['objects']['jets']['central_abs_eta_max']}$. "
        "The documented b-tag definition is "
        f"`{cfg['objects']['jets']['btag_variable']} >= "
        f"{cfg['objects']['jets']['btag_min_quantile']}`. "
        f"{object_record['jets']['forward_jet_availability']}\n"
    )
    A(
        "**Channels.**\n\n"
        f"* *Hadronic* (required): {object_record['channels']['hadronic']} — "
        f"**{had['raw_events']}** rows.\n"
        f"* *Leptonic bookkeeping* (optional, provenance only): "
        f"{object_record['channels']['leptonic_bookkeeping']} — "
        f"**{lep['raw_events']}** rows.\n"
    )
    part = presel["partition"]
    A(
        f"**Partitioning.** Events are partitioned by the stable identifier "
        f"`{part['identifier']}` via {part['method']} with seed "
        f"{part['seed']} and fractions {part['fractions']} — never by row order. "
        f"Counts: {part['counts']}.\n"
    )
    xc = presel["scalar_vs_vectorised_crosscheck"]
    n_mm = sum(c.get("n_mismatches", 0) for c in xc)
    n_ck = sum(c.get("n_checked", 0) for c in xc)
    A(
        f"**Validation.** {n_ck} randomly chosen selected events were re-derived "
        "with the scalar reference implementations "
        "(`invariant_mass`, `build_jet_features`, `build_lepton_features`) and "
        f"compared to the vectorised pipeline: **{n_mm} mismatches**.\n"
    )

    # ------------------------------------------------------------------
    A("## Overview of the Analysis Strategy\n")
    A(
        "1. **Preselection** — build the diphoton candidate, count leptons, jets "
        "and b-jets, tag the channel, assign a stable partition, and record raw "
        "and weighted counts with signed-weight bookkeeping.\n"
        "2. **Continuum proxy** — normalise the NTI data control sample with the "
        "sideband scale factors `SF1`, `SF2`.\n"
        "3. **BDT training** — $ttH+tH$ (SM-normalised MC) versus a $ggH$ + NTI "
        "mixture; class balancing is applied *only after* the physical weights "
        "and the mixture have been constructed.\n"
        "4. **Boundary optimisation** — iterative, 5 % relative-improvement "
        "stopping rule on the expected combined counting significance.\n"
        "5. **Categorization** — six hadronic categories plus `unassigned`, with a "
        "0.8-event minimum-background retention requirement.\n"
        "6. **Statistical interpretation** — combined RooFit workspace, S+B Asimov "
        "with $\\mu_{gen} = 1$, expected discovery significance from the "
        "likelihood-ratio test statistic.\n"
    )
    A(
        "**BDT features** (exactly five, `BDT_FEATURES`): "
        + ", ".join(f"`{f}`" for f in meta["features"])
        + ". `m_gammagamma` is deliberately excluded so the classifier does not "
        "sculpt the continuum mass shape used by the workspace fit.\n"
    )
    hp = meta["model"]["hyperparameters"]
    A(
        f"**Classifier**: `{meta['model']['kind']}` — "
        + ", ".join(f"`{k}={v}`" for k, v in hp.items())
        + f". Deterministic ({meta['model']['determinism_note']}). "
        f"Training wall time **{meta['timing']['training_wall_time_seconds']:.2f} s** "
        f"(stage `{meta['timing']['stage']}`). Weighted AUC: "
        f"train {_fmt(meta['performance']['weighted_auc_train'])}, "
        f"val {_fmt(meta['performance']['weighted_auc_val'])}, "
        f"test {_fmt(meta['performance']['weighted_auc_test'])}.\n"
    )

    # ------------------------------------------------------------------
    A("## Signal and Control Regions\n")
    A(_table(
        [
            ["fit range", "105–160 GeV", "workspace observable range"],
            ["signal window", "123–127 GeV ($125 \\pm 2$)", "expected-yield model"],
            ["low sideband", "105–120 GeV", "continuum control"],
            ["high sideband", "130–160 GeV", "continuum control"],
            ["blinded (observed TI only)", "120–130 GeV", "never inspected"],
        ],
        ["region", "$m_{\\gamma\\gamma}$", "use"],
    ) + "\n")
    A(
        "**Signal definition.** $ttH$ + $tH$ TI MC in $125 \\pm 2$ GeV, hadronic "
        "preselection, weighted with the SM-normalised MC weight.\n"
    )
    A(
        "**Background definition for the classifier.** Resonant $ggH$ TI MC in "
        "$125 \\pm 2$ GeV **plus** the NTI continuum proxy built from the observed "
        "data sidebands.\n"
    )
    A(
        "**NTI continuum normalisation** (hadronic preselection, observed data):\n\n"
        + _table(
            [
                ["TI sideband yield", sf["counts"]["TI_sideband_yield"]],
                ["NTI sideband yield", sf["counts"]["NTI_sideband_yield"]],
                ["NTI $125\\pm2$ GeV yield", sf["counts"]["NTI_signal_window_yield"]],
                ["`SF1` = TI$_{SB}$/NTI$_{SB}$", _fmt(sf["SF1"], 6)],
                ["`SF2` = NTI$_{125\\pm2}$/NTI$_{SB}$", _fmt(sf["SF2"], 6)],
                ["`SF1*SF2`", _fmt(sf["SF1xSF2"], 6)],
                ["implied continuum yield in $125\\pm2$ GeV",
                 _fmt(sf["implied_continuum_yield_in_signal_window"])],
                ["TI $125\\pm2$ GeV yield", "**BLINDED**"],
            ],
            ["quantity", "value"],
        )
        + "\n"
    )
    bb = balance["before_balancing"]
    ab = balance["after_balancing"]
    A(
        "**Class balancing** is applied *only after* the SM-normalised signal "
        "weights and the $ggH$ + NTI background mixture weights have been "
        "constructed:\n\n"
        + _table(
            [
                ["signal class weight sum", _fmt(bb["signal_class_weight_sum"]),
                 _fmt(ab["signal_class_weight_sum"])],
                ["background class weight sum", _fmt(bb["background_class_weight_sum"]),
                 _fmt(ab["background_class_weight_sum"])],
                ["S/B weight ratio", _fmt(bb["ratio_signal_over_background"]),
                 _fmt(ab["ratio_signal_over_background"])],
                ["raw rows", bb["signal_raw_rows"], bb["background_raw_rows"]],
            ],
            ["quantity", "before balancing", "after balancing"],
        )
        + "\n"
    )
    A(
        "Nominal TI observed data in $125 \\pm 2$ GeV is **not** used for BDT "
        "training and **not** used for threshold optimisation.\n"
    )

    # ------------------------------------------------------------------
    A("## Cut Flow\n")
    stages = cutflows[0]["stages"]
    header = ["stage"] + [f"`{c['sample']}`" for c in cutflows]
    rows = []
    for i, st in enumerate(stages):
        rows.append([st["stage"]] + [f"{c['stages'][i]['raw_events']}" for c in cutflows])
    A(_table(rows, header) + "\n")
    A(
        "Weighted yields, sums of positive/negative weights and negative-weight "
        "event counts per stage are in `cutflow.json`.\n"
    )

    # ------------------------------------------------------------------
    A("## Distributions in Signal and Control Regions\n")
    A("![Preselection diphoton mass](plots/preselection_mass.png)\n")
    A("![Preselection channels](plots/preselection_channels.png)\n")
    A("![Preselection processes](plots/preselection_processes.png)\n")
    A(
        "BDT-score shape comparison, with each component normalised to the same "
        "area over explicit $[0, 1]$ binning "
        f"({cfg['bdt']['score_bins']['n']} bins):\n"
    )
    A("![BDT score shapes](plots/score_by_component_shape_bdt_v1.png)\n")
    A(
        "Machine-readable histogram: `plots/score_by_component_histograms.json` "
        "(bin edges, normalised bin contents, component totals *before* shape "
        "normalisation).\n"
    )
    A("![BDT model components](categorization/plots/bdt_score_model_components_36fb_v1.png)\n")
    A(
        "![BDT model components with boundaries]"
        "(categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png)\n"
    )
    A("![Per-category mass control shapes](categorization/plots/category_mgg_control_shapes_36fb_v1.png)\n")
    A(
        "The per-category $m_{\\gamma\\gamma}$ control shapes keep all NTI entries "
        "in 120–130 GeV; only the observed TI points are removed in that window.\n"
    )

    # ------------------------------------------------------------------
    A("## Categorization\n")
    A(
        "Category priority order (`CATEGORY_ORDER`): "
        + " → ".join(f"`{c}`" for c in cat_manifest["category_order"])
        + ".\n"
    )
    A(
        "The BDT boundaries were optimised iteratively: a boundary is added only "
        "while the relative improvement in expected significance with respect to "
        "the previous iteration is at least "
        f"{cfg['optimization']['min_relative_improvement'] * 100:.0f} %.\n"
    )
    rows = []
    for s in opt["accepted_splits"]:
        rows.append([
            s["iteration"], _fmt(s["candidate_boundary"], 3),
            str([round(t, 3) for t in s["thresholds"]]),
            _fmt(s["combined_significance"]),
            "—" if s["relative_improvement"] is None
            else f"{s['relative_improvement'] * 100:.1f} %",
            "accepted",
        ])
    for s in opt["iterations"]:
        if not s.get("accepted", True):
            rows.append([
                s.get("iteration"), _fmt(s.get("candidate_boundary"), 3),
                str([round(t, 3) for t in s.get("thresholds", [])]),
                _fmt(s.get("combined_significance")),
                "—" if s.get("relative_improvement") is None
                else f"{s['relative_improvement'] * 100:.1f} %",
                f"REJECTED ({opt['status']})",
            ])
    A(_table(rows, ["iteration", "new boundary", "boundary set", "combined $Z$",
                    "relative improvement", "decision"]) + "\n")
    A(
        f"Accepted boundary sequence: **{[round(t, 3) for t in thresholds]}** "
        f"(descending; the highest boundary defines `ttH_had_BDT1`). "
        "Optimisation used the 36 fb$^{-1}$ expected-yield weights "
        "(`significance_model_weight_36fb`); the class-balanced `bdt_fit_weight` "
        "is never used for yields or significance.\n"
    )
    A(
        "The `tH_had_4j1b` / `tH_had_4j2b` categories are cut-based and "
        "lower-priority: they are evaluated **only after** an event has failed "
        "every hadronic BDT category, and require $N_{leptons} = 0$, exactly four "
        "**central** jets, and exactly one b-tag (`4j1b`) or at least two b-tags "
        "(`4j2b`).\n"
    )
    A(f"**Retention.** {retention['requirement']}\n")
    A(
        f"Kept: {retention['kept_categories'] or 'none'}. "
        f"Dropped/merged into `unassigned`: "
        f"{retention['dropped_categories'] or 'none'}.\n"
    )
    disp = summary.copy()
    rows = []
    for _, r in disp.iterrows():
        rows.append([
            f"`{r['category']}`", _fmt(r["signal_ttH_tH_yield"]),
            _fmt(r["resonant_higgs_bkg_yield"]), _fmt(r["nti_continuum_bkg_yield"]),
            _fmt(r["total_background_yield"]), _fmt(r["total_model_yield"]),
            _fmt(r["S_over_B"]), _fmt(r["S_over_sqrtB"]),
            _fmt(r["expected_counting_significance"]),
        ])
    A(_table(rows, ["category", "$ttH+tH$", "resonant $H$", "NTI continuum",
                    "total bkg", "total model", "$S/B$", "$S/\\sqrt{B}$",
                    "expected $Z$"]) + "\n")
    A(
        f"**Combined expected counting significance: "
        f"{combined_z:.4f}** (quadrature sum over kept categories, "
        f"{lumi} fb$^{{-1}}$).\n"
    )
    A("![Category expected yields](categorization/plots/category_expected_yields_36fb_v1.png)\n")
    A("![Category expected significance](categorization/plots/category_expected_counting_z_36fb_v1.png)\n")
    A(
        "Expected yields use the signal-window model: TI MC events in "
        "$125 \\pm 2$ GeV normalised to 36 fb$^{-1}$ plus observed-data NTI "
        "sideband events scaled by `SF1*SF2`. Observed-data unit weights are kept "
        "separately in `observed_data_weight`, the NTI proxy weight in "
        "`nti_continuum_weight`, and the model weight in "
        "`significance_model_weight_36fb`.\n"
    )

    # ------------------------------------------------------------------
    A("## Systematic Uncertainties\n")
    A(
        "No systematic uncertainties are propagated in this starting-point "
        "pipeline: every number quoted above is statistical only, and the "
        "workspace contains no nuisance parameters beyond the floating continuum "
        "normalisation and shape parameters. The dominant systematic effects that "
        "a full analysis would need are listed here for completeness, together "
        "with where they would enter this pipeline.\n"
    )
    A(_table(
        [
            ["Continuum background modelling (spurious signal)",
             "choice of continuum PDF per category",
             "`fit/FIT1/background_pdf_scan.json` records the AIC scan over "
             "exponential / power-law / exponential-polynomial / Bernstein"],
            ["NTI proxy closure", "`SF1`, `SF2` and their region dependence",
             "recorded in `model/background_mixture_and_normalization.json`; "
             "an inclusive cross-check is stored alongside the hadronic values"],
            ["Photon energy scale/resolution", "signal and resonant mass shapes",
             "would shift `mean`/`sigma` in `signal_pdf.json`"],
            ["Jet energy scale, JVT, b-tagging",
             "migration between BDT categories and the 4j1b/4j2b cut-based ones",
             "`ScaleFactor_BTAG`, `ScaleFactor_JVT` are already applied nominally"],
            ["Luminosity, pileup, photon ID/isolation SFs",
             "overall normalisation", "`ScaleFactor_PILEUP`, `ScaleFactor_PHOTON`"],
            ["Higgs cross sections and branching ratio",
             "signal and resonant-background normalisation",
             "`xsec`, `kfac`, `filteff` taken from the input ntuple metadata"],
            ["MC statistics", "template shapes in low-population categories",
             "categories fall back to the inclusive hadronic shape below "
             f"{cfg['fit']['min_raw_entries_for_per_category_shape']} raw MC rows"],
        ],
        ["source", "affects", "handling / provenance in this run"],
    ) + "\n")

    # ------------------------------------------------------------------
    A("## Statistical Interpretation\n")
    if fit is None:
        A(f"**The RooFit workspace stage did not complete: `{fit_error}`.**\n")
    else:
        A(
            "A combined **ROOT/PyROOT/RooFit** workspace "
            f"(`{manifest['environment']['packages']['ROOT']}`) is built over the "
            f"{len(fit['categories'])} hadronic categories used in the final "
            "categorization; leptonic bookkeeping rows are excluded. In each "
            "category the expected mass spectrum is\n\n"
            "$$ \\mu \\cdot (ttH+tH) \\;+\\; \\text{fixed resonant-Higgs background} "
            "\\;+\\; \\text{floating smooth continuum} $$\n\n"
            "with **one shared signal-strength parameter $\\mu$** multiplying the "
            "$ttH+tH$ component across all categories. The $ttH+tH$ TI MC provides "
            "the signal mass shape and normalisation; the non-top Higgs TI MC "
            "provides the fixed resonant background.\n"
        )
        A(
            "For the statistical workspace the smooth continuum is determined "
            "**from observed TI data sidebands only** (105–120 and 130–160 GeV): "
            "the fitted PDF and the fitted sideband normalisation are extrapolated "
            "into the full 105–160 GeV fit range, and that fitted PDF generates "
            "the continuum part of the S+B Asimov data. This is deliberately "
            "distinct from the NTI proxy used for BDT training and categorization "
            "control estimates.\n"
        )
        rows = []
        for pc in fit["per_category"]:
            rows.append([
                f"`{pc['category']}`", _fmt(pc["n_sig_36fb"]),
                _fmt(pc["n_resonant_36fb"]), pc["n_ti_sideband_observed"],
                _fmt(pc["n_continuum_full_range_extrapolated"]),
                f"`{pc['background_pdf']}`",
            ])
        A(_table(rows, ["category", "$N_{sig}$ (36 fb$^{-1}$)",
                        "$N_{res}$ (36 fb$^{-1}$)", "TI sideband events",
                        "extrapolated continuum (105–160)", "continuum PDF"]) + "\n")
        A(
            f"S+B Asimov pseudo-data is generated with $\\mu_{{gen}} = "
            f"{fit['mu_gen']:.0f}$; a free-$\\mu$ fit and a $\\mu = 0$ fit give:\n\n"
            + _table(
                [
                    ["$\\hat{\\mu}$", _fmt(fit["mu_hat"])],
                    ["$\\sigma_{\\mu}$", _fmt(fit["mu_uncertainty"])],
                    ["free-$\\mu$ fit status / covQual",
                     f"{fit['free_fit']['fit_status']} / {fit['free_fit']['cov_quality']}"],
                    ["$\\mu=0$ fit status / covQual",
                     f"{fit['conditional_fit']['fit_status']} / "
                     f"{fit['conditional_fit']['cov_quality']}"],
                    ["$q_0 = 2(\\mathrm{NLL}_0 - \\mathrm{NLL}_{\\hat{\\mu}})$",
                     _fmt(fit["q0"])],
                    ["**expected $Z = \\sqrt{q_0}$**", f"**{_fmt(fit['expected_Z'])}**"],
                    ["observed $Z$", "**blocked (blinded)**"],
                ],
                ["quantity", "value"],
            )
            + "\n"
        )
        A("![Sideband background fits](fit/FIT1/plots/sidebands_background_fit.png)\n")
        A(
            "Per-category sideband-fit diagnostics (observed TI sideband data, "
            "fitted continuum PDF, blinded window, explicit binning) are also "
            "written as individual files:\n\n"
            + "\n".join(
                f"* `fit/FIT1/plots/sidebands_background_fit_{c}.png` — "
                f"![{c}](fit/FIT1/plots/sidebands_background_fit_{c}.png)"
                for c in fit["categories"]
            )
            + "\n"
        )
        A("![Asimov S+B fit](fit/FIT1/plots/asimov_sb_fit.png)\n")
        A(
            "Observed TI data in $125 \\pm 2$ GeV remains blinded; the observed "
            "significance is **blocked unless an explicit unblinding step is "
            "added**. The combined expected counting significance "
            f"({combined_z:.4f}) and the RooFit Asimov expected significance "
            f"({_fmt(fit['expected_Z'])}) are complementary estimates: the former "
            "is a pure counting estimate in the $125 \\pm 2$ GeV window, the "
            "latter exploits the full 105–160 GeV mass shape.\n"
        )

    # ------------------------------------------------------------------
    A("## Artifact Checklist\n")
    rows = []
    n_missing = 0
    for rel in REQUIRED_ARTIFACTS:
        p = paths(rel)
        # report.md is this very file: it is written immediately after the
        # checklist is rendered, so stat() would spuriously report it missing.
        ok = p.exists() or rel == "report.md"
        if not ok:
            n_missing += 1
        size = f"{p.stat().st_size:,} B" if p.exists() else (
            "written on completion" if rel == "report.md" else "—")
        rows.append([f"`{rel}`", "yes" if ok else "**MISSING**", size])
    A(_table(rows, ["artifact", "present", "size"]) + "\n")
    A(f"**{len(REQUIRED_ARTIFACTS) - n_missing}/{len(REQUIRED_ARTIFACTS)} "
      f"required artifacts present.**\n")
    A(
        "Additional artifacts written by this run: per-category sideband-fit "
        "plots, `model/bdt_model.pkl`, and the full file index in "
        "`run_manifest.json`.\n"
    )

    # ------------------------------------------------------------------
    A("## Summary\n")
    A(
        f"* {metrics['counts']['selected_rows']} rows pass preselection "
        f"({metrics['counts']['hadronic_rows']} hadronic, "
        f"{metrics['counts']['leptonic_bookkeeping_rows']} leptonic bookkeeping "
        "only), read in place from the `tb-hyy` `GamGam` input contract with only "
        "nominal Higgs MC and observed data — Sherpa $\\gamma\\gamma$ and other "
        "continuum MC are excluded.\n"
        f"* A deterministic five-variable classifier "
        f"({', '.join('`' + f + '`' for f in meta['features'])}) separates "
        "$ttH+tH$ from the $ggH$ + NTI mixture with weighted test AUC "
        f"{_fmt(meta['performance']['weighted_auc_test'])}; training took "
        f"{meta['timing']['training_wall_time_seconds']:.2f} s.\n"
        f"* NTI normalisation: `SF1` = {_fmt(sf['SF1'], 5)}, "
        f"`SF2` = {_fmt(sf['SF2'], 5)}, `SF1*SF2` = {_fmt(sf['SF1xSF2'], 5)}.\n"
        f"* Boundary optimisation accepted "
        f"{len(opt['accepted_splits'])} boundary/boundaries "
        f"({[round(t, 3) for t in thresholds]}) and stopped with status "
        f"`{opt['status']}`.\n"
        f"* Retained categories: {retention['kept_categories'] or 'none'}; "
        f"dropped by the 0.8-event background requirement: "
        f"{retention['dropped_categories'] or 'none'}.\n"
        f"* Combined expected counting significance at {lumi} fb$^{{-1}}$: "
        f"**{combined_z:.4f}**.\n"
        + (
            f"* RooFit Asimov expected discovery significance: "
            f"**{_fmt(fit['expected_Z'])}** "
            f"($\\hat{{\\mu}} = {_fmt(fit['mu_hat'])} \\pm "
            f"{_fmt(fit['mu_uncertainty'])}$, $q_0 = {_fmt(fit['q0'])}$).\n"
            if fit
            else "* RooFit workspace stage unavailable.\n"
        )
        + "* Observed TI data in the $125 \\pm 2$ GeV signal window is blinded "
        "throughout; the observed significance is blocked unless an explicit "
        "unblinding step is added.\n"
    )

    text = "\n".join(md)
    out = paths("report.md")
    out.write_text(text, encoding="utf-8")
    return str(out)
