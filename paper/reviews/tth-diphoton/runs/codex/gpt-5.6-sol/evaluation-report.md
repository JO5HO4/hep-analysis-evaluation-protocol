# Manual evidence review — ttH diphoton

Run: `20260905T022547Z-tth-diphoton-bd__MPttiyG` (`Codex / gpt-5.6-sol`). Generated 2026-09-09. This is non-authoritative manual evidence under `evaluation/ttH.md`, not an outcome grade. The readable bundle inventory covered metadata, terminal/agent logs, submitted source, CSV/JSON tables, model, plots, and RooFit workspace artifacts. Harbor completion and verifier reward are context, not this report's score.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / gpt-5.6-sol | 26 | 2 | 10 | completed / 0.000000 |

| Summary | Codex / gpt-5.6-sol |
|---|---:|
| Total reward | 26 / 38 |

| Summary | Codex / gpt-5.6-sol |
|---|---:|
| Overall equal-category reward | 0.5914 |

The zero verifier reward is traceable to `verifier/score_report.json` schema/API failures, including the submitted feature-list mismatch. It does not erase the directly readable produced analysis evidence. No baseline comparison is evaluated from the checked-in development proxies: their own documentation says that they require a trusted evaluator table, and this bundle has no compatible frozen evaluator comparison record.

## Per-question binary rewards

| Group | Q | Reward |
|---|---:|---:|
| I Execution and documentation | 1–3 | 1, 1, 1 |
| II Object definition and preselection | 4–7 | 1, 1, 1, 1 |
| III BDT training/configuration | 8–13 | 0, 0, 1, 1, 1, 1 |
| IV Categorization/purity | 14–18 | 1, 1, 1, 0, 0 |
| V Workspace/background/fit | 19–27 | 1, 1, 0, 1, 1, 1, 1, 1, 1 |
| VI Inclusive baseline | 28–30 | 0, 0, 0 |
| VII Presentation | 31–33 | 1, 1, 0 |
| VIII Validation/reproducibility | 34–37 | 0, 1, 1, 0 |
| IX Quantile baseline | 38 | 0 |

## Observed values and evidence reasoning

