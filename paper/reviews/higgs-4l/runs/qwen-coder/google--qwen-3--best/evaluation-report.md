# Manual evidence review — Higgs 4l

Non-authoritative natural-language rubric review, generated 2026-09-09. Run: `higgs-4l / qwen-coder / google--qwen-3--best / 20260829T173916Z-higgs-4l-significance-qwen-coder-1554570` (trial `20260829T173916Z-higgs-4l-signif__eNaET5b`). This is review evidence, not an outcome grade. The complete readable preserved bundle was inventoried: metadata, Harbor/trial/agent logs, trajectory, verifier material, submitted source, README, and saved results JSON. The artifact manifest records an empty `/logs/artifacts` capture, so its generated diagnostics JSON/PNGs are established by the successful transcript but are not themselves preserved for reopening.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Qwen Coder / google--qwen-3--best | 20 | 4 | 8 | completed / 0.587500 |

## Total reward (raw, no averaging)

| Summary | Qwen Coder / google--qwen-3--best |
|---|---:|
| Total reward | 20 / 32 |

## Overall equal-category reward

| Summary | Qwen Coder / google--qwen-3--best |
|---|---:|
| Overall equal-category reward | 0.558 |

This is the mean of Group I–VII pass fractions: `2/3, 6/6, 4/7, 4/6, 0/4, 3/3, 0/3`. It is a rubric-review summary only.

## Per-question binary rewards

| Category | Question | Qwen Coder / google--qwen-3--best |
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

| Category | Question | Qwen Coder / google--qwen-3--best |
|---|---|---|
| I | Q1 | wall `441.356 s`; agent execution `205.973 s` [1] |
| I | Q2 | `cost_usd: null` [0] |
| I | Q3 | runnable README; likelihood, toys, scan stated [1] |
| II | Q4 | reads `observed/background/signal`; `zip` over arrays [1] |
| II | Q5 | `-lam + k*log(lam) - sum(log(1..k))` [1] |
| II | Q6 | `sum(... for ... in zip(...))` [1] |
| II | Q7 | `logL_b=-11.0827503203`, `logL_sb=-5.8159224919` [1] |
| II | Q8 | `q=-10.5336556567 = -2(logL_sb-logL_b)` [1] |
| II | Q9 | three equal-length recorded input arrays consumed pairwise [1] |
| III | Q10 | `n_toys=1,000,000` [1] |
| III | Q11 | `np.random.poisson(b)` per background channel [1] |
| III | Q12 | implemented `q_toy >= q_obs`; rubric requires `<=` [0] |
| III | Q13 | `p=0.999785`; tail numerator absent [0] |
| III | Q14 | no binomial uncertainty or interval [0] |
| III | Q15 | `Z=-3.5209522755 = Phi^-1(1-0.999785)` [1] |
| III | Q16 | stated no 3σ evidence; `Z<3` [1] |
| IV | Q17 | `lambda=mu*s+b`, optimizer bounds `[0,10]` [1] |
| IV | Q18 | `mu_hat=1.6238866986`, bounded minimization [1] |
| IV | Q19 | scan subtracts fitted `min_q` [1] |
| IV | Q20 | `mu_lo=0`, no established `profile(mu_lo)=1` [0] |
| IV | Q21 | `mu_hat=1.6239`, interval `[0,2.3666]`; `-1.6239/+0.7428` [1] |
| IV | Q22 | endpoint `0` but no boundary interpretation [0] |
| V | Q23 | only verifier reference is inconsistent apparent input [0] |
| V | Q24 | same-input reference/tail count unavailable [0] |
| V | Q25 | same-input reference unavailable [0] |
| V | Q26 | same-input reference unavailable [0] |
| VI | Q27 | toy histogram `density=True`, observed-q line [1] |
| VI | Q28 | finite 1,000-point `-2ΔlogL` scan; line at 1 [1] |
| VI | Q29 | toy histogram labeled Density [1] |
| VII | Q30 | unseeded global `np.random.poisson` [0] |
| VII | Q31 | toys/range/resolution present; seed and versions absent [0] |
| VII | Q32 | only `lam<=0`; no finite/crossing checks [0] |

## Per-question evidence and reasoning

