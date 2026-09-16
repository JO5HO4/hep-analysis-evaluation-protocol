# Manual evidence review: ttH diphoton BDT categorization

Reviewed 2026-09-09. This is non-authoritative review evidence under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`; it is not an outcome grade.

Run: `tth-diphoton / openhands / gpt-5.6-sol / 20260905T044026Z-tth-diphoton-bd__cMU3hZC`.
Execution context: Harbor completed; verifier reward `0.000000`. `result.json` records wall time 164.707452 s (04:41:10.181143Z--04:43:54.888595Z) and agent execution 24.309630 s (04:41:42.520778Z--04:42:06.830408Z). It records `cost_usd: null`.

## Evidence audit

The readable artifact root was enumerated in full: `lock.json`, `trial.log`, `result.json`, `config.json`, `artifacts/manifest.json`, agent logs/trajectories/completion/session events, and verifier `reward.txt`, `score_report.json`, `ctrf.json`, and `test-stdout.txt`. It contains no submitted source tree, task-output tree, JSON/CSV/Parquet table, plot, workspace, or report. `artifacts/manifest.json` records failed capture of both `/root/submission/tth-diphoton-bdt` and `/root/results/tth-diphoton-bdt`; `verifier/score_report.json` directly reports absent submission API, preselection table, training metadata, input contract, and run manifest. Searches of all readable logs, trajectories, verifier output, and metadata for the criterion quantities/configuration found only task instructions, not executed results. `agent/openhands.txt:41-63` records a pre-action OpenHands `AssertionError: Only one choice is supported for now`.

`P` = pass, `F` = fail, `M` = missing. No scientific item is failed: the missing output establishes that no result was preserved, but does not directly contradict a physics quantity or method.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| OpenHands / gpt-5.6-sol | 1 | 0 | 37 | completed / 0.000000 |

## Total reward (raw, no averaging)

| Summary | OpenHands / gpt-5.6-sol |
|---|---:|
| Total reward | 1 / 38 |

## Overall equal-category reward

| Summary | OpenHands / gpt-5.6-sol |
|---|---:|
| Overall equal-category reward | 0.037037 |

Nine group fractions are `1/3, 0/4, 0/6, 0/5, 0/9, 0/3, 0/3, 0/4, 0/1`; their arithmetic mean is `1/27`.

## Per-question binary rewards

| Group | Criterion IDs | Reward |
|---|---|---:|
| I Execution and Documentation Meta | Q1, Q2, Q3 | 1, 0, 0 |
| II Object Definition and Hadronic Preselection | Q4, Q5, Q6, Q7 | 0, 0, 0, 0 |
| III BDT Model Training and Configuration | Q8, Q9, Q10, Q11, Q12, Q13 | 0, 0, 0, 0, 0, 0 |
| IV Categorization, Event Assignment, and Purity | Q14, Q15, Q16, Q17, Q18 | 0, 0, 0, 0, 0 |
| V Statistical Workspace, Background Modeling, and Sensitivity Fit | Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27 | 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| VI Inclusive Hadronic Baseline Comparison | Q28, Q29, Q30 | 0, 0, 0 |
| VII Plotting and Presentation Quality | Q31, Q32, Q33 | 0, 0, 0 |
| VIII Validation and Reproducibility | Q34, Q35, Q36, Q37 | 0, 0, 0, 0 |
| IX Fixed-Quantile Category Baseline Comparison | Q38 | 0 |

## Per-question observed values, evidence, and reasoning

| ID | Observed value [reward] | Status and exact evidence/reason |
|---|---|---|
| Q1 | `164.707452 s wall; 24.309630 s agent` [1] | **pass** — `result.json: started_at/finished_at` and `agent_execution.started_at/finished_at` are finite nonnegative intervals. |
| Q2 | `cost_usd = null` [0] | **missing** — `result.json: agent_result.cost_usd`; no USD total in metadata, logs, completion, or verifier output. Zero model token-price configuration is not a recorded total cost. |
| Q3 | `no readable narrative` [0] | **missing** — artifact inventory and `artifacts/manifest.json` show no results tree/report; `trial.log` is task instruction, not an agent narrative. |
| Q4 | `not established` [0] | **missing** — no object-definition record/source; verifier reports missing result tree. Instruction’s no-TI/no-isolation requirement is not execution evidence. |
| Q5 | `not established` [0] | **missing** — no preselection table/summary; `score_report.json: preselection_physics` reports missing preselected-events table. |
| Q6 | `not established` [0] | **missing** — no selected-event/source evidence; logs contain requested cuts only, not applied cuts. |
| Q7 | `not established` [0] | **missing** — no process-separated yield table or report after searched artifact inventory. |
| Q8 | `not established` [0] | **missing** — no training metadata/package record; verifier identifies missing `model/training_metadata.json`. |
| Q9 | `not established` [0] | **missing** — no saved API/source or final feature list; `BDT_FEATURES` appears only in task instruction. |
| Q10 | `not established` [0] | **missing** — no executed held-out AUC in logs, tables, metrics, or training metadata. |
| Q11 | `not established` [0] | **missing** — no executed class-definition evidence; only task-request text. |
| Q12 | `not established` [0] | **missing** — no SM weights, balancing sums, or training table. |
| Q13 | `not established` [0] | **missing** — no event-ID partition table, split record, or source implementation. |
| Q14 | `not established` [0] | **missing** — no category output/source; the required names occur only in the prompt. |
| Q15 | `not established` [0] | **missing** — no assignment trace or implementation showing BDT-first priority. |
| Q16 | `not established` [0] | **missing** — no threshold sequence, gains, or stopping result. |
| Q17 | `not established` [0] | **missing** — no retained-category yields or purity result. |
| Q18 | `not established` [0] | **missing** — no retained-category yields or purity result. |
| Q19 | `not established` [0] | **missing** — no workspace/Asimov artifact; captured results root is absent. |
| Q20 | `not established` [0] | **missing** — no statistical model/workspace configuration. |
| Q21 | `not established` [0] | **missing** — no candidate-function, selection-statistic, or chosen-PDF evidence. |
| Q22 | `not established` [0] | **missing** — no TI-sideband fit/extrapolation result. |
| Q23 | `not established` [0] | **missing** — no S+B Asimov artifact or `mu_gen` record. |
| Q24 | `not established` [0] | **missing** — no `mu_hat`, uncertainty, fit status, or covariance output. |
| Q25 | `not established` [0] | **missing** — no 123–127 GeV continuum yield/category scope. |
| Q26 | `not established` [0] | **missing** — no 123–127 GeV resonant yield/category scope. |
| Q27 | `not established` [0] | **missing** — no `q0` or `Z` output. |
| Q28 | `agent Z: not established; baseline: not comparable` [0] | **missing** — no agent fit/event table, hence no same-frozen-sample compatible comparison. |
| Q29 | `agent mu uncertainty: not established; baseline: not comparable` [0] | **missing** — no agent fit/event table, hence no compatible comparison. |
| Q30 | `Pareto comparison: not established` [0] | **missing** — Q28/Q29 quantities are absent; no valid baseline comparison. |
| Q31 | `not established` [0] | **missing** — no PNG/PDF/JSON plots or finite plotted bins in the complete inventory. |
| Q32 | `not established` [0] | **missing** — no histogram artifact states statistical normalization. |
| Q33 | `not established` [0] | **missing** — no performance plot or evaluated-partition record. |
| Q34 | `not established` [0] | **missing** — no score–mass diagnostic/sample/result. |
| Q35 | `not established` [0] | **missing** — no two configurations or common validation metrics. |
| Q36 | `not established` [0] | **missing** — no pre/post class-weight sums or balancing record. |
| Q37 | `not established` [0] | **missing** — no final features, hyperparameters, thresholds, seeds, versions, or input IDs. |
| Q38 | `agent Z: not established; quantile baseline: not comparable` [0] | **missing** — no continuous BDT scores, agent fit, or same-sample comparison record. |

All unavailable scientific items were searched in `trial.log`, `agent/openhands.txt`, `agent/trajectory.json`, `agent/openhands.trajectory.json`, agent completion/session-event records, `result.json`, `config.json`, `artifacts/manifest.json`, `verifier/test-stdout.txt`, and `verifier/score_report.json`. No preferred filename alone was used to assign a status.
