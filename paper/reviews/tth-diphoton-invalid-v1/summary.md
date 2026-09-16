# ttH diphoton manual-review summary

This summary covers every preserved logical trial in `results/paper/tth-diphoton-bdt-categorization-paper-version`: the 15 nested trial `result.json` records, not their enclosing job summaries. It is a non-authoritative manual review under `evaluation/ttH.md`; the task has no indexed specification and therefore has no newly created outcome grade.

`P` = pass (reward 1), `F` = fail (reward 0), and `M` = missing (reward 0). A `missing` cell is based on the concrete evidence-search trail in that run’s [evaluation report](runs/), including logs, trajectory, submitted source, saved tables, plots, workspaces, JSON/CSV/Parquet outputs and report—not an absent expected filename. All Harbor trials completed with verifier reward 0.000000; it is execution context, not a blanket rubric decision.

## Run status totals

| Run | Agent / model | P | F | M | Raw manual reward | Harbor status / verifier reward |
|---|---|---:|---:|---:|---:|---|
| R1 | Claude Code / claude-opus-5 | 30 | 1 | 7 | 30 / 38 | completed / 0.000000 |
| R2 | Claude Code / claude-sonnet-5 | 2 | 1 | 35 | 2 / 38 | completed / 0.000000 |
| R3 | Claude Code / lbl--cborg-coder | 1 | 0 | 37 | 1 / 38 | completed / 0.000000 |
| R4 | Codex / gpt-5.6-sol | 30 | 1 | 7 | 30 / 38 | completed / 0.000000 |
| R5 | Codex / gpt-5.6-terra | 2 | 1 | 35 | 2 / 38 | completed / 0.000000 |
| R6 | Codex / lbl--cborg-coder | 0 | 1 | 37 | 0 / 38 | completed / 0.000000 |
| R7 | OpenHands / gpt-5.6-sol | 0 | 0 | 38 | 0 / 38 | completed / 0.000000 |
| R8 | OpenHands / gpt-5.6-terra | 1 | 0 | 37 | 1 / 38 | completed / 0.000000 |
| R9 | OpenHands / openai--lbl-cborg-coder | 0 | 0 | 38 | 0 / 38 | completed / 0.000000 |
| R10 | Qwen Coder / google--qwen-3--best | 0 | 0 | 38 | 0 / 38 | completed / 0.000000 |
| R11 | Qwen Coder / google--qwen-3--medium | 1 | 1 | 36 | 1 / 38 | completed / 0.000000 |
| R12 | Qwen Coder / lbl--cborg-coder | 1 | 1 | 36 | 1 / 38 | completed / 0.000000 |
| R13 | Terminus 2 / gpt-5.6-sol | 29 | 1 | 8 | 29 / 38 | completed / 0.000000 |
| R14 | Terminus 2 / gpt-5.6-terra | 2 | 1 | 35 | 2 / 38 | completed / 0.000000 |
| R15 | Terminus 2 / openai--lbl-cborg-coder | 0 | 0 | 38 | 0 / 38 | completed / 0.000000 |


## Every criterion × every logical run

| Rubric group | Criterion | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13 | R14 | R15 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Execution and documentation | Q1 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Execution and documentation | Q2 | P | P | P | P | P | M | M | P | M | M | M | M | P | P | M |
| Execution and documentation | Q3 | P | P | M | P | P | M | M | M | M | M | P | P | P | P | M |
| Object and preselection | Q4 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Object and preselection | Q5 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Object and preselection | Q6 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Object and preselection | Q7 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| BDT training | Q8 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| BDT training | Q9 | F | F | M | F | F | F | M | M | M | M | F | F | F | F | M |
| BDT training | Q10 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| BDT training | Q11 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| BDT training | Q12 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| BDT training | Q13 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Categorization and purity | Q14 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Categorization and purity | Q15 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Categorization and purity | Q16 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Categorization and purity | Q17 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Categorization and purity | Q18 | P | M | M | P | M | M | M | M | M | M | M | M | M | M | M |
| Workspace and sensitivity | Q19 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q20 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q21 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q22 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q23 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q24 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q25 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q26 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Workspace and sensitivity | Q27 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Inclusive baseline | Q28 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Inclusive baseline | Q29 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Inclusive baseline | Q30 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Plotting | Q31 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Plotting | Q32 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Plotting | Q33 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Validation and reproducibility | Q34 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Validation and reproducibility | Q35 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| Validation and reproducibility | Q36 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Validation and reproducibility | Q37 | P | M | M | P | M | M | M | M | M | M | M | M | P | M | M |
| Quantile baseline | Q38 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |


## Evidence highlights and comparison limits

The reports preserve direct positive evidence rather than treating zero verifier reward as an eraser: R1 (Claude Opus), R4 (Codex Sol), and R13 (Terminus Sol) contain readable reports plus saved training, categorization, workspace, fit and plot artifacts; their cells reflect those sources. R2, R5, R11, R12, and R14 have partially readable analyses, while R3, R6–R10, and R15 have sparse or incomplete evidence and therefore retain `M` where no direct condition can be established.

Q9 is `F` only for the runs whose `verifier/score_report.json:selection_api.errors` directly reports an incompatible final feature API. Q28–Q30 and Q38 are `M` for every run: the required compatible, evaluator-owned same-sample baseline comparison is not preserved. Q34–Q35 are `M` for every run after searching reports, metrics, optimization records, plot payloads and source; no finite score–mass diagnostic or two common-validation attempts are directly established.

Per-run workflow accounts, including the separate non-scoring process characterization, are colocated beside each individual evaluation report under `runs/<agent>/<model>/`.

