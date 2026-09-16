# Workflow characterization: ttH diphoton BDT categorization

Protocol: `workflow-characterization/v1`  
Generated: 2026-09-09  
Run identifiers covered: `tth-diphoton / openhands / gpt-5.6-sol / 20260905T044026Z-tth-diphoton-bd__cMU3hZC`

This descriptive profile is separate from the task rubric, Harbor verifier reward, and any authoritative outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / openhands / gpt-5.6-sol / 20260905T044026Z-tth-diphoton-bd__cMU3hZC` | `completed / 0.000000` | 0 | 0 | 1 | 0 | 0 | 0 | not established | not established | `0 / not established` |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton` (`haichenwangberkeley/tth-diphoton-bdt-categorization`) |
| Agent / model | `openhands / gpt-5.6-sol` |
| Run identifier | `20260905T044026Z-tth-diphoton-bd__cMU3hZC` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `0` | `agent/openhands.trajectory.json` has five system/user/agent state records and no shell/tool action; `agent/openhands.txt` reaches controller error before an action. Harness launch in `trial.log` is excluded. |
| Failed-command count | `0` | No recorded shell/tool invocation has a nonzero status. The controller exception is an error signature, not a command invocation. |
| Distinct error signatures | `1` | `agent/openhands.txt:41-63`: `AssertionError: Only one choice is supported for now`. |
| Analysis iterations | `0` | No action or distinct analysis configuration was recorded before termination. |
| Final iteration | `not established` | No submitted result, configuration, or analysis action exists. |
| Superseded iterations | `0` | No result-producing iteration was recorded. |
| Recovery count | `0` | The sole error has no later direct evidence that the same stage completed. |
| Tool categories | `not established` | Tools were registered (`execute_bash`, editor, Python, etc.) in `agent/openhands.txt:37`, but none was invoked; registration is not use. |
| Reproducibility attempt | `not established` | No clean-location rerun or result-comparison record. |
| Artifact coverage | `0 / not established` | Complete run-root inventory has no submitted source or results tree. `artifacts/manifest.json` records failed capture of both required roots, so expected constituent-output count cannot be established from produced artifacts. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `unknown` | `AssertionError: Only one choice is supported for now` | 1 | none; controller changes to `ERROR` and shuts down in `agent/openhands.txt:41-67` | unrecovered |

The diagnostic has no absolute path, timestamp, numeric ID, or run ID needing normalization. It arose while OpenHands converted the first model response to actions, before a task-stage action was identifiable.

### Iteration lineage

No directly evidenced analysis iteration produced a result; therefore there are no lineage rows.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `setup` | yes | yes | none | no | `15.720872 s` environment setup; `16.401893 s` agent setup | `result.json: environment_setup`, `agent_setup`; agent runtime becomes `RUNNING` in `agent/openhands.txt:38`. |
| `unknown` | yes | no | E1 | not established | `24.309630 s` total agent-execution interval; stage-specific duration not established | `result.json: agent_execution`; `agent/openhands.txt:41-63`. |

No `input_inspection`, `data_preparation`, `training`, `validation`, `optimization`, `inference_or_selection`, `fit`, `plotting`, or `reporting` action was observed, so those stages are omitted rather than represented as failures.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established | No agent computation or output table was produced. |
| Duplicate IDs | not established | No agent computation or output table was produced. |
| Invalid weights | not established | No agent computation or output table was produced. |
| Empty categories | not established | No category output was produced. |
| Zero denominators | not established | No calculation output was produced. |
| Invalid model or fit states | not established | No model/fit was executed; the recorded failure is agent-controller infrastructure, not a model or fit state. |

The direct artifact audit covered `result.json`, `config.json`, `trial.log`, `artifacts/manifest.json`, all readable agent logs/trajectories/completion/session events, and verifier reports. The verifier’s `0.000000` reward is execution context only and is not used as a workflow-quality score.
