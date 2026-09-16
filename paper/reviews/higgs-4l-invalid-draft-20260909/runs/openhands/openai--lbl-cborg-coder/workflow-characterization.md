Protocol version: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile is not a workflow score or outcome grade. Evidence was traced within `results/paper/higgs-4l-significance-paper-version/openhands/openai--lbl-cborg-coder/20260902T201549Z-higgs-4l-significance-openhands-1286844`.

# Workflow characterization — OpenHands / openai--lbl-cborg-coder

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | OpenHands / openai--lbl-cborg-coder |
| Run identifier | `20260902T201549Z-higgs-4l-significance-openhands-1286844` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.950000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `I/T`; heterogeneous completion records do not expose a complete countable stream |
| Failed-command count | at least 1 | `I/T`; explicit `exit code 1` only |
| Distinct error signatures | 1 | `I/T`; one normalized explicit shell failure |
| Analysis iterations | 1 | `I/T`, `I/R` |
| Final iteration | 1 | `I/R` |
| Superseded iterations | 0 | `I/T`, `I/R` |
| Recovery count | 1 | `I/T`; later successful inference/selection execution |
| Tool categories | shell, source editing, Python/scientific computation, plotting, file inspection | `I/T`, `I/S` |
| Reproducibility attempt | not established | `I/T`, `I/R` |
| Artifact coverage | found required task result / expected required task result | `I/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | inference_or_selection | `exit code 1: python3.12 … analysis.py` | 1 | later successful final execution in `I/T`; result in `I/R` | recovered |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | rewritten final analysis after E1 | not established | submitted result | final | `I/T`, `I/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | not established | not established | not established | `I/T` |
| input_inspection | yes | yes | not established | not established | not established | `I/T` |
| inference_or_selection | yes | yes | E1 | yes | not established | `I/T` |
| fit | yes | yes | not established | not established | not established | `I/S`, `I/R` |
| plotting | yes | yes | not established | not established | not established | `I/S` |
| reporting | yes | yes | not established | not established | not established | `I/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| invalid Poisson mean guard | present in final source; execution outcome not established | `I/S` |
