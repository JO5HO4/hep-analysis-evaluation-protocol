# Manual evidence review — higgs-4l

Non-authoritative single-run review under `evaluation/higgs_4l.md` and `evaluation/evaluation_rubric.md`. Reviewed 2026-09-09. Run: `higgs-4l / terminus-2 / gpt-5.6-terra / 20260829T162334Z-higgs-4l-significance-terminus-2-1496619`.

The readable artifact root was fully inventoried before assessment: job/trial result metadata and configuration, job/trial logs, terminal pane and trajectory, verifier records, artifact manifest, submitted launcher/source/README, executed JSON result, and both PNG diagnostics. The root contains no CSV, Parquet, ROOT workspace, additional table, or standalone report. Searches of those sources found no same-visible-input evaluator reference calculation; `verifier/score_report.json` is an execution on a different hidden input and is context rather than Q23–Q26 evidence.

## 1. Status Summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus 2 / gpt-5.6-terra | 25 | 0 | 7 | completed / 1.000000 |

## 2. Total Reward (Raw, No Averaging)

| Summary | Terminus 2 / gpt-5.6-terra |
|---|---:|
| Total reward | 25 / 32 |

## 3. Overall Equal-Category Reward

| Summary | Terminus 2 / gpt-5.6-terra |
|---|---:|
| Overall equal-category reward | 0.741497 |

`(3/3 + 6/6 + 6/7 + 6/6 + 0/4 + 3/3 + 1/3) / 7`.

## 4. Per-Question Binary Rewards

| Category | Question | Terminus 2 / gpt-5.6-terra |
|---|---|---:|
| I | Q1 Run timing | 1 |
| I | Q2 Run cost | 1 |
| I | Q3 Analysis documentation | 1 |
| II | Q4 Input generality | 1 |
| II | Q5 Poisson likelihood | 1 |
| II | Q6 Channel combination | 1 |
| II | Q7 Likelihood values | 1 |
| II | Q8 Observed test statistic | 1 |
| II | Q9 Input preservation | 1 |
| III | Q10 Toy count | 1 |
| III | Q11 Toy hypothesis | 1 |
| III | Q12 Tail convention | 1 |
| III | Q13 Toy p-value | 1 |
| III | Q14 Toy statistical uncertainty | 0 |
| III | Q15 Gaussian significance | 1 |
| III | Q16 Evidence conclusion | 1 |
| IV | Q17 Signal-strength model | 1 |
| IV | Q18 Best-fit strength | 1 |
| IV | Q19 Profile definition | 1 |
| IV | Q20 One-sigma crossings | 1 |
| IV | Q21 Asymmetric interval | 1 |
| IV | Q22 Boundary handling | 1 |
| V | Q23 Likelihood reference agreement | 0 |
| V | Q24 Toy p-value consistency | 0 |
| V | Q25 Significance reference agreement | 0 |
| V | Q26 Signal-strength reference agreement | 0 |
| VI | Q27 Toy-test-statistic diagnostic | 1 |
| VI | Q28 Profile diagnostic | 1 |
| VI | Q29 Plot normalization | 1 |
| VII | Q30 Randomness control | 1 |
| VII | Q31 Final configuration | 0 |
| VII | Q32 Numerical validity checks | 0 |

## 5. Per-Question Observed Values and Rewards

| Category | Question | Terminus 2 / gpt-5.6-terra |
|---|---|---|
| I | Q1 | wall 264.120730 s; agent 89.706017 s [1] |
| I | Q2 | $0.08077993 USD [1] |
| I | Q3 | runnable README; likelihood, toys, μ scan [1] |
| II | Q4 | `n=len(observed)` and equal-length validation [1] |
| II | Q5 | `Σ(-λ+k logλ-gammaln(k+1))` [1] |
| II | Q6 | vectorized sum over all arrays [1] |
| II | Q7 | −11.0827503203; −5.8159224919 [1] |
| II | Q8 | q=−10.5336556567; identity residual 0 [1] |
| II | Q9 | all input vector entries consumed once [1] |
| III | Q10 | N=1,000,000 [1] |
| III | Q11 | independent `poisson(background)` draws [1] |
| III | Q12 | `q_toy <= q_observed` [1] |
| III | Q13 | 212/1,000,000=0.000212 [1] |
| III | Q14 | uncertainty/interval not reported [0] |
| III | Q15 | Z=3.5246766534 [1] |
| III | Q16 | `evidence_at_3sigma=true`; Z≥3 [1] |
| IV | Q17 | λ=b+μs; μ≥0 [1] |
| IV | Q18 | μhat=1.6238865611 [1] |
| IV | Q19 | −2ΔlogL relative to fitted minimum [1] |
| IV | Q20 | μlo=1.0089693335; μhi=2.3666431666 [1] |
| IV | Q21 | −0.6149172276, +0.7427566055 [1] |
| IV | Q22 | interior lower crossing, not boundary-limited [1] |
| V | Q23 | same-input reference unavailable [0] |
| V | Q24 | same-input tail reference unavailable [0] |
| V | Q25 | same-input Z reference unavailable [0] |
| V | Q26 | same-input profile reference unavailable [0] |
| VI | Q27 | 100-bin density toy-q histogram + q marker [1] |
| VI | Q28 | 800-point −2ΔlogL scan with y=1 [1] |
| VI | Q29 | histogram normalized density [1] |
| VII | Q30 | `default_rng`, seed 20250308 [1] |
| VII | Q31 | versions absent from preserved evidence [0] |
| VII | Q32 | no explicit non-finite-likelihood/crossing checks [0] |

## 6. Per-Question Evidence and Reasoning

