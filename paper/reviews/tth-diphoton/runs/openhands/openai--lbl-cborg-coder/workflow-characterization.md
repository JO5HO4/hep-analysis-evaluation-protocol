# Workflow characterization: OpenHands / openai--lbl-cborg-coder

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. Descriptive only; it is neither a rubric reward nor an outcome grade.

Run identifiers covered: `tth-diphoton / openhands / openai--lbl-cborg-coder / 20260902T050526Z-tth-diphoton-bd__fm8URtk`.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / openhands / openai--lbl-cborg-coder / 20260902T050526Z-tth-diphoton-bd__fm8URtk` | `completed / 0.000000` | not established | not established | not established | not established | 1 | 0 | 1 | not established | `13 / 67 named result outputs` |

## Run identity

| Field | Value |
|---|---|
| Task | `tth-diphoton` |
| Agent / model | `openhands / openai--lbl-cborg-coder` |
| Run identifier | `20260902T050526Z-tth-diphoton-bd__fm8URtk` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

The preserved root was enumerated and the metadata, terminal log, trajectories/events, submitted source, verifier evidence, all readable JSON/CSV/report artifacts, and both plots were opened. `trial.log` preserves the task prompt and harness launch, while the session material does not provide a complete, exit-status-resolved invocation stream. Therefore command and error quantities are `not established`, not zero.

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | `agent/trajectory.json`, `openhands.trajectory.json`, session events and `openhands.txt` do not expose a complete command/outcome stream. |
| Failed-command count | not established | Same; no reliable recorded exit-status sequence. |
| Distinct error signatures | not established | Same; verifier failures are task-output checks, not an agent-command diagnostic. |
| Analysis iterations | 1 | One hard-coded synthetic XGBoost configuration and one threshold sequence are saved; no second changed configuration is evidenced. |
| Final iteration | 1 | `run.py` generates the saved output tree in one invocation path. |
| Superseded iterations | 0 | No earlier produced result replaced before the saved final artifacts. |
| Recovery count | not established | No same-stage error followed by a directly logged successful retry. |
| Tool categories | shell, source editing, Python/scientific computation, plotting, file inspection | Agent/session records and submitted Python source; Python creates CSV/JSON/PNG outputs. |
| Reproducibility attempt | not established | No clean-output rerun or stated agreement tolerance in logs/results. |
| Artifact coverage | `13 / 67 named result outputs` | `artifacts/manifest.json` and complete `artifacts/root/results` inventory versus output list preserved in `trial.log`. |

## Error signatures and recoveries

No data rows. `verifier/score_report.json` directly identifies absent/mismatched deliverables, but neither it nor the trajectory supplies a normalized failed shell/tool diagnostic followed by a successful retry at the same stage.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Synthetic-data XGBoost (`n_estimators=100`, `max_depth=3`, `learning_rate=.1`, seed 42); thresholds `.8,.6,.4,.2` | not established | Saved preselection/category/fit placeholder outputs | final | `submission/.../run.py`; `results/.../optimization/*.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | not established | yes | 28.294 s environment + agent setup | `result.json:environment_setup,agent_setup` |
| data_preparation | yes | yes | not established | yes | not established | `run.py:simulate_data,apply_preselection`; `preselected_events.csv` |
| training | yes | yes | not established | yes | not established | `run.py:train_bdt`; category outputs evidence inference ran |
| optimization | yes | yes | not established | yes | not established | `optimization/thresholds.json`, `accepted_splits.json` |
| inference_or_selection | yes | yes | not established | yes | not established | `run.py:run_inference,calculate_category_yields`; `category_summary.csv` |
| fit | yes | completed as a mock placeholder | not established | no | not established | `run.py:run_statistical_fit`; `fit/FIT1/{results,significance}.json` |
| plotting | yes | yes | not established | no | not established | two saved PNG files and `run.py:generate_all_plots` |
| reporting | yes | yes | not established | no | not established | `results/.../report.md` |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Finite BDT-input validation | not established | No NaN/infinity check is recorded. |
| Duplicate-ID validation | not established | No duplicate-ID check is recorded. |
| Invalid-weight validation | not established | No signed/invalid-weight validation is recorded. |
| Empty-category validation | not established | `category_summary.csv` shows zero-yield categories, but no explicit validation outcome. |
| Zero-denominator validation | source guards only | `run.py:calculate_category_yields` sets ratios to zero when background is zero. |
| Model/fit-state validation | incomplete | `results.json` says `converged`; source labels fit output mock and has no covariance/fit-state check. |

## Criterion-ID coverage

This workflow profile accompanies the full manual audit of `Q1`, `Q2`, `Q3`, `Q4`, `Q5`, `Q6`, `Q7`, `Q8`, `Q9`, `Q10`, `Q11`, `Q12`, `Q13`, `Q14`, `Q15`, `Q16`, `Q17`, `Q18`, `Q19`, `Q20`, `Q21`, `Q22`, `Q23`, `Q24`, `Q25`, `Q26`, `Q27`, `Q28`, `Q29`, `Q30`, `Q31`, `Q32`, `Q33`, `Q34`, `Q35`, `Q36`, `Q37`, and `Q38`; workflow facts do not alter any of those scientific-review statuses.
