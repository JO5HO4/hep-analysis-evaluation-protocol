# Manual evidence evaluation: Codex / gpt-5.6-terra

Non-authoritative review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`, generated 2026-09-09. This natural-language rubric is not an indexed evaluation specification and creates no outcome grade.

| Run | Task | Harbor status / verifier reward |
|---|---|---|
| `20260902T213233Z-tth-diphoton-bd__zWiAt8N` | `tth-diphoton` | `completed / 0.000000` |

All readable evidence was audited: job metadata, `trial.log`, agent transcript/trajectory, submitted Python source, verifier output, report, all JSON/CSV tables, PNG/PDF plot payloads, and the ROOT workspace under `artifacts/root`. Zero verifier reward is context, not a rubric result.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / gpt-5.6-terra | 25 | 2 | 11 | completed / 0.000000 |

| Summary | Codex / gpt-5.6-terra |
|---|---:|
| Total reward | 25 / 38 |
| Overall equal-category reward | 0.580 |

The equal-category value is the mean of Group I–IX fractions: 1, .5, .667, 1, .889, 0, .667, .5, 0.

## Per-question binary rewards

| Group | Criterion | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 1 |
| I | Q3 Human-facing documentation | 1 |
| II | Q4 Photon ID/isolation policy | 1 |
| II | Q5 Hadronic count and 36 fb^-1 yield | 0 |
| II | Q6 Hadronic preselection | 1 |
| II | Q7 Post-preselection Higgs yields | 0 |
| III | Q8 BDT package/version | 0 |
| III | Q9 Exact BDT features | 0 |
| III | Q10 Held-out AUC | 0 |
| III | Q11 Training classes | 1 |
| III | Q12 Training weights/balancing | 1 |
| III | Q13 Stable disjoint partitions | 1 |
| IV | Q14 Categories plus unassigned | 1 |
| IV | Q15 BDT-priority assignment | 1 |
| IV | Q16 5% optimization rule | 1 |
| IV | Q17 Highest BDT purity | 1 |
| IV | Q18 Second-highest BDT purity | 1 |
| V | Q19 RooFit workspace and Asimov fit | 1 |
| V | Q20 Required combined statistical model | 0 |
| V | Q21 Background-function choice | 1 |
| V | Q22 TI-sideband procedure | 1 |
| V | Q23 S+B Asimov `mu_gen=1` | 1 |
| V | Q24 Unbiased fit | 1 |
| V | Q25 Continuum yield | 1 |
| V | Q26 Resonant yield | 1 |
| V | Q27 One-sided expected significance | 1 |
| VI | Q28 Z vs inclusive baseline | 0 |
| VI | Q29 uncertainty vs inclusive baseline | 0 |
| VI | Q30 Pareto vs inclusive baseline | 0 |
| VII | Q31 Plot quantity/labels | 1 |
| VII | Q32 Histogram normalization | 1 |
| VII | Q33 Performance partition | 0 |
| VIII | Q34 Score-mass correlation | 1 |
| VIII | Q35 Two validation optimization attempts | 0 |
| VIII | Q36 Class-imbalance accounting | 1 |
| VIII | Q37 Final configuration reproducibility | 0 |
| IX | Q38 Z vs fixed-quantile baseline | 0 |

## Criterion evidence and reasoning

| ID | Status / observed value | Exact evidence and reason |
|---|---|---|
| Q1 | pass [1]; wall 1200.318 s, agent 1070.807 s | `result.json: started_at/finished_at` and `agent_execution` timestamps establish finite durations. |
| Q2 | pass [1]; $1.021473 USD | `result.json:agent_result.cost_usd`. |
| Q3 | pass [1]; narrative with all required report headings | `results/tth-diphoton-bdt/report.md` contains input, objects, strategy, controls, categorization, systematics, fit and linked plots. |
| Q4 | pass [1]; tight ID=false, isolation=false | `object_definition_record.json:photons`; executed source `run_analysis.py: getrows` retains photons before TI/NTI bookkeeping. |
| Q5 | missing [0]; raw hadronic=272,376, but no total 36-fb weighted yield | `cutflow.json` and `preselection_summary.json` give raw/signed per-process counts, while `category_yields_36fb.json`, report, source and CSVs give no aggregate hadronic 36-fb yield. |
| Q6 | pass [1]; 2 photons pT>25, eta acceptance/crack exclusion; e/mu pT>10; 0 leptons, >=3 jets pT>25, >=1 b tag q>=4 | `preselection_summary.json:selection_definitions`, `object_definition_record.json`, and executed `run_analysis.py`. |
| Q7 | missing [0]; raw process counts and signed weights, not process-separated 36-fb yields | Searched `preselection_summary.json`, `cutflow.json`, `preselected_events.csv`, report and source. |
| Q8 | missing [0]; algorithm named, version absent | `model/training_metadata.json` says `HistGradientBoostingClassifier`; source imports sklearn, but no saved package version. |
| Q9 | fail [0]; feature API is `[n_jets,n_bjets,jet_ht,lead_jet_pt,central_jet_fraction]` | `analysis/top_categorization.py:BDT_FEATURES`, `training_metadata.json`, and `verifier/score_report.json:selection_api.errors` directly record mismatch. |
| Q10 | missing [0]; no finite test AUC | Searched `metrics.json`, model metadata, report, training CSV and source: model is fitted on train but no AUC calculation/result. |
| Q11 | pass [1]; signal ttH+tH; background ggH+scaled NTI | `background_mixture_and_normalization.json` and report. |
| Q12 | pass [1]; signed pre (bkg 72.5076, sig 7.82558), absolute pre (72.6594,10.8170), post both 41.7382 | `model/class_balance_check.json`, with construction in executed source. |
| Q13 | pass [1]; train/validation/test 31,433/10,549/10,658 unique IDs; 0 duplicates | Direct read of `model/training_sample.csv`; stable hash partition implementation in `top_categorization.py`. |
| Q14 | pass [1]; six named categories plus unassigned | `CATEGORY_ORDER` and `assign_top_category`; executed `categorization_manifest.json` and `category_summary.csv`. |
| Q15 | pass [1]; score thresholds precede 4-central-jet cut categories | `top_categorization.py:assign_top_category` checks BDT branches before tH branches. |
| Q16 | pass [1]; thresholds .80,.53; gains 44.839%,7.356%; minimum .05 | `optimization/thresholds.json`, `accepted_splits.json`, and executed stopping implementation. |
| Q17 | pass [1]; BDT1 ttH=2.18483, all-Higgs=2.19330, purity=.99614 | Direct aggregation of `hadronic_features.csv` with category/model weights; BDT1 is highest retained lower-bound category. |
| Q18 | pass [1]; BDT2 ttH=2.92182, all-Higgs=2.94364, purity=.99259 | Direct aggregation of the same executed table; BDT2 is second-highest retained boundary. |
| Q19 | pass [1]; ROOT/PyROOT/RooFit workspace, S+B Asimov results | Readable `fit/FIT1/workspace.root` contains `combined_hadronic_workspace`; `workspace_manifest.json` and `significance_asimov.json`. |
| Q20 | fail [0]; workspace has only `m_gammagamma` and `mu`, no recorded combined component PDFs/floating continuum | ROOT-key inspection plus `run_analysis.py:124-127` directly shows a minimal workspace and counting approximation, contradicting the required shared-mu combined model. |
| Q21 | pass [1]; candidates exponential/linear, selected exponential, applied to retained categories | `background_pdf_scan.json`, `background_pdf_choice.json`, `sideband_fit_plots.json`, and source loop over `kept`. |
| Q22 | pass [1]; TI sidebands 105–120,130–160; full 105–160 | `sideband_fit_plots.json` and source `side` predicate / fit construction. |
| Q23 | pass [1]; `mu_gen=1` | `significance_asimov_construction.json`. |
| Q24 | pass [1]; mu_hat=1.0, uncertainty=.696821, statuses=0/0, covQual=3 | `fit/FIT1/results.json`. |
| Q25 | pass [1]; continuum proxy=68.5313 expected events at 36 fb^-1, retained categories BDT1–3 and tH_4j1b | Sum of `category_component_yields.json:nti_continuum_proxy`; 36-fb schema in `category_yields_36fb.json`. |
| Q26 | pass [1]; resonant=4.73681 expected events at 36 fb^-1, same scope | Sum of `category_component_yields.json:resonant_higgs`; category scope and luminosity are explicit. |
| Q27 | pass [1]; q0=2.0594772800, Z=1.4350878998, Z^2=q0 | `fit/FIT1/results.json`; finite and algebraically consistent. |
| Q28 | missing [0]; no evaluator-owned compatible inclusive baseline | Searched `evaluation/ttH-baseline/` and run fit/output tree; no same frozen table rerun. |
| Q29 | missing [0]; no compatible baseline uncertainty | Same searched sources as Q28. |
| Q30 | missing [0]; no compatible two-metric baseline comparison | Same searched sources as Q28. |
| Q31 | pass [1]; finite explicit bins and units | JSON payloads give nonempty finite bins: BDT [0,1], mass [105,160]; source labels BDT score, mgg [GeV], expected yield (36 fb-1), and unit-area entries. |
| Q32 | pass [1]; score shapes unit-area; yield/count plots labeled expected yield/counting Z | `plots/score_by_component_histograms.json` has normalized contents and pre-normalization totals; plotting source provides labels. |
| Q33 | missing [0]; no required performance plot with named evaluated partition | Searched plot payloads, report, metadata, training CSV and source; partitions exist but are not tied to a performance plot. |
| Q34 | pass [1]; Pearson r(score,mgg)=-.00416515 on 272,376 hadronic rows | Reproducible direct calculation from finite `hadronic_features.csv` score and mass columns; sample and method stated. |
| Q35 | missing [0]; accepted boundaries are sequential but no two named configs evaluated on common validation partition | Searched trajectory, report, model metadata, optimization JSON and source. |
| Q36 | pass [1]; abs sig/bkg=.14887 before, 1.00000 after absolute-weight balancing | `class_balance_check.json`; balancing method explicitly recorded. |
| Q37 | missing [0]; feature list/hyperparameters/thresholds/seeds/input identifiers exist, package versions do not | `config_resolved.yaml`, metadata, `thresholds.json`, source and input contract searched. |
| Q38 | missing [0]; no compatible `fixed-score-quantiles-4/v1` same-table result | Searched evaluator baseline records and all run outputs. |

Missing means the specified condition could not be established after the concrete search stated above; it is not a generic artifact-name failure. Fail is used only for the direct Q9/Q20 contradictions.
