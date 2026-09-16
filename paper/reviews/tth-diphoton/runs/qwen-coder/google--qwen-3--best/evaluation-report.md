# Manual ttH diphoton rubric evaluation

Manual, evidence-backed, non-authoritative review of one preserved trial. This is not an indexed outcome grade. The readable bundle contains source, sparse metadata, six placeholder-style plots, terminal trajectory, and verifier records, but not the submitted tables, trained-model metadata, workspace, fit JSON, or `report.md` claimed by the agent. Consequently no evaluator-side baseline comparison is available. Harbor completed; verifier reward is separately retained as `0.000000`.

Run: `qwen-coder / google/qwen-3 / 20260905T041241Z-tth-diphoton-bd__JmY5P4p` (cohort `Best`). Status codes: P pass, F fail, M missing; every non-pass has reward 0.

## 1. Status summary

### Best

| Status | qwen-coder / google/qwen-3 |
|---|---:|
| P | 6 |
| F | 5 |
| N | 0 |
| M | 27 |
| A | 0 |
| E | 0 |
| Harbor status / verifier reward | completed / 0.000000 |

## 2. Total reward (raw, no averaging)

| Cohort | qwen-coder / google/qwen-3 |
|---|---:|
| Best | 6 / 38 |

## 3. Overall equal-category reward

| Cohort | qwen-coder / google/qwen-3 |
|---|---:|
| Best | 0.1401 |

Arithmetic mean of the nine rubric-group pass fractions: 1/3, 1/4, 1/6, 2/5, 1/9, 0/3, 0/3, 0/4, and 0/1.

## 4. Per-question binary rewards

### Best

| Category | Question | qwen-coder / google/qwen-3 |
|---|---|---:|
| Execution and Documentation Meta | Q1. Run timing | 1 |
| Execution and Documentation Meta | Q2. Run cost | 0 |
| Execution and Documentation Meta | Q3. Human-facing documentation | 0 |
| Object Definition and Hadronic Preselection | Q4. Photon identification and isolation policy | 1 |
| Object Definition and Hadronic Preselection | Q5. Hadronic-channel event count | 0 |
| Object Definition and Hadronic Preselection | Q6. Hadronic preselection | 0 |
| Object Definition and Hadronic Preselection | Q7. Post-preselection Higgs yields | 0 |
| BDT Model Training and Configuration | Q8. BDT training package | 0 |
| BDT Model Training and Configuration | Q9. BDT input features | 0 |
| BDT Model Training and Configuration | Q10. Signal-background AUC | 0 |
| BDT Model Training and Configuration | Q11. Training classes | 1 |
| BDT Model Training and Configuration | Q12. Training class weights | 0 |
| BDT Model Training and Configuration | Q13. Train/validation/test partition | 0 |
| Categorization, Event Assignment, and Purity | Q14. BDT category count | 1 |
| Categorization, Event Assignment, and Purity | Q15. BDT event categorization | 1 |
| Categorization, Event Assignment, and Purity | Q16. Categorization figure of merit | 0 |
| Categorization, Event Assignment, and Purity | Q17. Highest-score ttH purity | 0 |
| Categorization, Event Assignment, and Purity | Q18. Second-highest-score ttH purity | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q19. Fit-based sensitivity assessment | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q20. Statistical signal definition | 1 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q21. Analytical fit-function choice | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q22. Background PDF determination | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q23. S+B Asimov data set | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q24. S+B Asimov fit result | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q25. Continuum background yield, 123–127 GeV | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q26. Resonant background yield, 123–127 GeV | 0 |
| Statistical Workspace, Background Modeling, and Sensitivity Fit | Q27. Expected significance | 0 |
| Inclusive Hadronic Baseline Comparison | Q28. Expected-significance comparison | 0 |
| Inclusive Hadronic Baseline Comparison | Q29. Signal-strength precision comparison | 0 |
| Inclusive Hadronic Baseline Comparison | Q30. Baseline Pareto improvement | 0 |
| Plotting and Presentation Quality | Q31. Plot quantity and labeling | 0 |
| Plotting and Presentation Quality | Q32. Histogram normalization | 0 |
| Plotting and Presentation Quality | Q33. Performance-plot partition | 0 |
| Validation and Reproducibility | Q34. Score–mass correlation | 0 |
| Validation and Reproducibility | Q35. Optimization attempts | 0 |
| Validation and Reproducibility | Q36. Class-imbalance accounting | 0 |
| Validation and Reproducibility | Q37. Final configuration reproducibility | 0 |
| Fixed-Quantile Category Baseline Comparison | Q38. Expected significance vs. fixed quantile categories | 0 |

## 5. Per-question observed values and rewards

