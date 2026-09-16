# Manual evidence review: Higgs → 4l significance

Non-authoritative natural-language-rubric review generated 2026-09-09 for `higgs-4l / Codex / gpt-5.6-sol / 20260829T170234Z-higgs-4l-signif__G4rVSn2`. Harbor: completed, one trial, zero errors, verifier reward `1.000000` (context only, not an outcome grade).

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / gpt-5.6-sol | 24 | 0 | 8 | completed / 1.000000 |

| Summary | Codex / gpt-5.6-sol |
|---|---:|
| Total reward (raw, no averaging) | 24 / 32 |
| Overall equal-category reward | 0.694 |

Equal-category fractions: I `2/3`; II `6/6`; III `6/7`; IV `6/6`; V `0/4`; VI `3/3`; VII `1/3`.

## Per-question binary rewards and observed values

| Category | Question | Observed value [reward] |
|---|---|---|
| I | Q1 timing | Agent time not established; job wall `323.641 s` [0] |
| I | Q2 cost | `$0.325812 USD` [1] |
| I | Q3 documentation | Runnable method, likelihood, toys, scan documented [1] |
| II | Q4 input generality | Arbitrary aligned arrays/no fixed channel count [1] |
| II | Q5 Poisson likelihood | `sum(-means+xlogy(counts,means)-gammaln(counts+1))` [1] |
| II | Q6 combination | complete `np.sum` [1] |
| II | Q7 likelihood values | `-11.0827503203`, `-5.8159224919` [1] |
| II | Q8 q definition | `-10.5336556567`, residual 0 [1] |
| II | Q9 channels | `4mu, 2e2mu, 4e` retained [1] |
| III | Q10 toys | `2,000,000` [1] |
| III | Q11 hypothesis | `rng.poisson(background,...)` [1] |
| III | Q12 tail | `q_toy <= q_observed` [1] |
| III | Q13 p value | `543/2,000,000=0.0002715` [1] |
| III | Q14 uncertainty | `1.1649598443e-05` [1] |
| III | Q15 Z | `3.4585953665=Phi^-1(1-p)` [1] |
| III | Q16 conclusion | no saved explicit evidence statement [0] |
| IV | Q17 model | `mu*signal+background`, `mu>=0` [1] |
| IV | Q18 minimum | `mu_hat=1.6238865613` [1] |
| IV | Q19 profile | `2*(logl_hat-logl(mu))` [1] |
| IV | Q20 crossings | `1.0089693335`, `2.3666431666`; root target 1 [1] |
| IV | Q21 interval | `1.6238865613 -0.6149172277 +0.7427566053` [1] |
| IV | Q22 boundary | nonzero `mu_lo`, not boundary limited [1] |
| V | Q23 likelihood reference | same-input reference unavailable [0] |
| V | Q24 p reference | same-input reference unavailable [0] |
| V | Q25 Z reference | same-input reference unavailable [0] |
| V | Q26 profile reference | same-input reference unavailable [0] |
| VI | Q27 toy plot | q histogram, count/bin, observed marker [1] |
| VI | Q28 profile plot | scan, level-1, crossings [1] |
| VI | Q29 normalization | `Pseudo-experiments per bin` [1] |
| VII | Q30 RNG | NumPy `default_rng(20260829)` [1] |
| VII | Q31 config | package versions absent [0] |
| VII | Q32 validity | no explicit finite-computed-logL check [0] |

## Evidence and reasoning

`artifacts/root/submission/analysis.py`, `run.sh`, and README establish the runnable implementation. Produced `artifacts/root/results/results.json` establishes all saved numeric values above. `analysis.py: load_counts` reads the named arrays, enforces equal length/finite valid counts and means; `log_likelihood` has the correct stable Poisson form and vector sum; toy generation samples all channel backgrounds; and profile fitting uses a physical-boundary score root and `brentq` crossings. The generated output records seed, count, tail, tail count, p-value, binomial MC error, Z, and profile endpoints.

Q1 is **missing**, not failed: top `result.json` supplies start/end timestamps only; `job.log`, `trial.log`, source/output, and verifier records supply no pure-agent duration. Q16 is **missing**: the searched result, README, source, logs, verifier stdout/report and manifest establish `Z>3` but contain no explicit “evidence” conclusion. Q23–Q26 are **missing**: `verifier/score_report.json` does show a successful separate verifier rerun/reference (`logL_b=-7.9512456802`, p=`0.030017`, profile `1.03399/0.42089/1.77023`), but these differ from the saved main-result values, so no evaluator-owned same-input comparison is preserved. Q31 is **missing** because versions are not retained. Q32 is **missing** because inputs and bracketing are checked, but computed log-likelihood finiteness is not explicitly checked.

Both required PNG diagnostics are retained and listed by verifier diagnostics. `make_diagnostics` establishes the q histogram/observed line/count-per-bin unit and 700-point profile curve/level-1/crossings.

## Artifact-root enumeration

Before missing calls, the bounded root was enumerated: top config/lock/result/job log; trial config/lock/result/log; agent transcript, trajectory and session JSONL; verifier CTRF/reward/report/stdout; artifact manifest; output JSON; README; `run.sh`; `analysis.py`; Python cache; and both PNGs. No CSV, Parquet, ROOT/fitting workspace, or other report/table is in this bundle. Missing statuses follow these concrete searches, never a preferred-filename assumption.
