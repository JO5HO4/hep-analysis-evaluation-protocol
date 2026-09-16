# Workflow characterization — Higgs to four leptons

Protocol version: `workflow-characterization/v1`. Generated 2026-09-09.
This is descriptive manual evidence only: it creates no workflow score, rank,
weighted total, or task outcome grade.

## Included and excluded paths

Included: the same 15 logical completed bundles A–O listed in
[`evaluation-report.md`](evaluation-report.md), in the same order. Excluded:
the nested trial `result.json` is the trial record for its outer bundle;
wrapper logs, agent directories, and artifact subdirectories are evidence, not
additional runs. No superseded bundle is present in the evidence root.

`H` below is each outer `result.json`; `T` is that run's readable agent
trajectory/transcript. Counts are `not established` unless the transcript
directly exposed an invocation and outcome; no count is inferred from file
presence. Artifact coverage is task-contract context only.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| A | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| B | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| C | completed / 0.950000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| D | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| E | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| F | completed / 0.950000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| G | completed / 0.000000 | not established | not established | not established | not established | not established | not established | not established | not established | task-output tree unavailable / expected task result unavailable |
| H | completed / 0.000000 | not established | not established | not established | not established | not established | not established | not established | not established | task-output tree unavailable / expected task result unavailable |
| I | completed / 0.950000 | not established | at least 1 | 1 | 1 | 1 | 0 | 1 | not established | found task result / expected task result |
| J | completed / 0.587500 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| K | completed / 0.750000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| L | completed / 0.687500 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| M | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| N | completed / 1.000000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |
| O | completed / 0.700000 | not established | not established | not established | not established | 1 | 0 | 1 | not established | found task result / expected task result |

## Per-run workflow profiles

`S`, `R`, `T`, and `H` use the exact bundle-relative evidence notation defined
in `evaluation-report.md`; each prefix expands through that report's included
run table to one preserved bundle. The outer `H:result.json` and nested
`<trial>/result.json` were inspected for every profile. A source file or final
result establishes that a stage completed; it does not establish an unrecorded
terminal-command count or duration.

### A — Claude Code / claude-opus-5 / 20260829T171737Z-higgs-4l-significance-claude-code-1534712

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Claude Code / claude-opus-5 |
| Run identifier | `20260829T171737Z-higgs-4l-significance-claude-code-1534712` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `A/T`; retained transcript does not expose a countable invocation stream |
| Failed-command count | not established | `A/T`; no complete exit-status stream |
| Distinct error signatures | not established | `A/T` |
| Analysis iterations | 1 | `A/S`, `A/R`; one submitted computation is directly evidenced |
| Final iteration | 1 | `A/R` |
| Superseded iterations | 0 | `A/S`, `A/R`; no earlier produced result is evidenced |
| Recovery count | not established | `A/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `A/S`, `A/R` |
| Reproducibility attempt | not established | `A/T`, `A/R` |
| Artifact coverage | found required task result / expected required task result | `A/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `A/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `A/S` |
| fit | yes | yes | not established | not established | not established | `A/S`, `A/R` |
| plotting | yes | yes | not established | not established | not established | `A/S` |
| reporting | yes | yes | not established | not established | not established | `A/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `A/S`, `A/R` |

