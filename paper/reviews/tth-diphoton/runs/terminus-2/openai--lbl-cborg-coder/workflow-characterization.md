# Workflow characterization

Protocol: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Ordered run identifiers: `tth-diphoton / terminus-2 / openai/lbl/cborg-coder / 20260905T003430Z-tth-diphoton-bd__st37ant`

This is descriptive workflow evidence only. It is not a workflow score, task-rubric reward, verifier reward, or authoritative outcome grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / terminus-2 / openai/lbl/cborg-coder / 20260905T003430Z-tth-diphoton-bd__st37ant` | `completed / 0.000000` | 86 | 12 | 4 | 4 | 11 | not established | final saved `run_pipeline.py` + `final_stage.py` revisions | not established | `6 / 55` readable required task outputs; expected unavailable: 49 |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton-bdt-categorization` |
| Agent / model | `terminus-2 / openai/lbl/cborg-coder` |
| Run identifier | `20260905T003430Z-tth-diphoton-bd__st37ant` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `86` | `agent/terminus_2.pane`: 87 shell prompts; final prompt has no invocation, leaving 86 recorded invocations. |
| Failed-command count | `12` | `agent/terminus_2.pane`: explicit Python traceback invocations during pipeline/final-stage repair. |
| Distinct error signatures | `4` | Error table below; absolute paths and line numbers normalized. |
| Analysis iterations | `11` | Eleven distinct `run_pipeline.py`/`final_stage.py` source-writing revisions directly visible in transcript. |
| Final iteration | final saved pipeline and second final-stage revision | Transcript lines 2304–2426 and 2558–2634; preserved source files match final artifacts. |
| Superseded iterations | not established | Earlier rewrites are direct evidence of changed code, but no common completed analysis result identifies which completed results were superseded. |
| Recovery count | `4` | Each signature below is followed by a successful same-stage invocation. |
| Tool categories | shell; source editing; Python/scientific computation; file inspection; package/environment management | Transcript commands include `ls/find/head`, heredoc/`sed` source edits, Python/uproot/sklearn, and `pip install`. No ROOT/RooFit execution or plotting artifact is evidenced. |
| Reproducibility attempt | not established | No clean-output rerun or stated headline-result tolerance in transcript/output. |
| Artifact coverage | `6 / 55`; 49 expected required outputs unavailable | `artifacts/manifest.json` and complete inventory: present source API/config/pipeline/final stage plus result `predictions.csv`, `preselected_events.csv`, `report.md`, `category_summary.csv`, `thresholds.json`; task’s required-output list has 55 named output entries, of which these six result entries are present. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | data_preparation | `KeyInFileError: not found: Events` | 1 | Transcript subsequently changes tree name to `analysis` and reaches `Pipeline completed.` at lines 1960–1976/2106–2110. | recovered |
| E2 | data_preparation | `TypeError: list object is not callable` (`data.fields()`) | 2 | `sed` correction at lines 1548–1550 and later successful pipeline completion at 1960–1976. | recovered |
| E3 | data_preparation | `ValueError: cannot broadcast RegularArray ... in ak.where` | 4 | After rewrites at 1664 and 1842, execution reaches `Pipeline completed.` and writes CSVs (1960–1976, 2106–2119). | recovered |
| E4 | fit | `KeyError: m_gammagamma` | 1 | Final-stage rewrite at 2558 followed by `Final stage completed.` at 2631–2634. | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1–9 | pipeline input/tree, awkward-array handling, preselection serialization, classifier/categorization implementation | not established | intermediate attempts include E1–E3 and later CSV production | not established | `agent/terminus_2.pane`: source write/run sequence lines 222–2426. |
| 10 | final pipeline adds persisted thresholds and category assignment | not established | `Pipeline completed with Categorization.` | final pipeline revision | transcript 2304–2426; preserved `run_pipeline.py`. |
| 11 | final-stage photon-mass calculation replaces missing input field | not established | `Final stage completed.` and writes report/category CSV | final final-stage revision | transcript 2558–2635; preserved `final_stage.py`. |

No common validation metric was emitted, so this lineage is descriptive rather than a comparative optimization record.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none established | yes | not established | Transcript lines 25–222: environment inspection, directories, packages, config/API creation. |
| input_inspection | yes | yes | none established | yes | not established | Transcript lines 25–56, 526–653, 915–921: mounted-input and tree-field inspection. |
| data_preparation | yes | yes | E1, E2, E3 | yes | not established | Transcript lines 485–2426; final execution processes seven MC files and data. |
| training | yes | yes | none established | yes | not established | Final `run_pipeline.py` calls `GradientBoostingClassifier.fit`; transcript line 2426 says pipeline completed. |
| optimization | yes | yes | none established | yes | not established | Final pipeline invokes `optimize_bdt_boundaries` and writes `optimization/thresholds.json`; transcript 2406–2426. |
| inference_or_selection | yes | yes | none established | yes | not established | `predictions.csv` created after final pipeline; transcript 2423–2426. |
| fit | yes | yes | E4 | yes | not established | `final_stage.py` runs after rewrite at 2631–2634. This is a counting/normalization stage, not a RooFit fit. |
| reporting | yes | yes | none established | yes | not established | final stage writes `report.md`; transcript 2631–2635. |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Input ROOT tree/field inspection | performed; tree name corrected to `analysis`, field names displayed | transcript lines 506–653 and 915–921. |
| Pipeline process completion | successful final pipeline invocation | transcript lines 2423–2426; result CSVs in artifact inventory. |
| Final-stage execution | successful after mass-field repair | transcript lines 2522–2547 and 2558–2634. |
| NaNs/infinities | not established | No explicit check in transcript/source/output. |
| Duplicate IDs | not established | No explicit check in transcript/source/output. |
| Invalid weights | not established | No explicit check in transcript/source/output. |
| Empty categories | not established | No explicit check; predictions show no BDT2–BDT4 rows, but no agent validation check was recorded. |
| Zero denominators | partial guard only | `final_stage.py` guards `nti_sb_yield > 0` and category background >0; no execution summary validates all denominators. |
| Invalid model/fit states | not established | No model metric or fit-status record; no RooFit workflow executed. |
