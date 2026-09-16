# Workflow characterization — tth-diphoton / Claude Code / claude-opus-5

Protocol `workflow-characterization/v1`; generated 2026-09-09. This is descriptive execution evidence only, never a rubric reward or outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / claude-code / claude-opus-5 / 20260908T234508Z-tth-diphoton-bd__UezeyUP` | completed / 0.000000 | 2 | not established | not established | not established | 4 | 2 | accepted configuration 3 | not established | 61 / 61 required; 84 readable root files |

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `claude-code / claude-opus-5` |
| Run identifier | `20260908T234508Z-tth-diphoton-bd__UezeyUP` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

The audit read the complete preserved bundle: execution `result.json` and eight-line `trial.log`, readable `agent/trajectory.json`, verifier report, submitted analysis source, full artifact manifest, all readable JSON/CSV/Parquet tables, report, plots and plot payloads, workspace JSON and ROOT file. `trial.log` records two explicit `Running command:` invocations. It only says “Command outputs captured,” without each command’s exit status; therefore a failed-command count, normalized error signatures, and recoveries cannot be established. The two `container inspect returned 125` skip notices are harness diagnostics, not exit-status-resolved task-solving invocations.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 2 | `trial.log`: two `Running command:` records |
| Failed-command count | not established | `trial.log` omits invocation exit statuses |
| Distinct error signatures | not established | same; skip notices cannot be assigned to a recorded solver-stage command |
| Analysis iterations | 4 threshold configurations | `optimization/accepted_splits.json`: candidates `0.73`, `0.88`, `0.36`, `0.60` |
| Final iteration | accepted configuration 3: `[0.88,0.73,0.36]` | `metrics.json.optimization`, `thresholds.json`, report |
| Superseded iterations | 2 | accepted one- and two-boundary configurations were replaced by the three-boundary final configuration in `accepted_splits.json` |
| Recovery count | not established | no directly evidenced same-stage error followed by successful repeat |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection | `trial.log`, submitted `analysis/*.py`, generated workspace/tables/plots |
| Reproducibility attempt | not established | deterministic settings are recorded, but no clean-output rerun and agreement test is preserved |
| Artifact coverage | 61 / 61 required; 84 readable files | `report.md` checklist and bounded artifact inventory |

## Error signatures and recoveries

No data rows. The preserved terminal transcript does not expose a solver-command exit status or a normalized diagnostic paired with a later successful run of the same workflow stage. This avoids treating an incomplete transcript as zero errors.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | initial BDT boundary `0.73` | expected combined counting significance | `1.5127509` | superseded | `optimization/accepted_splits.json` |
| 2 | add boundary `0.88` | same metric | `1.6404605`; +8.442% | superseded | same |
| 3 | add boundary `0.36` | same metric | `1.7516610`; +6.779% | final | same; `metrics.json.optimization.thresholds` |
| 4 | proposed boundary `0.60` | same metric | `1.767`; +0.9%, rejected below 5% | rejected, not a submitted result | `accepted_splits.json`, `report.md` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | not established | no | `20.702 s` agent setup (separate environment setup `14.135 s`) | `result.json.agent_setup`, `environment_setup` |
| input_inspection | yes | yes | not established | no | `0.267 s` resolve inputs | `metrics.json.timing_seconds.resolve_inputs`, input contract |
| data_preparation | yes | yes | not established | no | `17.176 s` preselection; `1.284 s` training sample | timing JSON and preselection/training outputs |
| training | yes | yes | not established | model hyperparameters and seed fixed | `1.628 s` pipeline BDT stage (`0.966 s` fitted classifier) | `metrics.json.timing_seconds`, `training_metadata.json` |
| validation | yes | yes | not established | no | not separately established | scalar/vector crosscheck and AUC fields in `metrics.json` |
| optimization | yes | yes | not established | yes, final thresholds | `0.150 s` | `metrics.json.timing_seconds.boundary_optimization`, `accepted_splits.json` |
| inference_or_selection | yes | yes | not established | final category assignment | `2.285 s` inference; `0.610 s` categorization | timing JSON, inference and categorization manifests |
| fit | yes | yes | not established | final workspace/PDF choices | `2.142 s` fit + `1.952 s` fit plots | timing JSON, `workspace.root`, `results.json` |
| plotting | yes | yes | not established | no | `2.006 s` histograms/plots plus stage-specific plot times above | timing JSON and PNG/PDF outputs |
| reporting | yes | yes | not established | no | report says total pipeline `40.4 s`; isolated reporting duration not established | `report.md`, run manifest |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| finite model features | `39,719` finite; `0` dropped non-finite | `model/training_metadata.json.rows` |
| scalar/vectorized rederivation | `1,099` checked, `0` mismatches | `metrics.json.validation.scalar_vs_vectorised_crosscheck` |
| stable partitioning | train/val/test counts `75,175/25,045/25,161`; order-independent stable IDs | `preselection_summary.json.partition` |
| partition duplicate IDs | single partition true | `verifier/score_report.json.provenance.checks.event_ids_single_partition` |
| BDT score range | `[0.0398535,0.9658414]`, unit interval check true | `metrics.json.bdt.score_range`, validation |
| fit validity | free/mu0 statuses `0/0`, covariance `3/3` | `fit/FIT1/results.json` |
| category retention | BDT4 and tH 4j2b dropped below retention requirement; no empty kept category | `categorization/category_retention.json`, `metrics.json` |

## Rubric criterion coverage cross-reference

This workflow audit inspected evidence for every selected rubric identifier: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38. Criterion outcomes and their independent scientific evidence are in the paired `evaluation-report.md`; this file does not score them.
