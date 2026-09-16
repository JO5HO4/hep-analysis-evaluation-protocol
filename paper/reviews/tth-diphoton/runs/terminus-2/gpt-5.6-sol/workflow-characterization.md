# Workflow characterization — ttH diphoton

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile is not a rubric score, verifier reward, or outcome grade.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / terminus-2 / gpt-5.6-sol / 20260905T033334Z-tth-diphoton-bd__u5KdDyp` | `completed / 0.000000` | 25 | 3 | 3 | 3 | 1 | 0 | final uncapped pipeline | not established | 61 / expected count not independently established |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `terminus-2 / gpt-5.6-sol` |
| Run identifier | `20260905T033334Z-tth-diphoton-bd__u5KdDyp` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 25 recorded tool invocations (23 shell plus 2 completion calls) | `agent/trajectory.json:steps[].tool_calls` |
| Failed-command count | 3 | trajectory steps 7, 13, 14, with explicit diagnostics |
| Distinct error signatures | 3 | E1–E3 below |
| Analysis iterations | 1 completed analysis configuration | final output lineage; no second completed configuration with a distinct model/feature/selection/fit configuration |
| Final iteration | uncapped deterministic full pipeline | trajectory steps 15–17; `run_manifest.json:status=complete` |
| Superseded iterations | 0 completed result iterations | trajectory has repairs of failed setup/fit attempts, but no earlier completed analysis result replaced before submission |
| Recovery count | 3 | E1–E3 each followed by direct same-stage success |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection; package/environment management | trajectory and submitted scripts |
| Reproducibility attempt | not established | final audit validates outputs but does not evidence a clean-output rerun and result comparison |
| Artifact coverage | `61 / expected count not independently established` | trajectory steps 16–17 reports 61 nonempty audited artifacts; no independent required-output denominator is preserved |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | data_preparation | `SyntaxError: invalid syntax` in `top_categorization.py` delta-phi expression | 1 | step 8 reports API compiles and passes kinematic test | recovered |
| E2 | fit | `ModuleNotFoundError: ROOT` after `PYTHONPATH=.` hides ROOT environment | 1 | step 14 reports PyROOT loads after normal-environment rerun | recovered |
| E3 | fit | `segfault` constructing/minimizing combined RooFit NLL; import conflict noted | 1 | step 15 reports workspace stage succeeds with status 0/covariance 3 | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | deterministic five-feature HistGradientBoosting model; one 5%-rule boundary; RooFit shared-mu fit | no common multi-iteration validation metric established | completed: expected Z `1.378313` | final | `training_metadata.json`, `accepted_splits.json`, `fit/FIT1/results.json` |

Failed setup and workspace executions are recoveries, not superseded completed analysis iterations: their final scientific configuration/result was not produced before repair.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none established after initial repository inspection | yes: constructed missing submission pipeline | `not established` | trajectory steps 2–6 |
| input_inspection | yes | yes | none | no | approximately 122 s from step 2 to step 6 | trajectory steps 2–6 |
| data_preparation | yes | yes | E1 | yes: corrected API syntax and GeV-unit diagnosis | `not established` | steps 5–10; `run_analysis.py` |
| training | yes | yes | none | no further documented change | training `1.335684 s`; whole initial pipeline `39 s` | `training_metadata.json`; trajectory step 10 |
| validation | yes | yes | none | no | `not established` | step 16 finite-score/category audit; `inference_manifest.json` |
| optimization | yes | yes | none | yes: accepted boundary `0.6338268` | `not established` | `optimization/accepted_splits.json`; step 11 |
| inference_or_selection | yes | yes | none | no | `not established` | `inference_manifest.json`; `categorization_manifest.json` |
| fit | yes | yes | E2, E3 | implementation repair only; final fit model unchanged in documented target | `not established` | trajectory steps 12–15; `fit/FIT1/results.json` |
| plotting | yes | yes | none | no | `not established` | step 12; saved PNG/PDF and JSON payloads |
| reporting | yes | yes | none | no | `not established` | `report.md`; steps 12, 16–17 |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| finite feature inputs and BDT scores | 272,376 selected rows finite; score range 0.3710165–0.6344022 | `inference_manifest.json`; trajectory steps 11, 16 |
| event-partition assignment | train/validation/test present; zero IDs observed across partitions in reviewer table audit | `predictions.csv`; `training_metadata.json` |
| JSON/YAML parsing | all audited machine-readable files parse | trajectory steps 16–17 |
| empty categories / retention | BDT2–4 explicitly empty/not kept; BDT1 and two tH categories retained under 0.8 minimum background policy | `category_retention.json`; `category_component_yields.json` |
| invalid model/fit state | free and null fits status 0; covariance quality 3 | `fit/FIT1/results.json` |
| blinding | observed TI 123–127 GeV signal window remains blocked | `significance_asimov.json`; report |

### Rubric-evidence cross-reference

All 38 criterion IDs were considered independently in the companion manual evaluation: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38. Workflow facts above are descriptive input only and do not alter any of their rewards.

