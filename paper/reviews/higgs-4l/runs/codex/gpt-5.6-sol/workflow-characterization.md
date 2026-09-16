# Workflow characterization: Higgs → 4l significance

Protocol: `workflow-characterization/v1`  
Generated: 2026-09-09  
Run: `higgs-4l / Codex / gpt-5.6-sol / 20260829T170234Z-higgs-4l-signif__G4rVSn2`

Descriptive evidence only; not a workflow score, rubric reward, verifier reward, or outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / Codex / gpt-5.6-sol / 20260829T170234Z-higgs-4l-signif__G4rVSn2` | completed / 1.000000 | not established | not established | not established | not established | not established | not established | not established | not established | 5 / 5 |

## Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `Codex / gpt-5.6-sol` |
| Run identifier | `20260829T170234Z-higgs-4l-signif__G4rVSn2` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | Host `job.log`/`trial.log` show harness invocation, not a countable agent command ledger. |
| Failed-command count | not established | No per-agent invocation exit-status ledger. |
| Distinct error signatures | not established | No countable normalized agent-error ledger; trial completed cleanly. |
| Analysis iterations | not established | Final source/output do not expose attempted configurations. |
| Final iteration | not established | No indexed iteration lineage. |
| Superseded iterations | not established | No directly evidenced replaced result. |
| Recovery count | not established | No same-stage error/recovery evidence. |
| Tool categories | Python/scientific computation; plotting; source editing; reporting | `analysis.py`, JSON result, PNGs, README. |
| Reproducibility attempt | not established | Fixed seed/runnable code exist, but no clean-output rerun comparison. |
| Artifact coverage | `5 / 5` | Found executable, README, output JSON, and both required diagnostics. |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| — | — | not established | not established | not established | not established |

Trial `result.json` reports one completed and zero errored trials, but this is not an agent-terminal error count.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| — | not established | not established | not established | not established | Final source/output only; no distinct configuration lineage. |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| inference_or_selection | yes | yes | not established | not established | not established | `submission/analysis.py`; `results/results.json` |
| plotting | yes | yes | not established | not established | not established | `analysis.py: make_diagnostics`; two PNGs |
| reporting | yes | yes | not established | not established | not established | README and result JSON |

Top-level elapsed wall interval is `323.641413 s` from `result.json`; no stage/pure-agent duration is retained.

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | rejected in inputs | `analysis.py: load_counts` uses `np.isfinite`. |
| Invalid observed counts | rejected unless finite non-negative integers | `analysis.py: load_counts`. |
| Invalid Poisson means | rejected unless background positive and signal non-negative with one positive | `analysis.py: load_counts`. |
| Failed fit/crossing bracket | `RuntimeError` | `analysis.py: fit_signal_strength`. |
| Duplicate IDs, invalid weights, empty categories, zero denominators | not applicable/not established | Count-array analysis uses no IDs, weights, or event categories. |

## Evidence scope

The bounded run was enumerated across metadata, harness/trial logs, agent/session artifacts, source, output JSON, plots, manifest, and verifier records. It contains no CSV, Parquet, ROOT/RooFit workspace, or separate workflow ledger. Unavailable values are `not established`, never zero.
