# Manual top-reconstruction rubric evaluation

This is a manual, evidence-backed review of the 15 copied Harbor run bundles in
`results/top-reconstruction-paper-version`. It is **not** an indexed outcome
grade: this task has no `evaluation/index.json`.

Each completed pipeline was reviewed through its `result.json`, `trial.log`,
verifier files, artifact manifest, reports, Parquet schemas, selected-triplet
Parquet, and available plots. Harbor verifier reward is reported separately
and is never used as a rubric answer.

## Scope and unresolved rubric inputs

- `TEST_AUC_THRESHOLD`, `OVERALL_EFFICIENCY_THRESHOLD`, and
  `TWO_CANDIDATE_EFFICIENCY_THRESHOLD` are `null`. Q12, Q18, and Q19 are
  therefore `ambiguous` and receive 0; this is not a statement that the
  measured values are bad.
- Q35 requires a predefined overfitting tolerance, which is absent. It is
  also `ambiguous` and receives 0 even when train/validation AUC are available.
- The documented `mass-greedy/v1` selector accepts up to four candidates while
  the task caps agent selections at two. Its results below are faithful to the
  documented selector, but this mismatch should be reconciled before using the
  comparison as a future authoritative measurement.
- Five completed runs discarded `triplet_mass` from both the saved test
  candidate table and raw candidate artifact. Their Q21--Q29 status is
  `artifact_missing`; no baseline value was invented.

Status shorthand in the tables is `P/F/N/M/A/E` for
`pass/fail/not_evaluated/artifact_missing/ambiguous/evaluator_error`.

## 1. Status summary

### Best cohort

| Status | Codex / gpt-5.6-sol | Claude Code / claude-opus-5 | Terminus-2 / gpt-5.6-sol | Qwen Coder / google/qwen-3 | OpenHands / gpt-5.6-sol |
|---|---:|---:|---:|---:|---:|
| P | 24 | 1 | 23 | 14 | 1 |
| F | 3 | 0 | 3 | 1 | 0 |
| N | 2 | 0 | 3 | 7 | 0 |
| M | 2 | 30 | 2 | 9 | 30 |
| A | 4 | 4 | 4 | 4 | 4 |
| E | 0 | 0 | 0 | 0 | 0 |
| Harbor status / verifier reward | completed / 0.916667 | agent API failure / 0.000000 | completed / 0.916667 | completed / 0.350805 | completed without pipeline artifacts / 0.000000 |

### Medium cohort

| Status | Codex / gpt-5.6-terra | Claude Code / claude-sonnet-5 | Terminus-2 / gpt-5.6-terra | Qwen Coder / google/qwen-3 | OpenHands / gpt-5.6-terra |
|---|---:|---:|---:|---:|---:|
| P | 25 | 26 | 23 | 15 | 1 |
| F | 2 | 2 | 3 | 1 | 0 |
| N | 2 | 2 | 3 | 7 | 0 |
| M | 2 | 1 | 2 | 9 | 30 |
| A | 4 | 4 | 4 | 4 | 4 |
| E | 0 | 0 | 0 | 0 | 0 |
| Harbor status / verifier reward | completed / 0.916667 | completed / 0.833333 | completed / 0.916667 | completed / 0.833333 | completed without pipeline artifacts / 0.000000 |

### Free cohort

| Status | Codex / lbl/cborg-coder | Claude Code / lbl/cborg-coder | Terminus-2 / openai/lbl/cborg-coder | Qwen Coder / lbl/cborg-coder | OpenHands / openai/lbl/cborg-coder |
|---|---:|---:|---:|---:|---:|
| P | 23 | 21 | 12 | 16 | 12 |
| F | 2 | 3 | 2 | 1 | 1 |
| N | 2 | 2 | 4 | 4 | 4 |
| M | 3 | 1 | 9 | 9 | 9 |
| A | 4 | 4 | 4 | 4 | 4 |
| E | 0 | 0 | 0 | 0 | 0 |
| Harbor status / verifier reward | completed / 0.896937 | completed / 0.916667 | completed / 0.346174 | completed / 0.166667 | completed / 0.083333 |

## 2. Total reward (raw, no averaging)

| Cohort | Codex | Claude Code | Terminus-2 | Qwen Coder | OpenHands |
|---|---:|---:|---:|---:|---:|
| Best | 24 / 35 | 1 / 35 | 23 / 35 | 14 / 35 | 1 / 35 |
| Medium | 25 / 35 | 26 / 35 | 23 / 35 | 15 / 35 | 1 / 35 |
| Free | 23 / 35 | 21 / 35 | 12 / 35 | 16 / 35 | 12 / 35 |

## 3. Overall equal-category reward

