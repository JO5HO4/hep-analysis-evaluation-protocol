# Workflow characterization — Higgs four-lepton significance

Generation date: 2026-09-09. Protocol: `workflow-characterization/v1`. Ordered run identifiers: `haichenwangberkeley/higgs-4l-significance / openhands / gpt-5.6-sol / 20260829T174904Z-higgs-4l-signif__V5CzXRE`.

This descriptive profile is separate from the manual rubric review, Harbor verifier reward, and any authoritative outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / OpenHands / gpt-5.6-sol / 20260829T174904Z-higgs-4l-signif__V5CzXRE` | `completed / 0.000000` | 0 | 0 | 1 | 0 | 0 | 0 | not established | not established | `0 / 5` task-output classes found; expected source/run script, result JSON, README, and two diagnostics unavailable |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/higgs-4l-significance` |
| Agent / model | `openhands / gpt-5.6-sol` |
| Run identifier | `20260829T174904Z-higgs-4l-signif__V5CzXRE` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `0` | `agent/trajectory.json: steps` has four system/user context steps and no action/tool event; `agent/openhands.txt` records startup then controller error. |
| Failed-command count | `0` | No shell or tool invocation was recorded, so no invocation has a nonzero exit status. The controller exception is recorded separately, not counted as a command. |
| Distinct error signatures | `1` | `agent/openhands.txt:41-64`: `AssertionError: Only one choice is supported for now`. |
| Analysis iterations | `0` | No configuration attempt or produced analysis result is directly evidenced. |
| Final iteration | `not established` | No result was produced. |
| Superseded iterations | `0` | No produced iteration is recorded. |
| Recovery count | `0` | No later completion of the failed controller/startup stage is recorded. |
| Tool categories | `not established` | Tools were registered, but no tool invocation occurred; registration is not use. |
| Reproducibility attempt | `not established` | No rerun from a clean output location is recorded. |
| Artifact coverage | `0 / 5` task-output classes found: source/run script, results JSON, README, toy diagnostic, profile diagnostic | `artifacts/manifest.json`; `verifier/score_report.json: framework, diagnostics`. Expected classes are task-contract context, not a workflow score. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `setup` | `AssertionError: Only one choice is supported for now` | 1 | No subsequent agent-controller success or action event in `agent/openhands.txt` or `agent/trajectory.json` | not recovered |

### Iteration lineage

No analysis configuration or result-producing iteration is directly evidenced. The sole model response is a plan to inspect the input; it did not execute.

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| none | not established | not established | no produced result | not established | `agent/trajectory.json`; `agent/completions/gpt-5.6-sol-1788025845.0566354.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | no | E1 | no | `~8 s` from agent RUNNING at `17:50:37` to controller error at `17:50:45`; this is controller-stage duration, not analysis time | `agent/openhands.txt:39-64` |

The Harbor timing record separately gives environment setup `18.012534 s`, agent setup `17.320247 s`, agent execution allocation `29.537057 s`, and verifier `71.139049 s` (`result.json` timestamp fields). Those are harness phase durations; the transcript does not establish a completed scientific workflow stage.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established | No source, command, output table, or result JSON; `artifacts/manifest.json` says results collection failed. |
| Duplicate IDs | not established | No source or input-inspection invocation in `agent/trajectory.json`. |
| Invalid weights | not established | No source or computation invocation in `agent/trajectory.json`. |
| Empty categories | not established | No source or computation invocation in `agent/trajectory.json`. |
| Zero denominators | not established | No source or computation invocation in `agent/trajectory.json`. |
| Invalid model or fit states | not established | No source/profile execution or result JSON; verifier reports missing `run.sh`. |

The trial result has `exception_info: null` and one completed Harbor trial, but this does not conflict with the agent-controller error: the transcript shows the agent entered `ERROR` before any action, while Harbor proceeded to artifact collection and verifier execution. The verifier then directly found missing deliverables and returned reward zero.
