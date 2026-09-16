# Workflow characterization

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Ordered run identifiers: `haichenwangberkeley/tth-diphoton-bdt-categorization / qwen-coder / google/qwen-3 / 20260905T041241Z-tth-diphoton-bd__JmY5P4p`

This is descriptive workflow evidence only; it is not a workflow score, Harbor reward, rubric reward, or outcome grade. Rubric coverage cross-reference (all IDs assessed independently in the companion report): Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / qwen-coder / google/qwen-3 / 20260905T041241Z-tth-diphoton-bd__JmY5P4p` | `completed / 0.000000` | 50 | 0 | 0 | 0 | not established | not established | not established | not established | `12 found / 65 expected`; 53 unavailable |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `qwen-coder / google/qwen-3` |
| Run identifier | `20260905T041241Z-tth-diphoton-bd__JmY5P4p` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 50 recorded tool invocations | `agent/trajectory.json: steps[].tool_calls` |
| Failed-command count | 0 | Only displayed shell results with explicit exit status are zero; other command observations are empty/unknown and are not counted. |
| Distinct error signatures | 0 | No invocation exposes a nonzero exit status or explicit tool failure; empty observations are unknown. |
| Analysis iterations | not established | Repeated script invocations and edits are visible, but no distinct completed, result-producing configuration is directly evidenced. |
| Final iteration | not established | `results/.../run_manifest.json` remains `status=running`, `end_time=0`, with no produced-artifact list. |
| Superseded iterations | not established | No completed intermediate result is preserved. |
| Recovery count | 0 | No normalized explicit error signature has direct same-stage completion evidence. |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection; package/environment management | `trajectory.json: tool_calls`; source imports and invocation commands. |
| Reproducibility attempt | not established | No clean-output rerun and no tolerance comparison are recorded. |
| Artifact coverage | `12 found / 65 expected`; 53 unavailable | `trial.log: Required output artifacts`; artifact inventory from `rg --files` and `artifacts/manifest.json`. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| N/A | unknown | not established: empty tool observations do not expose diagnostics or exit statuses | N/A | N/A | not established |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| not established | Trajectory edits mention duplicate-column repair and rename to `diphoton_pt_jet_feature`, but no completed analysis configuration is preserved. | not established | not established | not established | `agent/trajectory.json: steps 25–37`; `agent/qwen-code.txt` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none established | no | 20.773 s agent setup | `result.json: agent_setup`; trajectory steps 2–5 |
| input_inspection | yes | not established | none established | not established | not established | `trajectory.json: task prompt`; source uses declared input path but synthesizes data |
| data_preparation | yes | not established | none established | yes | not established | `analyze.py: load_root_file/select_events`; `metrics.json` is all zero |
| training | yes | not established | none established | yes | not established | trajectory steps 15–37; absent `model/training_metadata.json` |
| validation | yes | not established | none established | not established | not established | source calculates validation AUC, but no result artifact |
| optimization | yes | not established | none established | not established | not established | `top_categorization.py: optimize_bdt_boundaries`; absent optimization JSON |
| inference_or_selection | yes | not established | none established | not established | not established | source functions; absent preselected/inference/prediction tables |
| fit | yes | not established | none established | not established | not established | source labels ROOT/RooFit and results as placeholders; workspace absent |
| plotting | yes | yes, limited placeholder outputs | none established | no | not established | six `plots/*.png|pdf`; `analyze.py: create_placeholder_plots` |
| reporting | yes | not established | none established | not established | not established | source contains `create_report`; preserved `report.md` absent |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established | No saved table/check result. |
| Duplicate IDs | not established | No saved table/check result. |
| Invalid weights | not established | Intended bookkeeping exists only in source; class-balance JSON absent. |
| Empty categories | not established | Category outputs absent. |
| Zero denominators | not established | Source guards divisions, but no executed check result. |
| Invalid model states | not established | Training metadata/model absent. |
| Invalid fit states | not established | Fit status artifact absent; source placeholders are not an executed validation. |

### Artifact roots

`<source-repository>/results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/google--qwen-3--best/20260905T041241Z-tth-diphoton-bdt-categorization-qwen-coder-503382/20260905T041241Z-tth-diphoton-bd__JmY5P4p`

The 12 found files are the two submitted source files, six plot files, `metrics.json`, `run_manifest.json`, `cutflow.json`, and four configuration/selection JSON/YAML files (some categories overlap as paths); the count is artifact-contract coverage, not a physics result. The expected-output inventory is the 65 entries enumerated in `trial.log` lines 110–179. The verifier independently confirms absent preselected table and training metadata in `verifier/score_report.json`.
