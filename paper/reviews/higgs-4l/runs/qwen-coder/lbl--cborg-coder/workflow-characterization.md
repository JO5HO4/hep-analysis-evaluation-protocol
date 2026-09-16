# Workflow characterization — Higgs → 4l

Generated 2026-09-09 using `workflow-characterization/v1`. This is descriptive, non-scoring evidence and does not affect the Harbor verifier reward or any outcome grade. Ordered run identifiers: `20260902T192318Z-higgs-4l-significance-qwen-coder-1513207 / 20260902T192318Z-higgs-4l-signif__D2WKKsA`.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| higgs-4l / qwen-coder / lbl-cborg-coder / `20260902T192318Z-higgs-4l-signif__D2WKKsA` | completed / 0.687500 | 8 | 0 | 0 | 0 | 1 | 0 | 1 | not established | 6 / 6 |

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/higgs-4l-significance` |
| Agent / model | `qwen-coder / lbl-cborg-coder` |
| Run identifier | `20260902T192318Z-higgs-4l-significance-qwen-coder-1513207 / 20260902T192318Z-higgs-4l-signif__D2WKKsA` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.687500` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 8 recorded tool invocations | `agent/trajectory.json:steps`: read input; todo write; mkdir shell; write Python; write shell wrapper; write README; run shell; read results. |
| Failed-command count | 0 | Every recorded shell/tool result has success or exit code 0; especially the final `run.sh` invocation has exit code 0. |
| Distinct error signatures | 0 | No nonzero exit or explicit tool failure in `agent/trajectory.json` or session JSONL. Harbor's image-OS-validation “Skipping” lines are harness messages, not an agent command failure. |
| Analysis iterations | 1 | One created analysis configuration and one executed `run.sh`; no altered configuration/result attempt is recorded. |
| Final iteration | 1 | The sole execution writes `results/results.json`, which is preserved in artifacts. |
| Superseded iterations | 0 | No earlier generated result or changed configuration appears in trajectory/session trace. |
| Recovery count | 0 | No agent error signature precedes a later completion of the same stage. |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection | Trajectory shows file read/write and shell execution; submitted Python executes numerical likelihood/toys and saves two plots. |
| Reproducibility attempt | not established | One successful run is recorded; no clean-location rerun/comparison is preserved. |
| Artifact coverage | 6 / 6 required task outputs | Found `run.sh`, `run_analysis.py`, `README.md`, `results.json`, `test_statistic.png`, `likelihood_profile.png`; `artifacts/manifest.json` records them as preserved submission/results content. |

## Error signatures and recoveries

No rows: the complete readable agent trajectory contains no failed invocation or explicit tool failure. Consequently there is no recovery evidence to count.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial and only Poisson/toy/profile configuration | Successful wrapper exit; produced JSON and plots | logL_b −11.082750320272; p 0.999732; μhat 1.623886698632 | final | `agent/trajectory.json` final shell invocation and `artifacts/root/results/results.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none | yes — created submission/results directories | not established | `trajectory.json` mkdir invocation, exit 0 |
| input_inspection | yes | yes | none | no | not established | `trajectory.json` read of `/root/data/four_lepton_counts.json` |
| inference_or_selection | yes | yes | none | yes — implemented likelihood ratio and 1,000,000 background toys | not established | submitted `run_analysis.py`; successful final wrapper invocation |
| fit | yes | yes | none | yes — bounded μ optimizer and crossings | not established | `run_analysis.py:minimize_scalar`, `results.json` μ fields |
| plotting | yes | yes | none | no | not established | `run_analysis.py` savefig calls; two preserved PNGs |
| reporting | yes | yes | none | yes — README and JSON result | not established | `README.md`, `results.json`, trajectory writes |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Final output readability | JSON produced and read after execution | `trajectory.json` final `read_file` of `/root/results/results.json` |
| Wrapper execution | completed, exit code 0 | `trajectory.json` final `run_shell_command` |
| NaNs/infinities | not established as an explicit validation check | Source/result search: no dedicated check recorded. |
| Duplicate IDs | not applicable/not recorded for count-vector task | Input and source use channel-aligned count arrays; no ID validation command exists. |
| Invalid weights | not applicable/not recorded for count-vector task | No weighted-event inputs or check in readable evidence. |
| Empty categories | not established as an explicit validation check | No explicit empty-channel check in source/trace. |
| Zero denominators | not established as an explicit validation check | No dedicated denominator validation is recorded. |
| Invalid fit states | not established as an explicit validation check | Source does not record optimizer-success or crossing-success validation. |

## Criterion-ID coverage audit

This workflow profile accompanies, but does not score, every selected rubric identifier. Covered identifiers (and no absent-rubric identifiers) are: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32.

The available chronology is: setup → input inspection → source editing/analysis configuration → inference_or_selection and fit in the one final wrapper execution → plotting → reporting. The transcript establishes no rerun, error-recovery cycle, or stage-duration measurement.
