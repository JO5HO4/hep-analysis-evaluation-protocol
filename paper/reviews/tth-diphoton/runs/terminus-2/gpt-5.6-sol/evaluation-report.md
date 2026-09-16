# Manual evidence evaluation — ttH diphoton

Non-authoritative review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`, generated 2026-09-09. This is review evidence, not an outcome grade. Evidence audit covered the complete preserved trial: metadata, `trial.log`, `agent/trajectory.json`, verifier outputs, submitted source, all readable result JSON/CSV artifacts, plot payloads and images/PDFs, report, and the RooFit workspace manifest.

## Run identity

| Field | Value |
|---|---|
| Task / agent / model | `tth-diphoton-bdt-categorization` / `terminus-2` / `gpt-5.6-sol` |
| Trial | `20260905T033334Z-tth-diphoton-bd__u5KdDyp` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Review result | 24 pass, 3 fail, 11 missing; raw `24 / 38` |

The verifier's zero reward is execution context only. Its recorded feature-API mismatch is direct contrary evidence for Q9; its other schema failures do not erase independently readable output evidence.

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus-2 / gpt-5.6-sol | 24 | 3 | 11 | completed / 0.000000 |

## 2. Total reward (raw, no averaging)

| Summary | Terminus-2 / gpt-5.6-sol |
|---|---:|
| Total reward | 24 / 38 |

## 3. Overall equal-category reward

| Summary | Terminus-2 / gpt-5.6-sol |
|---|---:|
| Overall equal-category reward | 0.556 |

This is the mean of Group I–IX pass fractions: `1, 1, 0.5, 0.8, 0.778, 0, 0.667, 0.25, 0`.

## 4. Per-question binary rewards

| Group | Criterion | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 1 |
| I | Q3 Human-facing documentation | 1 |
| II | Q4 Photon policy | 1 |
| II | Q5 Hadronic count/yield | 1 |
| II | Q6 Hadronic preselection | 1 |
| II | Q7 Higgs yields | 1 |
| III | Q8 BDT package/version | 0 |
| III | Q9 Exact BDT features | 0 |
| III | Q10 Held-out AUC | 0 |
| III | Q11 Training classes | 1 |
| III | Q12 Physical weighting/balancing | 1 |
| III | Q13 Stable disjoint partitions | 1 |
| IV | Q14 Categories | 1 |
| IV | Q15 Priority assignment | 1 |
| IV | Q16 5% split rule | 1 |
| IV | Q17 Highest-score purity | 1 |
| IV | Q18 Second-highest purity | 0 |
| V | Q19 RooFit/Asimov | 1 |
| V | Q20 Statistical signal definition | 1 |
| V | Q21 Background function choice | 1 |
| V | Q22 TI-sideband procedure | 1 |
| V | Q23 S+B Asimov | 1 |
| V | Q24 Asimov fit result | 1 |
| V | Q25 Continuum 123–127 yield | 0 |
| V | Q26 Resonant 123–127 yield | 0 |
| V | Q27 Expected significance | 1 |
| VI | Q28 Inclusive-Z comparison | 0 |
| VI | Q29 Inclusive-mu comparison | 0 |
| VI | Q30 Inclusive Pareto comparison | 0 |
| VII | Q31 Plot quantity/values | 1 |
| VII | Q32 Histogram normalization | 1 |
| VII | Q33 Performance partition | 0 |
| VIII | Q34 Score–mass diagnostic | 0 |
| VIII | Q35 Optimization attempts | 0 |
| VIII | Q36 Class-imbalance ratios | 1 |
| VIII | Q37 Final reproducibility fields | 0 |
| IX | Q38 Fixed-quantile comparison | 0 |

## 5. Per-question observed values and rewards

| Criterion | Observed value [reward] |
|---|---|
| Q1 | wall `692.540 s`; agent execution `554.467 s` [1] |
| Q2 | `$2.095334 USD` [1] |
| Q3 | readable narrative plus linked artifacts [1] |
| Q4 | tight ID `false`, isolation `false` [1] |
| Q5 | `272376` rows; `30.129381` signed events at 36 fb^-1 [1] |
| Q6 | photons 25 GeV/2.37/crack exclusion; lepton 10 GeV; jets 25 GeV; `nlep=0,njet>=3,nb>=1,q>=4` [1] |
| Q7 | ttH `57677, 20.182054`; tH `7566, 0.156128` (raw, 36 fb^-1) [1] |
| Q8 | sklearn named; version not saved [0] |
| Q9 | verifier records BDT_FEATURES mismatch [0] |
| Q10 | `0.762271` is explicitly training AUC, not held-out [0] |
| Q11 | signal `ttH+tH`; background `ggH+NTI` [1] |
| Q12 | pre `B=43.505438,S=6.561248`; post `B=S=0.5` [1] |
| Q13 | train/validation/test `163770/54309/54297`; cross-partition IDs `0` [1] |
| Q14 | BDT1–4, tH_4j1b, tH_4j2b, unassigned [1] |
| Q15 | BDT priority precedes tH fallback [1] |
| Q16 | boundary `0.633827`; gain `45.317%`; stop `<5%` [1] |
| Q17 | BDT1 ttH `2.723424`, all-Higgs `3.034059`, purity `0.897617` [1] |
| Q18 | no second retained BDT category: BDT2–4 all `kept=false` [0] |
| Q19 | ROOT/PyROOT/RooFit workspace plus Asimov fit [1] |
| Q20 | shared mu, top signal, fixed resonant, floating continuum [1] |
| Q21 | RooExponential; documented single-baseline selection [1] |
| Q22 | TI sidebands 105–120,130–160 GeV; fit range 105–160 GeV [1] |
| Q23 | `mu_gen=1`, binned RooFit S+B Asimov [1] |
| Q24 | muhat `1.000027`, sigma `0.803194`, statuses `0/0`, covariances `3/3` [1] |
| Q25 | full-range continuum only; no 123–127 yield [0] |
| Q26 | full-range resonant values only; no 123–127 yield [0] |
| Q27 | `q0=1.899747`, `Z=1.378313`, `Z²-q0≈0` [1] |
| Q28 | evaluator same-sample inclusive baseline absent [0] |
| Q29 | evaluator same-sample inclusive baseline absent [0] |
| Q30 | evaluator same-sample inclusive baseline absent [0] |
| Q31 | explicit nonempty finite score/mass/fit bin payloads [1] |
| Q32 | score components unit area; mass controls events/bin [1] |
| Q33 | no saved evaluated partition for every performance plot [0] |
| Q34 | no finite score–mass correlation/diagnostic [0] |
| Q35 | no two saved common-validation attempts/results [0] |
| Q36 | S/B pre `0.150813`; post `1.0` [1] |
| Q37 | sklearn/ROOT named but complete package-version set absent [0] |
| Q38 | no compatible fixed-score-quantiles-4/v1 rerun [0] |

## 6. Per-question evidence and reasoning

| Criterion | Status | Evidence and reason |
|---|---|---|
| Q1 | pass | `result.json: started_at/finished_at/agent_execution` directly gives finite 692.540 s wall and 554.467 s pure agent time. |
| Q2 | pass | `result.json:agent_result.cost_usd=2.0953339`. |
| Q3 | pass | `results/.../report.md` covers inputs, selection, model, categories, systematics, fit, plots, summary. |
| Q4 | pass | `object_definition_record.json:photons.tight_id_required/isolation_required=false`; report agrees. |
| Q5 | pass | `preselection_summary.json:overall_raw/overall_signed_weighted_yield_36fb`, with process scope. |
| Q6 | pass | `object_definition_record.json` and `preselection_summary.json:hadronic_definition` give every required predicate. |
| Q7 | pass | `preselection_summary.json:counts` gives raw and 36-fb yields by Higgs process. |
| Q8 | missing | Audited report, `training_metadata.json`, config, source and trajectory: sklearn is identified but no sklearn package version is recorded. |
| Q9 | fail | `verifier/score_report.json:selection_api.errors` directly states `BDT_FEATURES mismatch`; saved list cannot override that direct contract contradiction. |
| Q10 | fail | `metrics.json:weighted_training_auc`; `submission/.../postprocess.py` computes it from `training_sample.csv`, directly contradicting held-out requirement. |
| Q11 | pass | `background_mixture_and_normalization.json:signal/background` and report identify exact classes. |
| Q12 | pass | `class_balance_check.json` records physical pre-balance sums, factors, post-balance sums, and separation from yield weights. |
| Q13 | pass | `training_metadata.json:partitions`; `predictions.csv` audit finds three nonempty partitions and zero event IDs assigned across partitions. |
| Q14 | pass | `categorization_manifest.json:category_priority` plus `category_component_yields.json` includes all required labels and unassigned. |
| Q15 | pass | `categorization_manifest.json:lower_priority_tH_definition`; `top_categorization.py:assign_top_category` implements BDT-first fallback. |
| Q16 | pass | `optimization/accepted_splits.json` gives accepted gain 0.453170, threshold, and `<5%` stop rule. |
| Q17 | pass | `predictions.csv` weighted BDT1 TI 123–127 audit gives ttH/all-Higgs values and finite ratio; BDT1 is retained. |
| Q18 | fail | `category_retention.json` directly shows BDT2, BDT3 and BDT4 not kept, so the required second retained BDT category does not exist. |
| Q19 | pass | `workspace_manifest.json:backend/workspace_*` and `significance_asimov_construction.json` establish produced RooFit workspace and Asimov fit. |
| Q20 | pass | `workspace_manifest.json:model` and `significance_asimov_construction.json:components`. |
| Q21 | pass | `background_pdf_scan.json:candidates/selection` and `background_pdf_choice.json:choice` name RooExponential and selection scope. |
| Q22 | pass | `workspace_manifest.json:continuum_source`; `sideband_fit_plots.json:explicit_binning_GeV` supports the range. |
| Q23 | pass | `significance_asimov_construction.json:type/mu_gen/components`. |
| Q24 | pass | `fit/FIT1/results.json` gives finite unbiased mu, uncertainty and successful status/covariance fields. |
| Q25 | missing | Audited report, fit JSON, workspace manifest, plot payloads and source: only full-range extrapolated continuum yields are saved, not 123–127 values. |
| Q26 | missing | Same audited sources contain category/full-fit resonant yields but no direct 123–127 resonant yield. |
| Q27 | pass | `fit/FIT1/results.json:q0/expected_Z`; numeric identity satisfies tolerance. |
| Q28 | missing | Audited saved fit tree and evaluator baseline records: no compatible same-frozen-sample inclusive baseline rerun. |
| Q29 | missing | Same concrete baseline/evidence audit; no comparable baseline mu uncertainty. |
| Q30 | missing | Same concrete baseline/evidence audit; Pareto comparison cannot be formed. |
| Q31 | pass | `score_by_component_histograms.json` and `sideband_fit_plots.json` supply bin edges, finite contents and GeV binning; plot files are present. |
| Q32 | pass | `score_by_component_histograms.json:normalization` says unit area; submitted `postprocess.py` labels mass controls `Events/bin`. |
| Q33 | missing | Audited report, metrics, plot payloads, source and tables: plots are identified but no evaluated partition is recorded for every required performance plot. |
| Q34 | missing | Audited report, metrics, source, tables and payloads: no saved finite score-versus-mass correlation or sculpting result. |
| Q35 | missing | Audited trajectory, report, `training_metadata.json` and optimization records: one final configuration/accepted split is evidenced, not two common-validation attempt metrics. |
| Q36 | pass | `class_balance_check.json:before/after` yields finite ratios and explicitly describes balancing. |
| Q37 | missing | Audited config, manifest, metadata, source, report: features/hyperparameters/thresholds/seeds/input identifiers exist, but complete package versions (notably sklearn) do not. |
| Q38 | missing | Audited evaluator fixed-quantile records and saved fit/output tree: no compatible same-table fixed-score-quantiles-4/v1 comparison. |