### B — Claude Code / claude-sonnet-5 / 20260829T161300Z-higgs-4l-significance-claude-code-1487708

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Claude Code / claude-sonnet-5 |
| Run identifier | `20260829T161300Z-higgs-4l-significance-claude-code-1487708` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `B/T` |
| Failed-command count | not established | `B/T` |
| Distinct error signatures | not established | `B/T` |
| Analysis iterations | 1 | `B/S`, `B/R` |
| Final iteration | 1 | `B/R` |
| Superseded iterations | 0 | `B/S`, `B/R` |
| Recovery count | not established | `B/T` |
| Tool categories | Python/scientific computation, file inspection | `B/S`, `B/R` |
| Reproducibility attempt | not established | `B/T`, `B/R` |
| Artifact coverage | found required task result / expected required task result | `B/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `B/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `B/S` |
| fit | yes | yes | not established | not established | not established | `B/S`, `B/R` |
| reporting | yes | yes | not established | not established | not established | `B/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `B/S`, `B/R` |

### C — Claude Code / lbl--cborg-coder / 20260902T192326Z-higgs-4l-significance-claude-code-1370864

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Claude Code / lbl--cborg-coder |
| Run identifier | `20260902T192326Z-higgs-4l-significance-claude-code-1370864` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.950000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `C/T` |
| Failed-command count | not established | `C/T` |
| Distinct error signatures | not established | `C/T` |
| Analysis iterations | 1 | `C/S`, `C/R` |
| Final iteration | 1 | `C/R` |
| Superseded iterations | 0 | `C/S`, `C/R` |
| Recovery count | not established | `C/T` |
| Tool categories | Python/scientific computation, file inspection | `C/S`, `C/R` |
| Reproducibility attempt | not established | `C/T`, `C/R` |
| Artifact coverage | found required task result / expected required task result | `C/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `C/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `C/S` |
| fit | yes | yes | not established | not established | not established | `C/S`, `C/R` |
| reporting | yes | yes | not established | not established | not established | `C/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `C/S`, `C/R` |

### D — Codex / gpt-5.6-sol / 20260829T170234Z-higgs-4l-significance-codex-1524332

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Codex / gpt-5.6-sol |
| Run identifier | `20260829T170234Z-higgs-4l-significance-codex-1524332` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `D/T` |
| Failed-command count | not established | `D/T` |
| Distinct error signatures | not established | `D/T` |
| Analysis iterations | 1 | `D/S`, `D/R` |
| Final iteration | 1 | `D/R` |
| Superseded iterations | 0 | `D/S`, `D/R` |
| Recovery count | not established | `D/T` |
| Tool categories | Python/scientific computation, file inspection | `D/S`, `D/R` |
| Reproducibility attempt | not established | `D/T`, `D/R` |
| Artifact coverage | found required task result / expected required task result | `D/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `D/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `D/S` |
| fit | yes | yes | not established | not established | not established | `D/S`, `D/R` |
| reporting | yes | yes | not established | not established | not established | `D/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `D/S`, `D/R` |

### E — Codex / gpt-5.6-terra / 20260829T160141Z-higgs-4l-significance-codex-1477637

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Codex / gpt-5.6-terra |
| Run identifier | `20260829T160141Z-higgs-4l-significance-codex-1477637` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `E/T` |
| Failed-command count | not established | `E/T` |
| Distinct error signatures | not established | `E/T` |
| Analysis iterations | 1 | `E/S`, `E/R` |
| Final iteration | 1 | `E/R` |
| Superseded iterations | 0 | `E/S`, `E/R` |
| Recovery count | not established | `E/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `E/S`, `E/R` |
| Reproducibility attempt | not established | `E/T`, `E/R` |
| Artifact coverage | found required task result / expected required task result | `E/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `E/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `E/S` |
| fit | yes | yes | not established | not established | not established | `E/S`, `E/R` |
| plotting | yes | yes | not established | not established | not established | `E/S` |
| reporting | yes | yes | not established | not established | not established | `E/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `E/S`, `E/R` |

### F — Codex / lbl--cborg-coder / 20260902T192326Z-higgs-4l-significance-codex-1785193

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Codex / lbl--cborg-coder |
| Run identifier | `20260902T192326Z-higgs-4l-significance-codex-1785193` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.950000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `F/T` |
| Failed-command count | not established | `F/T` |
| Distinct error signatures | not established | `F/T` |
| Analysis iterations | 1 | `F/S`, `F/R` |
| Final iteration | 1 | `F/R` |
| Superseded iterations | 0 | `F/S`, `F/R` |
| Recovery count | not established | `F/T` |
| Tool categories | Python/scientific computation, file inspection | `F/S`, `F/R` |
| Reproducibility attempt | not established | `F/T`, `F/R` |
| Artifact coverage | found required task result / expected required task result | `F/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `F/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `F/S` |
| fit | yes | yes | not established | not established | not established | `F/S`, `F/R` |
| reporting | yes | yes | not established | not established | not established | `F/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `F/S`, `F/R` |

