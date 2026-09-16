# Manual evidence review: ttH diphoton BDT categorization

Run: `20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158/20260904T225909Z-tth-diphoton-bd__3FYYT6o`  
Task / agent / model: `tth-diphoton / qwen-coder / google/qwen-3`  
Review date: 2026-09-09. This is non-authoritative review evidence under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`; the rubric is natural language and no outcome grade is asserted. The complete readable bundle was audited: metadata, trial/verifier logs, ATIF trajectory, submitted Python/YAML/README, CSV/JSON tables, plots, workspace files, and report.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| qwen-coder / google-qwen-3 | 5 | 13 | 20 | completed / 0.000000 |

## Total reward (raw, no averaging)

| Summary | qwen-coder / google-qwen-3 |
|---|---:|
| Total reward | 5 / 38 |

## Overall equal-category reward

| Summary | qwen-coder / google-qwen-3 |
|---|---:|
| Overall equal-category reward | 0.204 |

The nine equal-weight group fractions are I `1/3`, II `1/4`, III `0/6`, IV `2/5`, V `0/9`, VI `0/3`, VII `0/3`, VIII `1/4`, IX `0/1`; their arithmetic mean is `0.2037`.

## Per-question binary rewards

| Group | Question | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 0 |
| I | Q3 Human-facing documentation | 0 |
| II | Q4 Photon identification and isolation policy | 1 |
| II | Q5 Hadronic-channel event count | 0 |
| II | Q6 Hadronic preselection | 0 |
| II | Q7 Post-preselection Higgs yields | 0 |
| III | Q8 BDT training package | 0 |
| III | Q9 BDT input features | 0 |
| III | Q10 Signal-background AUC | 0 |
| III | Q11 Training classes | 0 |
| III | Q12 Training class weights | 0 |
| III | Q13 Train/validation/test partition | 0 |
| IV | Q14 BDT category count | 1 |
| IV | Q15 BDT event categorization | 1 |
| IV | Q16 Categorization figure of merit | 0 |
| IV | Q17 Highest-score ttH purity | 0 |
| IV | Q18 Second-highest-score ttH purity | 0 |
| V | Q19 Fit-based sensitivity assessment | 0 |
| V | Q20 Statistical signal definition | 0 |
| V | Q21 Analytical fit-function choice | 0 |
| V | Q22 Background PDF determination | 0 |
| V | Q23 S+B Asimov data set | 0 |
| V | Q24 S+B Asimov fit result | 0 |
| V | Q25 Continuum yield, 123-127 GeV | 0 |
| V | Q26 Resonant yield, 123-127 GeV | 0 |
| V | Q27 Expected significance | 0 |
| VI | Q28 Expected-significance comparison | 0 |
| VI | Q29 Signal-strength precision comparison | 0 |
| VI | Q30 Baseline Pareto improvement | 0 |
| VII | Q31 Plot quantity and labeling | 0 |
| VII | Q32 Histogram normalization | 0 |
| VII | Q33 Performance-plot partition | 0 |
| VIII | Q34 Score-mass correlation | 0 |
| VIII | Q35 Optimization attempts | 0 |
| VIII | Q36 Class-imbalance accounting | 1 |
| VIII | Q37 Final configuration reproducibility | 0 |
| IX | Q38 Expected significance vs fixed quantiles | 0 |

## Per-question observed values and rewards

| Group | Question | qwen-coder / google-qwen-3 |
|---|---|---|
| I | Q1 | wall `504.459 s`; agent `365.157 s` [1] |
| I | Q2 | `null USD` [0] |
| I | Q3 | required narrative coverage incomplete [0] |
| II | Q4 | `pT > 20 GeV`; no tight ID/isolation [1] |
| II | Q5 | hadronic raw `1`; no 36 fb^-1 process-scoped yield [0] |
| II | Q6 | synthetic `n_jets/n_bjets`; no reconstructed photon selection [0] |
| II | Q7 | no process-separated hadronic raw/36 fb^-1 yields [0] |
| III | Q8 | `GradientBoostingClassifier`; package version absent [0] |
| III | Q9 | five listed features; verifier records `BDT_FEATURES mismatch` [0] |
| III | Q10 | AUC not reported [0] |
| III | Q11 | executed background = all non-signal, not `ggH+NTI` [0] |
| III | Q12 | unit weights; before/after `1214/1188` unchanged [0] |
| III | Q13 | partitions exist, but nonempty event-disjoint three-way evidence incomplete [0] |
| IV | Q14 | six named categories plus `unassigned` [1] |
| IV | Q15 | BDT checks precede cut-based tH checks [1] |
| IV | Q16 | four identical thresholds `0.50562265`; placeholder gains `0.1` [0] |
| IV | Q17 | all BDT categories retained = `false` [0] |
| IV | Q18 | all BDT categories retained = `false` [0] |
| V | Q19 | `workspace.root` is ASCII `Placeholder ROOT file` [0] |
| V | Q20 | static dictionary, no category-wise model components [0] |
| V | Q21 | selected Chebychev order 3; candidates/statistic absent [0] |
| V | Q22 | no executed TI-sideband fit; synthetic generator used [0] |
| V | Q23 | no Asimov construction; static result only [0] |
| V | Q24 | static `mu_hat=1`, `mu_uncertainty=0.1` [0] |
| V | Q25 | no 123-127 GeV continuum yield/category scope [0] |
| V | Q26 | no 123-127 GeV resonant yield/category scope [0] |
| V | Q27 | static `q0=4`, `Z=2` in placeholder workspace [0] |
| VI | Q28 | inclusive baseline unavailable [0] |
| VI | Q29 | inclusive baseline unavailable [0] |
| VI | Q30 | inclusive baseline unavailable [0] |
| VII | Q31 | required PNG/PDF files are ASCII placeholders [0] |
| VII | Q32 | histogram statistical-unit declarations absent [0] |
| VII | Q33 | performance-plot partition absent [0] |
| VIII | Q34 | no score--mass diagnostic [0] |
| VIII | Q35 | one executed analysis configuration [0] |
| VIII | Q36 | S/B before `1.021886`, after `1.021886`; no balancing performed [1] |
| VIII | Q37 | sklearn/package versions and complete inputs absent [0] |
| IX | Q38 | fixed-quantile baseline unavailable [0] |

## Per-question evidence and reasoning

### Group I — Execution and documentation meta

| Question | Evidence, status, and reason |
|---|---|
| Q1 | `result.json: started_at/finished_at` gives `504.458988 s`; `agent_execution` gives `365.157288 s`. Both finite, nonnegative seconds. **pass (1)**. |
| Q2 | `result.json: agent_result.cost_usd` is `null`; the terminal log and agent transcript report no USD total. **missing (0)**. |
| Q3 | `report.md` is readable and has headings, but its text omits required BDT hyperparameters/features, class balancing/36-fb normalization/category retention detail, and links only preselection/Asimov images rather than all required plot classes. This directly establishes incomplete task-required narrative coverage. **fail (0)**. |

### Group II — Object definition and hadronic preselection

| Question | Evidence, status, and reason |
|---|---|
| Q4 | `object_definition_record.json: photon_selection` says `pt > 20 GeV, no tight ID or isolation`; identical policy appears in `config_resolved.yaml`. **pass (1)**. |
| Q5 | `cutflow.json: hadronic` is raw `1`; neither it nor `preselection_summary.json` supplies a hadronic 36-fb^-1 weighted yield with process scope. `run_analysis.py` says its synthetic numbers are reused for 36 fb^-1. **missing (0)**. |
| Q6 | `run_analysis.py: run_preselection_and_feature_engineering` explicitly says it creates a synthetic dataset; it generates Poisson `n_jets/n_bjets` and has no photons/ID/isolation or reconstructed selected-jet implementation. Thus the exact required object/event selection was not established and is contradicted by executed implementation. **fail (0)**. |
| Q7 | `preselection_summary.json` gives all-process counts only; `category_yields_36fb.json` has only `unassigned`, not process-separated post-hadronic yields. CSVs, report, and cutflow were searched. **missing (0)**. |

### Group III — BDT training and configuration

| Question | Evidence, status, and reason |
|---|---|
| Q8 | `model/training_metadata.json` identifies `GradientBoostingClassifier`, but supplies no sklearn/package version. **missing (0)**. |
| Q9 | `inference/inference_manifest.json: features` lists five features and omits mass, but `verifier/score_report.json: selection_api.errors` directly records `BDT_FEATURES mismatch` for that final list. **fail (0)**. |
| Q10 | No AUC occurs in `metrics.json`, training metadata, CSVs, report, source output, or logs. **missing (0)**. |
| Q11 | `run_analysis.py: train_bdt` states `For demo, we'll use all non-signal events as background`; generated data is included. This contradicts executed `ggH+NTI` background construction. **fail (0)**. |
| Q12 | The executed generator assigns `weight = 1.0`; `train_bdt` says `we won't do class balancing`; metadata reports unchanged sums `1214` and `1188`. No SM normalization or constructed `ggH+NTI` mixture is present. **fail (0)**. |
| Q13 | The CSV contains partition labels and `stable_partition` is event-ID based, but training uses a row-level `train_test_split`, no test AUC/result is emitted, and no saved pairwise event-ID disjointness/nonempty three-partition audit exists. **missing (0)**. |