This is the arithmetic mean of the eight category pass fractions, so a
three-question category has the same weight as a nine-question category.

| Cohort | Codex | Claude Code | Terminus-2 | Qwen Coder | OpenHands |
|---|---:|---:|---:|---:|---:|
| Best | 0.676 | 0.063 | 0.635 | 0.450 | 0.063 |
| Medium | 0.690 | 0.739 | 0.635 | 0.492 | 0.063 |
| Free | 0.586 | 0.572 | 0.387 | 0.496 | 0.387 |

## 4. Per-question binary rewards

`1` is pass; `0` includes every non-passing status above. The three tables
retain a stable agent order while keeping the report readable.

### Best

| Q | Codex / sol | Claude / opus | Terminus / sol | Qwen / qwen-3 | OpenHands / sol |
|---|---:|---:|---:|---:|---:|
| 1--2 | 1, 1 | 1, 0 | 1, 1 | 1, 0 | 1, 0 |
| 3--7 | 1, 1, 1, 1, 0 | 0, 0, 0, 0, 0 | 1, 1, 1, 1, 0 | 1, 1, 0, 1, 0 | 0, 0, 0, 0, 0 |
| 8--11 | 1, 1, 1, 1 | 0, 0, 0, 0 | 1, 1, 1, 1 | 1, 0, 0, 1 | 0, 0, 0, 0 |
| 12--17 | 0, 1, 0, 1, 0, 1 | 0, 0, 0, 0, 0, 0 | 0, 1, 0, 1, 0, 1 | 0, 1, 1, 0, 1, 1 | 0, 0, 0, 0, 0, 0 |
| 18--20 | 0, 0, 1 | 0, 0, 0 | 0, 0, 1 | 0, 0, 1 | 0, 0, 0 |
| 21--29 | 0, 0, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0, 0, 0, 0, 0 | 0, 0, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| 30--32 | 0, 1, 0 | 0, 0, 0 | 0, 1, 0 | 1, 1, 0 | 0, 0, 0 |
| 33--35 | 1, 1, 0 | 0, 0, 0 | 0, 1, 0 | 0, 1, 0 | 0, 0, 0 |

### Medium

| Q | Codex / terra | Claude / sonnet | Terminus / terra | Qwen / qwen-3 | OpenHands / terra |
|---|---:|---:|---:|---:|---:|
| 1--2 | 1, 1 | 1, 1 | 1, 1 | 1, 0 | 1, 0 |
| 3--7 | 1, 1, 1, 1, 0 | 1, 1, 1, 1, 0 | 1, 1, 1, 1, 0 | 1, 1, 0, 1, 0 | 0, 0, 0, 0, 0 |
| 8--11 | 1, 1, 1, 1 | 1, 1, 1, 1 | 1, 1, 1, 1 | 1, 0, 0, 1 | 0, 0, 0, 0 |
| 12--17 | 0, 1, 0, 1, 0, 1 | 0, 1, 0, 1, 1, 1 | 0, 1, 0, 1, 0, 1 | 0, 1, 1, 0, 1, 1 | 0, 0, 0, 0, 0, 0 |
| 18--20 | 0, 0, 1 | 0, 0, 1 | 0, 0, 1 | 0, 0, 1 | 0, 0, 0 |
| 21--29 | 0, 1, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| 30--32 | 0, 1, 0 | 1, 1, 0 | 0, 1, 0 | 1, 1, 0 | 0, 0, 0 |
| 33--35 | 1, 1, 0 | 1, 1, 0 | 0, 1, 0 | 1, 1, 0 | 0, 0, 0 |

### Free

| Q | Codex / cborg | Claude / cborg | Terminus / cborg | Qwen / cborg | OpenHands / cborg |
|---|---:|---:|---:|---:|---:|
| 1--2 | 1, 0 | 1, 1 | 1, 0 | 1, 0 | 1, 0 |
| 3--7 | 1, 1, 1, 1, 0 | 1, 1, 1, 1, 0 | 1, 1, 0, 1, 0 | 1, 1, 1, 1, 0 | 1, 1, 0, 1, 0 |
| 8--11 | 1, 1, 1, 1 | 1, 0, 0, 1 | 1, 0, 0, 1 | 1, 1, 1, 1 | 1, 0, 0, 1 |
| 12--17 | 0, 1, 0, 1, 0, 1 | 0, 1, 0, 1, 0, 1 | 0, 1, 1, 0, 0, 1 | 0, 1, 1, 1, 0, 1 | 0, 1, 1, 0, 0, 1 |
| 18--20 | 0, 0, 1 | 0, 0, 1 | 0, 0, 1 | 0, 0, 1 | 0, 0, 1 |
| 21--29 | 0, 1, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 1, 1, 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| 30--32 | 0, 1, 0 | 0, 1, 0 | 0, 1, 0 | 0, 1, 0 | 0, 1, 0 |
| 33--35 | 1, 0, 0 | 1, 0, 0 | 1, 0, 0 | 1, 0, 0 | 1, 0, 0 |

