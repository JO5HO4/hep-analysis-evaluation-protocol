# Workflow characterization: qwen-coder / cborg-coder / 20260902T205011Z-top-reconstruct__nqv9SXY

Protocol version: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile does not contribute to any rubric reward, Harbor reward, or outcome grade.

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/top-reconstruction-full-chain-no-pipeline` |
| Agent / model | `qwen-coder / cborg-coder` |
| Run identifier | `20260902T205011Z-top-reconstruct__nqv9SXY` |
| Harbor status / verifier reward | `completed / 0.166667` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `trial.log` and readable trajectory do not expose a complete invocation ledger with outcomes. |
| Failed-command count | not established | Same sources; unknown outcomes were not counted. |
| Distinct error signatures | not established | Same sources; no normalized, attributable command diagnostics were established. |
| Analysis iterations | not established | `optimization_summary.json` if present was inspected; only directly named configurations qualify. |
| Final iteration | not established | No transcript-to-submission lineage establishes it unambiguously. |
| Superseded iterations | not established | No complete per-trial lineage establishes replacements. |
| Recovery count | not established | No same-stage error/recovery pair was directly established. |
| Tool categories | shell; file inspection; source editing; Python/scientific computation | `trial.log`, agent transcript/trajectory, and `artifacts/root/results/`. |
| Reproducibility attempt | not established | No clean-output rerun with a stated agreement tolerance was found. |
| Artifact coverage | 15 readable result files / task-contract total not established | `artifacts/root/results/` recursive bounded inventory. |

## Error signatures and recoveries

No directly established normalized error signature followed by a same-stage recovery. This is `not established`, not zero.

## Iteration lineage

No complete, directly attributable iteration-to-final-submission lineage was established from the readable transcript and saved reports.

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| data_preparation | yes | yes | not established | not established | not established | `artifacts/root/results/` |
| training | yes | yes | not established | not established | not established | `artifacts/root/results/train/` |
| inference_or_selection | yes | yes | not established | not established | not established | `artifacts/root/results/select_triplets/` |
| reporting | yes | yes | not established | not established | not established | saved JSON/plots/reports under `artifacts/root/results/` |

## Validation checks

No explicit NaN/infinity, duplicate-ID, invalid-weight, empty-category, zero-denominator, or invalid-model-state check was credited unless a saved report directly named it during the rubric audit.
