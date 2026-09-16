# Workflow Characterization — higgs-4l

Generation date: 2026-09-09. Protocol version: `workflow-characterization/v1`. Ordered run identifiers: `20260902T201549Z-higgs-4l-significance-openhands-1286844` (trial `20260902T201549Z-higgs-4l-signif__hJL9JqC`). This is descriptive evidence, not a score or outcome grade. Cross-file criterion coverage is `Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32`; these IDs are not workflow rewards.

## 1. Cross-run workflow summary
| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / OpenHands / openai/lbl/cborg-coder / 20260902T201549Z-higgs-4l-significance-openhands-1286844` | `completed / 0.950000` | 30 | 5 | 3 | 3 | 2 | 1 | 2 | not established | `6 / 6` |

## 2. Per-run workflow profile
### Run identity
| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `OpenHands / openai/lbl/cborg-coder` |
| Run identifier | `20260902T201549Z-higgs-4l-significance-openhands-1286844` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.950000` |

### Workflow metrics
| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `30` | `agent/sessions/.../event_cache/{0-25,25-50,50-75}.json`: 9 + 13 + 8 `run`/`run_ipython` invocations. |
| Failed-command count | `5` | `agent/trajectory.json`: two SciPy failures, command-batching rejection, two matplotlib import failures. |
| Distinct error signatures | `3` | same trajectory: missing SciPy; multiple-command rejection; matplotlib `_c_internal_utils` ImportError. |
| Analysis iterations | `2` | trajectory first source has `q_toys >= q_obs`; final source has `q_toys <= q_obs`. |
| Final iteration | `2` | final `PYTHONPATH="" python3.12` execution produces exported results. |
| Superseded iterations | `1` | first tail convention/result replaced before final saved output. |
| Recovery count | `3` | E1 Python-3.12 route, E2 standalone command, E3 empty-PYTHONPATH run complete. |
| Tool categories | `shell; source editing; Python/scientific computation; plotting; file inspection; package/environment management` | trajectory commands/cells and exported source/plots. |
| Reproducibility attempt | `not established` | final rerun occurs, but no clean-output rerun or stated tolerance. |
| Artifact coverage | `6 / 6` | `artifacts/manifest.json`; run.sh, analysis.py, README, results JSON, two PNGs readable. |

### Error signatures and recoveries
| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `setup` | `ModuleNotFoundError: No module named scipy` | 2 | later Python 3.12 successful analysis execution in trajectory. | `recovered` |
| E2 | `setup` | `ERROR: Cannot execute multiple commands at once` | 1 | later standalone Python-3.12 probe in trajectory. | `recovered` |
| E3 | `validation` | `ImportError: matplotlib _c_internal_utils from partially initialized module` | 2 | later empty-PYTHONPATH execution and exported PNGs/results. | `recovered` |

### Iteration lineage
| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Tail `q_toys >= q_obs` | p-value/significance | executed then replaced; separate output unavailable. | `superseded` | `agent/trajectory.json` initial interactive source. |
| 2 | Tail corrected to `q_toys <= q_obs`; Python 3.12 with empty `PYTHONPATH` | p `0.000223`, Z `3.5112528289` | final results/diagnostics produced. | `final` | trajectory final source/execution; `artifacts/root/results/results.json`. |

### Stage timeline
| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `input_inspection` | `yes` | `yes` | none | `no` | `not established` | trajectory `ls -R /root/data`, `cat` input. |
| `setup` | `yes` | `yes` | E1, E2 | `yes` | `not established` | package/interpreter probes; final Python 3.12 choice. |
| `data_preparation` | `yes` | `yes` | none | `no` | `not established` | creates submission/diagnostics/results directories. |
| `inference_or_selection` | `yes` | `yes` | none | `yes` | `not established` | final `analysis.py:18-40` tail correction. |
| `fit` | `yes` | `yes` | none | `no` | `not established` | `analysis.py:43-70` profile minimization/crossings. |
| `plotting` | `yes` | `yes` | E3 | `yes` | `not established` | `analysis.py:84-104`; two final PNGs. |
| `validation` | `yes` | `yes` | E3 | `yes` | `not established` | repeated execution/output inspection, final rerun. |
| `reporting` | `yes` | `yes` | none | `no` | `not established` | creates wrapper/README; exports confirm them. |

### Validation checks
| Check | Outcome | Evidence location |
|---|---|---|
| SciPy availability | initial interpreter absent; final Python-3.12 route works | `agent/trajectory.json` errors and final command. |
| Matplotlib compatibility | two failures; empty-PYTHONPATH recovery | trajectory plus exported diagnostic PNGs. |
| Output presence | eight numerical result fields are finite | `artifacts/root/results/results.json:2-9`. |
| Tail convention | corrected from `>=` to required `<=` before final execution | trajectory source blocks; final `analysis.py:38-39`. |
| NaNs/infinities, duplicate IDs, invalid weights, empty categories, zero denominators, invalid model/fit states | `not established` | no explicit checks in searched source, results, logs, or trajectory. |
