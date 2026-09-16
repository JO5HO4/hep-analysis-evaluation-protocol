# Top Reconstruction Evaluation Rubric

Each criterion follows the shared evaluation status, binary-reward, and flexible
evidence policy in [`evaluation_rubric.md`](evaluation_rubric.md). The report-level overall metric
is the shared equal-category reward: the arithmetic mean of category pass
fractions.

Workflow behavior is reported separately under the non-scoring
[workflow-characterization protocol](workflow-characterization.md); it does
not contribute to this rubric's reward.

## Baseline comparison protocol

Comparative criteria use
[`mass-greedy/v2-n-top-2`](top-reconstruction-baseline/README.md), the deterministic
mass-only selector defined in this repository. For each event it ranks
candidates by ascending `abs(m_jjj - 172.5 GeV)`,
breaks ties by the canonical sorted jet-index triplet, and greedily accepts
mutually jet-disjoint candidates until the rubric limit of two selections is
reached. It does not use the candidate classifier score, truth labels, or
learned quantities.

### Evaluator artifact inputs

| Input | Required fields | What the evaluator derives |
|---|---|---|
| Labeled evaluator candidate Parquet | `event_id`, `i`, `j`, `k`, `triplet_mass`, `is_truth` | Baseline selection; truth labels; candidate-level confusion matrix; mass statistics. |
| Agent selected-candidate Parquet | `event_id`, `i`, `j`, `k` | Selected/not-selected decisions, joined to the evaluator's labeled candidate table. |

All comparison metrics are calculated from those two inputs. The agent does not
need to emit a metric report or baseline result.

The evaluator canonicalizes a selected candidate as
`(event_id, sorted(i,j,k))`. Duplicate or unknown candidates, shared jets
within an event, and more than two selected candidates in an event invalidate
the agent selection for every baseline-comparison criterion.

The checked-in [development-sample reference results](top-reconstruction-baseline/baseline_results.json)
are reproducibility evidence, not a hidden-test score. The evaluator—not the
task-solving agent—reruns `mass-greedy/v2-n-top-2` on the same frozen, labeled
evaluation sample and compares its results with the agent's saved selection,
using the metric definitions in that report.

The current task artifact does not contain an agent-produced continuous score
for every candidate. ROC AUC is therefore not a valid evaluator-side comparison
for this task; `compare.py` records that limitation rather than fabricating an
AUC from binary selections.

## Group I: Execution and Meta

| Criterion | Desired answer | Scoring |
|---|---|---|
| 1. Run timing | Both trial wall-clock and pure agent execution time established | 1 if direct evidence establishes both times as finite nonnegative values with units; otherwise 0. |
| 2. Run cost | Total cost established in USD | 1 if direct evidence establishes one finite nonnegative USD total, including `$0.00`; otherwise 0. |

## Group II: BDT Setup and Features

| Criterion | Desired answer | Scoring |
|---|---|---|
| 3. BDT classification | Classifier trained and used, with package identified | 1 if direct execution evidence establishes that a BDT or classifier was trained and used for inference and identifies its package or library; otherwise 0. |
| 4. Final input features | At least two final input features identified | 1 if direct evidence identifies at least two final model input features; otherwise 0. |
| 5. Feature exploration | Additional feature set tested | 1 if direct evidence establishes that at least one training-feature set beyond the final set was tested; otherwise 0. |
| 6. Train/validation/test partition | Nonempty event-disjoint partitions | 1 if direct evidence establishes nonempty train, validation, and test event-ID sets that are pairwise disjoint; otherwise 0. |
| 7. ML setup exploration | At least two distinct ML setups tried | 1 if direct evidence identifies two ML setups and at least one difference in algorithm family, objective, learning formulation, or other named setup property; otherwise 0. |

---

## Group III: Candidate Selection

| Criterion | Desired answer | Scoring |
|---|---|---|
| 8. Final candidate-selection algorithm | Specific algorithm established | 1 if direct evidence establishes a specific algorithm used for final selection; otherwise 0. |
| 9. Selection exploration | At least two configurations compared on common validation data | 1 if direct evidence establishes at least two selection algorithms or score thresholds evaluated on the same validation partition, with reconstruction efficiency for each; otherwise 0. |
| 10. Candidate multiplicity constraint | `N_top <= 2` for every event | 1 if direct evidence establishes no event has more than two selected candidates; otherwise 0. |

---

## Group IV: Physics and Diagnostics

| Criterion | Desired answer | Scoring |
|---|---|---|
| 11. Score–mass correlation | Measured and reported | 1 if direct evidence gives the correlation method, evaluated sample, and finite score–mass correlation result; otherwise 0. |
| 12. Final model mass use | No triplet mass feature or hard mass window | 1 if direct evidence establishes that the final configuration used for selected candidates does not use `triplet_mass` or `m123` as an input feature and has no hard mass-window cut; otherwise 0. |
| 13. Pipeline optimization | At least two optimization attempts | 1 if direct evidence establishes two attempts differing in a named hyperparameter, feature list, training seed, or selection parameter, with a common validation metric; otherwise 0. |
| 14. BDT-score distribution | Quantity, normalization, and finite values established | 1 if direct evidence establishes the plotted score quantity, its unit or normalization, relevant class scope, and at least one finite nonempty bin or plotted value; otherwise 0. |
| 15. Reconstructed-mass comparison | Quantity, normalization, and finite values established | 1 if direct evidence establishes a reconstructed-mass comparison, its unit or normalization, compared scopes, and at least one finite nonempty bin or plotted value; otherwise 0. |