| Q | Observed value [reward] | Status and direct evidence |
|---:|---|---|
| 1 | wall 734.229 s; agent 613.718 s [1] | **pass** — finite ISO timestamps in `result.json` (`started_at`/`finished_at`, `agent_execution`). |
| 2 | $1.9020216 USD [1] | **pass** — `result.json: agent_result.cost_usd`. |
| 3 | complete narrative with all required named sections [1] | **pass** — `artifacts/root/results/tth-diphoton-bdt/report.md` contains Introduction through Summary and links the requested plots. |
| 4 | tight ID=false; isolation=false [1] | **pass** — `object_definition_record.json: photons`; source `run_analysis.py: read_selected`. |
| 5 | 101,471 rows; signed MC 29.5784 at 36 fb^-1; data 33,655 rows [1] | **pass** — process-scoped raw and weighted counts in `preselection_summary.json`. |
| 6 | photons >25 GeV, abs(eta)<2.37/crack removed; leptons >10; jets >25; 0 leptons, >=3 jets, >=1 b; btag>=4 [1] | **pass** — `object_definition_record.json` and `run_analysis.py: read_selected`. |
| 7 | ttH 55,701 / 19.5572; tH 7,332 / 0.149931; other Higgs process rows/yields listed [1] | **pass** — `preselection_summary.json: raw_and_weighted_counts_by_process`. |
| 8 | sklearn HistGradientBoostingClassifier; sklearn version not recorded [0] | **missing** — `training_metadata.json` names the package/class but records no sklearn version; inspected manifest/config/report/source. |
| 9 | submitted list `[n_central_jets,n_bjets,jet1_pt,jet_ht,diphoton_pt]` [0] | **fail** — `verifier/score_report.json: selection_api` directly reports this list as `BDT_FEATURES mismatch`; it excludes mass but is not the task-required list. |
| 10 | test weighted ROC AUC=0.817605 [1] | **pass** — `metrics.json: training.test_weighted_roc_auc`, evaluation partition=test. |
| 11 | signal `ttH+tH`; background TI ggH + NTI data sidebands [1] | **pass** — `model/background_mixture_and_normalization.json`. |
| 12 | pre S/B=14.280744/41.165049; post=27.722897/27.722897 [1] | **pass** — `model/class_balance_check.json` says balancing follows physical-mixture construction. |
| 13 | SHA-256 event ID, seed 240513, fractions 60/20/20 [1] | **pass** — `inference/inference_manifest.json: stable_partition`; source maps each stable ID once to train/validation/test. |
| 14 | six names plus `unassigned` [1] | **pass** — `categorization/categorization_manifest.json: final_category_order`. |
| 15 | tH cuts only after BDT failure [1] | **pass** — manifest flag `th_categories_evaluated_after_bdt_failure=true` and `analysis/top_categorization.py: assign_top_category`. |
| 16 | minimum=0.680609; split=0.868546; relative gain=5.5209%; stop below 5% [1] | **pass** — `optimization/thresholds.json`/`metrics.json: optimization`. |
| 17 | combined ttH+tH yield 1.46437 in BDT1; separate ttH and all-Higgs yields absent [0] | **missing** — searched category JSON/CSV, inference table, report, workspace, and source. None records the required separate ttH and all-Higgs ratio for highest retained category. |
| 18 | combined ttH+tH yield 3.28013 in BDT2; separate ttH and all-Higgs yields absent [0] | **missing** — same concrete searched sources as Q17; no required second-category ratio. |
| 19 | ROOT 6.38.00, ROOT/PyROOT/RooFit; S+B Asimov fit [1] | **pass** — `workspace_manifest.json`, `fit/FIT1/backend.json`, and `significance_asimov.json`. |
| 20 | shared mu, ttH+tH signal, fixed non-top-Higgs, floating continuum [1] | **pass** — `significance_asimov_construction.json` and `workspace.json`. |
| 21 | candidate list only `RooExponential`; no selection statistic [0] | **fail** — `background_pdf_scan.json` shows one candidate and `background_pdf_choice.json` supplies no candidate-selection statistic, contrary to the required candidate-functions-and-statistic evidence. |
| 22 | TI sidebands 105–120 and 130–160, extrapolated to 105–160 [1] | **pass** — `significance_asimov_construction.json: continuum_generation`; sideband plot payload/source corroborate. |
| 23 | Asimov mu_gen=1 [1] | **pass** — `fit/FIT1/significance_asimov.json`. |
| 24 | mu_hat=0.993881, uncertainty=0.765066, both statuses=0/covQual=3 [1] | **pass** — `fit/FIT1/results.json: fits`. |
| 25 | continuum proxy total=22.134206 events at 36 fb^-1 across BDT1, BDT2, 4j1b, 4j2b [1] | **pass** — sum of named 123–127 category components in `category_component_yields.json`; category scope and 36 fb^-1 weight column are explicit. |
| 26 | resonant total=2.436305 events at 36 fb^-1 across the same four categories [1] | **pass** — sum of named resonant components in `category_component_yields.json`; scope/normalization explicit. |
| 27 | q0=2.0690128601; Z=1.4384063613; Z²=q0 [1] | **pass** — `fit/FIT1/significance_asimov.json`; equality holds within the stated tolerance. |
| 28 | agent Z=1.438406; compatible evaluator baseline unavailable [0] | **missing** — checked `evaluation/ttH-baseline/baseline_results.json`; it is explicitly a development proxy requiring a trusted evaluator table, not this run's same frozen sample. |
| 29 | agent mu uncertainty=0.765066; compatible evaluator baseline unavailable [0] | **missing** — same incompatibility as Q28; no comparison record in the run bundle. |
| 30 | Pareto comparison not established [0] | **missing** — both compatible baseline metrics are unavailable, so no Pareto inference. |
| 31 | PNG/PDF plots and machine histogram payloads have finite populated values [1] | **pass** — inventory plus `plots/score_by_component_histograms.json` (0–1 bins and populated signal/NTI bins) and categorization histogram JSONs. |
| 32 | shapes: unit area; count/control histograms: bin contents with sumw2 [1] | **pass** — `score_by_component_histograms.json: normalization`; categorization histograms record bin contents/sumw2 and source labels count plots. |
| 33 | test partition is stated for AUC, but not for every required performance plot [0] | **missing** — searched metrics, report, histogram payloads, plots, source; no per-required-plot partition statement. |
| 34 | no finite score–mass correlation/sculpting statistic [0] | **missing** — searched logs, report, metrics, tables, plots, source; mass is retained and plotted but no requested diagnostic result is produced. |
| 35 | validation boundary iterations: 3.339806 then 3.524192 for changed boundary [1] | **pass** — source `run_analysis.py:349–352` selects validation; `thresholds.json` gives two common-validation categorization attempts and named metric. |
| 36 | S/B ratios: 0.346907 before, 1.000000 after [1] | **pass** — finite class sums/balance factors in `model/class_balance_check.json`. |
| 37 | features, hyperparameters, seeds, thresholds, input identifiers and several versions; sklearn version absent [0] | **missing** — `config_resolved.yaml`, `metrics.json`, `run_manifest.json`, and input contract establish most fields but not all required package versions. |
| 38 | agent Z=1.438406; compatible fixed-quantile baseline unavailable [0] | **missing** — `fixed_quantile_baseline_results.json` is a development proxy, not rerun on this bundle's frozen evaluator event table/continuous score under demonstrated identical fit assumptions. |

Category pass fractions used only for the equal-category summary: I 3/3, II 4/4, III 4/6, IV 3/5, V 8/9, VI 0/3, VII 2/3, VIII 2/4, IX 0/1.