### Group I — Execution and Documentation

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q1 | `agent_execution` is 89.706017 s and trial elapsed time is 264.120730 s [pass]. `trial/result.json: agent_execution, started_at, finished_at`. |
| Q2 | `cost_usd=0.08077993000000001` [pass]. Top-level and trial `result.json`. |
| Q3 | The README supplies launcher, Poisson likelihood, toy-tail, significance, and μ-profile assumptions [pass]. `artifacts/root/submission/README.md`, `run.sh`, `analyze.py`. |

### Group II — Input and Likelihood Construction

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q4 | The code derives `n=len(observed)` and rejects unequal/nonempty arrays, without a fixed channel number [pass]. `analyze.py:main`. |
| Q5 | `loglike` computes `-mean + observed*log(mean) - gammaln(observed+1)` [pass]. `analyze.py:loglike`. |
| Q6 | `np.sum` combines the vector likelihood terms [pass]. `analyze.py:loglike`. |
| Q7 | Executed finite values are `logL_b=-11.082750320271758`, `logL_sb=-5.8159224919108095` [pass]. `artifacts/root/results/results.json`. |
| Q8 | `q=-10.533655656721898`; substituting the two saved likelihoods gives zero residual in `q+2(logL_sb-logL_b)` [pass]. `results.json`, `analyze.py:q_obs`. |
| Q9 | No masking, slicing, or aggregation occurs between input arrays and vectorized likelihood/toy operations [pass]. `analyze.py`; executed result in `results.json`. |

### Group III — Background-Only Toy Significance

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q10 | `n_toys=1000000` [pass]. `results.json`. |
| Q11 | Each batch is generated with `rng.poisson(background, size=(m,n))` [pass]. `analyze.py`. |
| Q12 | Tail count is `count_nonzero(q_toys <= q_obs)`; README defines lower q as signal-like [pass]. `analyze.py`, `README.md`. |
| Q13 | Saved direct calculation is `n_signal_like_toys=212`, `n_toys=1000000`, `p_value=0.000212` [pass]. `results.json`. |
| Q14 | No binomial standard error or interval is given in the result, README, source, trajectory, verifier output, or plots [missing]. The readable sources searched report only count, denominator, and p-value. |
| Q15 | Saved `Z=3.5246766533968237`; source applies `ndtri(1-p_value)` [pass]. `results.json`, `analyze.py`. |
| Q16 | `evidence_at_3sigma=true` and Z is 3.5246766534 [pass]. `results.json`. |

### Group IV — Signal-Strength Profile

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q17 | Means are `background + mu*signal`; optimizer bounds start at 0 [pass]. `analyze.py:loglike, minimize_scalar`. |
| Q18 | Finite `mu_hat=1.6238865611147593` comes from bounded scalar minimization of negative log likelihood [pass]. `results.json`, `analyze.py`. |
| Q19 | `profile=-2*(loglike(mu)-ll_hat)` and `ll_hat` is the fitted maximum [pass]. `analyze.py`. |
| Q20 | Saved endpoints bracket μhat; `brentq` solves `loglike(mu)-(ll_hat-0.5)=0` with `xtol=1e-12`, which establishes profile=1 [pass]. `results.json`, `analyze.py`. |
| Q21 | Saved asymmetric uncertainties are `0.6149172275751937` below and `0.7427566054804227` above [pass]. `results.json`. |
| Q22 | The code and README specify `mu_lo=0` only if the physical boundary remains within one unit; saved `mu_lo=1.0089693335` establishes this run's interior endpoint [pass]. `analyze.py`, `README.md`, `results.json`. |

### Group V — Evaluator Reference Comparison

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q23 | Same-visible-input evaluator likelihood/q reference is absent [missing]. Metadata, logs, trajectory, source, output, plots, and verifier were searched; verifier q=−3.345276… is from a different hidden input. |
| Q24 | Same-visible-input evaluator tail probability is absent [missing]. Submission p=0.000212 and verifier p=0.030322 describe different inputs. |
| Q25 | Same-visible-input evaluator p-to-Z reference is absent [missing]. Verifier Z=1.876082… is a hidden-input result. |
| Q26 | Same-visible-input evaluator profile reference is absent [missing]. Verifier `(mu_hat,mu_lo,mu_hi)=(1.033991,0.420891,1.770226)` is a hidden-input result. |

### Group VI — Plotting and Presentation Quality

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q27 | Source produces a 100-bin background-only q distribution and `axvline(q_obs)`; preserved PNG is 1050×675 [pass]. `analyze.py`; `diagnostics/test_statistic_toys.png`. |
| Q28 | Source creates an 800-point finite profile scan, y=1 line, and crossing markers; preserved PNG is 1050×675 [pass]. `analyze.py`; `diagnostics/mu_profile.png`. |
| Q29 | `ax.hist(..., density=True)` and y-label `Density` establish normalized-density units [pass]. `analyze.py:test_statistic_toys plot`. |

### Group VII — Validation and Reproducibility

| Question | Terminus 2 / gpt-5.6-terra |
|---|---|
| Q30 | `np.random.default_rng(SEED)`, `SEED=20250308`, and saved `toy_seed=20250308` [pass]. `analyze.py`, `results.json`. |
| Q31 | N=1,000,000, seed/RNG, profile scan construction (800 points and dynamic upper bound), and `xatol=1e-12` are present, but NumPy/SciPy/Matplotlib versions are absent from all readable metadata, logs, source, output, and README [missing]. |
| Q32 | Input checks reject nonpositive means and invalid counts, but the source contains no explicit non-finite likelihood check and no explicit failed-crossing check beyond allowing solver exceptions [missing]. `analyze.py`; trajectory and output searched. |