### G — OpenHands / gpt-5.6-sol / 20260829T174904Z-higgs-4l-significance-openhands-1563552

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | OpenHands / gpt-5.6-sol |
| Run identifier | `20260829T174904Z-higgs-4l-significance-openhands-1563552` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `G/T` |
| Failed-command count | not established | `G/T` |
| Distinct error signatures | not established | `G/T` |
| Analysis iterations | not established | `G/T`; no submitted task result retained |
| Final iteration | not established | `G/T`, `G/R` |
| Superseded iterations | not established | `G/T` |
| Recovery count | not established | `G/T` |
| Tool categories | not established | `G/T` |
| Reproducibility attempt | not established | `G/T` |
| Artifact coverage | task-output tree unavailable / expected task result unavailable | `G/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | not established | not established | not established | not established | `G/T`, `G/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | not established | not established | not established | not established | `G/T` |
| input_inspection | yes | not established | not established | not established | not established | `G/T` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `G/T` |

### H — OpenHands / gpt-5.6-terra / 20260829T164001Z-higgs-4l-significance-openhands-1515494

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | OpenHands / gpt-5.6-terra |
| Run identifier | `20260829T164001Z-higgs-4l-significance-openhands-1515494` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `H/T` |
| Failed-command count | not established | `H/T` |
| Distinct error signatures | not established | `H/T` |
| Analysis iterations | not established | `H/T`; no submitted task result retained |
| Final iteration | not established | `H/T`, `H/R` |
| Superseded iterations | not established | `H/T` |
| Recovery count | not established | `H/T` |
| Tool categories | not established | `H/T` |
| Reproducibility attempt | not established | `H/T` |
| Artifact coverage | task-output tree unavailable / expected task result unavailable | `H/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | not established | not established | not established | not established | `H/T`, `H/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | not established | not established | not established | not established | `H/T` |
| input_inspection | yes | not established | not established | not established | not established | `H/T` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `H/T` |

### I — OpenHands / openai--lbl-cborg-coder / 20260902T201549Z-higgs-4l-significance-openhands-1286844

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

### J — Qwen Coder / google--qwen-3--best / 20260829T173916Z-higgs-4l-significance-qwen-coder-1554570

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Qwen Coder / google--qwen-3--best |
| Run identifier | `20260829T173916Z-higgs-4l-significance-qwen-coder-1554570` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.587500 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `J/T` |
| Failed-command count | not established | `J/T` |
| Distinct error signatures | not established | `J/T` |
| Analysis iterations | 1 | `J/S`, `J/R` |
| Final iteration | 1 | `J/R` |
| Superseded iterations | 0 | `J/S`, `J/R` |
| Recovery count | not established | `J/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `J/S`, `J/R` |
| Reproducibility attempt | not established | `J/T`, `J/R` |
| Artifact coverage | found required task result / expected required task result | `J/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `J/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `J/S` |
| fit | yes | yes | not established | not established | not established | `J/S`, `J/R` |
| plotting | yes | yes | not established | not established | not established | `J/S` |
| reporting | yes | yes | not established | not established | not established | `J/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `J/S`, `J/R` |

### K — Qwen Coder / google--qwen-3--medium / 20260829T163057Z-higgs-4l-significance-qwen-coder-1506981

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Qwen Coder / google--qwen-3--medium |
| Run identifier | `20260829T163057Z-higgs-4l-significance-qwen-coder-1506981` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.750000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `K/T` |
| Failed-command count | not established | `K/T` |
| Distinct error signatures | not established | `K/T` |
| Analysis iterations | 1 | `K/S`, `K/R` |
| Final iteration | 1 | `K/R` |
| Superseded iterations | 0 | `K/S`, `K/R` |
| Recovery count | not established | `K/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `K/S`, `K/R` |
| Reproducibility attempt | not established | `K/T`, `K/R` |
| Artifact coverage | found required task result / expected required task result | `K/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `K/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `K/S` |
| fit | yes | yes | not established | not established | not established | `K/S`, `K/R` |
| plotting | yes | yes | not established | not established | not established | `K/S` |
| reporting | yes | yes | not established | not established | not established | `K/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `K/S`, `K/R` |

