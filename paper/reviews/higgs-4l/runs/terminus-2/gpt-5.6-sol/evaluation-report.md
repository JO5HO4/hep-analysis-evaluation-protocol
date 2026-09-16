# Manual evidence review — higgs-4l

Non-authoritative single-run review under `evaluation/higgs_4l.md` and the shared evidence policy. Reviewed 2026-09-09. Run: `higgs-4l / terminus-2 / gpt-5.6-sol / 20260829T173058Z-higgs-4l-significance-terminus-2-1543955`.

The readable bundle was completely inventoried: metadata/configuration, job/trial logs, terminal pane/trajectory, verifier output, README/source/launcher, executed `results.json`, and both PNG diagnostics. No CSV, Parquet, ROOT workspace, or separate report was present. Verifier values are a separate hidden-input execution, not same-input references for Q23–Q26.

## 1. Status Summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus 2 / gpt-5.6-sol | 26 | 0 | 6 | completed / 1.000000 |

## 2. Total Reward (Raw, No Averaging)

| Summary | Terminus 2 / gpt-5.6-sol |
|---|---:|
| Total reward | 26 / 32 |

## 3. Overall Equal-Category Reward

| Summary | Terminus 2 / gpt-5.6-sol |
|---|---:|
| Overall equal-category reward | 0.789116 |

`(3/3 + 6/6 + 6/7 + 6/6 + 0/4 + 3/3 + 2/3) / 7`.

## 4. Per-Question Binary Rewards

| Category | Question | Terminus 2 / gpt-5.6-sol |
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
| VII | Q31 Final configuration | 1 |
| VII | Q32 Numerical validity checks | 0 |

## 5. Per-Question Observed Values and Rewards

| Category | Question | Terminus 2 / gpt-5.6-sol |
|---|---|---|
| I | Q1 | wall 329.009 s; agent 112.195 s [1] |
| I | Q2 | $0.25772945 USD [1] |
| I | Q3 | runnable README, likelihood/toys/profile [1] |
| II | Q4 | `n=len(channels)` [1] |
| II | Q5 | `Σ(-λ+k logλ-gammaln(k+1))` [1] |
| II | Q6 | sum over all channels [1] |
| II | Q7 | −11.0827503203; −5.8159224919 [1] |
| II | Q8 | q=−10.5336556567; residual 0 [1] |
| II | Q9 | 3 channels used once [1] |
| III | Q10 | N=1,000,000 [1] |
| III | Q11 | independent background Poisson draws [1] |
| III | Q12 | `q_toy <= q_observed` [1] |
| III | Q13 | 258/1,000,000=0.000258 [1] |
| III | Q14 | uncertainty/interval not reported [0] |
| III | Q15 | Z=3.4723100619 [1] |
| III | Q16 | evidence=true and Z≥3 [1] |
| IV | Q17 | λ=b+μs, μ≥0 [1] |
| IV | Q18 | μhat=1.6238865855 [1] |
| IV | Q19 | −2ΔlogL relative to minimum [1] |
| IV | Q20 | μlo=1.0089693335; μhi=2.3666431666 [1] |
| IV | Q21 | −0.6149172519, +0.7427565811 [1] |
| IV | Q22 | boundary rule documented [1] |
| V | Q23 | same-input reference unavailable [0] |
| V | Q24 | same-input tail reference unavailable [0] |
| V | Q25 | same-input Z reference unavailable [0] |
| V | Q26 | same-input profile reference unavailable [0] |
| VI | Q27 | 100-bin toy-q histogram + marker [1] |
| VI | Q28 | finite 600-point profile; y=1 [1] |
| VI | Q29 | toys/bin count normalization [1] |
| VII | Q30 | default_rng seed 123456789 [1] |
| VII | Q31 | N, RNG/seed, xatol, package versions [1] |
| VII | Q32 | no explicit non-finite likelihood check [0] |

## 6. Per-Question Evidence and Reasoning

### Group I — Execution and Documentation

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q1 | `112.194795 s` agent execution and `329.009400 s` wall time [pass]. Trial `result.json: agent_execution, started_at, finished_at`. |
| Q2 | `cost_usd=0.25772945` [pass]. Top-level and trial `result.json`. |
| Q3 | Launcher plus likelihood, toys, profile, and assumptions documented [pass]. `submission/README.md`, `run.sh`, `analyze.py`. |

