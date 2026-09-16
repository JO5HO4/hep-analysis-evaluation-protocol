# Non-Invasive Evaluation Prompt for Top Reconstruction Full Chain (No Pipeline) Task

This file contains the complete, standardized 60-question non-invasive evaluation prompt used to evaluate agent benchmark runs on the `top-reconstruction-full-chain-no-pipeline` task.

```markdown
You are tasked with performing a non-invasive evaluation of agent benchmark runs for the `top-reconstruction-full-chain-no-pipeline` task.

### Core Evaluation Directives & Constraints:
1. **Strict Non-Invasiveness**:
   - You must NOT modify, alter, or write to any files, artifacts, or workspaces in the task job folders or existing result displays.
   - All scratch scripts, temporary files, and evaluation outputs must be created exclusively within your own local working workspace.

2. **Data Source Scope**:
   - Inspect raw job results ONLY under:
     `/Users/haichenwang/.local/state/terminal-bench-collider/harbor-jobs/`
   - Do NOT use second-hand public summaries or viewer outputs.

3. **LLM Probing & Deterministic Output Strategy**:
   - Different agents use varying file structures, variable naming conventions, and JSON formats. Use LLM-based probing to inspect raw python code (`/root/submission/...`) and output JSON records (`/root/results/...`).
   - Derive deterministic outcomes (exact numbers, booleans, or explicit "N/A" for errored runs) for each question based strictly on empirical evidence in the raw files.

4. **Required Audit Response Format**:
   - For every question, report `Status: PASS | PARTIAL | FAIL | UNAVAILABLE`, followed by `Answer`, `Evidence`, `Independent verification`, and `Impact if wrong`.
   - `PASS` requires evidence that fully addresses the question; `PARTIAL` requires an explicit statement of the unresolved portion. Never replace unavailable evidence with a plausible narrative.

---

### The 20 Probing Questions (Grouped by Category):

#### Group I: Execution & Meta
1. How long did the agent take to complete the run? (Report both trial wall-clock time and pure agent execution time).
2. What is the cost of the agent run in USD?

#### Group II: BDT Setup & Features
3. Did the agent perform BDT classification for top decay triplet candidates?
4. How many BDT features were engineered and used in the model?
5. Did the agent optimize or select a refined feature list?
6. Did the agent implement a proper Train / Validation / Test dataset partition?
7. Did the agent explore or compare machine learning algorithms beyond standard XGBoost binary classification (e.g. ranking losses)?

#### Group III: Candidate Selection
8. Which candidate selection algorithm was used to pick the final top decay candidates per event (e.g., greedy disjoint, best pair sum)?
9. Did the agent compare multiple candidate selection algorithms or thresholds?
10. How many selection algorithms or score thresholds were evaluated?
11. Was the top candidate count constraint ($N_{\text{top}} \le 2$ candidates per event) strictly imposed?

#### Group IV: Physics & Diagnostics
12. What is the achieved BDT Classifier ROC AUC score?
13. Did the agent take steps to evaluate or avoid mass sculpting in candidate selection?
14. Was top quark invariant mass information used in the candidate selection or feature engineering process?
15. How many optimization iterations or pipeline tuning steps were performed?
16. Was the BDT score distribution plotted or saved as a diagnostic graphic?
17. Were mass distribution comparison plots generated for top candidate invariant masses?

#### Group V: Reconstruction Performance & Jet Disjointness
18. What is the overall top candidate selection efficiency achieved by the agent?
19. What is the top selection efficiency when considering only the first 2 non-overlapping candidates per event?
20. Did the selection produce any overlapping (shared jet) triplets in the selected candidates?

#### Group VI: Provenance, Evaluation Integrity & Execution Health
21. Was a machine-readable provenance manifest produced, including task version, input scope, artifact checksums, and schema version? Identify every missing element explicitly.
22. Were all reported metrics evaluated on a held-out test set, with an explicit event-ID leakage audit across train, validation, and test splits?
23. What exact artifact path supports each reported metric? Report a path-to-metric mapping rather than only a result-directory root.
24. What were trial wall-clock time, pure agent execution time, input tokens, cache tokens, output tokens, and cost? State which fields are unavailable rather than estimating them.
25. Did the run complete without Harbor trial errors or cancellations, and what was the Harbor verifier reward? Keep this separate from scientific-quality conclusions.

#### Group VII: Additional Selection, Mass & Hold-out Diagnostics
26. At fixed $N_{\text{top}} \le 2$ and jet-disjoint selection, what were selection precision/purity, fake-to-true selected-candidate ratio, and reconstruction efficiency?
27. What quantitative mass-sculpting diagnostic was reported, what acceptance criterion was specified, and did the result meet it? Do not treat the existence of a plot alone as a quantitative answer.
28. What was the performance change relative to the baseline model/selection under identical split and selection constraints? If the comparison is not paired, identify the mismatch.
29. Was model and selection choice made solely using validation information before the final held-out test evaluation? Identify any test-informed choice explicitly.

#### Group VIII: Shared Audit Questions
30. Which explicit task requirements were satisfied, partially satisfied, omitted, or contradicted? Cite one artifact for every judgment.
31. Did the agent change any specified selection, feature, model, dataset, luminosity, threshold, or statistical procedure? Was every deviation documented and justified?
32. Did the agent process every required input file and expected sample? List missing, unreadable, skipped, or silently filtered inputs.
33. Were all reported outputs generated by this run rather than reused? Compare timestamps, configuration identifiers, and checksums where available.
34. Can the final workflow rerun from a clean output directory using one documented command and reproduce metrics within a declared tolerance?
35. Which stages are stochastic? Are relevant seeds recorded, and is repeatability of splits, model, selection, and headline metrics demonstrated?
36. Do headline numbers agree across reports, JSON, tables, plots, logs, and verifier output? List discrepancies rather than silently choosing one.
37. Are there NaNs, infinities, empty categories, zero denominators, negative yields, duplicate event IDs, or invalid model states?
38. Was the test set, blinded region, or final evaluation artifact used during feature engineering, hyperparameter tuning, threshold choice, selection choice, or debugging?
39. Was the final result compared with a clearly defined baseline on the same partition under identical constraints?
40. Are headline results accompanied by statistical uncertainty or variation across seeds, bootstraps, folds, or reasonable analysis variations?
41. What fraction of wall time, tokens, and cost produced the final result versus failed attempts, repeated inspection, or superseded implementations?
42. What substantive errors occurred, how were they detected, and does the evidence show that any correction addressed the root cause?
43. Did the agent modify files outside requested scope, leave large temporary outputs, duplicate artifacts, or introduce unrelated dependencies?
44. Which key conclusions were independently recomputed by the verifier rather than copied from the agent's own report?
45. What are the three most important residual limitations that could change the scientific conclusion?

#### Group IX: Top-Reconstruction Scientific Validity
46. How is a true hadronic-top triplet labeled? Record matching radius, ancestry rules, ambiguity resolution, and matching completeness.
47. Does candidate construction enumerate every valid unique three-jet combination exactly once, with no repeated jet indices or permutation duplicates?
48. Define the reconstruction-efficiency denominator exactly, including treatment of events with zero reconstructable tops.
49. Are candidates, events, and samples weighted correctly in training and evaluation? Can high-multiplicity events dominate because they generate more triplets?
50. What are positive and negative candidate counts before and after sampling or weighting, and is AUC evaluated on the natural held-out distribution?
51. Are duplicated events, augmentations, or common source groups confined to one data split?
52. Report efficiency and purity versus jet multiplicity, b-tag multiplicity, top pT, and number of reconstructable tops.
53. For events with two reconstructable tops, how often are zero, one, and both reconstructed correctly?
54. What is the selected-candidate multiplicity distribution, including zero-selected events?
55. Report efficiency, purity, and fake-to-true ratio as functions of score threshold, with thresholds fixed using validation data only.
56. Compare the BDT on the identical test set with a simple resolved-top mass-based baseline.
57. Quantify mass sculpting before and after score selection with a numeric statistic and prespecified acceptance threshold.
58. Ablate direct top- and W-mass features and report the change in AUC, efficiency, purity, and mass sculpting.
59. Is selection deterministic under equal scores or multiple optimal disjoint pairs?
60. Does performance remain stable in independent files, samples, or kinematic regions not used for model selection?

---

### Required Deliverables:
- A side-by-side Markdown comparison matrix listing all job runs (both completed and early-terminated) across all 60 questions.
- A detailed section-by-section analysis documenting raw evidence, file paths, and exact values for each probing question.
```
