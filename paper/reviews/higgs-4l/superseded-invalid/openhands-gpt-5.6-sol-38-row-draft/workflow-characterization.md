# Workflow characterization: Higgs 4l

Generation date: 2026-09-09. Protocol version: `workflow-characterization/v1`. Run identifiers: `20260829T174904Z-higgs-4l-significance-openhands-1563552`.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / OpenHands / gpt-5.6-sol / 20260829T174904Z-higgs-4l-significance-openhands-1563552` | `completed / 0.000000` | 0 | 0 | 1 | 0 | 0 | 0 | not established | not established | `0 / 4`; missing `run.sh`, `README.md`, diagnostics, `results.json` |

This is descriptive only: no workflow score, ranking, or task-rubric contribution is implied.

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `OpenHands / gpt-5.6-sol` |
| Run identifier | `20260829T174904Z-higgs-4l-significance-openhands-1563552` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `0` agent shell/tool invocations | `agent/openhands.txt`: controller reaches ERROR before any recorded `execute_bash`, editor, or notebook action; trajectory has no task action. |
| Failed-command count | `0` | Same transcript; the recorded assertion is an agent-controller error, not an invocation with nonzero exit status. |
| Distinct error signatures | `1` | `agent/openhands.txt`: `AssertionError: Only one choice is supported for now`. |
| Analysis iterations | `0` | No agent action, analysis configuration, or result before controller error. |
| Final iteration | `not established` | No submitted result; `artifacts/manifest.json` says results artifact failed. |
| Superseded iterations | `0` | No evidenced analysis result was produced. |
| Recovery count | `0` | No later completed action at the same stage follows E1. |
| Tool categories | `not established` | Runtime listed available tools, but no tool invocation was recorded; availability is not use. |
| Reproducibility attempt | `not established` | No rerun or final result exists. |
| Artifact coverage | `0 / 4`; `run.sh`, `README.md`, diagnostics, `results.json` absent | Task deliverables in `job.log`; empty copied submission inventory; `artifacts/manifest.json` records failed results download. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `setup` | `AssertionError: Only one choice is supported for now` | 1 | none; controller transitions to `ERROR` and shuts down | unrecovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| no data rows | not established | not established | No analysis attempt produced a result. | not established | `agent/openhands.txt` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | no | E1 | no | approximately `8 s` from controller RUNNING at 17:50:37 to ERROR at 17:50:45 | `agent/openhands.txt` controller state records |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established | No analysis invocation/source/output after E1. |
| duplicate IDs | not established | No analysis invocation/source/output after E1. |
| invalid weights | not established | No analysis invocation/source/output after E1. |
| empty categories | not established | No analysis invocation/source/output after E1. |
| zero denominators | not established | No analysis invocation/source/output after E1. |
| invalid model or fit states | not established | No analysis invocation/source/output after E1. |
