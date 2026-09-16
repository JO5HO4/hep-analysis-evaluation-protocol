# Workflow characterization: qwen-coder / lbl--cborg-coder

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile is separate from the rubric and creates neither a Harbor reward nor an outcome grade.

## Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton` |
| Agent / model | `qwen-coder / lbl--cborg-coder` |
| Run identifier | `20260902T050526Z-tth-diphoton-bd__2Jw5SMu` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

Evidence opened: the complete R-level metadata/log/verifier/agent bundle and every readable submitted source, JSON/CSV result, plot, workspace/fit record, and report. The task transcript exposes the two outer shell invocations but not Qwen's internal tool-call stream or per-command exit statuses. Rubric coverage reviewed independently: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 2 recorded outer invocations | `R/trial.log:2,181` |
| Failed-command count | not established | outer commands have no exit status; container-inspect diagnostics are harness messages, not resolved agent invocations |
| Distinct error signatures | 1 observed harness signature | `container inspect returned 125`, twice; `R/trial.log:1,183` |
| Analysis iterations | 1 directly evidenced saved configuration | `submission/run_bdt.py`, `results/model/training_metadata.json`, `results/optimization/*` |
| Final iteration | 1: synthetic RandomForest, threshold `0.7693877551` | same; `agent/qwen-code.txt:3,14` |
| Superseded iterations | 0 directly evidenced | no alternative saved configuration/result in transcript, source, or output inventory |
| Recovery count | 0 | the only repeated error signature remains present; no same-stage success is recorded |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection; other (harness/container) | `trial.log`, submitted `.py`, CSV/JSON/PDF/PNG artifacts |
| Reproducibility attempt | not established | no clean-output rerun and result agreement evidence |
| Artifact coverage | 35 readable result artifacts / 58 task-requested artifact paths | bounded `rg --files R`; required list in `R/trial.log:113-172` |

## Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | setup | `container inspect returned EXIT_125` | 2 | none; second occurrence is the same diagnostic | unrecovered |

The agent also states that the actual ATLAS ROOT inputs were absent (`agent/qwen-code.txt:3`) and substituted synthetic data. It is an observed workflow limitation, not a shell-command failure count because the preserved stream has no corresponding resolved invocation.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | RandomForest with five saved features; synthetic generator; one threshold | no common validation metric established | `bdt_auc=0.88` is saved but not identified as validation/test | final | `submission/run_bdt.py`; `results/metrics.json`; `results/optimization/{thresholds,accepted_splits}.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | not established | E1 | no | `13.093559 s` environment setup; `4.719154 s` agent setup | `R/result.json:environment_setup,agent_setup`; `R/trial.log:1` |
| input_inspection | yes | no actual-input access | none directly resolved | synthetic substitution | not established | `agent/qwen-code.txt:3`; `submission/run_preselection.py` |
| data_preparation | yes | synthetic preparation completed | none | yes | not established | `submission/run_bdt.py:generate_mock_data`; `results/predictions.csv` |
| training | yes | synthetic classifier output saved | none | yes | `0.979642 s` recorded training time | `results/model/training_metadata.json`; `submission/run_bdt.py` |
| optimization | yes | one accepted boundary saved | none | yes | not established | `results/optimization/{thresholds,accepted_splits}.json` |
| inference_or_selection | yes | CSV/category products saved | none | yes | not established | `submission/run_categorization.py`; `results/inference/events_with_bdt_scores.csv` |
| fit | yes | mock files written; physical fit not completed | none | yes | not established | `submission/run_fit.py`; `results/fit/FIT1/*.json` |
| plotting | yes | products exist, but fit plots are mock text payloads | none | no | not established | `results/plots/*`; `results/fit/FIT1/plots/*` |
| reporting | yes | `report.md` saved | none | no | not established | `results/report.md`; `agent/qwen-code.txt` |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established | no explicit validation record; CSVs and source were inspected |
| Duplicate IDs | not established | no duplicate-ID audit artifact |
| Invalid weights | not established | no signed-weight/invalid-weight validation artifact |
| Empty categories | observed: BDT2 and BDT3 have zero model yield | `results/categorization/category_summary.csv` |
| Zero denominators | source substitutes `+1e-9` in `S/B` and `S/sqrt(B)` | `submission/run_categorization.py` |
| Invalid model/fit states | fit artifacts explicitly mocked; not a valid RooFit-state check | `submission/run_fit.py`; `results/fit/FIT1/{backend,significance_asimov*.json}` |

Stage timing that is directly established: full trial `729.664439 s`, agent execution `609.033194 s`, verifier `70.747948 s` (`R/result.json`). The workflow profile does not interpret the zero verifier reward as an agent-workflow score.
