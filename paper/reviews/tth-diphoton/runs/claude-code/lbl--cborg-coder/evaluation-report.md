# Manual evidence review: ttH diphoton BDT categorization

This is a non-authoritative, single-run evidence review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`.  It is not an indexed outcome grade.  Reviewed run: `20260904T210145Z-tth-diphoton-bd__MqqLxno` (`haichenwangberkeley/tth-diphoton-bdt-categorization`, Claude Code / `lbl/cborg-coder`).

## Evidence-audit scope

The complete readable run root was inventoried before assessment. It contains run metadata (`result.json`, `config.json`, `lock.json`), terminal/agent records (`trial.log`, `agent/claude-code.txt`, `agent/trajectory.json`, and the session JSONL plus tool-result text), verifier records (`verifier/ctrf.json`, `verifier/test-stdout.txt`, `verifier/score_report.json`, `verifier/reward.txt`), and `artifacts/manifest.json`.  There are no saved submitted-source files, task-output tables (JSON/CSV/Parquet), plots, workspaces, analysis reports, or captured results directories in the inventory. `artifacts/manifest.json` records both requested artifact roots as failed downloads because the corresponding container paths did not exist.

The transcript was searched for preselection/object definitions, yields, BDT training/features/AUC/classes/splits/categories, RooFit/workspace/Asimov/fit/significance quantities, baselines, plots, correlation/optimization/reproducibility, and validation checks. The only task-relevant direct result is that `/root/submission/tth-diphoton-bdt` did not exist; its parent `/root/submission` and `/root/results` were empty. The verifier independently reports missing submission module, preselected-event table, training metadata, input contract, and run manifest. Thus a missing status below means the specified evidence is unavailable after these concrete searches; it is not based merely on a preferred filename. No criterion receives a failure because no criterion-specific calculation was produced that directly contradicts its required condition.

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / lbl/cborg-coder | 2 | 0 | 36 | completed / 0.000000 |

## 2. Total reward (raw, no averaging)

| Summary | Claude Code / lbl/cborg-coder |
|---|---:|
| Total reward | 2 / 38 |

## 3. Overall equal-category reward

| Summary | Claude Code / lbl/cborg-coder |
|---|---:|
| Overall equal-category reward | 0.074074 |

This is the mean of the nine group pass fractions: `2/3, 0/4, 0/6, 0/5, 0/9, 0/3, 0/3, 0/4, 0/1`.

## 4. Per-question binary rewards

| Category | Question | Claude Code / lbl/cborg-coder |
|---|---|---:|
| Execution and documentation meta | Q1 Run timing | 1 |
| Execution and documentation meta | Q2 Run cost | 1 |
| Execution and documentation meta | Q3 Human-facing documentation | 0 |
| Object definition and hadronic preselection | Q4 Photon identification and isolation policy | 0 |
| Object definition and hadronic preselection | Q5 Hadronic-channel event count | 0 |
| Object definition and hadronic preselection | Q6 Hadronic preselection | 0 |
| Object definition and hadronic preselection | Q7 Post-preselection Higgs yields | 0 |
| BDT model training and configuration | Q8 BDT training package | 0 |
| BDT model training and configuration | Q9 BDT input features | 0 |
| BDT model training and configuration | Q10 Signal-background AUC | 0 |
| BDT model training and configuration | Q11 Training classes | 0 |
| BDT model training and configuration | Q12 Training class weights | 0 |
| BDT model training and configuration | Q13 Train/validation/test partition | 0 |
| Categorization, event assignment, and purity | Q14 BDT category count | 0 |
| Categorization, event assignment, and purity | Q15 BDT event categorization | 0 |
| Categorization, event assignment, and purity | Q16 Categorization figure of merit | 0 |
| Categorization, event assignment, and purity | Q17 Highest-score ttH purity | 0 |
| Categorization, event assignment, and purity | Q18 Second-highest-score ttH purity | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q19 Fit-based sensitivity assessment | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q20 Statistical signal definition | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q21 Analytical fit-function choice | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q22 Background PDF determination | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q23 S+B Asimov data set | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q24 S+B Asimov fit result | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q25 Continuum background yield, 123–127 GeV | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q26 Resonant background yield, 123–127 GeV | 0 |
| Statistical workspace, background modeling, and sensitivity fit | Q27 Expected significance | 0 |
| Inclusive hadronic baseline comparison | Q28 Expected-significance comparison | 0 |
| Inclusive hadronic baseline comparison | Q29 Signal-strength precision comparison | 0 |
| Inclusive hadronic baseline comparison | Q30 Baseline Pareto improvement | 0 |
| Plotting and presentation quality | Q31 Plot quantity and labeling | 0 |
| Plotting and presentation quality | Q32 Histogram normalization | 0 |
| Plotting and presentation quality | Q33 Performance-plot partition | 0 |
| Validation and reproducibility | Q34 Score–mass correlation | 0 |
| Validation and reproducibility | Q35 Optimization attempts | 0 |
| Validation and reproducibility | Q36 Class-imbalance accounting | 0 |
| Validation and reproducibility | Q37 Final configuration reproducibility | 0 |
| Fixed-quantile category baseline comparison | Q38 Expected significance vs. fixed quantile categories | 0 |

## 5. Per-question observed values and rewards

| Category | Question | Claude Code / lbl/cborg-coder |
|---|---|---|
| Meta | Q1 | `242.377458 s` wall clock; `124.641067 s` agent execution [1] |
| Meta | Q2 | `$1.032273 USD` total cost [1] |
| Meta | Q3 | No task analysis narrative [0] |
| Preselection | Q4 | Not established [0] |
| Preselection | Q5 | Not established [0] |
| Preselection | Q6 | Not established [0] |
| Preselection | Q7 | Not established [0] |
| Training | Q8 | Not established [0] |
| Training | Q9 | Not established [0] |
| Training | Q10 | Not established [0] |
| Training | Q11 | Not established [0] |
| Training | Q12 | Not established [0] |
| Training | Q13 | Not established [0] |
| Categorization | Q14 | Not established [0] |
| Categorization | Q15 | Not established [0] |
| Categorization | Q16 | Not established [0] |
| Categorization | Q17 | Not established [0] |
| Categorization | Q18 | Not established [0] |
| Fit | Q19 | Not established [0] |
| Fit | Q20 | Not established [0] |
| Fit | Q21 | Not established [0] |
| Fit | Q22 | Not established [0] |
| Fit | Q23 | Not established [0] |
| Fit | Q24 | Not established [0] |
| Fit | Q25 | Not established [0] |
| Fit | Q26 | Not established [0] |
| Fit | Q27 | Not established [0] |
| Inclusive baseline | Q28 | Agent/baseline values not established [0] |
| Inclusive baseline | Q29 | Agent/baseline values not established [0] |
| Inclusive baseline | Q30 | Agent/baseline values not established [0] |
| Plots | Q31 | No task-required plots [0] |
| Plots | Q32 | No task-required histograms [0] |
| Plots | Q33 | No task-required performance plots [0] |
| Validation | Q34 | Not established [0] |
| Validation | Q35 | Not established [0] |
| Validation | Q36 | Not established [0] |
| Validation | Q37 | Not established [0] |
| Quantile baseline | Q38 | Agent/quantile-baseline values not established [0] |

## 6. Per-question evidence and reasoning

### Execution and documentation meta

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q1 Run timing | `242.377458 s` wall clock (`result.json`: 21:02:28.286801Z–21:06:30.664259Z) and `124.641067 s` pure agent execution (`agent_execution`: 21:02:46.151355Z–21:04:50.792422Z). **pass**, both finite nonnegative values with units. |
| Q2 Run cost | `$1.032273 USD` in `result.json: agent_result.cost_usd`, consistent with `agent/trajectory.json: final_metrics.total_cost_usd`. **pass**. |
| Q3 Human-facing documentation | **missing**. `agent/claude-code.txt` ends with a request for the absent pipeline; inventory and `artifacts/manifest.json` contain no analysis report or output. |

### Object definition and hadronic preselection

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q4 Photon identification and isolation policy | **missing**. Searched transcript, session, source-artifact destination, outputs, tables, and reports; no saved object-definition evidence. `artifacts/manifest.json` says submission root failed. |
| Q5 Hadronic-channel event count | **missing**. No preselected-event table or produced count/yield; verifier `score_report.json: artifact_contract` reports the table missing. |
| Q6 Hadronic preselection | **missing**. No implementation or executed selection exists in the readable bundle; verifier `score_report.json: preselection_physics` reports the preselected table missing. |
| Q7 Post-preselection Higgs yields | **missing**. No process-separated table, report, or terminal output was produced after the exhaustive artifact and transcript search. |

### BDT model training and configuration

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q8 BDT training package | **missing**. No source or training record; verifier `score_report.json: bdt_training` reports missing `model/training_metadata.json`. |
| Q9 BDT input features | **missing**. No final feature list/source exists; transcript contains no BDT implementation. |
| Q10 Signal-background AUC | **missing**. No held-out prediction/result table, training record, or finite AUC exists. |
| Q11 Training classes | **missing**. No training configuration or source evidence exists. |
| Q12 Training class weights | **missing**. No class weights, pre/post balance values, or training result exists. |
| Q13 Train/validation/test partition | **missing**. No event-ID partitions, split rule, or source was saved. |

### Categorization, event assignment, and purity

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q14 BDT category count | **missing**. No categorization source/output exists; verifier reports missing required submission module. |
| Q15 BDT event categorization | **missing**. No priority-assignment implementation or output exists. |
| Q16 Categorization figure of merit | **missing**. No thresholds, split gains, or stopping record exists. |
| Q17 Highest-score ttH purity | **missing**. No retained-category yields or ratio exists. |
| Q18 Second-highest-score ttH purity | **missing**. No retained-category yields or ratio exists. |

### Statistical workspace, background modeling, and sensitivity fit

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q19 Fit-based sensitivity assessment | **missing**. Inventory contains no RooFit workspace or Asimov-fit output, and transcript shows the source pipeline was absent. |
| Q20 Statistical signal definition | **missing**. No workspace, source, or fit report defines signal/background components. |
| Q21 Analytical fit-function choice | **missing**. No candidate/selected function, statistic, or category scope exists. |
| Q22 Background PDF determination | **missing**. No TI-sideband fit or 105–160 GeV extrapolation record exists. |
| Q23 S+B Asimov data set | **missing**. No `mu_gen = 1` Asimov construction evidence exists. |
| Q24 S+B Asimov fit result | **missing**. No `mu_hat`, uncertainty, fit status, or covariance status exists. |
| Q25 Continuum background yield, 123–127 GeV | **missing**. No finite 36 fb^-1 continuum yield/category scope exists. |
| Q26 Resonant background yield, 123–127 GeV | **missing**. No finite 36 fb^-1 resonant yield/category scope exists. |
| Q27 Expected significance | **missing**. No finite one-sided `q0`/`Z` calculation exists. |

### Inclusive hadronic baseline comparison

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q28 Expected-significance comparison | **missing**. Agent expected `Z`, compatible fit inputs, and same-sample inclusive-baseline result are all unavailable; no comparison can be formed. |
| Q29 Signal-strength precision comparison | **missing**. Agent `mu_uncertainty`, compatible fit inputs, and baseline value are unavailable. |
| Q30 Baseline Pareto improvement | **missing**. Both required comparison metrics and compatibility evidence are unavailable. |

### Plotting and presentation quality

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q31 Plot quantity and labeling | **missing**. The run inventory has no task-required plot files or produced plotted values. |
| Q32 Histogram normalization | **missing**. No task-required histogram or normalization declaration exists. |
| Q33 Performance-plot partition | **missing**. No task-required performance plot or partition record exists. |

### Validation and reproducibility

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q34 Score–mass correlation | **missing**. No score/mass table, diagnostic method, sample, or finite correlation result exists. |
| Q35 Optimization attempts | **missing**. No model/feature/category attempt with a common validation metric exists; the transcript only investigates absent files. |
| Q36 Class-imbalance accounting | **missing**. No pre/post balancing ratios or balancing treatment exists. |
| Q37 Final configuration reproducibility | **missing**. No final source/configuration or clean-output rerun exists; all required configuration fields are unavailable. |

### Fixed-quantile category baseline comparison

| Question | Claude Code / lbl/cborg-coder |
|---|---|
| Q38 Expected significance vs. fixed quantile categories | **missing**. No continuous BDT score table, agent `Z`, compatible fixed-quantile evaluator result, or fit-assumption evidence exists. |

## Execution context and direct negative evidence

The Harbor trial completed without `exception_info`; that does not establish task-scientific outputs. The verifier reward is `0.000000`. Direct execution evidence is: `agent/claude-code.txt` first records `ls -R /root/submission/tth-diphoton-bdt` with exit code 2, then shows empty `/root/submission` and `/root/results`, and ends without a submission. `verifier/ctrf.json` records six failed checks (0 passed): missing `analysis/top_categorization.py`, missing preselected-events table, missing input-data contract, missing training metadata, and missing run manifest. This report retains those facts separately from its non-authoritative rubric evidence.