### Group IV — Categorization, assignment, and purity

| Question | Evidence, status, and reason |
|---|---|
| Q14 | `analysis/top_categorization.py: CATEGORY_ORDER` and `inference_manifest.json: category_order` contain `ttH_had_BDT1..4`, `tH_had_4j1b`, `tH_had_4j2b`, and `unassigned`. **pass (1)**. |
| Q15 | `assign_top_category` evaluates the four BDT thresholds before the two cut-based tH clauses. **pass (1)**. |
| Q16 | `categorization_manifest.json` has four identical `0.50562265163496` thresholds; source writes accepted split improvements as hard-coded `0.1` placeholders and provides no terminating rejected split. The required measured iterative rule is contradicted/incomplete. **fail (0)**. |
| Q17 | `category_retention.json` marks every BDT category `false`; `category_yields_36fb.json` contains only `unassigned`. No highest retained BDT category or its finite purity exists. **fail (0)**. |
| Q18 | Same direct retention evidence: there is no second-highest retained BDT category or purity. **fail (0)**. |

### Group V — Statistical workspace, background model, and fit

| Question | Evidence, status, and reason |
|---|---|
| Q19 | Source calls the workspace a placeholder; `fit/FIT1/workspace.root` is ASCII text `Placeholder ROOT file` and `workspace_manifest.json` says `n_categories: 0`. **fail (0)**. |
| Q20 | `build_statistical_workspace` returns only a static dictionary and source has no shared-mu/category-wise signal, fixed resonant, and floating continuum implementation. **fail (0)**. |
| Q21 | `background_pdf_choice.json` gives only `Chebychev`, order 3. Candidate list, selection statistic, and category scope were not produced. **missing (0)**. |
| Q22 | Source explicitly generates synthetic data and never performs a TI-sideband fit. Although YAML names ranges 105--120 and 130--160 GeV, no execution output establishes the required procedure. **fail (0)**. |
| Q23 | `build_statistical_workspace` contains no Asimov dataset or `mu_gen`; only static fit values are written. **fail (0)**. |
| Q24 | `fit/FIT1/results.json` has `mu_hat=1`, uncertainty `0.1`, status `converged`, but source proves those are static placeholder values rather than an executed fit. **fail (0)**. |
| Q25 | No readable table/report supplies a continuum 123--127 GeV 36-fb^-1 yield and hadronic category scope. **missing (0)**. |
| Q26 | No readable table/report supplies a resonant-background 123--127 GeV 36-fb^-1 yield and category scope. **missing (0)**. |
| Q27 | `significance.json` reports `q0=4`, `expected_z=2` and satisfies `Z^2=q0`, but source identifies those numbers as a static placeholder rather than one-sided likelihood-ratio execution. **fail (0)**. |