### Group II — Input and Likelihood Construction

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q4 | `validate` derives `n` from channels and requires matching arrays [pass]. `analyze.py:validate`. |
| Q5 | Stable Poisson log likelihood uses `gammaln(counts+1)` [pass]. `analyze.py:loglike`. |
| Q6 | `np.sum` combines every channel [pass]. `analyze.py:loglike`. |
| Q7 | Finite executed `logL_b=-11.082750320271758`, `logL_sb=-5.8159224919108095` [pass]. `results.json`. |
| Q8 | q=−10.533655656721898 and identity residual is zero [pass]. `results.json`, `analyze.py:q_obs`. |
| Q9 | Transcript gives 3 channels; vectorized source consumes all entries once [pass]. `agent/terminus_2.pane`, `analyze.py`. |

### Group III — Background-Only Toy Significance

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q10 | `n_toys=1000000` [pass]. `results.json`. |
| Q11 | `rng.poisson(bkg, size=(m,len(bkg)))` [pass]. `analyze.py`. |
| Q12 | `qvals <= q_obs + 1e-12`; README defines smaller q signal-like [pass]. Source and README. |
| Q13 | `258/1000000=0.000258` [pass]. `results.json`. |
| Q14 | No binomial SE/interval in output, README, source, transcript, verifier, or plots [missing]. |
| Q15 | `Z=3.4723100618884772`; source uses `norm.isf(p_value)` [pass]. Output/source. |
| Q16 | `reaches_3sigma_evidence=true`, matching Z≥3 [pass]. `results.json`. |

### Group IV — Signal-Strength Profile

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q17 | `bkg+mu*sig`, bounded at zero [pass]. `analyze.py:nll2,minimize_scalar`. |
| Q18 | finite μhat=1.6238865854853561 from bounded minimum [pass]. Output/source. |
| Q19 | profile is `nll2(mu)-min_nll2`, zero at μhat [pass]. `analyze.py`. |
| Q20 | endpoints bracket μhat; transcript asserts each −2ΔlogL=1 to <1e−8 [pass]. Output/pane. |
| Q21 | finite −0.6149172519457902 and +0.7427565811097685 [pass]. `results.json`. |
| Q22 | missing physical lower crossing explicitly maps to μlo=0; this run is interior [pass]. README/source. |

### Group V — Evaluator Reference Comparison

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q23 | Same-input evaluator likelihood/q reference absent [missing]. All bundle sources searched; verifier q=−3.345276… is different hidden input. |
| Q24 | Same-input evaluator tail probability absent [missing]. Submission p=0.000258 and verifier p=0.030459 are different-input values. |
| Q25 | Same-input p-to-Z reference absent [missing]; verifier Z=1.874090 is different input. |
| Q26 | Same-input profile reference absent [missing]; verifier `(1.033991,0.420891,1.770226)` is different input. |

### Group VI — Plotting and Presentation Quality

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q27 | 100-bin background toy-q distribution and observed-q line are produced [pass]. `analyze.py`, `diagnostics/test_statistic_distribution.png`, pane. |
| Q28 | Finite 600-point −2ΔlogL scan and y=1 line are produced [pass]. `analyze.py`, `diagnostics/mu_profile_likelihood.png`. |
| Q29 | Toy histogram y-axis is `Background-only toys / bin` [pass]. Source/PNG. |

### Group VII — Validation and Reproducibility

| Question | Terminus 2 / gpt-5.6-sol |
|---|---|
| Q30 | `np.random.default_rng(SEED)`, `SEED=123456789`, saved as `toy_seed` [pass]. Source/output. |
| Q31 | N, RNG/seed, optimizer xatol=1e−12, NumPy 2.1.3, SciPy 1.14.1, Matplotlib 3.9.2 [pass]. Source/pane. |
| Q32 | Input validation covers invalid means and non-finite inputs; bracketing failure is checked, but no explicit non-finite likelihood check exists [missing]. Source/output/transcript searched. |
