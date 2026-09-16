# Manual evidence review — Higgs four-lepton

Non-authoritative review of exactly one preserved trial, generated 2026-09-09.

Run: `higgs-4l / claude-code / claude-opus-5 / 20260829T171737Z-higgs-4l-signif__qUE9b6C`. Harbor context: `completed / 1.000000`; this is neither a rubric reward nor an outcome grade.

## Evidence scope

The readable run root was enumerated completely: run/trial metadata and logs; agent transcript and trajectory; verifier reward, CTRF, stdout, and score report; source (`analysis.py`, `plots.py`, `run.sh`, `README.md`); produced `results.json`; and two PNGs. `artifacts/manifest.json` records `/logs/artifacts` empty. No readable CSV, Parquet, workspace, or separate report artifact exists. Both PNGs are valid 1440×832 RGBA files. Missing decisions below follow searches of this inventory, not a filename assumption.

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / claude-opus-5 | 28 | 1 | 3 | completed / 1.000000 |

## 2. Total reward (raw, no averaging)

| Summary | Claude Code / claude-opus-5 |
|---|---:|
| Total reward | 28 / 32 |

## 3. Overall equal-category reward

| Summary | Claude Code / claude-opus-5 |
|---|---:|
| Overall equal-category reward | 0.8690 |

`(3/3 + 6/6 + 7/7 + 4/6 + 3/4 + 3/3 + 2/3) / 7 = 73/84`.

## 4. Per-question binary rewards

| Category | Question | Claude Code / claude-opus-5 |
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
| III | Q14 Toy uncertainty | 1 |
| III | Q15 Gaussian significance | 1 |
| III | Q16 Evidence conclusion | 1 |
| IV | Q17 Signal-strength model/domain | 0 |
| IV | Q18 Best-fit strength | 1 |
| IV | Q19 Profile definition | 1 |
| IV | Q20 One-sigma crossings | 1 |
| IV | Q21 Asymmetric interval | 1 |
| IV | Q22 Boundary handling | 0 |
| V | Q23 Likelihood reference agreement | 1 |
| V | Q24 Toy p-value consistency | 0 |
| V | Q25 Significance reference agreement | 1 |
| V | Q26 Signal-strength reference agreement | 1 |
| VI | Q27 Toy-statistic diagnostic | 1 |
| VI | Q28 Profile diagnostic | 1 |
| VI | Q29 Plot normalization | 1 |
| VII | Q30 Randomness control | 1 |
| VII | Q31 Final configuration | 1 |
| VII | Q32 Numerical validity checks | 0 |

## 5. Per-question observed values and rewards

| Category | Question | Claude Code / claude-opus-5 |
|---|---|---|
| I | Q1 | wall 615.938 s; agent 429.290 s [1] |
| I | Q2 | $5.3911 USD [1] |
| I | Q3 | runnable likelihood/toy/scan method [1] |
| II | Q4 | `len(n)`-driven channels [1] |
| II | Q5 | `-λ+k log λ-gammaln(k+1)` [1] |
| II | Q6 | independent-channel sum [1] |
| II | Q7 | −11.0827503203; −5.8159224919 [1] |
| II | Q8 | q −10.5336556567; residual 0 [1] |
| II | Q9 | three inputs, used once [1] |
| III | Q10 | 10,000,000 [1] |
| III | Q11 | `Poisson(b_i)` [1] |
| III | Q12 | `q_toy <= q_obs + tol` [1] |
| III | Q13 | 0.000259 = 2,590/10,000,000 [1] |
| III | Q14 | 5.088545e-06 [1] |
| III | Q15 | Z 3.4712714882 [1] |
| III | Q16 | evidence=true [1] |
| IV | Q17 | μ > max(−b/s), not μ≥0 [0] |
| IV | Q18 | μhat 1.6238865885 [1] |
| IV | Q19 | qmin −11.566366593; zero at μhat [1] |
| IV | Q20 | [1.0089693335, 2.3666431666], crossings=1 [1] |
| IV | Q21 | −0.6149172549, +0.7427565781 [1] |
| IV | Q22 | not established [0] |
| V | Q23 | verifier test all deltas 0 [1] |
| V | Q24 | p values present; same-input N/count absent [0] |
| V | Q25 | |ΔZ|=0.0019722591 [1] |
| V | Q26 | all |Δμ|<2.3e-4 [1] |
| VI | Q27 | q density + observed marker [1] |
| VI | Q28 | 900-point profile, level 1 [1] |
| VI | Q29 | probability density [1] |
| VII | Q30 | `default_rng(20260829)` [1] |
| VII | Q31 | N, seed, batch, tolerances, versions [1] |
| VII | Q32 | only b<=0 check established [0] |