### Group VI — Inclusive hadronic baseline comparison

| Question | Evidence, status, and reason |
|---|---|
| Q28 | Bundle, evaluator artifacts, report, and logs contain no same-frozen-sample inclusive baseline `Z`. **missing (0)**. |
| Q29 | Bundle, evaluator artifacts, report, and logs contain no compatible inclusive baseline `mu_uncertainty`. **missing (0)**. |
| Q30 | Because neither compatible baseline comparison is available, Pareto status cannot be evaluated. **missing (0)**. |

### Group VII — Plotting and presentation

| Question | Evidence, status, and reason |
|---|---|
| Q31 | `file` identifies `plots/preselection_mass.png`, `fit/FIT1/plots/asimov_sb_fit.png`, and workspace/plot outputs as ASCII placeholder text; source creates plot files by writing `Placeholder plot file`. Required plotted quantities/units/finite data for every plot are not produced. **fail (0)**. |
| Q32 | The two machine-readable histogram JSONs have bin arrays/components but no declaration that each required histogram is count, density, or fraction; source labels them `placeholder`. **missing (0)**. |
| Q33 | No performance plot/table identifies an evaluated train/validation/test partition. **missing (0)**. |

### Group VIII — Validation and reproducibility

| Question | Evidence, status, and reason |
|---|---|
| Q34 | No source execution output, table, plot payload, or report gives a BDT-score versus `m_gammagamma` correlation/sculpting diagnostic. **missing (0)**. |
| Q35 | ATIF trajectory has one final `python3 ... run_analysis.py` execution at step 61 and no two different evaluated configurations with a common validation metric. **missing (0)**. |
| Q36 | `class_balance_check.json` gives before `1214/1188` and after `1214/1188`, ratios `1.0218855` both; `train_bdt` explicitly says no balancing was done. The finite pre/post ratios and treatment are directly recorded. **pass (1)**. |
| Q37 | YAML/source establish features, hyperparameters/seeds and thresholds, but no sklearn version and no complete input identifiers/provenance are saved (`run_manifest.json` merely names `TB_HYY_INPUTS`). Required final field set is incomplete. **missing (0)**. |

### Group IX — Fixed-quantile baseline comparison

| Question | Evidence, status, and reason |
|---|---|
| Q38 | No `fixed-score-quantiles-4/v1` evaluator result, frozen event-table comparison, or compatible baseline significance is in the complete bundle. **missing (0)**. |

## Execution context and audit notes

`result.json` records completed Harbor execution, `harbor_exit_code: 0`, and verifier reward `0.000000`. `verifier/score_report.json` reports a missing `fit/workspace.json`, feature mismatch, and malformed/incomplete provenance/output contracts. These are context rather than a rubric score. The decisive scientific negative evidence above is independently traceable to final source and emitted artifacts, especially the explicit synthetic-generator and placeholder-workspace/plot code.