## 5. Observed values and rewards

### Execution, final reconstruction, and direct Parquet constraints

| Run | Wall / agent time | Cost | Test efficiency | Selected rows; max/event; overlap pairs |
|---|---|---:|---:|---|
| Codex / sol | 571.98 s / 422.69 s [1] | $0.809560 [1] | 470 / 643 = 0.730949 [Q18 A] | 1,650; 2; 0 [Q11,Q20 1] |
| Claude / sonnet | 827.61 s / 674.66 s [1] | $4.071828 [1] | 527 / 689 = 0.764877 [Q18 A] | 1,410; 2; 0 [1,1] |
| Claude / cborg | 748.39 s / 637.58 s [1] | $2.395707 [1] | 0.633262 [Q18 A] | 2,222; 2; 0 [1,1] |
| Codex / terra | 719.29 s / 578.88 s [1] | $0.598514 [1] | 245 / 338 = 0.724852 [Q18 A] | 847; 2; 0 [1,1] |
| Codex / cborg | 1,717.95 s / 1,606.48 s [1] | missing [0] | 0.613611 [Q18 A] | 2,202; 2; 0 [1,1] |
| Terminus / sol | 560.68 s / 389.35 s [1] | $0.589839 [1] | 476 / 685 = 0.694891 [Q18 A] | 1,649; 2; 0 [1,1] |
| Terminus / terra | 574.86 s / 372.61 s [1] | $0.280413 [1] | 623 / 887 = 0.702368 [Q18 A] | 2,194; 2; 0 [1,1] |
| Terminus / cborg | 406.51 s / 279.67 s [1] | missing [0] | 0.454158 [Q18 A] | 2,222; 2; 0 [1,1] |
| Qwen / Best | 882.99 s / 683.19 s [1] | missing [0] | 435 / 938 = 0.463753 [Q18 A] | 2,222; 2; 0 [1,1] |
| Qwen / Medium | 532.27 s / 362.80 s [1] | missing [0] | 627 / 900 = 0.696667 [Q18 A] | 6,865; 2; 0 [1,1] |
| Qwen / cborg | 602.12 s / 485.05 s [1] | missing [0] | 0.411636 [Q18 A] | 1,633; 2; 0 [1,1] |
| OpenHands / cborg | 1,110.27 s / 991.75 s [1] | missing [0] | 331 / 938 = 0.352878 [Q18 A] | 1,177; 2; 0 [1,1] |

`A` after Q18 means the value is measured but the reward is 0 because its
threshold is absent. Q19 is likewise ambiguous for every run.

### Baseline-comparison values (Q21--Q29)

The comparator ran on each run's labeled saved test candidates and selected
triplets. Claude Free's `m123` was normalized to the documented semantic field
`triplet_mass` before comparison. A dash means no recoverable labeled mass
candidate table, hence Q21--Q29 are `artifact_missing`.