### L — Qwen Coder / lbl--cborg-coder / 20260902T192318Z-higgs-4l-significance-qwen-coder-1513207

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Qwen Coder / lbl--cborg-coder |
| Run identifier | `20260902T192318Z-higgs-4l-significance-qwen-coder-1513207` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.687500 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `L/T` |
| Failed-command count | not established | `L/T` |
| Distinct error signatures | not established | `L/T` |
| Analysis iterations | 1 | `L/S`, `L/R` |
| Final iteration | 1 | `L/R` |
| Superseded iterations | 0 | `L/S`, `L/R` |
| Recovery count | not established | `L/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `L/S`, `L/R` |
| Reproducibility attempt | not established | `L/T`, `L/R` |
| Artifact coverage | found required task result / expected required task result | `L/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `L/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `L/S` |
| fit | yes | yes | not established | not established | not established | `L/S`, `L/R` |
| plotting | yes | yes | not established | not established | not established | `L/S` |
| reporting | yes | yes | not established | not established | not established | `L/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `L/S`, `L/R` |

### M — Terminus 2 / gpt-5.6-sol / 20260829T173058Z-higgs-4l-significance-terminus-2-1543955

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Terminus 2 / gpt-5.6-sol |
| Run identifier | `20260829T173058Z-higgs-4l-significance-terminus-2-1543955` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `M/T` |
| Failed-command count | not established | `M/T` |
| Distinct error signatures | not established | `M/T` |
| Analysis iterations | 1 | `M/S`, `M/R` |
| Final iteration | 1 | `M/R` |
| Superseded iterations | 0 | `M/S`, `M/R` |
| Recovery count | not established | `M/T` |
| Tool categories | Python/scientific computation, file inspection | `M/S`, `M/R` |
| Reproducibility attempt | not established | `M/T`, `M/R` |
| Artifact coverage | found required task result / expected required task result | `M/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `M/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `M/S` |
| fit | yes | yes | not established | not established | not established | `M/S`, `M/R` |
| reporting | yes | yes | not established | not established | not established | `M/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `M/S`, `M/R` |

### N — Terminus 2 / gpt-5.6-terra / 20260829T162334Z-higgs-4l-significance-terminus-2-1496619

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Terminus 2 / gpt-5.6-terra |
| Run identifier | `20260829T162334Z-higgs-4l-significance-terminus-2-1496619` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 1.000000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `N/T` |
| Failed-command count | not established | `N/T` |
| Distinct error signatures | not established | `N/T` |
| Analysis iterations | 1 | `N/S`, `N/R` |
| Final iteration | 1 | `N/R` |
| Superseded iterations | 0 | `N/S`, `N/R` |
| Recovery count | not established | `N/T` |
| Tool categories | Python/scientific computation, plotting, file inspection | `N/S`, `N/R` |
| Reproducibility attempt | not established | `N/T`, `N/R` |
| Artifact coverage | found required task result / expected required task result | `N/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `N/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `N/S` |
| fit | yes | yes | not established | not established | not established | `N/S`, `N/R` |
| plotting | yes | yes | not established | not established | not established | `N/S` |
| reporting | yes | yes | not established | not established | not established | `N/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `N/S`, `N/R` |

### O — Terminus 2 / openai--lbl-cborg-coder / 20260902T192401Z-higgs-4l-significance-terminus-2-1410561

#### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | Terminus 2 / openai--lbl-cborg-coder |
| Run identifier | `20260902T192401Z-higgs-4l-significance-terminus-2-1410561` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | completed / 0.700000 |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `O/T` |
| Failed-command count | not established | `O/T` |
| Distinct error signatures | not established | `O/T` |
| Analysis iterations | 1 | `O/S`, `O/R` |
| Final iteration | 1 | `O/R` |
| Superseded iterations | 0 | `O/S`, `O/R` |
| Recovery count | not established | `O/T` |
| Tool categories | Python/scientific computation, file inspection | `O/S`, `O/R` |
| Reproducibility attempt | not established | `O/T`, `O/R` |
| Artifact coverage | found required task result / expected required task result | `O/R` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | not established | not established | not established | not established |

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | not established | not established | submitted result | final | `O/R` |

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | not established | not established | not established | `O/S` |
| fit | yes | yes | not established | not established | not established | `O/S`, `O/R` |
| reporting | yes | yes | not established | not established | not established | `O/R` |

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| not established | not established | `O/S`, `O/R` |
