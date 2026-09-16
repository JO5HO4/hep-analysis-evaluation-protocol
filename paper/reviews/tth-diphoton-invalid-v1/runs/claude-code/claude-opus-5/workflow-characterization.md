# Workflow characterization: claude-code / claude-opus-5

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive evidence only; it is not a scientific score or an outcome grade.

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `claude-code / claude-opus-5` |
| Run identifier | `20260908T234508Z-tth-diphoton-bd__UezeyUP` (R1) |
| Harbor status / verifier reward | `completed / 0.000000` |

## Evidence examined

The review opened the enclosing job `results/paper/tth-diphoton-bdt-categorization-paper-version/claude-code/claude-opus-5`, its nested trial `20260908T234508Z-tth-diphoton-bd__UezeyUP`, enclosing and nested `result.json`, `trial.log`, `agent/` trajectory where readable, `verifier/` output, submitted source, and every readable saved result table, JSON, CSV/Parquet manifest, workspace, plot payload, and report below `artifacts/root/`. The preserved transcript does not provide a complete exit-status-resolved command stream; absent counts below are therefore **not established**, never zero.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | preserved `trial.log` and trajectory lack a complete invocation/outcome stream |
| Failed-command count | not established | same |
| Distinct error signatures | not established | same |
| Recovery count | not established | no same-stage error/success pair is directly established |
| Tool categories | shell, source editing, Python/scientific computation, ROOT/RooFit, plotting, file inspection | submitted source and saved outputs |
| Analysis iterations | four threshold configurations; final [0.88, 0.73, 0.36] | saved optimization/result records |
| Final iteration | not established | no complete, ordered submission lineage |
| Superseded iterations | not established | no complete, ordered submission lineage |
| Reproducibility attempt | 61 / 61 | report, manifests, and preserved output tree |
| Artifact coverage | 72 outputs / 61 expected task outputs | recursive artifact inventory under `artifacts/root/` |

## Error signatures and recoveries

No data rows: the preserved command transcript does not resolve invocation exit statuses or normalized diagnostics consistently enough to count errors or recoveries.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | four threshold configurations; final [0.88, 0.73, 0.36] | not established | not established | not established | saved optimization records and report, where present |

## Stage timeline

| Stage sequence directly evidenced | Completion | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|
| input_inspection → data_preparation → training → optimization → fit → plotting → reporting | stages represented by saved result artifacts where listed | not established | only changes stated above are directly evidenced | not established | submitted source, saved manifests, JSON/CSV/Parquet outputs, workspace and report |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Output/readability review | 72 outputs / 61 expected task outputs | artifact inventory and readable files under `artifacts/root/` |
| Harness context | completed, verifier reward 0.000000 | enclosing `result.json:stats.evals.*.reward_stats` |

The zero Harbor reward is execution context only. It neither creates workflow failures nor removes readable analysis evidence.

