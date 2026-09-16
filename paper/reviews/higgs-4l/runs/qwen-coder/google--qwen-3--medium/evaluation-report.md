# Manual evidence review — Higgs 4l

Non-authoritative natural-language rubric review, generated 2026-09-09. Run: `higgs-4l / qwen-coder / google--qwen-3--medium / 20260829T163057Z-higgs-4l-significance-qwen-coder-1506981` (trial `20260829T163057Z-higgs-4l-signif__fLFVgoS`). This is review evidence, not an outcome grade. The complete readable preserved bundle was audited: job and trial metadata/configuration, Harbor/trial/agent logs, trajectory and session transcript, verifier outputs, submission source/README/run wrapper, saved result JSON, and both diagnostic PNGs. Artifact manifest records the submission directory and results JSON as `ok` and `/logs/artifacts` as empty.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Qwen Coder / google--qwen-3--medium | 19 | 3 | 10 | completed / 0.750000 |

## Total reward (raw, no averaging)

| Summary | Qwen Coder / google--qwen-3--medium |
|---|---:|
| Total reward | 19 / 32 |

## Overall equal-category reward

| Summary | Qwen Coder / google--qwen-3--medium |
|---|---:|
| Overall equal-category reward | 0.558 |

This is the mean of Group I–VII pass fractions: `2/3, 6/6, 4/7, 4/6, 0/4, 3/3, 0/3`. It is a rubric-review summary only.

## Per-question binary rewards

| Category | Question | Reward |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 0 |
| I | Q3 Analysis documentation | 1 |
| II | Q4 Input generality | 1 |
| II | Q5 Poisson likelihood | 1 |
| II | Q6 Channel combination | 1 |
| II | Q7 Likelihood values | 1 |
| II | Q8 Observed test statistic | 1 |
| II | Q9 Input preservation | 1 |
| III | Q10 Toy count | 1 |
| III | Q11 Toy hypothesis | 1 |
| III | Q12 Tail convention | 0 |
| III | Q13 Toy p-value | 0 |
| III | Q14 Toy statistical uncertainty | 0 |
| III | Q15 Gaussian significance | 1 |
| III | Q16 Evidence conclusion | 1 |
| IV | Q17 Signal-strength model | 1 |
| IV | Q18 Best-fit strength | 1 |
| IV | Q19 Profile definition | 1 |
| IV | Q20 One-sigma crossings | 0 |
| IV | Q21 Asymmetric interval | 1 |
| IV | Q22 Boundary handling | 0 |
| V | Q23 Likelihood reference agreement | 0 |
| V | Q24 Toy p-value consistency | 0 |
| V | Q25 Significance reference agreement | 0 |
| V | Q26 Signal-strength reference agreement | 0 |
| VI | Q27 Toy-test-statistic diagnostic | 1 |
| VI | Q28 Profile diagnostic | 1 |
| VI | Q29 Plot normalization | 1 |
| VII | Q30 Randomness control | 0 |
| VII | Q31 Final configuration | 0 |
| VII | Q32 Numerical validity checks | 0 |

## Per-question observed values and rewards