---

## Group V: Reconstruction Performance and Jet Disjointness

| Criterion | Desired answer | Scoring |
|---|---|---|
| 16. Jet disjointness | Zero overlapping selected triplets | 1 if direct evidence establishes that no pair of selected candidates in an event shares a jet; otherwise 0. |


## Group VI: Baseline Comparison and Physics Quality

| Criterion | Desired answer | Scoring |
|---|---|---|
| 17. Selected-mass bias vs. baseline | No worse than baseline | 1 if agent bias is less than or equal to baseline bias on the same labeled evaluation sample, where bias is `abs(median triplet_mass of selected truth candidates - 172.5 GeV)`; otherwise 0. |
| 18. Selected truth-matched mass resolution vs. baseline | Strictly better than baseline | 1 if agent resolution is strictly less than baseline resolution on the same labeled evaluation sample, where resolution is the population standard deviation of `triplet_mass` across selected truth candidates; otherwise 0. |
| 19. Reconstruction efficiency vs. baseline | At least baseline | 1 if agent efficiency is greater than or equal to baseline efficiency on the same labeled evaluation sample, where efficiency is `true selected candidates / all truth candidates`; otherwise 0. |
| 20. Selected-candidate purity vs. baseline | At least baseline | 1 if agent purity is greater than or equal to baseline purity on the same labeled evaluation sample; otherwise 0. |
| 21. Fake-to-true ratio vs. baseline | No greater than baseline | 1 if agent fake-to-true ratio is less than or equal to baseline fake-to-true ratio on the same labeled evaluation sample; otherwise 0. |
| 22. Selected-candidate F1 vs. baseline | At least baseline | 1 if agent F1 is greater than or equal to baseline F1 on the same labeled evaluation sample, where `F1 = 2 * purity * efficiency / (purity + efficiency)`; otherwise 0. |
| 23. Candidate-level selection accuracy vs. baseline | At least baseline | 1 if agent accuracy is greater than or equal to baseline accuracy on the same labeled evaluation sample, where accuracy is `(true positives + true negatives) / all candidates` and selection is the positive decision; otherwise 0. |
| 24. Balanced selection accuracy vs. baseline | At least baseline | 1 if agent balanced selection accuracy is greater than or equal to baseline balanced selection accuracy on the same labeled evaluation sample, where it is `(reconstruction efficiency + specificity) / 2` and specificity is `true non-selected fakes / all fake candidates`; otherwise 0. |
| 25. Baseline Pareto improvement | Efficiency no lower and fake-to-true ratio no higher | 1 if agent efficiency is greater than or equal to baseline efficiency and agent fake-to-true ratio is less than or equal to baseline fake-to-true ratio, with at least one strict inequality; otherwise 0. |

## Group VII: Plotting and Presentation Quality

| Criterion | Desired answer | Scoring |
|---|---|---|
| 26. Plot quantity and labeling | Quantity, unit, and finite values established | 1 if direct evidence establishes the plotted quantity, physical unit where applicable, and at least one finite nonempty bin or plotted value for every required plot; otherwise 0. |
| 27. Histogram normalization | Statistical unit established | 1 if direct evidence identifies every histogram as event count, candidate count, normalized density, or fraction of events; otherwise 0. |
| 28. Performance-plot partition | Evaluated partition established | 1 if direct evidence identifies the evaluated partition for every performance plot; otherwise 0. |

## Group VIII: Methodology

| Criterion | Desired answer | Scoring |
|---|---|---|
| 29. Candidate-class imbalance | Ratio and declared treatment established | 1 if direct evidence gives the correct-to-incorrect candidate ratio and declares one of class weights, resampling, ranking objective, or `none`; otherwise 0. |
| 30. Final configuration | Required reproducibility fields established | 1 if direct evidence gives feature list, hyperparameters, threshold/selection rule, split seed, model seed, package versions, and input file identifiers; otherwise 0. |

## Group IX: Frozen Classifier Baseline Comparison

The evaluator-side `gaussian-naive-bayes-mass-blind/v1` classifier uses only
the six listed angular and mass-ratio features, excludes triplet mass, and
uses the fixed event-ID modulo-10 partition. It is evaluator-owned development
evidence, not an authoritative outcome grader.

| Criterion | Desired answer | Scoring |
|---|---|---|
| 31. Held-out AUC vs. frozen classifier baseline | At least the baseline AUC | 1 if the agent's finite ROC AUC is greater than or equal to `gaussian-naive-bayes-mass-blind/v1` on the same frozen evaluator test partition, using one score per candidate; otherwise 0. |
