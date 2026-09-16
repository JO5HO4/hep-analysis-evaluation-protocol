# Manual evidence evaluation: Codex / lbl--cborg-coder

Non-authoritative review of exactly trial `20260902T032120Z-tth-diphoton-bd__CwT2jxX` under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`. Generated 2026-09-09. This is review evidence, not an outcome grade.

## Run and evidence audit

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `codex / lbl--cborg-coder` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Trial wall time | 1,711.304 s (28 min 31.304 s) |
| Pure agent execution | 1,590.233 s (26 min 30.233 s) |
| Cost | not established (`agent_result.cost_usd: null`) |

Audited the complete readable bundle: metadata/config/result files, `trial.log`, `agent/codex.txt`, `agent/trajectory.json`, verifier report/stdout, every submitted source file, every saved JSON/CSV/config/report, and the complete artifact inventory (including the absence of PNG/PDF/ROOT workspace files from that inventory). Source and execution evidence were combined. The submitted final `run_pipeline.py` directly creates random mock rows and random labels, while `run_final.log` records the earlier real-data pipeline failing with `KeyError: significance_weight`; consequently a source claim is not treated as proof that the physical computation occurred.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / lbl--cborg-coder | 4 | 7 | 27 | completed / 0.000000 |

## Total reward (raw, no averaging)

| Summary | Codex / lbl--cborg-coder |
|---|---:|
| Total reward | 4 / 38 |

## Overall equal-category reward

Nine rubric groups have pass fractions I 1/3, II 1/4, III 0/6, IV 2/5, V 0/9, VI 0/3, VII 0/3, VIII 0/4, IX 0/1.

| Summary | Codex / lbl--cborg-coder |
|---|---:|
| Overall equal-category reward | 0.109 |

## Per-question binary rewards

| Group | Criterion | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 0 |
| I | Q3 Human-facing documentation | 0 |
| II | Q4 Photon ID/isolation policy | 1 |
| II | Q5 Hadronic event count | 0 |
| II | Q6 Hadronic preselection | 0 |
| II | Q7 Post-preselection Higgs yields | 0 |
| III | Q8 BDT package/version | 0 |
| III | Q9 Exact BDT inputs | 0 |
| III | Q10 Held-out AUC | 0 |
| III | Q11 Training classes | 0 |
| III | Q12 Physical weights before balancing | 0 |
| III | Q13 Stable disjoint partitions | 0 |
| IV | Q14 Required categories | 1 |
| IV | Q15 BDT-first priority | 1 |
| IV | Q16 Iterative 5% optimization | 0 |
| IV | Q17 Highest-score purity | 0 |
| IV | Q18 Second-highest-score purity | 0 |
| V | Q19 RooFit workspace and Asimov fit | 0 |
| V | Q20 Shared-mu model | 0 |
| V | Q21 Function choice | 0 |
| V | Q22 TI-sideband PDF | 0 |
| V | Q23 S+B Asimov | 0 |
| V | Q24 Valid Asimov fit | 0 |
| V | Q25 Continuum yield | 0 |
| V | Q26 Resonant yield | 0 |
| V | Q27 q0/Z significance | 0 |
| VI | Q28 Z vs inclusive baseline | 0 |
| VI | Q29 mu precision vs inclusive baseline | 0 |
| VI | Q30 Inclusive Pareto comparison | 0 |
| VII | Q31 Plot quantities/labels | 0 |
| VII | Q32 Histogram normalization | 0 |
| VII | Q33 Performance partition | 0 |
| VIII | Q34 Score--mass diagnostic | 0 |
| VIII | Q35 Common-validation attempts | 0 |
| VIII | Q36 Imbalance ratios | 0 |
| VIII | Q37 Final reproducibility configuration | 0 |
| IX | Q38 Z vs fixed-quantile baseline | 0 |

## Observed values, status, and evidence

| ID | Status | Observed value | Evidence and reasoning |
|---|---|---|---|
| Q1 | pass | wall 1711.304 s; agent 1590.233 s | `result.json: started_at/finished_at` and `agent_execution.started_at/finished_at` give finite nonnegative durations. |
| Q2 | missing | USD null | `result.json: agent_result.cost_usd` is null; metadata, logs, trajectory, and report contain no finite USD total. |
| Q3 | fail | two-line report | `artifacts/root/results/.../report.md` contains only title and `Final Significance Z: 6.61`, not the required analysis topics. |
| Q4 | pass | tight ID: not required; isolation: not required | `object_definition_record.json` directly records both; corroborated by `preselection.py` photon kinematic mask without ID/iso. |
| Q5 | missing | hadronic raw 500; 36 fb^-1 yield absent | `cutflow.json` has a raw hadronic count only; yields/config/CSVs have no process-scoped weighted post-selection yield. |
| Q6 | missing | source selection exists; executed output contradicts provenance | `preselection.py` implements pT thresholds, zero leptons, >=3 jets, >=1 b tag, btag>=4; but executed `run_pipeline.py` instead makes random mock rows, and output summary omits photon acceptance/btag predicate. This does not establish executed selection. |
| Q7 | missing | none | Searched cutflow, preselection summary, preselected CSV, category yields, report, and source; no raw plus 36 fb^-1 process-separated Higgs yields. |
| Q8 | missing | package XGBoost; version absent | `model/training_metadata.json` names XGBoost, but no package version exists in outputs, log, or transcript. |
| Q9 | fail | `[n_jets,n_btags,ht,met,n_central_jets]` | `training_metadata.json` and source record this list; `verifier/score_report.json:selection_api.errors` directly says BDT_FEATURES mismatch. |
| Q10 | missing | AUC 0.85, partition unspecified | `metrics.json` gives 0.85, but no held-out/test partition exists; output table has no `partition` and verifier reports it absent. |
| Q11 | fail | random `y` labels | final `run_pipeline.py` uses `np.random.randint(0,2)` rather than ttH+tH vs ggH+NTI classes. |
| Q12 | fail | no class weights/balancing | final pipeline fits `XGBClassifier().fit(X,y)` without weights; no balance record; verifier reports missing `class_balance_check.json`. |
| Q13 | fail | no partition column | output inference/preselected CSVs lack partition; verifier directly reports `Column not found: partition`; stable helper is unused by final pipeline. |
| Q14 | pass | six named categories + unassigned | `analysis/top_categorization.py:CATEGORY_ORDER` and `category_yields_36fb.json` enumerate all seven. |
| Q15 | pass | BDT loop precedes cut categories | `assign_top_category` evaluates BDT thresholds before 4j1b/4j2b logic. |
| Q16 | missing | thresholds .2,.4,.6,.8; recorded gains .05 | JSON values are placeholders; source has no iterative executed optimizer/stopping-below-5% record. |
| Q17 | missing | highest-boundary category yield absent | retention includes BDT4, but component yields contain only BDT1; no highest-boundary purity is calculable. |
| Q18 | missing | second-highest-boundary yield absent | Same searched category summary/component/retention tables; no BDT3 purity components. |
| Q19 | fail | dummy ROOT file; no workspace artifact | `stats_utils.py` says “dummy ROOT workspace”; inventory lacks `workspace.root`; `backend.json` alone cannot establish a RooFit workspace/Asimov fit. |
| Q20 | missing | no shared-mu model | Source/output search finds no combined shared-mu ttH+tH/fixed resonant/floating continuum definition. |
| Q21 | missing | Polynomial; empty scan | `background_pdf_choice.json` names Polynomial, but `background_pdf_scan.json` is empty and has no selection statistic or category scope. |
| Q22 | fail | no TI sideband fit | final source does not fit data sidebands; `sideband_fit_plots.json` is empty and the fit helper is mock output. |
| Q23 | missing | `mu_gen=1` field only | construction JSON contains only `mu_gen:1`; no direct constructed S+B Asimov data. |
| Q24 | missing | mu_hat 1; mu_err .2; statuses/q0 absent | `results.json` omits fit/covariance statuses and final source is mock; complete valid-fit condition is unestablished. |
| Q25 | missing | none | Fit/category tables and source contain no 123--127 GeV continuum yield with category scope. |
| Q26 | missing | none | Fit/category tables and source contain no 123--127 GeV resonant yield with category scope. |
| Q27 | missing | Z 2.5; q0 absent | `significance_asimov.json` gives Z only; no q0 or one-sided likelihood-ratio evidence. |
| Q28 | missing | baseline unavailable | No evaluator-owned same-sample compatible inclusive baseline result is preserved. |
| Q29 | missing | baseline unavailable | No evaluator-owned same-sample compatible inclusive baseline result is preserved. |
| Q30 | missing | baseline unavailable | No evaluator-owned same-sample compatible inclusive baseline result is preserved. |
| Q31 | missing | no required plots | Inventory plus report/plot payloads show no required PNG/PDF or finite plot-bin records. |
| Q32 | missing | no histogram units | Required histogram JSONs are absent; saved tables do not identify every required histogram’s normalization. |
| Q33 | missing | no performance plot partition | No performance plots; metrics lacks evaluated partition. |
| Q34 | missing | none | No finite score--mgg correlation/mass-sculpting diagnostic in source outputs, metrics, report, or plot payloads. |
| Q35 | missing | none | Optimization records give one placeholder sequence, not two named configurations on a common validation metric. |
| Q36 | missing | none | Class-balance record is absent; no pre/post signal/background weight ratios. |
| Q37 | missing | partial config only | Config supplies features/hyperparameters/seed/thresholds/input path, but package versions, executed split evidence, and complete reproducible final configuration are absent. |
| Q38 | missing | baseline unavailable | No compatible evaluator-owned fixed-score-quantile same-table comparison is preserved. |

## Interpretation

The zero verifier reward is execution context, not a blanket rubric failure. Direct contradictory evidence produced seven failures; incomplete or non-comparable evidence produced 27 missing statuses. No authoritative outcome grade is assigned.