| Question | Qwen Coder / google--qwen-3--best |
|---|---|
| Q1 | `pass`; trial `result.json: started_at/finished_at` gives 441.356317 s; `agent_execution` gives 205.973196 s. |
| Q2 | `missing`; top-level `result.json: stats.cost_usd` and trial `result.json: agent_result.cost_usd` are both `null`; no USD total in logs/source/results. |
| Q3 | `pass`; `artifacts/root/submission/README.md: Analysis Method, Usage` describes execution, Poisson likelihood, 10^6 toys and profile scan. |
| Q4 | `pass`; `analysis.py: main` reads schema arrays and all calculations iterate their values rather than a literal channel count. |
| Q5 | `pass`; `analysis.py: log_poisson` implements the stated Poisson log likelihood and computes `log(k!)` as a sum of logs. |
| Q6 | `pass`; `analysis.py: total_log_likelihood` sums all pairwise channel terms. |
| Q7 | `pass`; finite values are in `artifacts/root/results/results.json`. |
| Q8 | `pass`; the same JSON values satisfy the rubric identity (difference at floating-point precision); definition is in `analysis.py: test_statistic`. |
| Q9 | `pass`; trajectory step 2 records exactly three values in each input array; the executed code uses each equal-length array through `zip` once. |
| Q10 | `pass`; executed transcript (`agent/trajectory.json`, step 12) records the run, while `analysis.py: pseudo_experiments` is invoked with `n_toys=1000000`. |
| Q11 | `pass`; `analysis.py: pseudo_experiments` draws one independent `np.random.poisson(b)` for every background entry; execution completed in trajectory step 12. |
| Q12 | `fail`; `analysis.py: pseudo_experiments` explicitly uses `np.mean([q >= q_obs for q in q_toys])`, the opposite of required `q_toy <= q_observed`. |
| Q13 | `missing`; saved JSON gives finite `p_value`, but neither it, transcript, source output, nor preserved diagnostics reports the tail count/numerator. |
| Q14 | `missing`; logs, README, source, saved result, and the absent-from-capture diagnostics contain no binomial error/interval. |
| Q15 | `pass`; `results.json` gives finite p and Z; `analysis.py` uses `stats.norm.ppf(1-p_value)`, agreeing numerically. |
| Q16 | `pass`; trajectory step 12 states “does not reach” 3σ and saved `Z=-3.52095`, so the statement agrees with `Z>=3` rule. |
| Q17 | `pass`; `analysis.py: signal_strength_scan` defines `mu*s+b`; `minimize_scalar(... bounds=(0,10))` establishes physical nonnegative domain. |
| Q18 | `pass`; finite `mu_hat` is saved, and source minimizes negative log likelihood with bounded optimization. |
| Q19 | `pass`; source computes `q_mu-min_q`, with `min_q` evaluated at fitted `mu_hat`; this is zero at the fitted minimum by construction. |
| Q20 | `fail`; saved `mu_lo=0`. Source initializes it to zero and its lower-loop inequality cannot identify the descending-side crossing; no numeric crossing check is emitted. Thus both endpoints at profile 1 are directly not established, and lower endpoint is not the requested solved crossing. |
| Q21 | `pass`; saved finite edges directly give asymmetric `mu_hat-mu_lo=1.6238867` and `mu_hi-mu_hat=0.7427549`. |
| Q22 | `missing`; source defaults `mu_lo` to zero but README, transcript, output, and code do not state whether that is a boundary-limited endpoint. |
| Q23 | `missing`; `verifier/score_report.json` supplies a reference but its reported likelihoods/q (`-7.95125`, `-6.27861`, `-3.34528`) conflict with the executed saved result (`-11.08275`, `-5.81592`, `-10.53366`) and gives no same-input provenance. No valid same-input evaluator reference is readable. |
| Q24 | `missing`; no readable same-input reference tail probability, and Q13 has no tail count. |
| Q25 | `missing`; no readable same-input evaluator p-to-Z reference. |
| Q26 | `missing`; score report's profile reference is paired with the inconsistent apparent input; no readable same-input evaluator profile reference. |
| Q27 | `pass`; `plot_diagnostics.py: plot_test_statistic_distribution` constructs a 50-bin `density=True` histogram and observed-q vertical marker; trajectory step 15 records its successful PNG generation. |
| Q28 | `pass`; `analysis.py` calculates 1,000 finite scan points and `plot_diagnostics.py` plots `-2ΔlogL`, horizontal level 1; successful generation is recorded in step 15. |
| Q29 | `pass`; the only histogram (`plot_test_statistic_distribution`) is explicitly `density=True` with y label `Density`; transcript confirms it was generated. |
| Q30 | `fail`; `analysis.py` calls the unseeded global NumPy Poisson RNG; no seed or state is set in source, transcript, README, or results. |
| Q31 | `missing`; source establishes one million toys and a `[0,5]` 1,000-point scan (plus optimizer bounds), but all searched evidence lacks RNG seed/algorithm and numerical package versions. |
| Q32 | `fail`; `analysis.py` only rejects `lam<=0`; it has no checks for non-finite likelihoods, failed optimizer/crossing status, or invalid crossing output. |

The preserved `artifacts/manifest.json` and all listed readable source, result, transcript, log, verifier, and trajectory artifacts were searched before every missing determination. Verifier reward is retained as execution context only and is not substituted for rubric evidence.
