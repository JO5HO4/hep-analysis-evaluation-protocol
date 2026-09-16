# ttH diphoton revised manual-review synthesis

This summary synthesizes the 15 revised, per-run manual `evaluation-report.md` and `workflow-characterization.md` files under `paper/reviews/tth-diphoton/runs/`, using `evaluation/ttH.md` and the manual-review prompt as the review context. It is non-authoritative review evidence only. **No outcome grade is asserted.** Harbor completion and verifier reward are execution facts, not this review's result; the raw and equal-category figures below are the report-local manual-rubric summaries, not authoritative scientific scores.

`P`, `F`, and `M` mean pass, direct failure, and missing evidence. `Raw` is the report's pass count out of 38; `Equal-category` is its nine-group equal-weight summary.

## Included logical runs

| Code | Agent / model / run | P | F | M | Raw | Equal-category | Harbor status / reward |
|---|---|---:|---:|---:|---|---:|---|
| CO | Claude Code / claude-opus-5 / `20260908T234508Z-tth-diphoton-bd__UezeyUP` | 30 | 1 | 7 | 30 / 38 | 0.666667 | completed / 0.000000 |
| CS | Claude Code / claude-sonnet-5 / `20260908T203904Z-tth-diphoton-bd__mmgsDbk` | 28 | 4 | 6 | 28 / 38 | 0.633 | completed / 0.000000 |
| CC | Claude Code / lbl/cborg-coder / `20260904T210145Z-tth-diphoton-bd__MqqLxno` | 2 | 0 | 36 | 2 / 38 | 0.074074 | completed / 0.000000 |
| C5S | Codex / gpt-5.6-sol / `20260905T022547Z-tth-diphoton-bd__MPttiyG` | 26 | 2 | 10 | 26 / 38 | 0.5914 | completed / 0.000000 |
| C5T | Codex / gpt-5.6-terra / `20260902T213233Z-tth-diphoton-bd__zWiAt8N` | 25 | 2 | 11 | 25 / 38 | 0.580 | completed / 0.000000 |
| CCB | Codex / lbl--cborg-coder / `20260902T032120Z-tth-diphoton-bd__CwT2jxX` | 4 | 7 | 27 | 4 / 38 | 0.109 | completed / 0.000000 |
| OHS | OpenHands / gpt-5.6-sol / `20260905T044026Z-tth-diphoton-bd__cMU3hZC` | 1 | 0 | 37 | 1 / 38 | 0.037037 | completed / 0.000000 |
| OHT | OpenHands / gpt-5.6-terra / `20260902T220657Z-tth-diphoton-bd__E6LHpiw` | 7 | 4 | 27 | 7 / 38 | 0.19 | completed / 0.000000 |
| OHC | OpenHands / openai--lbl-cborg-coder / `20260902T050526Z-tth-diphoton-bd__fm8URtk` | 5 | 11 | 22 | 5 / 38 | 0.128 | completed / 0.000000 |
| QB | qwen-coder / google/qwen-3 (Best) / `20260905T041241Z-tth-diphoton-bd__JmY5P4p` | 6 | 5 | 27 | 6 / 38 | 0.1401 | completed / 0.000000 |
| QM | qwen-coder / google-qwen-3 (Medium) / `20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158` | 5 | 13 | 20 | 5 / 38 | 0.204 | completed / 0.000000 |
| QC | qwen-coder / lbl--cborg-coder / `20260902T050526Z-tth-diphoton-bd__2Jw5SMu` | 7 | 10 | 21 | 7 / 38 | 0.168 | completed / 0.000000 |
| T5S | Terminus-2 / gpt-5.6-sol / `20260905T033334Z-tth-diphoton-bd__u5KdDyp` | 24 | 3 | 11 | 24 / 38 | 0.556 | completed / 0.000000 |
| T5T | Terminus-2 / gpt-5.6-terra / `20260902T205321Z-tth-diphoton-bd__sfftAQT` | 15 | 7 | 16 | 15 / 38 | 0.4241 | completed / 0.000000 |
| TC | Terminus-2 / openai/lbl/cborg-coder / `20260905T003430Z-tth-diphoton-bd__st37ant` | 2 | 12 | 24 | 2 / 38 | 0.0593 | completed / 0.000000 |

The P/F/M and Raw columns above reproduce each report's status summary. Two report-internal accounting differences are retained rather than silently resolved: CO's detailed Q rows yield 31 P, 1 F, 6 M although its status summary says 30/1/7 (and raw 30/38); QM's detailed Q rows yield 5 P, 15 F, 18 M although its status summary says 5/13/20. The matrix below follows the detailed per-question statuses in the revised reports.

## Q1–Q38 cross-run status matrix

