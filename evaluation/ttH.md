# ttH Diphoton BDT Categorization Evaluation Rubric

Each criterion follows the shared evaluation status, binary-reward, and flexible evidence policy in [evaluation_rubric.md](evaluation_rubric.md). `Scoring` is the rule that determines a reward of 1 or 0; the first column is a short criterion label, and `Desired answer` states the condition required for a pass.

This is a natural-language evaluation protocol, not an indexed versioned evaluation specification. It may structure review evidence and a report-level reward under the shared policy, but cannot by itself produce an authoritative outcome grade.

Workflow behavior is reported separately under the non-scoring
[workflow-characterization protocol](workflow-characterization.md); it does
not contribute to this rubric's reward.

## Group I: Execution and Documentation Meta

| Criterion | Desired answer | Scoring |
|---|---|---|
| 1. Run timing | Both trial wall-clock and pure agent execution time established | 1 if direct evidence establishes both times as finite nonnegative values with units; otherwise 0. |
| 2. Run cost | Total cost established in USD | 1 if direct evidence establishes one finite nonnegative USD total, including `$0.00`; otherwise 0. |
| 3. Human-facing documentation | Analysis narrative covers required topics | 1 if a readable narrative covers the task-required report topics; otherwise 0. |

## Group II: Object Definition and Hadronic Preselection

| Criterion | Desired answer | Scoring |
|---|---|---|
| 4. Photon identification and isolation policy | No tight-ID or isolation requirement at preselection | 1 if saved object-definition evidence documents that preselection does not require tight photon identification or isolation, preserving both TI and NTI events; otherwise 0. |
| 5. Hadronic-channel event count | Raw count and 36 fb^-1 weighted yield | 1 if direct evidence gives the raw count and 36 fb^-1 weighted yield after hadronic preselection, with their process scope; otherwise 0. |
| 6. Hadronic preselection | Exact required object and event selection | 1 if direct evidence establishes photon kinematic acceptance without tight ID/isolation; lepton `pT > 10 GeV`; jet `pT > 25 GeV`; zero selected leptons; at least three selected jets; at least one selected b-jet; and the b-tag predicate; otherwise 0. |
| 7. Post-preselection Higgs yields | Process-separated yields | 1 if direct evidence gives raw counts and 36 fb^-1 weighted yields after hadronic preselection, separated by Higgs process; otherwise 0. |

## Group III: BDT Model Training and Configuration

| Criterion | Desired answer | Scoring |
|---|---|---|
| 8. BDT training package | Package and version identified | 1 if direct evidence identifies the BDT package/library and version; otherwise 0. |
| 9. BDT input features | Exact five required features used | 1 if direct evidence gives a final feature list exactly equal to `BDT_FEATURES` and excludes `m_gammagamma`; otherwise 0. |
| 10. Signal-background AUC | Held-out AUC established | 1 if direct execution evidence gives a finite AUC in `[0, 1]` on the test partition; otherwise 0. |
| 11. Training classes | `ttH+tH` signal and `ggH+NTI` background | 1 if direct evidence establishes those exact signal and background classes; otherwise 0. |
| 12. Training class weights | Physical weighting before balancing | 1 if direct evidence establishes SM-normalized weighting before class balancing and records both classes before and after balancing; otherwise 0. |
| 13. Train/validation/test partition | Nonempty, event-disjoint stable-ID partitions | 1 if direct evidence establishes nonempty train, validation, and test event-ID sets that are pairwise disjoint and assigned without row order; otherwise 0. |

## Group IV: Categorization, Event Assignment, and Purity

| Criterion | Desired answer | Scoring |
|---|---|---|
| 14. BDT category count | Required categories established | 1 if direct evidence establishes the six named hadronic categories and `unassigned`; otherwise 0. |
| 15. BDT event categorization | Required priority assignment used | 1 if direct evidence establishes that BDT categories are assigned before the two cut-based tH categories, which are evaluated only after BDT-category failure; otherwise 0. |
| 16. Categorization figure of merit | Iterative 5% expected-significance rule used | 1 if direct evidence gives category thresholds and accepted relative gains, with every accepted split at least 5% and the stopping rule below 5%; otherwise 0. |
| 17. Highest-score ttH purity | Finite purity for highest retained BDT category | 1 if direct evidence gives finite ttH yield and strictly positive all-Higgs yield for the retained BDT category with the highest lower score boundary, and reports their ratio; otherwise 0. |
| 18. Second-highest-score ttH purity | Finite purity for second-highest retained BDT category | 1 if direct evidence gives finite ttH yield and strictly positive all-Higgs yield for the retained BDT category with the second-highest lower score boundary, and reports their ratio; otherwise 0. |

## Group V: Statistical Workspace, Background Modeling, and Sensitivity Fit

