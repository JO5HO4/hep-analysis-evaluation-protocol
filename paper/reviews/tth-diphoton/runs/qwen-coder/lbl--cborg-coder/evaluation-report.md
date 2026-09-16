# Manual evidence evaluation: qwen-coder / lbl--cborg-coder

Non-authoritative evidence review of `tth-diphoton` under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`, generated 2026-09-09. This is not an outcome grade. `R` below denotes the supplied preserved trial directory; paths beginning `results/` and `submission/` are below `R/artifacts/root/`.

## Scope and evidence audit

The audit opened the complete readable bundle: job and trial `result.json`, `config.json`, `lock.json`, `trial.log`, agent response/session trajectory, verifier reward/report/stdout, artifact manifest, all submitted Python/YAML source, all JSON and CSV outputs, both PNG/PDF plot products, workspace/fit records, and `report.md`. The trial completed with Harbor reward `0.000000`; that is execution context only. Direct agent evidence says the ATLAS inputs were unavailable, the delivered analysis used synthetic data, and the ROOT/RooFit interpretation was mocked (`agent/qwen-code.txt:3,18`; `submission/run_bdt.py:12-15`; `submission/run_fit.py:6-7`).

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| qwen-coder / lbl--cborg-coder | 7 | 10 | 21 | completed / 0.000000 |

## 2. Total reward (raw, no averaging)

| Summary | qwen-coder / lbl--cborg-coder |
|---|---:|
| Total reward | 7 / 38 |

## 3. Overall equal-category reward

| Summary | qwen-coder / lbl--cborg-coder |
|---|---:|
| Overall equal-category reward | 0.168 |

This is the arithmetic mean of the nine rubric-group pass fractions, not an authoritative scientific score.

## 4. Per-question binary rewards

| Category | Question | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 0 |
| I | Q3 Human-facing documentation | 0 |
| II | Q4 Photon identification/isolation | 1 |
| II | Q5 Hadronic-channel event count | 0 |
| II | Q6 Hadronic preselection | 1 |
| II | Q7 Post-preselection Higgs yields | 0 |
| III | Q8 BDT training package | 0 |
| III | Q9 BDT input features | 0 |
| III | Q10 Signal-background AUC | 0 |
| III | Q11 Training classes | 1 |
| III | Q12 Training class weights | 0 |
| III | Q13 Train/validation/test partition | 0 |
| IV | Q14 BDT category count | 1 |
| IV | Q15 BDT event categorization | 0 |
| IV | Q16 Categorization figure of merit | 1 |
| IV | Q17 Highest-score ttH purity | 0 |
| IV | Q18 Second-highest-score ttH purity | 0 |
| V | Q19 Fit-based sensitivity assessment | 0 |
| V | Q20 Statistical signal definition | 1 |
| V | Q21 Analytical fit-function choice | 0 |
| V | Q22 Background PDF determination | 0 |
| V | Q23 S+B Asimov data set | 0 |
| V | Q24 S+B Asimov fit result | 0 |
| V | Q25 Continuum yield, 123–127 GeV | 0 |
| V | Q26 Resonant yield, 123–127 GeV | 0 |
| V | Q27 Expected significance | 0 |
| VI | Q28 Expected-significance comparison | 0 |
| VI | Q29 Signal-strength precision comparison | 0 |
| VI | Q30 Baseline Pareto improvement | 0 |
| VII | Q31 Plot quantity and labeling | 0 |
| VII | Q32 Histogram normalization | 0 |
| VII | Q33 Performance-plot partition | 0 |
| VIII | Q34 Score–mass correlation | 0 |
| VIII | Q35 Optimization attempts | 0 |
| VIII | Q36 Class-imbalance accounting | 0 |
| VIII | Q37 Final configuration reproducibility | 0 |
| IX | Q38 Expected significance vs fixed quantiles | 0 |

## 5. Per-question observed values and rewards

| Category | Question | Observed value [reward] |
|---|---|---|
| I | Q1 | `729.664439 s` trial wall time; `609.033194 s` agent time [1] |
| I | Q2 | `cost_usd: null` [0] |
| I | Q3 | Required report sections/links incomplete [0] |
| II | Q4 | `tight_id_required=false`, `isolation_required=false` [1] |
| II | Q5 | `15000/1500` conflicts with cutflow `8000` [0] |
| II | Q6 | photons kinematic; lepton `pT>10`, jets `pT>25`, `n_leptons=0,n_jets>=3,n_btags>=1`, btag `>=4` [1] |
| II | Q7 | claimed per-process values are unlinked to actual preselected table [0] |
| III | Q8 | `RandomForestClassifier`; sklearn version absent [0] |
| III | Q9 | `n_jets,n_btags,ht,pt_gammagamma,m_jjj`; verifier says mismatch [0] |
| III | Q10 | `bdt_auc=0.88`, but no held-out/test AUC [0] |
| III | Q11 | signal `ttH,tH`; background `ggH,NTI` [1] |
| III | Q12 | synthetic `1.0/0.1` weights; no recorded pre/post sums [0] |
| III | Q13 | partitions present, but unstable Python `hash()` and no disjoint-set audit [0] |
| IV | Q14 | six named hadronic categories plus `unassigned` [1] |
| IV | Q15 | source sends failed BDT1–3 events to tH cuts before BDT4 [0] |
| IV | Q16 | accepted relative gain `106.217937%`; source stops below `5%` [1] |
| IV | Q17 | no separate ttH/all-Higgs purity [0] |
| IV | Q18 | no second retained BDT-boundary purity [0] |
| V | Q19 | fit outputs explicitly `mocked_result` [0] |
| V | Q20 | declared `mu*(ttH+tH)+fixed resonant+floating continuum` [1] |
| V | Q21 | no candidates, statistic, or selected PDF [0] |
| V | Q22 | no executed TI-sideband fit [0] |
| V | Q23 | Asimov construction `mocked_result` [0] |
| V | Q24 | `mu_hat=1.02` (outside ±0.01) [0] |
| V | Q25 | no continuum 123–127 yield [0] |
| V | Q26 | no resonant 123–127 yield [0] |
| V | Q27 | `q0=0.45`, `Z=2.1`; `Z² != q0` [0] |
| VI | Q28 | compatible common-sample baseline absent [0] |
| VI | Q29 | compatible common-sample baseline absent [0] |
| VI | Q30 | compatible common-sample baseline absent [0] |
| VII | Q31 | two plot outputs are text `MOCK_PLOT_DATA`; required plot coverage absent [0] |
| VII | Q32 | only score shape uses `density=True`; required histogram inventory absent [0] |
| VII | Q33 | no evaluated partition for a performance plot [0] |
| VIII | Q34 | no finite score–mass diagnostic [0] |
| VIII | Q35 | one saved RandomForest configuration [0] |
| VIII | Q36 | pre/post class-weight ratios absent [0] |
| VIII | Q37 | package versions/hyperparameters/threshold sequence/input IDs incomplete [0] |
| IX | Q38 | compatible fixed-quantile baseline absent [0] |

## 6. Per-question evidence and reasoning

| Question | Status, evidence, and reason |
|---|---|
| Q1 | **pass** — `R/result.json:started_at,finished_at,agent_execution` gives finite durations above. |
| Q2 | **missing** — enclosing `result.json:stats.cost_usd` and `R/result.json:agent_result.cost_usd` are null. |
| Q3 | **fail** — `results/report.md` lacks required Systematic Uncertainties section and Markdown plot embeds/links; its checklist also omits required subjects. |
| Q4 | **pass** — `results/object_definition_record.json:photons` and `submission/run_preselection.py` explicitly preserve non-tight/non-isolated photons. |
| Q5 | **missing** — `preselection_summary.json:counts.overall` claims 15000/1500 while `cutflow.json:hadronic_preselection` is 8000; no saved preselected-events table resolves scope or 36-fb normalization. |
| Q6 | **pass** — direct object record, resolved config, and `apply_preselection` implement each stated predicate. |
| Q7 | **missing** — `preselection_summary.json:counts.by_process` is contradicted by the absent required table and synthetic generator; it cannot be tied to executed hadronic preselection. |
| Q8 | **missing** — source identifies sklearn's `RandomForestClassifier`, but neither source nor metadata records a library version. |
| Q9 | **fail** — `submission/analysis/top_categorization.py:12` and `training_metadata.json:features` use the displayed five-item list; `verifier/score_report.json:selection_api.errors` directly records `BDT_FEATURES mismatch`. |
| Q10 | **missing** — `metrics.json:bdt_auc=0.88` does not identify a test partition; source trains only `train_df` and reports no held-out calculation. |
| Q11 | **pass** — `config_resolved.yaml:bdt.{signal_processes,background_processes}` and source agree on `ttH+tH` versus `ggH+NTI`. |
| Q12 | **fail** — `run_bdt.py` labels weights simulated, uses fixed synthetic weights, and applies sklearn `class_weight='balanced'`; required physical normalization and pre/post records are not performed/recorded. |
| Q13 | **missing** — output has partition labels, but `stable_partition` uses process-randomized Python `hash()` and no ID-set/disjointness evidence. |
| Q14 | **pass** — `CATEGORY_ORDER`, `workspace_manifest.json:categories`, and category summary establish exactly the six names plus `unassigned`. |
| Q15 | **fail** — `assign_top_category` performs tH cuts after BDT1–3 failure and before returning BDT4, contradicting required all-BDT-first priority. |
| Q16 | **pass** — `optimize_bdt_boundaries` encodes `rel_imp >= .05`/break and executed `accepted_splits.json` records the accepted gain. |
| Q17 | **missing** — `category_summary.csv` combines ttH+tH and has no all-Higgs denominator. |
| Q18 | **missing** — one threshold is saved and no finite second-highest retained-category purity is reported. |
| Q19 | **fail** — `run_fit.py` and all construction/backend JSON records explicitly state mocked results; no real workspace/Asimov fit is established. |
| Q20 | **pass** — `workspace_manifest.json` and `report.md` directly document the requested shared-mu model definition (definition evidence only, not a real fit). |
| Q21 | **missing** — scanned fit JSONs are `mocked_result`; no candidate functions or selection statistic. |
| Q22 | **missing** — no readable TI-sideband fitted data/PDF/extrapolation record; source only creates mock placeholders. |
| Q23 | **missing** — `significance_asimov_construction.json` is `{status: mocked_result}`. |
| Q24 | **fail** — `fit/FIT1/results.json` reports `mu_hat=1.02`, exceeding the required 0.01 deviation despite claimed converged/good statuses. |
| Q25 | **missing** — category CSV has broad mock component sums, not a stated 123–127 continuum yield with workspace-category scope. |
| Q26 | **missing** — same audit finds no 123–127 resonant yield with stated category scope. |
| Q27 | **fail** — saved `q0=0.45`, `expected_Z=2.1`; `2.1²=4.41`, directly contradicting the required one-sided relation. |
| Q28 | **missing** — no evaluator-owned same frozen event table or compatible inclusive-baseline rerun in R or the named baseline records. |
| Q29 | **missing** — same absence prevents a compatible uncertainty comparison. |
| Q30 | **missing** — same absence prevents a Pareto determination. |
| Q31 | **fail** — audit found score/category plots but no required machine-readable histograms or mass-control suite; fit plots contain literal `MOCK_PLOT_DATA`, so required quantity/unit/finite coverage is directly not met. |
| Q32 | **fail** — `run_bdt.py` only labels its score shape `density=True`; required histogram set and normalization declarations are absent. |
| Q33 | **missing** — no performance plot identifies validation or test partition. |
| Q34 | **missing** — report, metrics, CSVs, source, and plot payloads contain no finite score–`m_gammagamma` correlation/diagnostic. |
| Q35 | **fail** — source and `training_metadata.json` evidence one RandomForest run/configuration; no second common-validation attempt exists. |
| Q36 | **missing** — no `class_balance_check.json` or equivalent finite pre/post ratio; source does not calculate one. |
| Q37 | **missing** — config supplies features/seed fragments but omits package versions, full hyperparameters, complete thresholds, and actual input identifiers. |
| Q38 | **missing** — no evaluator-owned fixed-score-quantiles-4/v1 result on the same continuous scores and compatible fit. |

The zero verifier reward is retained separately; it does not erase the seven directly evidenced implementation/documentation passes. Conversely, synthetic and mocked records are not treated as executed physics results.