| Q | CO | CS | CC | C5S | C5T | CCB | OHS | OHT | OHC | QB | QM | QC | T5S | T5T | TC |
|---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Q1 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| Q2 | P | P | P | P | P | M | M | P | M | M | M | M | P | P | M |
| Q3 | P | F | M | P | P | F | M | M | F | M | F | F | P | P | F |
| Q4 | P | P | M | P | P | P | M | P | P | P | P | P | P | P | F |
| Q5 | P | P | M | P | M | M | M | M | F | M | M | M | P | P | M |
| Q6 | P | P | M | P | P | M | M | P | F | M | F | P | P | P | F |
| Q7 | P | P | M | P | M | M | M | M | F | M | M | M | P | P | M |
| Q8 | P | P | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q9 | F | F | M | F | F | F | M | F | F | F | F | F | F | F | F |
| Q10 | P | P | M | P | M | M | M | M | M | M | M | M | F | M | M |
| Q11 | P | P | M | P | P | F | M | P | P | P | F | P | P | P | F |
| Q12 | P | P | M | P | P | F | M | M | M | F | F | F | P | P | M |
| Q13 | P | P | M | P | P | F | M | M | M | M | M | M | P | P | F |
| Q14 | P | P | M | P | P | P | M | P | P | P | P | P | P | P | F |
| Q15 | P | P | M | P | P | P | M | P | P | P | P | F | P | P | P |
| Q16 | P | P | M | P | P | M | M | M | M | M | F | P | P | M | M |
| Q17 | P | P | M | M | P | M | M | M | M | M | F | M | P | M | M |
| Q18 | P | P | M | M | P | M | M | M | M | M | F | M | F | M | F |
| Q19 | P | P | M | P | P | F | M | M | F | F | F | F | P | F | F |
| Q20 | P | F | M | P | F | M | M | F | F | P | F | P | P | F | F |
| Q21 | P | P | M | F | P | M | M | F | M | M | M | M | P | M | M |
| Q22 | P | P | M | P | P | F | M | F | F | F | F | M | P | M | F |
| Q23 | P | P | M | P | P | M | M | M | F | M | F | M | P | F | F |
| Q24 | P | F | M | P | P | M | M | M | M | F | F | F | P | F | M |
| Q25 | P | P | M | P | P | M | M | M | M | M | M | M | M | M | M |
| Q26 | P | P | M | P | P | M | M | M | M | M | M | M | M | M | M |
| Q27 | P | P | M | P | P | M | M | M | M | M | F | F | P | F | M |
| Q28 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q29 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q30 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q31 | P | P | M | P | P | M | M | M | M | M | F | F | P | P | M |
| Q32 | P | P | M | P | P | M | M | M | M | M | M | F | P | P | M |
| Q33 | P | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Q34 | M | M | M | M | P | M | M | M | M | M | M | M | M | M | M |
| Q35 | M | P | M | P | M | M | M | M | F | M | M | F | M | F | M |
| Q36 | P | P | M | P | P | M | M | M | M | M | P | M | P | P | M |
| Q37 | P | P | M | M | M | M | M | M | F | M | M | M | M | M | M |
| Q38 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |

## Evidence-grounded synthesis

Recurring direct failures are concentrated in the task-contract and statistical-execution parts of the rubric, not in Harbor execution: all 15 trials completed, while every verifier reward was zero. Q9 is a direct feature-list mismatch for 13 runs with saved contradictory feature/API evidence; the two remaining runs are missing rather than passes. Several lower-coverage runs contain direct implementation contradictions: absent submission artifacts (CC), source-only or timed-out work (OHT), synthetic/mock pipelines (OHC, QB, QC), or template/mock statistical outputs rather than an executed RooFit/Asimov result (OHC, QB, QC, T5T). Other direct failures include non-shared signal strengths (CS), an out-of-tolerance `mu_hat` (CS and QC), invalid or non-executed significance construction (QC and T5T), priority-order violations (QC), and missing/invalid retained-category purity conditions (T5S).

Missing is materially different from failure in this set. Q28–Q30 and Q38 are missing for every run because no compatible evaluator-owned same-frozen-table inclusive or fixed-quantile baseline rerun is preserved; development proxies cannot establish those comparisons. Q8 is missing for every run because a package is often named but the required version is not directly recorded. Q33 is missing in 14 runs because a required performance-plot partition was not established; Q34 is missing in 14 because no finite score--mass diagnostic was produced. Yield details, purity denominators, package versions, reproducibility fields, and a second common-validation attempt are also frequently absent after the per-run source/output audits. These are evidence gaps, not inferred physics or workflow failures.

## Workflow comparison

The revised workflow profiles show varied provenance and recovery patterns, without assigning a workflow score. The most complete output coverage is recorded for CO and CS (61/61 required), C5S (60/60), and T5S (61 with an independently unestablished denominator). CS has 82 recorded commands, 7 failed commands, 3 signatures, and one evidenced recovery; C5S has 35, 2, 1, and one recovery. T5S records 25 commands, 3 failures/signatures, and 3 recoveries; T5T records 45, 5, 4, and 4 recoveries. CCB and TC show the heaviest recorded debugging (98 commands/20 failures/12 signatures and 86/12/4 respectively) alongside incomplete output coverage (42/67 and 6/55).

Several profiles correctly retain uncertainty where the transcript cannot support a count: CO has only two outer commands with inner outcomes not established; C5T has 77 readable files but no complete tool-invocation ledger; OHC has 13/67 named outputs with command/error totals not established. OHT documents five timeout invocations and no result root (three submitted source files only). OHS records no solver commands and no preserved result artifacts. QB preserves 12/65 expected artifacts despite 50 recorded commands; QM records 54/61 with a recovery; QC records a synthetic-data workflow (35/58 readable artifacts) after actual-input unavailability. No profile establishes a clean-output reproducibility rerun with an agreement tolerance.

This summary deliberately does not use the historical `paper/reviews/tth-diphoton/summary.md` or invalid-v1 artifacts. Its only synthesized inputs are the revised reports and workflow profiles named above.