| Criterion | Desired answer | Scoring |
|---|---|---|
| 19. Fit-based sensitivity assessment | RooFit workspace and Asimov fit established | 1 if direct execution evidence establishes a RooFit workspace and an Asimov fit; otherwise 0. |
| 20. Statistical signal definition | Required combined statistical model | 1 if direct evidence establishes a shared-`mu` `ttH+tH` signal, fixed non-top-Higgs resonant background, and floating continuum in every hadronic category; otherwise 0. |
| 21. Analytical fit-function choice | Candidate functions and selection statistic established | 1 if direct evidence names the candidate functions, selection statistic, selected function, and category scope; otherwise 0. |
| 22. Background PDF determination | TI-sideband procedure established | 1 if direct evidence establishes a TI-data-sideband fit over 105–120 and 130–160 GeV, extrapolated over the 105–160 GeV fit range; otherwise 0. |
| 23. S+B Asimov data set | `mu_gen = 1` Asimov data established | 1 if direct execution evidence establishes signal-plus-background Asimov construction with `mu_gen = 1`; otherwise 0. |
| 24. S+B Asimov fit result | Valid unbiased fit with non-negligible uncertainty | 1 if direct execution evidence gives finite `mu_hat` with `abs(mu_hat - 1) <= 0.01`, finite `mu_uncertainty >= 0.01`, and successful fit and covariance statuses; otherwise 0. |
| 25. Continuum background yield, 123–127 GeV | 36 fb^-1 yield with stated category scope | 1 if direct evidence gives a finite continuum yield in 123–127 GeV at 36 fb^-1 and identifies the hadronic categories included; otherwise 0. |
| 26. Resonant background yield, 123–127 GeV | 36 fb^-1 yield with stated category scope | 1 if direct evidence gives a finite resonant-background yield in 123–127 GeV at 36 fb^-1 and identifies the hadronic categories included; otherwise 0. |
| 27. Expected significance | One-sided Asimov discovery significance | 1 if direct execution evidence gives finite `q0 >= 0` and finite expected `Z >= 0` from the one-sided `mu = 0` likelihood-ratio test, with `abs(Z^2-q0) <= 1e-6 * max(1, q0)`; otherwise 0. |

## Group VI: Inclusive Hadronic Baseline Comparison

Comparative criteria use [`inclusive-hadronic-constant-sideband/v1`](ttH-baseline/README.md), the evaluator-side baseline that assigns every hadronic-preselection event to one category and uses no BDT score or agent category. The evaluator reruns it on the same frozen event sample used for the agent comparison. A comparison is `missing`, rather than failed, if the agent fit and baseline do not use compatible signal definitions, fit range, sideband treatment, and 36 fb^-1 normalization.

| Criterion | Desired answer | Scoring |
|---|---|---|
| 28. Expected-significance comparison | Expected `Z` at least as high as baseline | 1 if the agent expected `Z` is greater than or equal to the baseline expected `Z` on the same frozen evaluator sample and compatible fit assumptions; otherwise 0. `q0` is retained as supporting evidence, not separately scored, because `Z = sqrt(q0)` for the one-sided Asimov discovery convention. |
| 29. Signal-strength precision comparison | `mu_uncertainty` no greater than baseline | 1 if the agent's finite positive `mu_uncertainty` is less than or equal to the baseline value on the same frozen evaluator sample and compatible fit assumptions; otherwise 0. |
| 30. Baseline Pareto improvement | At least one strict sensitivity or precision improvement with no regression | 1 if expected `Z` is no lower than baseline, `mu_uncertainty` is no greater than baseline, and at least one inequality is strict; otherwise 0. |

## Group VII: Plotting and Presentation Quality

| Criterion | Desired answer | Scoring |
|---|---|---|
| 31. Plot quantity and labeling | Quantity, unit, and finite values established | 1 if direct evidence establishes the plotted quantity, physical unit where applicable, and at least one finite nonempty bin or plotted value for every task-required plot; otherwise 0. |
| 32. Histogram normalization | Statistical unit established | 1 if direct evidence identifies every required histogram as event count, candidate count, normalized density, or fraction of events; otherwise 0. |
| 33. Performance-plot partition | Evaluated partition established | 1 if direct evidence identifies the evaluated partition for every required performance plot; otherwise 0. |

## Group VIII: Validation and Reproducibility

| Criterion | Desired answer | Scoring |
|---|---|---|
| 34. Score–mass correlation | BDT score versus `m_gammagamma` measured | 1 if direct evidence gives the correlation or mass-sculpting diagnostic method, evaluated sample, and finite result for BDT score versus `m_gammagamma`; otherwise 0. |
| 35. Optimization attempts | At least two attempts evaluated on common validation data | 1 if direct evidence establishes at least two model, feature, or categorization attempts differing in a named property and reports a common validation metric for each; otherwise 0. |
| 36. Class-imbalance accounting | Pre- and post-balancing class-weight ratios established | 1 if direct evidence gives finite signal-to-background class-weight ratios before and after balancing and identifies the balancing treatment; otherwise 0. |
| 37. Final configuration reproducibility | Required final configuration fields established | 1 if direct evidence gives final feature list, hyperparameters, category thresholds, split seed, model seed, package versions, and input identifiers; otherwise 0. |

## Group IX: Fixed-Quantile Category Baseline Comparison

The evaluator-side `fixed-score-quantiles-4/v1` baseline holds the supplied
continuous BDT score fixed, divides it into four empirical score quantiles, and
uses the same per-category constant-sideband Asimov fit. It isolates the value
of agent category-boundary optimization; it is development evidence, not an
authoritative outcome grader.

| Criterion | Desired answer | Scoring |
|---|---|---|
| 38. Expected significance vs. fixed quantile categories | Expected `Z` at least as high as baseline | 1 if the agent's expected `Z` is greater than or equal to `fixed-score-quantiles-4/v1` on the same frozen evaluator event table and continuous BDT scores, with identical mass range, signal definition, and continuum treatment; otherwise 0. |
