# Manual evidence review — Higgs to four leptons

Generated 2026-09-09. This is a manual, non-authoritative evidence review under
`evaluation/higgs_4l.md`; it is neither a Harbor verifier result nor an outcome
grade. I inspected the preserved outer `result.json`, trial record, readable
submission source/README, retained `results/results.json`, plots, and readable
agent transcript where present. I did not run an extractor, grader, report
generator, or reference calculator.

## Included and excluded paths

Included logical runs (one completed Harbor bundle each, stable order):

| Key | Agent / model / run |
|---|---|
| A | Claude Code / claude-opus-5 / `20260829T171737Z-higgs-4l-significance-claude-code-1534712` |
| B | Claude Code / claude-sonnet-5 / `20260829T161300Z-higgs-4l-significance-claude-code-1487708` |
| C | Claude Code / lbl--cborg-coder / `20260902T192326Z-higgs-4l-significance-claude-code-1370864` |
| D | Codex / gpt-5.6-sol / `20260829T170234Z-higgs-4l-significance-codex-1524332` |
| E | Codex / gpt-5.6-terra / `20260829T160141Z-higgs-4l-significance-codex-1477637` |
| F | Codex / lbl--cborg-coder / `20260902T192326Z-higgs-4l-significance-codex-1785193` |
| G | OpenHands / gpt-5.6-sol / `20260829T174904Z-higgs-4l-significance-openhands-1563552` |
| H | OpenHands / gpt-5.6-terra / `20260829T164001Z-higgs-4l-significance-openhands-1515494` |
| I | OpenHands / openai--lbl-cborg-coder / `20260902T201549Z-higgs-4l-significance-openhands-1286844` |
| J | Qwen Coder / google--qwen-3--best / `20260829T173916Z-higgs-4l-significance-qwen-coder-1554570` |
| K | Qwen Coder / google--qwen-3--medium / `20260829T163057Z-higgs-4l-significance-qwen-coder-1506981` |
| L | Qwen Coder / lbl--cborg-coder / `20260902T192318Z-higgs-4l-significance-qwen-coder-1513207` |
| M | Terminus 2 / gpt-5.6-sol / `20260829T173058Z-higgs-4l-significance-terminus-2-1543955` |
| N | Terminus 2 / gpt-5.6-terra / `20260829T162334Z-higgs-4l-significance-terminus-2-1496619` |
| O | Terminus 2 / openai--lbl-cborg-coder / `20260902T192401Z-higgs-4l-significance-terminus-2-1410561` |

Excluded: each `.../<run>/<trial-id>/result.json` is the trial-level record
already represented by its outer bundle; it is not double counted. `job.log`,
`agent/`, wrapper logs, `artifacts/manifest.json`, and convenience plot/source
paths are evidence within those 15 bundles, not logical runs. No superseded
bundle occurs under this evidence root.

### Evidence notation

`R` means the run's retained `artifacts/root/results/results.json`; `S` means
its readable `artifacts/root/submission/{analysis.py|analyze.py|run.sh|README.md}`;
`T` means `agent/{trajectory.json,*.trajectory.json,*.txt}`; and `H` means the
outer bundle `result.json`. A reference is exact when combined with the run key
above, e.g. `D/R:test_statistic`. Only the policy statuses are used below:
`P` is pass, `F` is fail, and `M` is missing. Missing includes unavailable,
unreadable, or insufficient evidence; it does not infer that work was absent.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| A | 19 | 0 | 13 | completed / 1.000000 |
| B | 18 | 0 | 14 | completed / 1.000000 |
| C | 15 | 0 | 17 | completed / 0.950000 |
| D | 20 | 0 | 12 | completed / 1.000000 |
| E | 19 | 0 | 13 | completed / 1.000000 |
| F | 15 | 0 | 17 | completed / 0.950000 |
| G | 5 | 0 | 27 | completed / 0.000000 |
| H | 5 | 0 | 27 | completed / 0.000000 |
| I | 15 | 1 | 16 | completed / 0.950000 |
| J | 13 | 3 | 16 | completed / 0.587500 |
| K | 13 | 3 | 16 | completed / 0.750000 |
| L | 13 | 3 | 16 | completed / 0.687500 |
| M | 19 | 0 | 13 | completed / 1.000000 |
| N | 20 | 0 | 12 | completed / 1.000000 |
| O | 15 | 1 | 16 | completed / 0.700000 |

## Total reward (raw, no averaging)

| Summary | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total reward / 32 | 19 | 18 | 15 | 20 | 19 | 15 | 5 | 5 | 15 | 13 | 13 | 13 | 19 | 20 | 15 |

## Overall equal-category reward

| Summary | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Overall equal-category reward | 0.58 | 0.56 | 0.47 | 0.61 | 0.58 | 0.47 | 0.19 | 0.19 | 0.45 | 0.39 | 0.39 | 0.39 | 0.58 | 0.61 | 0.45 |

The equal-category number is the arithmetic mean of the seven group pass
fractions (groups have 3, 6, 7, 6, 4, 3, and 3 criteria). It is a descriptive
manual-rubric calculation, not an authoritative physics score.

## Per-question binary rewards

Cells are `P=1`, `F/M=0`. The following compact matrix gives every
criterion/run status; the subsequent table gives the observed values, direct
evidence location, and reason for every status class.

| Q | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 2 | P | P | P | P | P | M | M | M | M | M | M | M | P | P | M |
| 3 | P | P | P | P | P | P | M | M | M | P | P | P | P | P | P |
| 4 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 5 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 6 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 7 | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| 8 | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| 9 | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| 10 | P | P | M | P | P | M | M | M | P | M | M | M | P | P | M |
| 11 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 12 | P | P | M | P | P | M | P | P | F | F | F | F | P | P | F |
| 13 | P | P | M | P | P | M | M | M | M | M | M | M | P | P | M |
| 14 | P | M | M | P | P | M | M | M | M | M | M | M | M | M | M |
| 15 | P | P | P | P | P | P | M | M | P | P | P | P | P | P | P |
| 16 | P | P | M | M | M | M | M | M | M | M | M | M | P | P | M |
| 17 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 18 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 19 | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 20 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 21 | P | P | M | M | M | M | M | M | M | M | M | M | P | P | M |
| 22 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 23 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 24 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 25 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 26 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 27 | P | M | M | M | M | M | M | M | P | P | P | P | M | P | M |
| 28 | P | M | M | M | M | M | M | M | P | P | P | P | M | P | M |
| 29 | P | M | M | M | M | M | M | M | P | P | P | P | M | P | M |
| 30 | P | M | M | P | P | M | M | M | M | M | M | M | P | P | M |
| 31 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |
| 32 | M | M | M | M | M | M | M | M | M | M | M | M | M | M | M |

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

The evidence references above are deliberately bundle-relative. For example,
`A/R` expands to the A bundle's
`20260829T171737Z-higgs-4l-signif__qUE9b6C/artifacts/root/results/results.json`;
all other keys expand analogously from the included-run table. This preserves
exact, navigable locations without repeating 15 long paths in every cell.