## 6. Per-question evidence and reasoning

### I. Execution and documentation

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q1 | `pass`: trial `result.json` timestamps establish 615.938056 s wall and 429.290428 s agent execution. |
| Q2 | `pass`: `result.json: agent_result.cost_usd=$5.391100000000001`. |
| Q3 | `pass`: submission `README.md` documents runnable command, likelihood, toys, and scan. |

### II. Input and likelihood construction

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q4 | `pass`: `analysis.py: analyse`/`run_toys` use JSON arrays and `len(n/b)`; no fixed count. |
| Q5 | `pass`: `analysis.py: log_poisson` is `-lam+k*log(lam)-gammaln(k+1)`. |
| Q6 | `pass`: `total_logL` is `np.sum` over channels. |
| Q7 | `pass`: produced JSON gives finite logL_b/logL_sb as above. |
| Q8 | `pass`: q + 2(logL_sb−logL_b)=0 to shown precision. |
| Q9 | `pass`: produced JSON echoes three channels and all three vectors; vector code consumes each once. |

### III. Background-only toy significance

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q10 | `pass`: `results.json: n_toys=10000000`. |
| Q11 | `pass`: `run_toys` uses `rng.poisson(b, size=(n,len(b)))`. |
| Q12 | `pass`: `np.count_nonzero(q <= q_obs + tol)`; README defines left tail. |
| Q13 | `pass`: p=0.000259, 2,590/10,000,000. |
| Q14 | `pass`: reported binomial SE=5.088545165368978e-06. |
| Q15 | `pass`: source `norm.isf(p_for_z)`; output Z=3.471271488167002. |
| Q16 | `pass`: `evidence_3sigma=true`, consistent with Z≥3. |

### IV. Signal-strength profile

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q17 | `fail`: `q_of_mu` uses λ=μs+b, but `mu_scan` lower-bounds μ at `max(-b/s)+epsilon`, allowing negative μ; this directly contradicts required μ≥0. |
| Q18 | `pass`: output μhat=1.6238865884773688 from bounded `minimize_scalar`. |
| Q19 | `pass`: source `delta=f(mu)-q_min-1`; profile is zero at fit. |
| Q20 | `pass`: output endpoints above; `brentq(delta)=0` establishes profile=1. |
| Q21 | `pass`: produced asymmetric nonnegative errors above. |
| Q22 | `missing`: searched source, README, results, transcript, logs, and verifier material. They state a nonzero-mean floor, not whether μlo=0 is a boundary-limited endpoint under μ≥0. |

### V. Evaluator reference comparison

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q23 | `pass`: `verifier/score_report.json` has identical agent/reference logL_b −7.951245680204405, logL_sb −6.278607590251635, q −3.3452761799055395; deltas 0. |
| Q24 | `missing`: score report has agent/reference p=0.0302033/0.0303385 but lacks same-input N/tail count. Searched all result/source/README/transcript/verifier outputs and tables; saved N/count are for a different input. No 99.7% interval is constructible. |
| Q25 | `pass`: verifier Z 1.8778141050826298 vs reference 1.8758418459887942; |Δ|=0.001972259094<0.02. |
| Q26 | `pass`: verifier μhat 1.0339912919/1.034, μlo .4208908423/.421, μhi 1.7702256921/1.770; all deltas <.02. |

### VI. Plotting and presentation

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q27 | `pass`: readable test-statistic PNG; `plots.py` makes B-only/S+B q density histograms and observed-q vertical marker. |
| Q28 | `pass`: readable μ PNG; `plots.py` makes 900-point −2ΔlogL scan and y=1 line. |
| Q29 | `pass`: histogram is normalized by samples and bin width and labeled `probability density`. |

### VII. Validation and reproducibility

| Question | Claude Code / claude-opus-5 |
|---|---|
| Q30 | `pass`: `np.random.default_rng(seed)`; output seed 20260829. |
| Q31 | `pass`: source sets N=10^7, seed 20260829, batch=2e6, xatol=1e-10, xtol=1e-12; transcript records NumPy 2.1.3, SciPy 1.14.1, Matplotlib 3.9.2. |
| Q32 | `missing`: full source/result/log inventory establishes only `background <= 0` guard; no checks for nonfinite likelihood/means or failed crossings (which may return NaN). |
