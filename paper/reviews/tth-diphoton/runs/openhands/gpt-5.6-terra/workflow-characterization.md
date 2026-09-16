# Workflow characterization: OpenHands / gpt-5.6-terra

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile is not a workflow score, scientific score, Harbor reward, or outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / openhands / gpt-5.6-terra / 20260902T220657Z-tth-diphoton-bd__E6LHpiw` | completed / 0.000000 | 19 | 5 | 2 | 0 | 1 | 0 | not established | not established | 3 source files / result root unavailable |

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `openhands / gpt-5.6-terra` |
| Run identifier | `20260902T220657Z-tth-diphoton-bd__E6LHpiw` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 19 | `agent/sessions/.../events/{9,11,13,15,19,21,23,25,27,29,31,33,35,37,41,43,45,47,49}.json`; plan/view events excluded. |
| Failed-command count | 5 | Event 41 and the four empty poll invocations 43/45/47/49 explicitly report timeout/exit `-1`. |
| Distinct error signatures | 2 | E1 timeout (five invocations); E2 loop termination. |
| Analysis iterations | 1 | Event 37 creates one deterministic HistGradientBoosting configuration and event 41 attempts it. |
| Final iteration | not established | The only run attempt timed out; no result was produced. |
| Superseded iterations | 0 | No result-producing iteration was replaced before submission. |
| Recovery count | 0 | No later same-stage completed analysis execution after E1. |
| Tool categories | shell; file inspection; package/environment management; source editing; Python/scientific computation; ROOT/RooFit (inspection and attempted source) | Events 9--37 and saved source. |
| Reproducibility attempt | not established | No clean-output rerun and no agreeing headline result. |
| Artifact coverage | 3 submitted source files / result-root artifact unavailable | `artifacts/manifest.json`: submission directory `ok`; `/root/results/tth-diphoton-bdt` `failed`. |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | training | `CmdRunAction: command timed out after 120.0 seconds` | 5 | None; each follow-up poll timed out. | unrecovered |
| E2 | unknown | `AgentStuckInLoopError: Agent got stuck in a loop` | 1 | None; agent entered ERROR/shutdown. | unrecovered |

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Deterministic HistGradientBoosting configuration; seed `20250308`; source created | not established | execution timed out; no metrics | neither final nor superseded result | `agent/openhands.trajectory.json` event 37; event 41 |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none established | no | not established | events 9--33 inspect submission, ROOT inputs and environment |
| setup | yes | yes | none established | yes | not established | events 19--37 install/prepare and `py_compile` exits 0 |
| data_preparation | yes | no | E1 | no | at least 120 s for first attempt | event 41 invokes end-to-end script; no completion output |
| training | yes | no | E1 | no | not established | event-37 source defines model; event 41 times out before preserved result |
| validation | no direct completed evidence | not established | none established | no | not established | no saved validation output |
| optimization | no direct completed evidence | not established | none established | no | not established | no saved thresholds/metrics |
| fit | no direct completed evidence | not established | none established | no | not established | no workspace/result root |
| plotting | no direct completed evidence | not established | none established | no | not established | no plots preserved |
| reporting | no direct completed evidence | not established | none established | no | not established | no report preserved |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Python syntax | passed | Event 37 runs `python3 -m py_compile`; metadata exit code `0`. |
| Package/input inspection | attempted | Events 13--33 inspect Python packages, ROOT availability and sample branches; no final data-validation outcome. |
| Invalid model/fit state | not established | No model or fit output survived collection. |
| NaNs/infinities, duplicate IDs, invalid weights, empty categories, zero denominators | not established | No result tables/check records were produced or preserved. |

The zero verifier reward is execution context only. It does not turn unavailable workflow evidence into a workflow failure.
