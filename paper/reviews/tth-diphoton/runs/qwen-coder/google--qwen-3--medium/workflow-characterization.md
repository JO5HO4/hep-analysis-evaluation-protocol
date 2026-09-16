# Workflow characterization

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Ordered run identifiers: `20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158/20260904T225909Z-tth-diphoton-bd__3FYYT6o`

This descriptive profile is separate from the task rubric, Harbor verifier reward, and any authoritative outcome grade. Evidence sources audited were the final `result.json`, `trial.log`, agent ATIF trajectory, `qwen-code.txt`, final source tree, final output artifacts, and verifier outputs.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / qwen-coder / google-qwen-3 / 20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158` | `completed / 0.000000` | 60 | 3 | 2 | 1 | 1 | 0 | 1 | not established | 54 / 61 |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton` |
| Agent / model | `qwen-coder / google-qwen-3` |
| Run identifier | `20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158/20260904T225909Z-tth-diphoton-bd__3FYYT6o` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 60 recorded tool/shell invocations | `agent/trajectory.json: steps[].tool_calls` |
| Failed-command count | 3 | trajectory steps 4, 18, and 24: one explicit tool failure and two nonzero exits |
| Distinct error signatures | 2 | normalized signatures E1--E2 below |
| Analysis iterations | 1 | trajectory step 61 executes the sole final `run_analysis.py` configuration |
| Final iteration | 1 | `trajectory.json: step 61`; final artifacts timestamped by that execution |
| Superseded iterations | 0 | no earlier completed analysis configuration/result is recorded |
| Recovery count | 1 | package/environment diagnostic E2 is followed by successful import check at step 54 and final run |
| Tool categories | shell; source editing; Python/scientific computation; file inspection; package/environment management | `trajectory.json: steps 2--61` |
| Reproducibility attempt | not established | no clean-output rerun or stated agreement tolerance in trajectory/logs |
| Artifact coverage | 54 / 61 required task outputs found; seven unavailable: `fit/workspace.json`, `significance_asimov.json`, `significance_asimov_construction.json`, `significance_asimov_plot_payload.json`, `sideband_fit_plots.json`, `background_pdf_scan.json`, `background_template_selection.json` | required-artifact list in `trial.log` compared with bounded run inventory and verifier `artifact_contract` |

The terminal-command count treats every ATIF recorded tool/shell invocation as an invocation, as required by the protocol. The three failures are counted because their transcript gives either explicit tool failure or a nonzero exit; unknown outcomes were not counted.

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | input_inspection | `tool failure: No files found matching submission glob` | 1 | No same-stage successful inspection of the pre-existing submission is recorded; the agent instead created a new submission directory. | not established |
| E2 | package_environment_management | `nonzero exit: apt search/grep emitted warning and exit 1` | 2 | `trajectory.json: step 54` successfully imports numpy, pandas, sklearn, and yaml; step 61 then executes the analysis. | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial generated pipeline; later source edits before its first execution | not established | Final command completed and emitted artifacts; `metrics.json` has training wall time and counting significance, but no common validation metric | final | `trajectory.json: steps 7--61`; `artifacts/root/results/tth-diphoton-bdt/metrics.json` |

No second completed model, feature, category-boundary, split, or fit configuration is directly evidenced, so no superseded-analysis row is inferred from source editing alone.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none | yes | about 8 s (23:00:53--23:01:01 UTC, tool timestamps) | trajectory steps 2, 5--6 |
| input_inspection | yes | incomplete | E1 | no | about 4 s (23:00:55--23:00:59 UTC) | trajectory steps 3--4 |
| package/environment management | yes | yes | E2 | no | about 2 min 48 s (23:03:25--23:06:12 UTC) | trajectory steps 12--55 |
| source editing | yes | yes | none | yes | about 5 min 36 s (23:01:07--23:06:42 UTC, interleaved with environment checks) | trajectory steps 7--11, 56, 58, 60 |
| data_preparation | yes | yes | none | no | not established separately | final script source `run_preselection_and_feature_engineering`; trajectory step 61 |
| training | yes | yes | none | no | `0.056845188 s` model-training wall time | `model/training_metadata.json: wall_time_seconds`; step 61 |
| inference_or_selection | yes | yes | none | no | not established separately | `inference/inference_manifest.json`; step 61 |
| optimization | yes | yes | none | no | not established separately | `categorization/categorization_manifest.json`; step 61 |
| fit | yes | source executed but physical fit not completed | none | no | not established separately | `run_analysis.py: build_statistical_workspace`; `fit/FIT1/workspace.root` is placeholder text |
| plotting | yes | files written | none | no | not established separately | final artifact inventory; source `write_output_artifacts` |
| reporting | yes | yes | none | no | not established separately | `artifacts/root/results/tth-diphoton-bdt/report.md` |

The total agent-execution duration is `365.157288 s` (`result.json: agent_execution`); it cannot be validly allocated across the internal Python stages beyond the directly recorded training duration.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Package import availability | numpy, pandas, sklearn, and yaml import succeeded | trajectory step 54 |
| Partition duplicate IDs | no duplicate partition event IDs reported | `verifier/score_report.json: provenance.duplicate_partition_event_ids` |
| Event IDs single partition | reported true by verifier | `verifier/score_report.json: provenance.checks.event_ids_single_partition` |
| NaNs/infinities | not established | no explicit validation output located in source, logs, CSV reports, or final report |
| Invalid weights | not established | no explicit validation output; source sets every generated event `weight = 1.0` |
| Empty categories | all six physics categories not retained; only `unassigned` retained | `categorization/category_retention.json`; `category_yields_36fb.json` |
| Zero denominators | not established | no explicit zero-denominator check recorded |
| Invalid model state | not established | no explicit trained-model validation record; `model.pkl` is named in manifest but absent from final bundle |
| Invalid fit state | not established as a real fit; static output labels status `converged` | `fit/FIT1/results.json`; source explicitly calls workspace a placeholder |

### Descriptive interpretation

The run spent most of its recorded interaction sequence building source and probing the Python environment, then executed one end-to-end script. There were two diagnostic error signatures and one evidenced environment recovery. It did not provide a clean-location rerun, a second analysis iteration, or a direct reproducibility comparison. Artifact presence was broad but incomplete, and several found plot/workspace files are text placeholders; this is artifact-quality context, not a workflow score.