### Best

| Category | Question | qwen-coder / google/qwen-3 |
|---|---|---|
| Meta | Q1 | 1764.054 s wall; 1624.299 s agent [1] |
| Meta | Q2 | N/A [M] |
| Meta | Q3 | N/A [M] |
| Preselection | Q4 | tight ID=false; isolation=false [1] |
| Preselection | Q5 | raw 0; 36 fb^-1 yield N/A [M] |
| Preselection | Q6 | photon eta_max=null; incomplete [M] |
| Preselection | Q7 | by-process={} [M] |
| Training | Q8 | scikit-learn named; version N/A [M] |
| Training | Q9 | verifier feature mismatch [0] |
| Training | Q10 | AUC N/A [M] |
| Training | Q11 | signal ttH+tH; background ggH+NTI [1] |
| Training | Q12 | heuristic constant weights, not SM-normalized [0] |
| Training | Q13 | partition output N/A [M] |
| Categorization | Q14 | 6 named categories plus unassigned [1] |
| Categorization | Q15 | BDT evaluated before cut-based tH [1] |
| Categorization | Q16 | 5% code; accepted splits/thresholds N/A [M] |
| Categorization | Q17 | N/A [M] |
| Categorization | Q18 | N/A [M] |
| Fit | Q19 | source explicitly says RooFit is a placeholder [0] |
| Fit | Q20 | shared mu; ttH+tH; fixed resonant; floating continuum [1] |
| Fit | Q21 | candidate/selection result N/A [M] |
| Fit | Q22 | synthetic placeholder, no TI-sideband result [0] |
| Fit | Q23 | mu_gen=1 N/A [M] |
| Fit | Q24 | hard-coded synthetic mu=1.02 ±0.15, no result artifact [0] |
| Fit | Q25 | N/A [M] |
| Fit | Q26 | N/A [M] |
| Fit | Q27 | q0/Z execution result N/A [M] |
| Inclusive baseline | Q28 | NaN / NaN [M] |
| Inclusive baseline | Q29 | NaN / NaN [M] |
| Inclusive baseline | Q30 | NaN / NaN [M] |
| Presentation | Q31 | required plot payloads N/A [M] |
| Presentation | Q32 | required histogram JSON N/A [M] |
| Presentation | Q33 | performance partition N/A [M] |
| Validation | Q34 | score–mass diagnostic N/A [M] |
| Validation | Q35 | common-validation attempts N/A [M] |
| Validation | Q36 | before/after ratios N/A [M] |
| Validation | Q37 | thresholds, versions, IDs N/A [M] |
| Quantile baseline | Q38 | NaN / NaN [M] |

## 6. Evidence and reasoning

### Execution and Documentation Meta

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q1. Run timing | `1764.054 s wall; 1624.299 s agent` [pass]; `result.json: started_at/finished_at` and `agent_execution`; finite timestamp differences. |
| Q2. Run cost | `N/A` [missing]; `result.json: agent_result.cost_usd=null`; no other USD total in `trial.log`, trajectory, source, or results. |
| Q3. Human-facing documentation | `N/A` [missing]; inventory and `artifacts/root/results/...` contain no `report.md`; `agent/qwen-code.txt` is unsupported prose, not the claimed report. |

### Object Definition and Hadronic Preselection

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q4. Photon identification and isolation policy | `false / false` [pass]; `object_definition_record.json: photon_selection.tight_id_required,isolation_required`. |
| Q5. Hadronic-channel event count | `0 raw; weighted 36 fb^-1 N/A` [missing]; `preselection_summary.json: counts`; `cutflow.json`, tables, and report searched. |
| Q6. Hadronic preselection | `eta_max=null` [missing]; object/config records give pT and b-tag but not full photon acceptance; source also applies `n_leptons`/`n_jets` without selected-object pT filtering. |
| Q7. Post-preselection Higgs yields | `by_process={}` [missing]; `preselection_summary.json`; no preselected table or yield JSON in inventory. |

### BDT Model Training and Configuration

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q8. BDT training package | `GradientBoostingClassifier; version N/A` [missing]; `analyze.py: train_bdt`; absent `model/training_metadata.json`. |
| Q9. BDT input features | `mismatched list` [fail]; `verifier/score_report.json: selection_api.errors` directly reports `BDT_FEATURES mismatch`. |
| Q10. Signal-background AUC | `N/A` [missing]; no training metadata/table/logged finite test AUC; source computes validation AUC only. |
| Q11. Training classes | `ttH+tH / ggH+NTI` [pass]; `analyze.py: create_training_sample` defines those masks and mixtures. |
| Q12. Training class weights | `constant 2.0/1.0/0.5` [fail]; `analyze.py: load_root_file` calls weights simplified constants, contradicting required SM-normalized construction. |
| Q13. Train/validation/test partition | `N/A` [missing]; source proposes `stable_partition`, but training/parquet outputs and saved ID sets are absent. |

