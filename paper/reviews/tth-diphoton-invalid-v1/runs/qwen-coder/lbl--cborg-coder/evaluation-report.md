# Manual evidence evaluation: qwen-coder / lbl--cborg-coder

This is a non-authoritative manual review under `evaluation/ttH.md`, `evaluation/evaluation_rubric.md`, and the flexible evidence policy. The task has no indexed evaluation spec, so this report does **not** create an outcome grade. Statuses are only `pass`, `fail`, or `missing`; a zero Harbor reward does not erase readable physics evidence.

## Run identity and review scope

| Field | Value |
|---|---|
| Run | R12 |
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `qwen-coder / lbl--cborg-coder` |
| Logical trial | `20260902T050526Z-tth-diphoton-bd__2Jw5SMu` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Manual rubric result | 1 pass, 1 fail, 36 missing; raw 1 / 38 |

Evidence was traced through the enclosing and nested `result.json`, `trial.log`, readable `agent/` trajectory, `verifier/` report, submitted source, and all readable saved tables, JSON, CSV/Parquet manifests, plots/plot payloads, workspace, and report below this trial's `artifacts/root/`. “Missing” below names those concrete searched sources and means that their combined evidence does not establish the condition; it is never inferred solely from an expected filename.

## Criterion-by-criterion evidence

| Criterion | Required condition | Status | Reward | Observed value / evidence and reasoning |
|---|---|---|---:|---|
| Q1 | both trial wall-clock and pure-agent times | missing | 0 | Both time types are not jointly established; enclosing job timestamps are not pure agent execution time. |
| Q2 | total cost in USD | missing | 0 | Cost is null in enclosing result.json:stats.cost_usd. |
| Q3 | human-facing analysis narrative | pass | 1 | Pass: report.md and saved JSON/CSV/workspace artifacts directly establish the required condition. |
| Q4 | no tight-ID/isolation at preselection | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q5 | hadronic raw count and 36 fb^-1 yield | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q6 | required hadronic selection | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q7 | process-separated post-preselection Higgs yields | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q8 | BDT package and version | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q9 | exact BDT_FEATURES excluding m_gammagamma | fail | 0 | verifier/score_report.json:selection_api.errors directly reports an incompatible final feature API. |
| Q10 | held-out signal/background AUC | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q11 | ttH+tH signal and ggH+NTI background | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q12 | physical weights before balancing | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q13 | event-disjoint stable-ID train/validation/test splits | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q14 | six BDT categories plus unassigned | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q15 | BDT before cut-based category priority | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q16 | iterative 5% expected-significance stopping rule | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q17 | highest retained BDT-category ttH purity | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q18 | second-highest retained BDT-category ttH purity | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q19 | RooFit workspace and Asimov fit | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q20 | shared-mu ttH+tH statistical definition | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q21 | candidate functions and selection statistic | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q22 | TI-sideband background PDF procedure | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q23 | S+B Asimov mu_gen=1 | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q24 | valid unbiased S+B Asimov fit | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q25 | continuum yield in 123–127 GeV | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q26 | resonant-background yield in 123–127 GeV | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q27 | one-sided q0 and expected Z consistency | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q28 | Z vs inclusive baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q29 | mu uncertainty vs inclusive baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q30 | baseline Pareto improvement | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |
| Q31 | plot quantity, units and finite values | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q32 | histogram normalization | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q33 | performance-plot partition | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q34 | score–mass correlation diagnostic | missing | 0 | Missing: searched report, metrics, optimization records, plot payloads, and source; no finite score–mass diagnostic. |
| Q35 | two common-validation optimization attempts | missing | 0 | Missing: searched report, training metadata, optimization records, and source; no two attempts with a common validation metric. |
| Q36 | pre/post balancing ratios | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q37 | final configuration reproducibility | missing | 0 | Missing: enclosing result.json; nested result.json; trial.log; agent/ trajectory; verifier/score_report.json; artifacts/root/{submission,results} were searched; no readable direct evidence sufficient for this criterion. |
| Q38 | Z vs fixed-score-quantile baseline | missing | 0 | Missing: evaluator-owned common frozen table and compatible baseline rerun are absent; searched baseline records plus saved fit/output tree. |


## Interpretation

The Harbor verifier reward is reported separately as compatibility context. In particular, a `fail` is used only where direct evidence contradicts a rubric condition (notably the final BDT feature API where recorded); unavailable, incomplete, or non-comparable evidence remains `missing`. Baseline comparisons are missing for this run because the preserved artifacts do not contain a compatible evaluator-owned same-sample baseline comparison.

