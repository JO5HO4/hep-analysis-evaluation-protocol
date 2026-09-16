# Workflow characterization: qwen-coder / google--qwen-3--best

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This is descriptive evidence only; it is not a scientific score or an outcome grade.

## Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `qwen-coder / google--qwen-3--best` |
| Run identifier | `20260905T041241Z-tth-diphoton-bd__JmY5P4p` (R10) |
| Harbor status / verifier reward | `completed / 0.000000` |

## Evidence examined

The review opened the enclosing job `results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/google--qwen-3--best`, its nested trial `20260905T041241Z-tth-diphoton-bd__JmY5P4p`, enclosing and nested `result.json`, `trial.log`, `agent/` trajectory where readable, `verifier/` output, submitted source, and every readable saved result table, JSON, CSV/Parquet manifest, workspace, plot payload, and report below `artifacts/root/`. The preserved transcript does not provide a complete exit-status-resolved command stream; absent counts below are therefore **not established**, never zero.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | preserved `trial.log` and trajectory lack a complete invocation/outcome stream |
| Failed-command count | not established | same |
| Distinct error signatures | not established | same |
| Recovery count | not established | no same-stage error/success pair is directly established |
| Tool categories | source editing, Python/scientific computation | submitted source and saved outputs |
| Analysis iterations | not established | saved optimization/result records |
| Final iteration | not established | no complete, ordered submission lineage |
| Superseded iterations | not established | no complete, ordered submission lineage |
| Reproducibility attempt | not established | report, manifests, and preserved output tree |
| Artifact coverage | 17 outputs / expected count not independently established | recursive artifact inventory under `artifacts/root/` |

## Error signatures and recoveries

No data rows: the preserved command transcript does not resolve invocation exit statuses or normalized diagnostics consistently enough to count errors or recoveries.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | not established | not established | not established | not established | saved optimization records and report, where present |

## Stage timeline

| Stage sequence directly evidenced | Completion | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|
| unknown | stages represented by saved result artifacts where listed | not established | only changes stated above are directly evidenced | not established | submitted source, saved manifests, JSON/CSV/Parquet outputs, workspace and report |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Output/readability review | 17 outputs / expected count not independently established | artifact inventory and readable files under `artifacts/root/` |
| Harness context | completed, verifier reward 0.000000 | enclosing `result.json:stats.evals.*.reward_stats` |

The zero Harbor reward is execution context only. It neither creates workflow failures nor removes readable analysis evidence.

