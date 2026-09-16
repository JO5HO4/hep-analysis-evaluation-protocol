# Manual evidence evaluation: OpenHands / openai--lbl-cborg-coder

Non-authoritative single-run review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`; the natural-language rubric does not create an outcome grade.

| Field | Value |
|---|---|
| Task / trial | `tth-diphoton / 20260902T050526Z-tth-diphoton-bd__fm8URtk` |
| Agent / model | `openhands / openai--lbl-cborg-coder` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Evidence root | supplied preserved trial, especially `artifacts/root/{submission,results}/tth-diphoton-bdt` |

I enumerated the readable root and opened result/config/lock metadata, `trial.log`, agent transcript/events, verifier files, all three submitted Python files, every saved JSON/CSV/report, and both PNGs. The two plots have no plot payload or labels to score visually. The saved source explicitly creates synthetic data and calls its fit “Mock Fit placeholders”; these are direct contradictions where relevant. Missing statuses below follow searches of those logs, source, tables, outputs, plots, workspaces, and reports—not a missing filename alone.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| OpenHands / openai--lbl-cborg-coder | 5 | 11 | 22 | completed / 0.000000 |

| Summary | OpenHands / openai--lbl-cborg-coder |
|---|---:|
| Total reward | 5 / 38 |

| Summary | OpenHands / openai--lbl-cborg-coder |
|---|---:|
| Overall equal-category reward | 0.128 |

Category fractions: Execution 1/3; Object/preselection 1/4; Training 1/6; Categorization 2/5; Workspace/fit 0/9; Inclusive baseline 0/3; Plotting 0/3; Validation/reproducibility 0/4; Quantile baseline 0/1.

## Per-question binary rewards

| Category | Question | Reward |
|---|---|---:|
| Execution | Q1 Run timing | 1 |
| Execution | Q2 Run cost | 0 |
| Execution | Q3 Documentation | 0 |
| Object/preselection | Q4 Photon ID/isolation | 1 |
| Object/preselection | Q5 Hadronic count/yield | 0 |
| Object/preselection | Q6 Exact preselection | 0 |
| Object/preselection | Q7 Process yields | 0 |
| Training | Q8 Package/version | 0 |
| Training | Q9 Exact features | 0 |
| Training | Q10 Held-out AUC | 0 |
| Training | Q11 Classes | 1 |
| Training | Q12 Physical weights/balancing | 0 |
| Training | Q13 Stable partitions | 0 |
| Categorization | Q14 Categories | 1 |
| Categorization | Q15 Priority | 1 |
| Categorization | Q16 5% optimization | 0 |
| Categorization | Q17 Highest purity | 0 |
| Categorization | Q18 Second purity | 0 |
| Workspace/fit | Q19 RooFit workspace/Asimov | 0 |
| Workspace/fit | Q20 Statistical definition | 0 |
| Workspace/fit | Q21 Fit-function choice | 0 |
| Workspace/fit | Q22 TI-sideband PDF | 0 |
| Workspace/fit | Q23 S+B Asimov | 0 |
| Workspace/fit | Q24 Asimov fit result | 0 |
| Workspace/fit | Q25 Continuum yield | 0 |
| Workspace/fit | Q26 Resonant yield | 0 |
| Workspace/fit | Q27 q0 and Z | 0 |
| Inclusive baseline | Q28 Z comparison | 0 |
| Inclusive baseline | Q29 mu-uncertainty comparison | 0 |
| Inclusive baseline | Q30 Pareto improvement | 0 |
| Plotting | Q31 Quantity/labels | 0 |
| Plotting | Q32 Histogram normalization | 0 |
| Plotting | Q33 Performance partition | 0 |
| Validation | Q34 Score-mass diagnostic | 0 |
| Validation | Q35 Optimization attempts | 0 |
| Validation | Q36 Imbalance ratios | 0 |
| Validation | Q37 Reproducibility fields | 0 |
| Quantile baseline | Q38 Z comparison | 0 |

## Evidence and reasoning

| Q | Status / observed value | Evidence and reason |
|---|---|---|
| Q1 | pass / 513.466 s wall; 376.168 s agent | `result.json` timestamps establish both finite intervals. |
| Q2 | missing / `cost_usd: null` | `result.json:agent_result.cost_usd`; no other USD total in logs or artifacts. |
| Q3 | fail / report has only Introduction | `results/.../report.md` is two lines and omits the required analysis topics. |
| Q4 | pass / no tight ID/iso | `object_definition_record.json:photon` explicitly says both are not required. |
| Q5 | fail / 5,222 raw, weighted 5,222 | `preselection_summary.json` is all selected rows (including leptonic), has no hadronic process scope or 36 fb^-1 weighted yield. |
| Q6 | fail / photons only `len>=2` | `run.py:apply_preselection` implements lepton/jet/b-tag/hadronic cuts, but has no photon kinematic acceptance test. |
| Q7 | fail / process weights only | `preselection_summary.json:by_process` has no raw counts or 36 fb^-1 yields and includes non-hadronic rows. |
| Q8 | missing / XGBoost, version absent | `run.py` imports `xgboost`; no package version is saved in source, logs, or results. |
| Q9 | fail / `[n_jets,n_bjets,h_pT,h_eta,m_jets]` | `top_categorization.py:BDT_FEATURES`; verifier directly records this list as a `BDT_FEATURES mismatch`. |
| Q10 | missing / no AUC | Searched source, report, JSON/CSV and transcript; no test partition or AUC output. |
| Q11 | pass / signal `ttH+tH`; background `ggH+data_GamGam` NTI | `run.py:prepare_bdt_training_set` directly defines these classes. |
| Q12 | missing / unrecorded class sums | Source balances signal by `bg_sum/sig_sum`, but no execution record gives both pre/post class sums or validated physical normalization. |
| Q13 | missing / helper unused | `stable_partition` exists in source, but no saved partition labels or nonempty/disjoint sets are produced. |
| Q14 | pass / four BDT, two tH, unassigned | `top_categorization.py:CATEGORY_ORDER` and `category_summary.csv` name all seven. |
| Q15 | pass / BDT before fallback | `assign_top_category` evaluates score thresholds before the tH cut branches. |
| Q16 | missing / thresholds .8,.6,.4,.2; gains .10,.07,.06,.051 | `optimization/*.json` gives accepted gains, but no tested rejected split or below-5% stopping evidence. |
| Q17 | missing / BDT3 combined signal 27,576, background 54,576 | `category_summary.csv` combines ttH+tH and does not give ttH or all-Higgs components needed for purity. |
| Q18 | missing / BDT4 combined signal 36, background 180 | Same table lacks separated ttH and all-Higgs yields. |
| Q19 | fail / mock JSON only | `run.py:run_statistical_fit` says “Mock Fit placeholders”; no workspace is saved. |
| Q20 | fail / no statistical model | Same mock function contains no shared mu, fixed resonant term, or floating continuum. |
| Q21 | missing / none named | No candidate-function scan, statistic, selected function, or scope in source/results/logs. |
| Q22 | fail / no TI sideband fit | `run.py` substitutes `data_GamGam`; `run_statistical_fit` does not fit 105–120/130–160 GeV sidebands. |
| Q23 | fail / no Asimov construction | Source’s mock fit emits only result/significance JSON; no `mu_gen=1` dataset evidence. |
| Q24 | missing / mu=1.0, uncertainty=.2, `converged` | `fit/FIT1/results.json` omits Asimov provenance and covariance status; mock source prevents direct validation. |
| Q25 | missing / no 123–127 continuum yield | Category background is mixed and no continuum component/scope is saved. |
| Q26 | missing / no 123–127 resonant yield | No separated resonant component/scope is saved. |
| Q27 | missing / Z=2.5, q0 absent | `fit/FIT1/significance.json`; no one-sided test statistic to check Z²=q0. |
| Q28 | missing / baseline unavailable | No same-frozen-sample compatible `inclusive-hadronic-constant-sideband/v1` rerun in run outputs or evaluator records searched. |
| Q29 | missing / baseline unavailable | Same comparison evidence gap; no reference mu uncertainty. |
| Q30 | missing / baseline unavailable | Same comparison evidence gap. |
| Q31 | missing / two unlabeled PNGs | Source identifies a count histogram and yield bar chart, but saved plots/report supply neither required units nor complete task-required finite plot evidence. |
| Q32 | missing / normalization incomplete | `plt.hist` defaults to counts, but no machine-readable required histogram set or normalization declaration exists. |
| Q33 | missing / no performance plot partition | No performance plot or evaluated-partition metadata in artifacts. |
| Q34 | missing / no finite diagnostic | No score–mass correlation/calculation in source or saved outputs. |
| Q35 | fail / one mock threshold configuration | `run.py:optimize_bdt_boundaries_real` hard-codes one threshold list; no two differing attempts/common validation metric. |
| Q36 | missing / ratios absent | Source has `sig_sum`/`bg_sum` but saves neither pre/post ratio. |
| Q37 | fail / incomplete configuration | Features, XGBoost hyperparameters, seeds and thresholds appear in source, but package versions/input identifiers and executed configuration record are absent. |
| Q38 | missing / baseline unavailable | No compatible same-table `fixed-score-quantiles-4/v1` rerun or reference Z was found. |

The verifier’s zero reward is preserved as execution context only. It is not an outcome grade and did not erase direct source/output evidence.
