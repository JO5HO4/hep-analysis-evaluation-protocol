# Manual evidence evaluation: claude-code / claude-opus-5

This is a non-authoritative manual review under `evaluation/ttH.md`, `evaluation/evaluation_rubric.md`, and the flexible evidence policy. The task has no indexed evaluation spec, so this report does **not** create an outcome grade. Statuses are only `pass`, `fail`, or `missing`; a zero Harbor reward does not erase readable physics evidence.

## Run identity and review scope

| Field | Value |
|---|---|
| Run | R1 |
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `claude-code / claude-opus-5` |
| Logical trial | `20260908T234508Z-tth-diphoton-bd__UezeyUP` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Manual rubric result | 30 pass, 1 fail, 7 missing; raw 30 / 38 |

Evidence was traced through the enclosing and nested `result.json`, `trial.log`, readable `agent/` trajectory, `verifier/` report, submitted source, and all readable saved tables, JSON, CSV/Parquet manifests, plots/plot payloads, workspace, and report below this trial's `artifacts/root/`. “Missing” below names those concrete searched sources and means that their combined evidence does not establish the condition; it is never inferred solely from an expected filename.

## Criterion-by-criterion evidence

| Criterion | Required condition | Status | Reward | Observed value / evidence and reasoning |
|---|---|---|---:|---|
| Q1 | both trial wall-clock and pure-agent times | missing | 0 | Both time types are not jointly established; enclosing job timestamps are not pure agent execution time. |
| Q2 | total cost in USD | pass | 1 | $9.962386 USD in enclosing result.json:stats.cost_usd. |
| Q3 | human-facing analysis narrative | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q4 | no tight-ID/isolation at preselection | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q5 | hadronic raw count and 36 fb^-1 yield | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q6 | required hadronic selection | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q7 | process-separated post-preselection Higgs yields | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q8 | BDT package and version | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q9 | exact BDT_FEATURES excluding m_gammagamma | fail | 0 | verifier/score_report.json:selection_api.errors directly reports an incompatible final feature API. |
| Q10 | held-out signal/background AUC | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q11 | ttH+tH signal and ggH+NTI background | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q12 | physical weights before balancing | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q13 | event-disjoint stable-ID train/validation/test splits | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q14 | six BDT categories plus unassigned | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q15 | BDT before cut-based category priority | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q16 | iterative 5% expected-significance stopping rule | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q17 | highest retained BDT-category ttH purity | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q18 | second-highest retained BDT-category ttH purity | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q19 | RooFit workspace and Asimov fit | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q20 | shared-mu ttH+tH statistical definition | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q21 | candidate functions and selection statistic | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q22 | TI-sideband background PDF procedure | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q23 | S+B Asimov mu_gen=1 | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q24 | valid unbiased S+B Asimov fit | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q25 | continuum yield in 123–127 GeV | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q26 | resonant-background yield in 123–127 GeV | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q27 | one-sided q0 and expected Z consistency | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q28 | Z vs inclusive baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q29 | mu uncertainty vs inclusive baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q30 | baseline Pareto improvement | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q31 | plot quantity, units and finite values | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q32 | histogram normalization | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q33 | performance-plot partition | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q34 | score–mass correlation diagnostic | missing | 0 | Missing: searched report, metrics, optimization records, plot payloads, and source; no finite score–mass diagnostic. |
| Q35 | two common-validation optimization attempts | missing | 0 | Missing: searched report, training metadata, optimization records, and source; no two attempts with a common validation metric. |
| Q36 | pre/post balancing ratios | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q37 | final configuration reproducibility | pass | 1 | Pass: direct saved report and corresponding machine-readable result record establish the required condition. |
| Q38 | Z vs fixed-score-quantile baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |


## Interpretation

The Harbor verifier reward is reported separately as compatibility context. In particular, a `fail` is used only where direct evidence contradicts a rubric condition (notably the final BDT feature API where recorded); unavailable, incomplete, or non-comparable evidence remains `missing`. Baseline comparisons are missing for this run because the preserved artifacts do not contain a compatible evaluator-owned same-sample baseline comparison.

