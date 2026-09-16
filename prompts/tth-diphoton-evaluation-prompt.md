# Non-Invasive Evaluation Prompt for ttH Diphoton BDT Categorization Task

This file contains the complete, standardized 73-question non-invasive evaluation prompt used to evaluate agent benchmark runs on the `tth-diphoton-bdt-categorization` task.

```markdown
You are tasked with performing a non-invasive evaluation of agent benchmark runs for the `tth-diphoton-bdt-categorization` task.

### Core Evaluation Directives & Constraints:
1. **Strict Non-Invasiveness**:
   - You must NOT modify, alter, or write to any files, artifacts, or workspaces in the task job folders or existing result displays.
   - All scratch scripts, temporary files, and evaluation outputs must be created exclusively within your own local working workspace.

2. **Data Source Scope**:
   - Inspect raw job results ONLY under:
     `/Users/haichenwang/.local/state/terminal-bench-collider/harbor-jobs/`
   - Do NOT use second-hand public summaries or viewer outputs (such as `tth-diphoton-bdt-physicist-viewer`).
   - Evaluate ONLY job runs executed on or after **July 24, 2026** (folder names starting with `20260724` or `20260725`).

3. **LLM Probing & Deterministic Output Strategy**:
   - Different agents use varying file structures, variable naming conventions, and JSON formats. Use LLM-based probing to inspect raw python code (`/root/submission/tth-diphoton-bdt/...`) and output JSON records (`/root/results/tth-diphoton-bdt/...`).
   - Derive deterministic outcomes (exact numbers, booleans, or explicit "N/A" for errored runs) for each question based strictly on empirical evidence in the raw files.

4. **Required Audit Response Format**:
   - For every question, report `Status: PASS | PARTIAL | FAIL | UNAVAILABLE`, followed by `Answer`, `Evidence`, `Independent verification`, and `Impact if wrong`.
   - `PASS` requires evidence that fully addresses the question; `PARTIAL` requires an explicit statement of the unresolved portion. Never replace unavailable evidence with a plausible narrative.

---

### The 27 Probing Questions (Grouped by Category):

#### Group I: Execution & Documentation Meta
1. How long does the run take to complete?
2. What is the cost of the agent run?
3. Did the agent produce any human-facing documentation?

#### Group II: Object Definition & Hadronic Preselection
4. Did the agent apply any isolation and/or identification requirements on photons?
5. What is the number of events selected for the hadronic channel?
6. Did the agent implement the correct hadronic channel preselection, with b-jet, jets, and lepton-veto requirements?
7. What are the expected Higgs boson signal yields after hadronic preselection?

#### Group III: BDT Model Training & Configuration
8. Which package is used for the BDT training?
9. What features are used to train the BDT and are these features identical to those specified in the original instruction passed to the agent?
10. What is the AUC between signal and background?
11. What is used as the signal and background classes in the training? Are those consistent with the requirements in the original instruction?
12. How are the classes weighed in the BDT training? Is it consistent with the procedure stated in the original instruction?
13. Did the agent implement any sort of partition of training, validation, and testing samples?

#### Group IV: Categorization, Event Assignment & Purity
14. How many categories did the agent implement using BDT?
15. Did the agent use BDT to categorize the event as instructed?
16. What is the figure of merit guiding the categorization?
17. What is the purity of the ttH events in the category with the highest BDT score, with purity defined as the ratio of the ttH yield to all Higgs yield?
18. What is the purity of the ttH events in the second highest BDT category?

#### Group V: Statistical Workspace, Background Modeling & Sensitivity Fit
19. Did the agent perform a fit-based assessment of the sensitivity?
20. In the fit/statistical interpretation, did the agent treat ttH as the signal or both ttH and tH, or all Higgs events?
21. How did the agent pick the analytical functions for the fit?
22. What is the procedure used to determine the background pdf?
23. In the sensitivity project, did the agent create an S+B asimov data set for that purpose?
24. In the fit to the S+B asimov data set, did the fit return mu = 1, and in that same fit, did the fit return an error that is not zero (or close to zero, e.g., <0.01)?
25. What is the expected continuum background yield in the mass window of 123 - 127 GeV if the agent reported it?
26. What is the expected resonant background yield in that mass window of 123 - 127 GeV if the agent reported it?
27. What is the expected significance?

#### Group VI: Provenance, Evaluation Integrity & Execution Health
28. Was a machine-readable provenance manifest produced, including task version, input scope, artifact checksums, and schema version? Identify every missing element explicitly.
29. Were all reported metrics evaluated on a held-out test set, with an explicit event-ID leakage audit across train, validation, and test splits?
30. What exact artifact path supports each reported metric? Report a path-to-metric mapping rather than only a result-directory root.
31. What were trial wall-clock time, pure agent execution time, input tokens, cache tokens, output tokens, and cost? State which fields are unavailable rather than estimating them.
32. Did the run complete without Harbor trial errors or cancellations, and what was the Harbor verifier reward? Keep this separate from scientific-quality conclusions.

#### Group VII: Category, Fit & Yield Completeness
33. Report separate ttH and tH yields in each category, the all-Higgs denominator, and the resulting ttH purity for the two highest-score categories. If only a combined ttH+tH yield is available, state that the requested purity is unavailable.
34. State the number of initially configured categories, retained categories, and rejected or merged categories; report every threshold and the retention rule.
35. Record fit status, covariance quality, $\hat{\mu}$, its uncertainty, $q_0$, expected $Z$, and observed-significance blinding state in one structured result.
36. State the background-model candidate set, selection method, and any model-choice systematic. A single prespecified function is a valid answer only when stated explicitly.
37. Report continuum and resonant yields with category scope, mass window, luminosity, and an explicit statement of whether unassigned categories are included.

#### Group VIII: Shared Audit Questions
38. Which explicit task requirements were satisfied, partially satisfied, omitted, or contradicted? Cite one artifact for every judgment.
39. Did the agent change any specified selection, feature, model, dataset, luminosity, threshold, or statistical procedure? Was every deviation documented and justified?
40. Did the agent process every required input file and expected sample? List missing, unreadable, skipped, or silently filtered inputs.
41. Were all reported outputs generated by this run rather than reused? Compare timestamps, configuration identifiers, and checksums where available.
42. Can the final workflow rerun from a clean output directory using one documented command and reproduce metrics within a declared tolerance?
43. Which stages are stochastic? Are relevant seeds recorded, and is repeatability of splits, model, categories, and headline metrics demonstrated?
44. Do headline numbers agree across reports, JSON, tables, plots, logs, and verifier output? List discrepancies rather than silently choosing one.
45. Are there NaNs, infinities, empty categories, zero denominators, negative yields, duplicate event IDs, or invalid model or fit states?
46. Was the test set, blinded region, or final evaluation artifact used during feature engineering, hyperparameter tuning, threshold choice, category choice, or debugging?
47. Was the final result compared with a clearly defined baseline on the same partition under identical constraints?
48. Are headline results accompanied by statistical uncertainty or variation across seeds, bootstraps, folds, or reasonable analysis variations?
49. What fraction of wall time, tokens, and cost produced the final result versus failed attempts, repeated inspection, or superseded implementations?
50. What substantive errors occurred, how were they detected, and does the evidence show that any correction addressed the root cause?
51. Did the agent modify files outside requested scope, leave large temporary outputs, duplicate artifacts, or introduce unrelated dependencies?
52. Which key conclusions were independently recomputed by the verifier rather than copied from the agent's own report?
53. What are the three most important residual limitations that could change the scientific conclusion?

#### Group IX: ttH Diphoton Scientific Validity
54. For every process, record luminosity, cross section, branching/filter efficiency, generator-weight sum, k-factor, and applied scale factors.
55. Are signed MC weights preserved through selection, training, categorization, yield calculation, and fitting? Report both signed and absolute-weight diagnostics.
56. Report unweighted counts and weighted yields for every process at every selection stage.
57. Do photon, lepton, jet, overlap-removal, and b-tag definitions exactly match the task specification? List every discrepancy.
58. Are training, validation, test, category-optimization, and final statistical-model events isolated from one another as required?
59. Can a physical event or correlated representation appear in both TI signal-like data and the NTI continuum proxy?
60. Is m_gammagamma, or a strongly mass-correlated variable, used directly or indirectly by the classifier? Quantify continuum mass-shape change across BDT categories.
61. What validation supports transfer of NTI sidebands to the TI continuum in the signal window?
62. What signal contamination is present in sidebands and the NTI control sample, and how is it treated?
63. Were boundaries optimized only on validation expected yields, without final test or Asimov-significance leakage?
64. How stable are thresholds, yields, purity, and expected significance under alternate seeds, binning, minimum-background requirements, and score perturbations?
65. What fraction and weighted yield are rejected or unassigned, by process, and how does this affect sensitivity?
66. Report separate ttH, tH, ggH, VBF, WH, ZH, ggZH, continuum, and total-Higgs yields and purities in every category.
67. Which background analytic functions were tested, which goodness-of-fit criterion selected one, and what spurious-signal or bias test was performed?
68. Which nuisance parameters and correlations are included? If none, is the result explicitly statistical-only?
69. Are convergence status, covariance quality, parameter bounds, pulls, correlations, likelihood scans, and goodness-of-fit diagnostics acceptable?
70. Do background-only and signal-plus-background Asimov fits recover injected signal strengths without appreciable bias?
71. What expected significance does each category contribute, and what is the incremental combined-fit gain from each category?
72. Does an independently reconstructed likelihood reproduce q0, mu_hat, its uncertainty, and expected significance?
73. Is there evidence that observed TI signal-window data were never read, plotted, summarized, or used in a decision?

---

### Required Deliverables:
- A side-by-side Markdown comparison matrix listing all job runs (both completed and early-terminated) across all 73 questions.
- A detailed section-by-section analysis documenting raw evidence, file paths, and exact values for each probing question.
```
