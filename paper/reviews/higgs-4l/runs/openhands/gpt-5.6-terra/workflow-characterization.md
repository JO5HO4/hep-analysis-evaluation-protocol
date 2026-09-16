# Workflow Characterization — higgs-4l

Generation date: 2026-09-09. Protocol version: `workflow-characterization/v1`. Ordered run identifiers: `20260829T164001Z-higgs-4l-significance-openhands-1515494`.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / OpenHands / gpt-5.6-terra / 20260829T164001Z-higgs-4l-significance-openhands-1515494` | `completed / 0.000000` | 0 | 0 | 1 | 0 | not established | not established | not established | not established | `0 / 5` |

This is descriptive workflow evidence, not a score or outcome grade.

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `OpenHands / gpt-5.6-terra` |
| Run identifier | `20260829T164001Z-higgs-4l-significance-openhands-1515494` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `0` | `agent/trajectory.json: steps` has four context steps and no shell/tool action; session events have no `execute_bash`. |
| Failed-command count | `0` | No recorded shell/tool invocation with exit status. |
| Distinct error signatures | `1` | `agent/openhands.txt:41-64`: `AssertionError: Only one choice is supported for now`. |
| Analysis iterations | `not established` | Transcript ends before an analysis action/configuration. |
| Final iteration | `not established` | No analysis configuration/result exists. |
| Superseded iterations | `not established` | No iteration lineage exists. |
| Recovery count | `0` | Error transitions to `ERROR`; no later same-stage completion. |
| Tool categories | `not established` | No agent tool invocation was recorded. |
| Reproducibility attempt | `not established` | No rerun/headline result occurs. |
| Artifact coverage | `0 / 5` | `artifacts/manifest.json`: empty submission and failed results; expected `run.sh`, README, results, toy plot, profile plot. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `unknown` | `AssertionError: Only one choice is supported for now` | 1 | No subsequent agent action; `openhands.txt:64` state `ERROR`. | `not recovered` |

### Iteration lineage

No directly evidenced analysis iteration exists.

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | not established | not established | not established | not established | `agent/trajectory.json: steps` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `unknown` | `yes` | `no` | E1 | `not established` | `1.681 s` context-to-error | `agent/trajectory.json`; session events `4.json`, `5.json` |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities, duplicate IDs, invalid weights, empty categories, zero denominators, invalid model/fit states | `not established`; no task-solving command/output. | `agent/trajectory.json`; `agent/openhands.txt:41-64` |