### Categorization, Event Assignment, and Purity

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q14. BDT category count | `six names + unassigned` [pass]; `analysis/top_categorization.py: CATEGORY_ORDER`. |
| Q15. BDT event categorization | `BDT before tH cuts` [pass]; `analysis/top_categorization.py: assign_top_category`. |
| Q16. Categorization figure of merit | `5% implemented; results N/A` [missing]; `optimize_bdt_boundaries` has 0.05 but no `accepted_splits.json` or `thresholds.json`. |
| Q17. Highest-score ttH purity | `N/A` [missing]; category yields/tables unavailable after inventory search. |
| Q18. Second-highest-score ttH purity | `N/A` [missing]; category yields/tables unavailable after inventory search. |

### Statistical Workspace, Background Modeling, and Sensitivity Fit

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q19. Fit-based sensitivity assessment | `placeholder` [fail]; `analyze.py: create_workspace` says real ROOT/RooFit is a placeholder; no workspace artifact. |
| Q20. Statistical signal definition | `shared mu, ttH+tH, fixed resonant, floating continuum` [pass]; `analyze.py: create_report/create_workspace` specifies this model. |
| Q21. Analytical fit-function choice | `N/A` [missing]; no candidate list/statistic/selected-function artifact or source implementation. |
| Q22. Background PDF determination | `synthetic plot` [fail]; `analyze.py: create_placeholder_plots` generates synthetic sidebands; no TI sideband-fit execution output. |
| Q23. S+B Asimov data set | `mu_gen N/A` [missing]; source/plots and missing `significance_asimov_construction.json` do not establish mu_gen=1 execution. |
| Q24. S+B Asimov fit result | `hard-coded synthetic 1.02 ± 0.15` [fail]; `create_workspace` labels synthetic results; absent fit result cannot validate a real fit. |
| Q25. Continuum yield | `N/A` [missing]; no category yield/fit result table. |
| Q26. Resonant yield | `N/A` [missing]; no category yield/fit result table. |
| Q27. Expected significance | `N/A` [missing]; source hard-codes 6.25/2.5 but no direct execution result artifact. |

### Inclusive Hadronic Baseline Comparison

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q28. Expected-significance comparison | `NaN / NaN` [missing]; no compatible agent fit, frozen comparison table, or baseline rerun. |
| Q29. Signal-strength precision comparison | `NaN / NaN` [missing]; no compatible fit/baseline uncertainty. |
| Q30. Baseline Pareto improvement | `NaN / NaN` [missing]; Q28–Q29 inputs unavailable. |

### Plotting and Presentation Quality

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q31. Plot quantity and labeling | `N/A` [missing]; six readable PNG/PDF files exist, but required BDT/category payloads and machine-readable values are absent; source calls them placeholders. |
| Q32. Histogram normalization | `N/A` [missing]; no required histogram JSON survives; no complete required-plot normalization evidence. |
| Q33. Performance-plot partition | `N/A` [missing]; no score histogram/training result; source's intended train+validation plot is not produced. |

### Validation and Reproducibility

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q34. Score–mass correlation | `N/A` [missing]; logs, source, output JSON/tables, plots, workspace, and report lack a diagnostic result. |
| Q35. Optimization attempts | `N/A` [missing]; trajectory shows retries but no two distinct scored configurations on common validation data. |
| Q36. Class-imbalance accounting | `N/A` [missing]; source intends a check but `model/class_balance_check.json` is absent. |
| Q37. Final configuration reproducibility | `N/A` [missing]; config has seed/features but lacks final hyperparameters, thresholds, package versions, and input identifiers. |

### Fixed-Quantile Category Baseline Comparison

| Question | qwen-coder / google/qwen-3 |
|---|---|
| Q38. Expected significance vs. fixed quantile categories | `NaN / NaN` [missing]; no frozen continuous-score table, compatible fit, or fixed-quantile baseline result. |

### Exact artifact roots

- `<source-repository>/results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/google--qwen-3--best/20260905T041241Z-tth-diphoton-bdt-categorization-qwen-coder-503382/20260905T041241Z-tth-diphoton-bd__JmY5P4p`
- Inspected: `result.json`, `config.json`, `trial.log`, `agent/qwen-code.txt`, `agent/trajectory.json`, session JSONL, all `verifier/*`, `artifacts/manifest.json`, both submitted source files, every listed `artifacts/root/results/tth-diphoton-bdt` JSON/YAML/plot file.