| Category | Question | Observed value [reward] |
|---|---|---|
| I | Q1 | trial wall `378.859 s`; agent execution `97.761 s` [1] |
| I | Q2 | `cost_usd: null` [0] |
| I | Q3 | runnable README; likelihood, toys, and scan described [1] |
| II | Q4 | reads schema arrays; no literal channel count [1] |
| II | Q5 | `-lam + k*log(lam) - sum(log(1..k))` [1] |
| II | Q6 | independent terms summed over `zip` [1] |
| II | Q7 | `logL_b=-11.0827503203`, `logL_sb=-5.8159224919` [1] |
| II | Q8 | `q=-10.5336556567 = -2(logL_sb-logL_b)` [1] |
| II | Q9 | three recorded channel entries in each input vector; used pairwise once [1] |
| III | Q10 | `n_toys=1,000,000` [1] |
| III | Q11 | `np.random.poisson(b)` for every background entry [1] |
| III | Q12 | implemented `q_toy >= q_obs`; rubric requires `<=` [0] |
| III | Q13 | `p=0.999774`; tail numerator absent [0] |
| III | Q14 | no binomial uncertainty or interval [0] |
| III | Q15 | `Z=-3.5076990897 = Phi^-1(1-0.999774)` [1] |
| III | Q16 | stated no 3-sigma evidence; `Z<3` [1] |
| IV | Q17 | `lambda=mu*s+b`, optimizer bounds `[0,5]` [1] |
| IV | Q18 | `mu_hat=1.6238865138`, bounded minimization [1] |
| IV | Q19 | scan subtracts fitted `min_q` [1] |
| IV | Q20 | `mu_lo=1.0060060060`, `mu_hi=2.3673673674`; profile values at endpoints not saved [0] |
| IV | Q21 | `-0.6178805078/+0.7434808535` about `mu_hat` [1] |
| IV | Q22 | no statement whether an endpoint is boundary limited [0] |
| V | Q23 | only readable verifier reference conflicts with saved-run apparent input [0] |
| V | Q24 | same-input reference and tail count unavailable [0] |
| V | Q25 | same-input reference conversion unavailable [0] |
| V | Q26 | same-input profile reference unavailable [0] |
| VI | Q27 | 50-bin density histogram; observed-q marker [1] |
| VI | Q28 | 1,000-point `-2 Delta logL` scan; level `1` [1] |
| VI | Q29 | histogram y-axis explicitly `Density` [1] |
| VII | Q30 | unseeded global NumPy RNG [0] |
| VII | Q31 | toys/range/resolution present; seed and package versions absent [0] |
| VII | Q32 | only `lam<=0` guard; no finite/crossing checks [0] |

## Per-question evidence and reasoning

