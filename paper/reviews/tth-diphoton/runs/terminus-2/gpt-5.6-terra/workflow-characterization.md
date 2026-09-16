# Workflow characterization — ttH diphoton

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive, non-scoring evidence for one preserved run; it does not affect the Harbor verifier reward or any outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton-bdt-categorization / terminus-2 / gpt-5.6-terra / 20260902T205321Z-tth-diphoton-bd__sfftAQT` | `completed / 0.000000` | 45 | 5 | 4 | 4 | 1 | not established | 1 | not established | `74 readable outputs / expected count not independently established` |

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `terminus-2 / gpt-5.6-terra` |
| Run identifier | `20260902T205321Z-tth-diphoton-bd__sfftAQT` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 45 recorded tool invocations | `agent/trajectory.json`, count of agent `tool_calls` |
| Failed-command count | 5 explicit tool failures | trajectory observations: two missing-directory commands, RField attribute error, Python indentation error, matplotlib invalid `histtype` error |
| Distinct error signatures | 4 | normalized signatures E1–E4 below |
| Analysis iterations | 1 directly evidenced final analysis configuration | saved `training_metadata.json`, thresholds, fit/output tree; no completed alternate configuration with common validation metric |
| Final iteration | 1 | final saved `run_analysis.py` generated preserved result tree |
| Superseded iterations | not established | edits/retries are visible but do not establish a distinct completed analysis result replaced before submission |
| Recovery count | 4 | each E1–E4 is followed by same-stage progress/completion noted below |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection; package/environment management | trajectory commands and submitted `run_analysis.py`/`finalize_compliance.py` |
| Reproducibility attempt | not established | no clean-output rerun with stated headline-result tolerance in trajectory, logs, or manifest |
| Artifact coverage | `74 readable outputs / expected count not independently established` | literal bounded artifact inventory; all readable JSON/CSV, report, workspace records, and PNG/PDF plot outputs audited |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | setup | `bash: cd: /root/submission/tth-diphoton-bdt: No such file or directory` | 2 | Later trajectory commands operate in `~/submission/tth-diphoton-bdt` and preserve submitted source/results. | recovered |
| E2 | input_inspection | `AttributeError: RField object has no attribute interpretation` | 1 | Later source uses `uproot.iterate(..., library='ak')` and produces `preselected_events.csv` / `cutflow.json`. | recovered |
| E3 | source editing | `IndentationError: unexpected indent (run_analysis.py, line 19)` | 1 | Final readable `run_analysis.py` executes sufficiently to produce training, inference, categorization, plots, and reports. | recovered |
| E4 | plotting | `ValueError: 'errorbar' is not a valid value for histtype` | 1 | Final outputs include the required PNG/PDF plot families and machine-readable histogram payloads. | recovered |

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Deterministic GradientBoosting configuration: five saved features, seed `20240517`, thresholds `0.7916175, 0.7425552` | not established | final saved analysis outputs | final | `model/training_metadata.json`, `optimization/thresholds.json`, submitted source |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | E1 | yes, corrected working location | not established | trajectory |
| input_inspection | yes | yes | E2 | yes, changed ROOT reading approach | not established | trajectory; `input_data_contract.json` |
| data_preparation | yes | yes | none directly retained | not established | not established | `preselected_events.csv`, `preselection_summary.json`, source |
| training | yes | yes | none directly retained | final model settings evidenced | `1.882996 s` | `model/training_metadata.json` |
| validation | yes | incomplete for held-out performance | none directly retained | no | not established | partitioned training table; no AUC artifact |
| optimization | yes | yes | none directly retained | thresholds saved | not established | `optimization/accepted_splits.json`, `thresholds.json` |
| inference_or_selection | yes | yes | none directly retained | categories saved | not established | `inference/events_with_bdt_scores.csv`, categorization outputs |
| fit | yes | incomplete: template statistical summary, not executed likelihood fit | none directly retained | no | not established | `fit/FIT1/results.json:status`; source |
| plotting | yes | yes | E4 | yes, plotting call corrected | not established | saved PNG/PDFs and histogram JSON |
| reporting | yes | yes | none directly retained | yes | not established | `report.md`, `finalize_compliance.py` |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Finite BDT inputs/scores | hadronic table is selected with finite features; scores are clipped to `[0,1]` | `run_analysis.py:44,55`; inference manifest/table |
| Duplicate/stable IDs | stable hashed partition implementation; no duplicate-ID validation outcome explicitly saved | `analysis/top_categorization.py:stable_partition`, training/inference tables |
| Class balancing | pre/post class sums recorded and post sums equal | `model/class_balance_check.json` |
| Empty categories | BDT3 and BDT4 have zero model yield and are merged/represented through final categorization handling; no invalid-model-state crash recorded | `category_component_yields.json`, retention record |
| Blinding | TI observed `125+/-2 GeV` explicitly declared blinded | `run_manifest.json`, categorization manifest, source |
| Fit validity | not established as a real fit; output explicitly says `template statistical summary` | `fit/FIT1/results.json`, source |

## Rubric-identifier coverage

This workflow profile is separate from scientific scoring, but it deliberately preserves the complete identifier set audited in its companion report: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38.

The reported verifier reward is execution context, not a workflow assessment. Counts are based only on recorded invocations and explicit diagnostics; unknown outcomes were not counted as failures.
