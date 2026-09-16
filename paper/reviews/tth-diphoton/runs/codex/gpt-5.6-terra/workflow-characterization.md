# Workflow characterization: Codex / gpt-5.6-terra

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive evidence only: it is not a workflow score, rubric reward, verifier reward, or outcome grade.

## Companion criterion coverage

This workflow profile accompanies the independently evidenced rubric review and explicitly covers its complete identifier set: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38. The workflow protocol does not assign scientific statuses or rewards to them; see `evaluation-report.md`.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / codex / gpt-5.6-terra / 20260902T213233Z-tth-diphoton-bd__zWiAt8N` | completed / 0.000000 | not established | not established | not established | not established | not established | not established | not established | not established | 77 readable files / expected count not independently established |

## Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton` |
| Agent / model | `codex / gpt-5.6-terra` |
| Run identifier | `20260902T213233Z-tth-diphoton-bd__zWiAt8N` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

The audit opened `result.json`, `config.json`, `trial.log`, `agent/codex.txt`, `agent/trajectory.json` (71 chronological records), verifier outputs, both submission-source files, every readable JSON/CSV, the ROOT workspace, all plot payloads and referenced PNG/PDF outputs, and `report.md`. The preserved harness log records the outer Codex invocation but does not expose an exit-status-resolved inner shell/tool stream. Counts must consequently remain not established rather than being inferred as zero.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `trial.log` has harness commands; `trajectory.json` is chronological messages, not a complete invocation ledger. |
| Failed-command count | not established | No complete per-invocation exit-status stream. |
| Distinct error signatures | not established | Same limitation; verifier failures are task-output findings, not agent-command failures. |
| Analysis iterations | not established | `optimization/accepted_splits.json` records two boundary additions but not distinct complete analysis configurations/validation attempts. |
| Final iteration | not established | No ordered final-submission lineage in transcript. |
| Superseded iterations | not established | No complete result-replacement lineage. |
| Recovery count | not established | No directly evidenced same-stage failure followed by success. |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection | `trial.log`; `run_analysis.py`; `workspace.root`; saved figures/tables. |
| Reproducibility attempt | not established | `run_manifest.json`, report, source and trajectory contain no clean-output rerun and tolerance comparison. |
| Artifact coverage | 77 readable artifact-root files / expected count not independently established | Literal-path `rg --files .../artifacts/root` inventory; task contract has optional/conditional artifacts, so denominator is not inferred. |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

The verifier’s direct findings—feature mismatch and incomplete workspace/model contract—are scientific/task-contract evidence recorded in the companion evaluation report. They are not terminal-command error signatures under this protocol.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | Boundary additions .80 then .53 are evidenced, but no common validation partition/metric is identified | not established | expected-significance gains 44.839% and 7.356% | not established | `optimization/accepted_splits.json`; `thresholds.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | not established | not established | 14.944 s environment; 5.335 s agent setup | `result.json:environment_setup,agent_setup` |
| input_inspection | yes | yes | not established | not established | not established | `input_data_contract.json`, `preselection_summary.json`, executed source input loop |
| data_preparation | yes | yes | not established | not established | included in 63.888 s analysis runtime | `preselected_events.csv`, `cutflow.json`, `metrics.json` |
| training | yes | yes | not established | final HGB settings recorded | 1.697 s | `model/training_metadata.json`; `metrics.json` |
| optimization | yes | yes | not established | thresholds .80,.53 plus floor .35 | not established | `optimization/thresholds.json`; source |
| inference_or_selection | yes | yes | not established | final category thresholds recorded | not established | `inference/events_with_bdt_scores.csv`, `categorization_manifest.json` |
| fit | yes | completed as recorded, but task-model contract incomplete | not established | no | not established | `workspace.root`, `fit/FIT1/results.json`, source |
| plotting | yes | yes | not established | no | not established | plot inventory and machine-readable histogram payloads |
| reporting | yes | yes | not established | no | not established | `report.md` |

The overall agent-execution interval is 1070.807 s (`result.json:agent_execution`); this cannot be apportioned to uninstrumented stages.

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Finite BDT scores | 272,376 / 272,376 hadronic rows finite | direct read of `hadronic_features.csv`; verifier also reports finite scores |
| Duplicate stable IDs in training table | 0 duplicates; train/validation/test present | direct read of `model/training_sample.csv`; `score_report.json:provenance` |
| Empty categories | BDT4 and tH_4j2b zero yield and merged/not kept; unassigned retained | `category_yields_36fb.json`, `category_retention.json` |
| Fit-state checks | statuses 0/0 and covariance quality 3 | `fit/FIT1/results.json` |
| Zero denominator handling | category source guards `b>0`; no invalid resulting significance | `run_analysis.py` category computation and `category_summary.csv` |

The trial completed; its zero verifier reward remains execution context and does not make missing workflow quantities equal zero.
