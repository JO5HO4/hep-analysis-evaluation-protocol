# ttH diphoton manual evidence review

Run: `20260905T003430Z-tth-diphoton-bd__st37ant`  
Task / agent / model: `tth-diphoton / terminus-2 / openai/lbl/cborg-coder`  
Scope: non-authoritative review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`. This is not an outcome grade. Evidence audit covered the complete readable bundle: metadata, terminal transcript, submitted source, CSV outputs, JSON, report, verifier outputs, artifact manifest, and the artifact inventory (no plots, workspaces, Parquet files, or additional reports were present).

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus-2 / lbl-cborg-coder | 2 | 12 | 24 | completed / 0.000000 |

## Total reward (raw, no averaging)

| Summary | Terminus-2 / lbl-cborg-coder |
|---|---:|
| Total reward | 2 / 38 |

## Overall equal-category reward

| Summary | Terminus-2 / lbl-cborg-coder |
|---|---:|
| Overall equal-category reward | 0.0593 |

The nine group pass fractions are I `1/3`, II `0/4`, III `0/6`, IV `1/5`, V `0/9`, VI `0/3`, VII `0/3`, VIII `0/4`, IX `0/1`; their arithmetic mean is shown above.

## Per-question binary rewards and observed values

| Group | Criterion | Reward | Observed value |
|---|---|---:|---|
| I | Q1 Run timing | 1 | wall `2412.898 s`; agent execution `2276.882 s` |
| I | Q2 Run cost | 0 | `null USD` |
| I | Q3 Human-facing documentation | 0 | two-line report only |
| II | Q4 Photon ID/isolation policy | 0 | no photon selection in executed preselection source |
| II | Q5 Hadronic-channel event count | 0 | raw hadronic rows `286,845`; no reported 36-fb^-1 yield |
| II | Q6 Hadronic preselection | 0 | lepton/jet/b-tag portions only; photon acceptance absent |
| II | Q7 Post-preselection Higgs yields | 0 | process rows exist; no process-separated 36-fb^-1 yield output |
| III | Q8 BDT training package | 0 | `sklearn.ensemble.GradientBoostingClassifier`; version absent |
| III | Q9 BDT input features | 0 | uses `central_jets`, not required `central_jet_multiplicity` |
| III | Q10 Signal-background AUC | 0 | no held-out AUC |
| III | Q11 Training classes | 0 | signal `ttH+tH`; background is all non-signal, not `ggH+NTI` |
| III | Q12 Training class weights | 0 | no physical/balancing records |
| III | Q13 Train/validation/test partition | 0 | `train_test_split`; no validation partition or stable-ID use |
| IV | Q14 BDT category count | 0 | predictions: only `ttH_had_BDT1`, tH cuts, unassigned |
| IV | Q15 BDT event categorization | 1 | BDT branch precedes tH cut branches |
| IV | Q16 Categorization figure of merit | 0 | thresholds `[0.2,0.4,0.6,0.8]`; no executed gains/stopping record |
| IV | Q17 Highest-score ttH purity | 0 | no physical ttH/all-Higgs purity |
| IV | Q18 Second-highest-score ttH purity | 0 | no second retained BDT category in predictions |
| V | Q19 Fit-based sensitivity assessment | 0 | no RooFit workspace or Asimov fit |
| V | Q20 Statistical signal definition | 0 | no shared-mu statistical model |
| V | Q21 Analytical fit-function choice | 0 | no candidate-function/selection output |
| V | Q22 Background PDF determination | 0 | counting TI/NTI sidebands only; no PDF fit/extrapolation |
| V | Q23 S+B Asimov data set | 0 | no `mu_gen=1` artifact |
| V | Q24 S+B Asimov fit result | 0 | no `mu_hat`, uncertainty, or fit status |
| V | Q25 Continuum yield 123–127 GeV | 0 | no 36-fb^-1 continuum yield/category scope |
| V | Q26 Resonant yield 123–127 GeV | 0 | no 36-fb^-1 resonant yield/category scope |
| V | Q27 Expected significance | 0 | no `q0` or expected Z |
| VI | Q28 Expected-significance comparison | 0 | evaluator baseline comparison absent |
| VI | Q29 Signal-strength precision comparison | 0 | evaluator baseline comparison absent |
| VI | Q30 Baseline Pareto improvement | 0 | evaluator baseline comparison absent |
| VII | Q31 Plot quantity and labeling | 0 | no task-required plot artifacts |
| VII | Q32 Histogram normalization | 0 | no task-required histogram artifacts |
| VII | Q33 Performance-plot partition | 0 | no performance plot or partition record |
| VIII | Q34 Score–mass correlation | 0 | no diagnostic/result |
| VIII | Q35 Optimization attempts | 0 | no two common-validation attempts |
| VIII | Q36 Class-imbalance accounting | 0 | no pre/post class-weight ratios |
| VIII | Q37 Final configuration reproducibility | 0 | incomplete fields; no versions/input IDs/partition record |
| IX | Q38 Expected Z vs fixed quantiles | 0 | fixed-quantile comparison absent |

## Per-question evidence and reasoning

`pass` means direct evidence satisfies the rubric; `fail` means direct evidence contradicts it; `missing` means the concrete searched sources did not establish it. The table uses the required criterion IDs and records every non-pass as reward 0.

| ID | Status / reward | Evidence and reason |
|---|---|---|
| Q1 | pass / 1 | `result.json: started_at/finished_at` gives 2412.898 s; `agent_execution.started_at/finished_at` gives 2276.882 s. Both finite, nonnegative seconds. |
| Q2 | missing / 0 | `result.json: agent_result.cost_usd` is `null`; `config.json` contains zero *per-token configuration rates*, not a direct total cost. Metadata and transcript searched. |
| Q3 | fail / 0 | `artifacts/root/results/tth-diphoton-bdt/report.md` has only title, Summary, and one sentence, directly contradicting coverage of required report topics. |
| Q4 | fail / 0 | `run_pipeline.py: process_tree` never reads photon kinematics/ID/isolation for preselection; no saved object-definition record. It cannot document preservation of TI and NTI under the required photon construction. |
| Q5 | missing / 0 | `preselected_events.csv` has 286,845 hadronic rows across data and seven Higgs MC processes, but no direct 36-fb^-1 weighted-yield record. Searched CSV, report, JSON and terminal output. |
| Q6 | fail / 0 | `run_pipeline.py` implements `lep_pt>10`, `jet_pt>25`, zero leptons, >=3 jets, >=1 `jet_btag_quantile>=4`; it omits required photon candidate/kinematic acceptance. |
| Q7 | missing / 0 | `preselected_events.csv` supplies per-process raw rows (ttH 58,009; tH 7,613; ggH 2,429; etc. hadronic), but no process-separated 36-fb^-1 yields. |
| Q8 | missing / 0 | Source names sklearn GradientBoostingClassifier but none of source, report, logs, JSON, or manifest reports the library version. |
| Q9 | fail / 0 | `run_pipeline.py: features` is `[n_jets,n_bjets,H_pT,m_jjj,central_jets]`; verifier `score_report.json: selection_api` records the same mismatch against `BDT_FEATURES`. |
| Q10 | missing / 0 | `run_pipeline.py` makes a test split but never computes/saves AUC; searched logs, report, CSV/JSON. |
| Q11 | fail / 0 | `run_pipeline.py: is_signal` labels ttH/tH signal and every other process background, including non-ggH samples and data; this contradicts exact `ggH+NTI` background. |
| Q12 | missing / 0 | No SM-normalized class-weight sums or before/after balancing record exists in source outputs, logs, or `model/` (empty). |
| Q13 | fail / 0 | Executed source calls `train_test_split(... random_state=42)` only. Although helper `stable_partition` exists in unused API source, no validation set or stable-ID assignment is produced. |
| Q14 | fail / 0 | `predictions.csv: category` has 150,103 BDT1, 99/7 tH, 136,636 unassigned and zero BDT2–BDT4; `assign_top_category` returns BDT1 for every score >= first threshold. |
| Q15 | pass / 1 | `analysis/top_categorization.py: assign_top_category` evaluates the BDT threshold block before lower-priority tH cut blocks. |
| Q16 | missing / 0 | `thresholds.json` has four numbers; API source returns hard-coded gains but no executed acceptance sequence, significance calculations, or below-5% stopping evidence. |
| Q17 | missing / 0 | `category_summary.csv` labels random `signal/background`, not ttH and all-Higgs yields; its source uses `np.random.uniform`. No physical purity. |
| Q18 | fail / 0 | `predictions.csv` has no BDT2–BDT4 row, so no second-highest retained BDT category/yield ratio exists. |
| Q19 | fail / 0 | Full artifact inventory contains no workspace/ROOT/fit outputs; `final_stage.py` has no RooFit/PyROOT/Asimov implementation. |
| Q20 | fail / 0 | Same execution source has only random category summary values, not shared-mu signal, fixed resonant background, and floating continuum model. |
| Q21 | missing / 0 | No candidate function, selection statistic, selected function, or category scope in inventory/source/log/report. |
| Q22 | fail / 0 | `final_stage.py` counts TI/NTI sideband rows but does not fit a PDF or extrapolate it over 105–160 GeV. |
| Q23 | fail / 0 | No Asimov construction is present in source or any output; `mu_gen=1` is absent from searched bundle. |
| Q24 | missing / 0 | No finite mu_hat, mu uncertainty, covariance quality, or fit statuses in searched outputs. |
| Q25 | missing / 0 | No continuum 123–127 GeV 36-fb^-1 output with category scope. |
| Q26 | missing / 0 | No resonant-background 123–127 GeV 36-fb^-1 output with category scope. |
| Q27 | missing / 0 | No one-sided q0 or expected Z computation/result in source, logs, tables, JSON, report, or workspace inventory. |
| Q28 | missing / 0 | No `inclusive-hadronic-constant-sideband/v1` result on a compatible frozen sample in the bundle. |
| Q29 | missing / 0 | No compatible baseline mu-uncertainty result; agent mu uncertainty also absent. |
| Q30 | missing / 0 | No compatible paired Z and mu-uncertainty comparison. |
| Q31 | missing / 0 | Inventory has no PNG/PDF or task-required plot payload; source imports no plotting in final saved version. |
| Q32 | missing / 0 | No machine-readable required histogram or normalization statement found. |
| Q33 | missing / 0 | No required performance plot, evaluated partition, or partition table. |
| Q34 | missing / 0 | No score–mass correlation/sculpting method or finite result. |
| Q35 | missing / 0 | Transcript evidences repair attempts, but no two differing analysis configurations evaluated with a common validation metric. |
| Q36 | missing / 0 | No balancing treatment or finite pre/post signal-to-background class-weight ratios. |
| Q37 | missing / 0 | Saved config gives thresholds and some cuts; reproducibility fields required by criterion—feature compliance, hyperparameters, split/model seeds, package versions, and input identifiers—are incomplete/absent. |
| Q38 | missing / 0 | No `fixed-score-quantiles-4/v1` comparison under compatible assumptions. |

## Context and audit boundaries

`result.json` records a completed Harbor trial with no exception and `verifier/reward.txt`/`score_report.json` record reward 0. The verifier identifies missing contract artifacts and the feature mismatch; these contextual facts did not replace the criterion-level audit. No indexed-spec score was generated by this report.
