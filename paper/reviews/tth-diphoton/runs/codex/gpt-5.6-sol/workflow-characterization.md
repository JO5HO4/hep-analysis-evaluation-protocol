# Workflow characterization

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. Run identifiers covered: `20260905T022547Z-tth-diphoton-bd__MPttiyG`.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / codex / gpt-5.6-sol / 20260905T022547Z-tth-diphoton-bd__MPttiyG` | completed / 0.000000 | 35 | 2 | 1 | 1 | 3 | 0 | 3 | not established | 60 / 60 |

This profile is descriptive only and is not a workflow score or a scientific/outcome grade.

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `codex / gpt-5.6-sol` |
| Run identifier | `20260905T022547Z-tth-diphoton-bd__MPttiyG` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 35 | `agent/trajectory.json`: 35 recorded `tool_calls` invocations. |
| Failed-command count | 2 | trajectory steps 23 and 26: `pandas.errors.InvalidIndexError`. |
| Distinct error signatures | 1 | E1 below; the two diagnostics normalize to the same pandas exception/message. |
| Analysis iterations | 3 | two failed `run_analysis.py` executions followed by the successful final execution (steps 22–23, 25–26, 29–30/37–38). |
| Final iteration | 3 | trajectory step 38 emitted `status: complete`; final `run_manifest.json` is complete. |
| Superseded iterations | 0 | iterations 1–2 failed before producing a result, so are not superseded produced results. |
| Recovery count | 1 | E1 recurred, then the data-preparation/score-join stage completed after the grouping repair. |
| Tool categories | shell; source editing; Python/scientific computation; ROOT/RooFit; plotting; file inspection; package/environment management | trajectory commands/patches and final analysis artifacts. |
| Reproducibility attempt | not established | multiple executions reused `/root/results/tth-diphoton-bdt`; no clean-output rerun plus tolerance comparison is recorded. |
| Artifact coverage | 60 / 60 | `run_manifest.json: required_artifacts_checked=60`, `missing_required_artifacts=[]`. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | data_preparation | `pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects` | 2 | trajectory step 27 changes score map to grouped event IDs; step 38 completes the pipeline and final manifest reports complete. | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---:|---|---|---|---|---|
| 1 | initial event-ID score join | not established | failed on non-unique index | neither (no produced result) | trajectory steps 22–23 |
| 2 | event ID expanded with channel number | not established | same non-unique-index failure | neither (no produced result) | trajectory steps 24–26 |
| 3 | score map grouped duplicate IDs | validation boundary Z: 3.339806 -> 3.524192 | completed; final Z=1.438406 | final | trajectory steps 27–38; `optimization/thresholds.json`; `fit/FIT1/significance_asimov.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none | no | not established | trajectory steps 6–10 inspect environment, inputs, ROOT/PyROOT. |
| input_inspection | yes | yes | none | no | not established | steps 6–10 inspect ROOT layouts/branches and data. |
| source editing | yes | yes | none | yes | not established | steps 11, 15, 21, 24, 27 patch analysis/API. |
| data_preparation | yes | yes | E1 | yes | not established | steps 22–30; source grouped duplicate IDs. |
| training | yes | yes | none | no | 1.237 s | `metrics.json: training.training_stage_duration_seconds`. |
| validation | yes | yes | none | no | not established | source `run_analysis.py:349–352`; threshold artifact. |
| optimization | yes | yes | none | no | not established | `optimization/thresholds.json`. |
| inference_or_selection | yes | yes | none | no | not established | `inference/inference_manifest.json`: 101,471 scored, 0 unscored. |
| fit | yes | yes | none | no | not established | final RooFit result and `workspace_manifest.json`. |
| plotting | yes | yes | none | no | not established | complete PNG/PDF inventory and manifests. |
| reporting | yes | yes | none | no | not established | final `report.md`, `run_manifest.json`. |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| finite BDT scores | all 101,471 hadronic scores finite; range 0.0680751–0.9302472 | `metrics.json`, `inference/inference_manifest.json` |
| duplicate IDs | detected indirectly by E1; final workflow groups duplicate IDs for score lookup | trajectory steps 23, 26–27 and `run_analysis.py` final source |
| invalid/nonpositive training weights | retained in signed yields, assigned zero classifier-fit weight | `model/class_balance_check.json`, `training_metadata.json` |
| empty categories | BDT3 and BDT4 identified with zero background and merged into unassigned | `categorization/category_retention.json` |
| invalid fit states | free-mu and mu=0 status 0, covariance quality 3 | `fit/FIT1/results.json` |
| blinding / zero-denominator safeguards | observed TI signal window marked blinded; sideband checks recorded | `run_manifest.json`, `report.md`, source guards |