| Question | Evidence, status, and reason |
|---|---|
| Q1 | **pass** — trial `result.json: started_at/finished_at` gives `378.858596 s`; `agent_execution` gives `97.761369 s`. Both are finite and nonnegative. |
| Q2 | **missing** — top-level `result.json: stats.cost_usd` and trial `result.json: agent_result.cost_usd` are both `null`; logs, source, result, and verifier outputs contain no USD total. |
| Q3 | **pass** — `artifacts/root/submission/README.md` documents invocation, Poisson likelihood, 10^6 toys, and profile scan. |
| Q4 | **pass** — `analysis.py: main` reads `channels`, `observed`, `background`, and `signal`; calculations iterate supplied arrays rather than a fixed count. |
| Q5 | **pass** — `analysis.py: log_poisson` implements `-lambda+k log(lambda)-log(k!)`; factorial is a numerically stable sum of logs. |
| Q6 | **pass** — `analysis.py: total_log_likelihood` sums per-channel terms; signal-plus-background construction iterates all background/signal pairs. |
| Q7 | **pass** — finite values are in `artifacts/root/results/results.json` and trajectory step 9. |
| Q8 | **pass** — saved values satisfy `q=-2(logL_sb-logL_b)` to floating-point precision; definition is `analysis.py: test_statistic`. |
| Q9 | **pass** — trajectory step 2 exposes three values for each required input vector; executed code uses those equal-length arrays through `zip` once. |
| Q10 | **pass** — trajectory step 8 records successful execution; `analysis.py: main` calls `pseudo_experiments(..., n_toys=1000000)`. |
| Q11 | **pass** — `analysis.py: pseudo_experiments` draws `np.random.poisson(b)` once for each background entry; the analysis invocation completed successfully in trajectory step 8. |
| Q12 | **fail** — `analysis.py: pseudo_experiments` explicitly computes `np.mean([q >= q_obs for q in q_toys])`, opposite the rubric's required `q_toy <= q_observed`. |
| Q13 | **missing** — `results.json` gives a finite p-value, but saved result, source output, terminal transcript, plots, and verifier material do not provide the tail numerator/count required to establish it. |
| Q14 | **missing** — no binomial uncertainty or interval appears in source, README, result, transcript, diagnostics, or verifier outputs. |
| Q15 | **pass** — finite saved `p` and `Z` agree with `Phi^-1(1-p)`; source uses `stats.norm.ppf(1-p_value)` for this p-value regime. |
| Q16 | **pass** — trajectory step 8 states “does not reach” 3 sigma and saved `Z=-3.5076990897`, consistent with the specified threshold. |
| Q17 | **pass** — `analysis.py: signal_strength_scan` defines `mu*s+b`; bounded optimization on `[0,5]` establishes `mu >= 0`. |
| Q18 | **pass** — saved finite `mu_hat` and `minimize_scalar(q_mu, bounds=(0,5), method='bounded')` establish a bounded profile minimum. |
| Q19 | **pass** — source forms `delta_q(mu)=q_mu(mu)-min_q`, with `min_q=result.fun`, so the profile is relative to the fitted minimum. |
| Q20 | **missing** — saved endpoints are finite and ordered, but no profile array/value at either endpoint is preserved. Source establishes only a grid search with `delta_q >= 1`, not the required within-0.01 execution values. |
| Q21 | **pass** — `results.json` directly gives finite edges; `1.6238865138-1.0060060060=0.6178805078` and `2.3673673674-1.6238865138=0.7434808535`. |
| Q22 | **missing** — README, source, result, transcript, diagnostics, and verifier outputs do not state whether a lower endpoint is boundary limited. |
| Q23 | **missing** — `verifier/score_report.json` provides reference-labelled values (`-7.9512456802`, `-6.2786075903`, `-3.3452761799`) inconsistent with this executed saved result (`-11.0827503203`, `-5.8159224919`, `-10.5336556567`) and gives no same-input provenance. No usable same-input evaluator reference is readable. |
| Q24 | **missing** — no readable same-input tail reference exists, and Q13 lacks a saved tail count. |
| Q25 | **missing** — no readable same-input evaluator p-to-Z reference exists; the verifier reference has the Q23 provenance conflict. |
| Q26 | **missing** — verifier profile references are paired with the inconsistent apparent input; no valid same-input evaluator profile reference is readable. |
| Q27 | **pass** — `analysis.py: plot_diagnostics` makes a 50-bin `density=True` toy-q histogram and an observed-q vertical line; both named PNGs are preserved under `submission/diagnostics/`. |
| Q28 | **pass** — source creates 1,000 scan values, plots `-2 Delta logL(mu)`, and draws level `1`; `signal_strength_scan.png` is preserved. |
| Q29 | **pass** — the required histogram is explicitly `density=True` with y-label `Density` in `analysis.py`; its PNG is preserved. |
| Q30 | **fail** — source uses global `np.random.poisson` with no seed/state initialization; no seed appears in transcript, README, result, environment config, or verifier outputs. |
| Q31 | **missing** — source establishes 1,000,000 toys, `[0,5]` scan range, 1,000 scan points, and bounded optimizer, but audit finds no RNG seed/algorithm or numerical package versions. |
| Q32 | **fail** — `analysis.py: log_poisson` guards only `lam<=0`; there are no non-finite-likelihood checks, optimizer-success checks, or interval-crossing validity checks. |

All missing determinations follow searches of the readable artifact root: metadata/configuration, logs, trajectory/session, submitted README/source/wrapper, results JSON, both PNG outputs, artifact manifest, and verifier materials. The Harbor reward is execution context only and has not been substituted for scientific evidence.

## Criterion-ID coverage index

Scientific rubric IDs: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32. Workflow cross-reference IDs: W1, W2, W3, W4, W5, W6; their descriptive evidence is reported in the companion workflow characterization.
