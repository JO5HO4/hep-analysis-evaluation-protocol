# Workflow characterization — Higgs 4l

Generated 2026-09-09 under `workflow-characterization/v1`. This is descriptive workflow evidence only; it contributes to neither rubric reward, Harbor reward, nor an authoritative outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / qwen-coder / google--qwen-3--best / 20260829T173916Z-higgs-4l-significance-qwen-coder-1554570` | completed / 0.587500 | 16 | 0 | 2 | 2 | 1 | 0 | 1 | not established | 2 / 2 declared preserved artifact roots |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` (`haichenwangberkeley/higgs-4l-significance`) |
| Agent / model | `qwen-coder / google--qwen-3--best` |
| Run identifier | `20260829T173916Z-higgs-4l-significance-qwen-coder-1554570` (trial `20260829T173916Z-higgs-4l-signif__eNaET5b`) |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.587500` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 16 recorded tool/shell/file invocations | `agent/trajectory.json`, agent steps 2–17 (one tool call each) |
| Failed-command count | 0 | Shell invocations in steps 6, 8, 11–13, 15–16 report exit code 0; the plotting traceback occurred inside `run.sh`, which itself exited 0. |
| Distinct error signatures | 2 | `trajectory.json` step 8 records `FileNotFoundError` for diagnostics path; step 13 records the plot y-limit failure. |
| Analysis iterations | 1 | One `analysis.py` configuration was written and executed; later edits target only plotting/run wrapper. |
| Final iteration | 1 | `analysis.py` executed successfully in step 12 and produced the preserved `results.json`. |
| Superseded iterations | 0 | No distinct analysis configuration/result is evidenced. |
| Recovery count | 2 | Diagnostics-path and y-limit plotting errors are each followed by source edits and successful plot generation in step 15. |
| Tool categories | file inspection; source editing; shell; Python/scientific computation; plotting | trajectory steps 2–17 |
| Reproducibility attempt | not established | A direct rerun generated diagnostics after setup repair, but no clean-output rerun/comparison tolerance is recorded. |
| Artifact coverage | 2 / 2 declared preserved artifact roots; generated diagnostics not preserved | `artifacts/manifest.json`: submission directory and results file `ok`; logs/artifacts directory `empty`. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | plotting | `FileNotFoundError: diagnostics.json absent at submission diagnostics path` | 1 | Steps 9–12 redirect plotting to `/root/results/diagnostics`, create directory, and regenerate diagnostics. | recovered |
| E2 | plotting | `ValueError: invalid y-axis limits during profile plot` | 1 | Step 14 replaces y-limit logic; step 15 successfully saves both diagnostic PNGs. | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial likelihood, toy, and profile implementation | saved numerical result | `q=-10.5336557`, `p=0.999785`, `mu_hat=1.6238867` | final | `trajectory.json` step 12; `artifacts/root/results/results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | 3.9 s to next recorded action | trajectory step 2 reads input JSON |
| setup | yes | yes | none | no | 44.1 s (steps 3–7) | writes analysis, plotter, wrapper, README; chmod |
| inference_or_selection | yes | yes | none | no | 28.3 s for final direct analysis run | trajectory step 12; saved results JSON |
| plotting | yes | yes | E1, E2 | yes (plot-path and y-limit fixes) | 81.6 s from initial wrapper execution to successful plots | trajectory steps 8–15 |
| reporting | yes | yes | none | no | 7.1 s | trajectory steps 16–18 final inventory and summary |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Required files/results inventory | submission files and result JSON listed | trajectory step 16 `ls -la` |
| Plot generation | both PNG paths reported saved after repair | trajectory step 15 |
| Result-field inspection | saved JSON read and values displayed | trajectory step 17 |
| Invalid Poisson means | code returns `-inf` when `lam<=0`; no execution check outcome | `artifacts/root/submission/analysis.py: log_poisson` |

The transcript does not establish duplicate-ID, invalid-weight, empty-category, zero-denominator, NaN/infinity, failed-fit, or interval-crossing validation outcomes; they are intentionally not counted as zero or as failed terminal commands.
