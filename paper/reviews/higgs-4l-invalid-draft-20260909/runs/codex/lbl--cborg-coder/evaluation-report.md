# Manual evidence review — Codex / lbl--cborg-coder

Run: `20260902T192326Z-higgs-4l-significance-codex-1785193`. Generated 2026-09-09 from the preserved-run audit. This is a
manual non-authoritative review under `evaluation/higgs_4l.md`, not an outcome
grade. Harbor status and verifier reward are execution context, not rubric points.

## Evidence traced

The full bundle `results/paper/higgs-4l-significance-paper-version/codex/lbl--cborg-coder/20260902T192326Z-higgs-4l-significance-codex-1785193` was inspected through its outer and nested
`result.json`, `job.log`/trial log, readable agent transcript or trajectory,
submitted source and README, retained `results/results.json`, and retained
diagnostics/plots where present. Missing below means those concrete sources
were searched but did not directly establish the condition; it never means a
filename alone was expected. The cross-run ledger links the exact field/source
and rationale for each decision.

## Status summary

| P | F | M | Harbor status / verifier reward |
|---:|---:|---:|---|
| 12 | 0 | 20 | See [summary](../../../summary.md#status-summary) |

## Every rubric criterion

| Criterion | Status | Reward | Direct-evidence ledger |
|---|---|---:|---|
| Q1 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q2 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q3 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q4 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q5 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q6 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q7 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q8 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q9 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q10 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q11 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q12 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q13 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q14 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q15 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q16 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q17 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q18 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q19 | pass | 1 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q20 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q21 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q22 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q23 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q24 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q25 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q26 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q27 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q28 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q29 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q30 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q31 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |
| Q32 | missing | 0 | [summary evidence ledger](../../../summary.md#observed-values-evidence-and-reasons) |

## Evidence ledger and decision basis

The following is the complete audited criterion ledger used for this run. Its
entries name the checked source classes (`H`, `R`, `S`, and `T`) and
distinguish pass, contradiction, and unavailable evidence. For this run, those
prefixes resolve within `results/paper/higgs-4l-significance-paper-version/codex/lbl--cborg-coder/20260902T192326Z-higgs-4l-significance-codex-1785193`. Frozen evaluator-reference values were
unavailable, so Q23–Q26 are `missing`, rather than inferred.

## Observed values, evidence, and reasons

| Questions | Per-run observed values, status, exact evidence, concise reason |
|---|---|
| Q1 | All: `missing`; `H:started_at,finished_at` establishes wall time only, not a separately recorded pure agent-execution time. |
| Q2 | A `$5.3911`, B `$2.2233186`, C `$0.914473`, D `$0.325812`, E `$0.1782162`, M `$0.25772945`, N `$0.08077993` — `pass`, `H:stats.cost_usd`; F–L,O `missing`, no finite USD total retained. |
| Q3 | A–F,J–O `pass`, `S:README.md` plus executable source describes invocation, likelihood/toys/profile; G–I `missing`, no readable retained task documentation. |
| Q4–6 | A–O `P`; `S` (or G–I `T` embedded final source) reads array/count schema, uses `gammaln`/equivalent stable factorial, and sums channel terms. |
| Q7 | A–F,I–O `P`, `R:logL_b=-11.082750320271758; logL_sb=-5.8159224919108095` (minor last-digit variants); G,H `M`, retained task result absent. |
| Q8 | A–F,I–O `P`, `R:test_statistic=-10.533655656721898` and `-2*(logL_sb-logL_b)` agrees; G,H `M`. |
| Q9 | A–F,I–O `P`, `R`/`S` establishes the three inputs used once; G,H `P`, `T` final source reads all vector entries. |
| Q10 | A `10,000,000`, B `5,000,000`, D/E `2,000,000`, I/M/N `1,000,000`: `pass` in `R` (I `T` final source and run); others `missing`, no executed count retained. |
| Q11 | A–O `P`; `S`/`T` creates independent Poisson draws with the background vector. |
| Q12 | A,B,D,E,M,N `pass` (`S` implements `q_toy <= q_observed`); C,F `missing` (no retained tail definition); G,H `pass` (embedded source); I,J,K,L,O `fail`, retained source explicitly uses `q_toys >= q_obs`, the opposite tail. |
| Q13 | A `2590/10000000=0.000259`, B `1288/5000000=0.0002576`, D `543/2000000=0.0002715`, E `579/2000000=0.0002895`, M `258/1000000=0.000258`, N `212/1000000=0.000212`: `P`, `R`; G,H `M`; remaining `N` because count and denominator are not both retained. |
| Q14 | A `5.088545e-06`, D `1.164960e-05`, E `1.202947e-05`: `pass`, `R:p_value_uncertainty/p_value_mc_se`; all others `missing`, no binomial uncertainty/interval retained. |
| Q15 | A–F,I–O `P`, `R:p_value,significance` obey `Phi^-1(1-p)` within tolerance; G,H `M`. (The negative Qwen Z values are mathematically consistent with their retained near-one p values.) |
| Q16 | A,B,M,N `P`, `R:evidence_3sigma/reaches_3sigma_evidence/evidence_at_3sigma=true` and Z≥3; G,H `M`; others `N`, no explicit conclusion retained. |
| Q17–19 | A–O `P`; `S`/`T` implements `lambda=mu*s+b`, bounded `mu>=0`, and `-2 Delta logL` relative to minimization. |
| Q20 | All `missing`: endpoints are retained in many `R` files, but no executed profile values at both endpoints (within 0.01 of one) are preserved. |
| Q21 | A,B,M,N `P`, `R:mu_err_{up,down}/mu_err_{plus,minus}`; all others `N`, only endpoints, not both reported uncertainties. |
| Q22 | All `missing`: no retained statement classifies a lower endpoint as boundary-limited; a zero endpoint alone is insufficient. |
| Q23–26 | All `missing`: the prompt specifies no compatible Higgs reference calculator; none was invented or run. |
| Q27–29 | A,I,J,K,L,N `P`: retained diagnostic plots and `S` identify toy-q distribution/observed marker and `-2Delta logL`/level 1, with density stated for histograms; G,H `M`; B–F,M,O `N`, no retained produced diagnostics with the required direct plotting evidence. |
| Q30 | A `20260829`, D/E `20260829`, M `123456789`, N `20250308`: `P`, `R:seed/random_seed/toy_seed`; all others `N`. |
| Q31–32 | All `missing`: source exposes parts of settings/checks but no retained direct final configuration establishes all required settings, package versions, and the full set of numerical validity checks. |