| Run | Bias GeV (agent / base) Q21 | Resolution GeV (agent / base) Q22 | Efficiency (agent / base) Q23 | Purity (agent / base) Q24 | Fake/true (agent / base) Q25 | F1 (agent / base) Q26 | Accuracy (agent / base) Q27 | Balanced accuracy (agent / base) Q28 | Pareto Q29 |
|---|---|---|---|---|---|---|---|---|---|
| Claude / sonnet | 7.576 / 2.050 [0] | 26.713 / 24.369 [0] | .7649 / .4064 (+88.2%) [1] | .3738 / .1667 (+124.3%) [1] | 1.676 / 5.000 (+66.5%) [1] | .5021 / .2364 (+112.4%) [1] | .9344 / .8864 (+5.4%) [1] | .8535 / .6573 (+29.9%) [1] | true [1] |
| Claude / cborg | 6.951 / 2.748 [0] | 19.673 / 17.891 [0] | .6333 / .4254 (+48.9%) [1] | .2673 / .1781 (+50.1%) [1] | 2.741 / 4.614 (+40.6%) [1] | .3759 / .2511 (+49.7%) [1] | .9075 / .8884 (+2.2%) [1] | .7767 / .6675 (+16.4%) [1] | true [1] |
| Codex / sol | 6.128 / 2.073 [0] | 20.070 / 19.743 [0] | .7309 / .4199 (+74.1%) [1] | .2848 / .1623 (+75.6%) [1] | 2.511 / 5.163 (+51.4%) [1] | .4099 / .2341 (+75.1%) [1] | .9124 / .8856 (+3.0%) [1] | .8256 / .6629 (+24.6%) [1] | true [1] |
| Codex / terra | 6.507 / 1.375 [0] | 24.416 / 26.289 (+7.1%) [1] | .7249 / .3905 (+85.6%) [1] | .2893 / .1538 (+88.0%) [1] | 2.457 / 5.500 (+55.3%) [1] | .4135 / .2207 (+87.3%) [1] | .9189 / .8913 (+3.1%) [1] | .8259 / .6512 (+26.8%) [1] | true [1] |
| Codex / cborg | 6.645 / 3.734 [0] | 21.521 / 21.800 (+1.3%) [1] | .6136 / .4193 (+46.3%) [1] | .2539 / .1717 (+47.9%) [1] | 2.939 / 4.825 (+39.1%) [1] | .3591 / .2436 (+47.4%) [1] | .9091 / .8919 (+1.9%) [1] | .7678 / .6659 (+15.3%) [1] | true [1] |
| Terminus / sol | 8.542 / 3.584 [0] | 20.510 / 18.166 [0] | .6949 / .4088 (+70.0%) [1] | .2887 / .1681 (+71.8%) [1] | 2.464 / 4.950 (+50.2%) [1] | .4079 / .2382 (+71.2%) [1] | .9143 / .8890 (+2.9%) [1] | .8095 / .6595 (+22.7%) [1] | true [1] |
| Terminus / terra | 7.271 / 3.118 [0] | 22.406 / 22.057 [0] | .7024 / .4228 (+66.1%) [1] | .2840 / .1693 (+67.7%) [1] | 2.522 / 4.907 (+48.6%) [1] | .4044 / .2418 (+67.3%) [1] | .9139 / .8896 (+2.7%) [1] | .8127 / .6663 (+22.0%) [1] | true [1] |
| Qwen Best/Medium/cborg; OpenHands cborg; Terminus cborg | -- [M] | -- [M] | -- [M] | -- [M] | -- [M] | -- [M] | -- [M] | -- [M] | -- [M] |

## 6. Evidence and reasoning

| Questions | Evidence reviewed | Manual finding |
|---|---|---|
| Q1--2 | Every run's `result.json`: `started_at`, `finished_at`, `agent_execution.*`, and `agent_result.cost_usd`. | All 15 have wall and execution timestamps. Six completed runs recorded USD cost; the other nine have `cost_usd: null`. |
| Q3--7, Q15, Q33--35 | `artifacts/root/results/train/training_report_xgb.json`, `optimization_report.md`, model reports, and `trial.log`. | Completed pipelines trained XGBoost with at least two features and event-level splitting. Only documented alternatives/configuration scans receive Q5/Q9/Q10/Q15 credit. No run gave sufficiently documented non-XGBoost comparison for Q7. |
| Q8--11, Q20 | `select_triplets/selection_report.json`, `event_selection.parquet`, and direct read of each `selected_triplets.parquet`. | Direct Parquet computation found `max_selected_per_event = 2` and `overlapping_selected_pairs = 0` for all 12 successful runs. |
| Q12, Q18, Q19, Q35 | Rubric threshold block plus training, inference, and selection reports. | Measured AUC/efficiency and train-vs-validation values cannot satisfy a criterion with a null threshold/tolerance. |
| Q13--17, Q30--32 | `sanity_checks/*`, `select_triplets/plots/*`, saved PNGs, and optimization reports. | Mass sanity checks are present in completed runs. BDT-score plots were confirmed for Claude Sonnet and Qwen Best/Medium; absent score plots receive Q16/Q30 zero. Plot-normalization labels were readable where histogram artifacts existed. No completed run provided sufficient train/validation/test distinction across every performance plot for Q32. |
| Q21--29 | `evaluation/top-reconstruction-baseline/compare.py`, saved test candidate/selection Parquet, and direct schema audit. | The seven numeric rows above are computed evaluator-side values. The other five lack a recoverable candidate `triplet_mass`; their comparison reward is zero because the evidence is missing, not because their performance is assumed worse. |

### Exact artifact roots

For a run shown above, artifact references are under:

`results/top-reconstruction-paper-version/<agent>/<model>/<trial>/artifacts/root/results/`

The concrete files used are `dataset_prepare/test.parquet`,
`dataset_build/triplets_raw.parquet`, `infer/inference_test_xgb.parquet`,
`train/training_report_xgb.json`, `select_triplets/selected_triplets.parquet`,
`select_triplets/selection_report.json`, `optimization_report.md`, and the
plot/sanity subdirectories. The bundle-level `result.json`, `trial.log`, and
`verifier/score_report.json` were reviewed alongside them.
