# Workflow characterization — tth-diphoton / Claude Code / claude-sonnet-5

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive review evidence, not a scientific score, Harbor reward, or outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / claude-code / claude-sonnet-5 / 20260908T203904Z-tth-diphoton-bd__mmgsDbk` | `completed / 0.000000` | 82 | 7 | 3 | 1 | 4 | 3 | full-scale final pipeline | not established | 61 required outputs found / 61 expected outputs |

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `claude-code / claude-sonnet-5` |
| Run identifier | `20260908T203904Z-tth-diphoton-bd__mmgsDbk` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

The audit read `trial.log`, full `agent/claude-code.txt`, `agent/trajectory.json`, submitted source, all structured outputs, plots, workspace and verifier outputs. The count below uses the 82 recorded `Bash` tool invocations in the Claude stream. It counts seven explicit failed tool results, grouped into three normalized signatures; a package-import traceback embedded in an otherwise successful package-survey shell invocation is not counted as a failed command.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 82 | `agent/claude-code.txt`, count of `name:Bash` tool-use records |
| Failed-command count | 7 | same transcript, explicit `is_error:true` tool-result records |
| Distinct error signatures | 3 | transcript diagnostics normalized below |
| Analysis iterations | 4 | development throttle result, full-run fit recovery configurations, and final full-scale configuration in ordered transcript/output lineage |
| Final iteration | full-scale uncapped pipeline with independent per-category analytic Asimov fits | `run_manifest.json:max_selected_per_sample_throttle=null`; final source and results |
| Superseded iterations | 3 | the 5,000-row development run and two failed RooFit generation configurations precede final result |
| Recovery count | 1 | RooFit `generateBinned` failures followed by saved analytic Asimov fit artifacts |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection; package/environment management | `agent/claude-code.txt`, source, output tree |
| Reproducibility attempt | not established | a throttled development run and final execution are recorded, but no clean-location rerun with stated agreement tolerance |
| Artifact coverage | 61 / 61 expected required outputs | bounded artifact inventory below `artifacts/root/results/tth-diphoton-bdt` compared with task-required output list |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | package/environment management | `ModuleNotFoundError: No module named xgboost` | 1 | Agent selected recorded `sklearn.ensemble.GradientBoostingClassifier`; final `training_metadata.json` and `metrics.json` are present. | recovered |
| E2 | fit | `Exit code 129: RooAbsPdf::generate / RooAddPdf segmentation violation` | 2 | Final `fit/FIT1/backend.json` documents analytic deterministic Asimov construction; `results.json`, workspace, and fit plots were subsequently written. | recovered |
| E3 | reporting | `Tool rejected: destructive multi-operation rm -rf results command requires approval` | 4 | Agent continued without the rejected deletion command; final full-scale output tree is present. | recovered |

`E1` is an explicit diagnostic from a combined package survey, though the enclosing shell returned success; it is included as an error signature but excluded from failed-command count. E2 and E3 account for six of the seven explicit failed tool results; the seventh is a transcript-level repeat whose full normalized diagnostic is unavailable after truncation, so its signature is not separately inferred.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Development cap `TTH_MAX_SELECTED_PER_SAMPLE=5000` | combined counting Z | `0.07962985` | superseded | `agent/claude-code.txt` recorded capped run output |
| 2 | Full-scale RooFit binned-generation attempt | fit completion | `Exit 129`, `generateBinned`/segfault | superseded | transcript E2 |
| 3 | Repeated RooFit generation attempt | fit completion | `Exit 129`, same normalized E2 | superseded | transcript E2 |
| 4 | Analytic deterministic Asimov construction, uncapped full input | combined expected Asimov Z | `1.83120245` | final | `run_manifest.json`, `fit/FIT1/significance_asimov.json`, `backend.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | E1 | yes — sklearn route used | not established | package survey and source imports in transcript |
| input_inspection | yes | yes | none established | no | not established | transcript lists MC/data inputs; `input_data_contract.json` |
| data_preparation | yes | yes | none established | no | not established | `preselection_summary.json`, Parquet tables |
| training | yes | yes | none established | no | `14.0267 s` BDT training | `model/training_metadata.json` |
| validation | yes | yes | none established | no | not established | `metrics.json` test AUC; partition tables |
| optimization | yes | yes | none established | yes — boundaries 0.68 then 0.87 | not established | `optimization/accepted_splits.json` |
| inference_or_selection | yes | yes | none established | yes — retained four categories | not established | inference manifest; categorization manifest |
| fit | yes | yes | E2 | yes — analytic Asimov fallback | not established | transcript; `fit/FIT1/backend.json`, results |
| plotting | yes | yes | none established | no | not established | PNG/PDF and JSON payload inventory |
| reporting | yes | yes | E3 | no | not established | `report.md`, `run_manifest.json`, transcript |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Finite BDT inputs | scored hadronic rows have finite features; 272,376 hadronic rows | `hadronic_features.parquet:bdt_inputs_finite`; inference manifest |
| Stable partition integrity | every stable event ID belongs to one partition | direct grouping of `preselected_events.parquet`; source `stable_partition` |
| Class-balance accounting | finite pre/post sums and equal post-balance weights | `model/class_balance_check.json` |
| Empty/low-background categories | two BDT categories merged to unassigned below retention threshold | `categorization/category_retention.json` |
| Fit state | final saved per-category fits have migrad/hesse 0 and cov_qual 3 | `fit/FIT1/results.json` |
| Output coverage | 61 required artifacts readable | bounded inventory under `artifacts/root/results/tth-diphoton-bdt` |

## Rubric-criterion coverage index

This index deliberately lists every evaluation criterion ID covered by the companion manual report; it is traceability only and carries no workflow reward.

| Criterion IDs reviewed | Primary workflow evidence |
|---|---|
| Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10 | metadata, report, object/preselection outputs, training metadata |
| Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20 | source, class-balance/partition/category records, workspace |
| Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30 | fit outputs and baseline-comparison audit |
| Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38 | plot payloads, transcript, optimization/configuration outputs, fixed-quantile audit |

The zero verifier reward is execution context. It neither converts the recovered workflow into a workflow failure nor removes the preserved analysis evidence.
