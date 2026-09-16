# Manual evidence review — Higgs four-lepton significance

This is a non-authoritative, single-run manual review under `evaluation_rubric.md` and `higgs_4l.md`. Reviewed 2026-09-09. Run: `higgs-4l / Codex / gpt-5.6-terra / 20260829T160141Z-higgs-4l-signif__2b7sffY`.

The readable artifact root was completely inventoried: metadata and configuration, job/trial/agent logs, ATIF trajectory, verifier output, submission source and README, `results.json`, and both PNG diagnostics. There are no CSV, Parquet, ROOT workspace, or separate report artifacts in the inventory. The verifier report is retained as context only: it exercised a different hidden input, so it cannot supply the same-input evaluator references required by Q23–Q26.

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / gpt-5.6-terra | 28 | 0 | 4 | completed / 1.000000 |

## 2. Total reward (raw, no averaging)

| Summary | Codex / gpt-5.6-terra |
|---|---:|
| Total reward | 28 / 32 |

## 3. Overall equal-category reward

| Summary | Codex / gpt-5.6-terra |
|---|---:|
| Overall equal-category reward | 0.857143 |

Arithmetic mean of group pass fractions: `(3/3 + 6/6 + 7/7 + 6/6 + 0/4 + 3/3 + 3/3) / 7`.

## 4. Per-question binary rewards

| Category | Question | Codex / gpt-5.6-terra |
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
| III | Q14 Toy statistical uncertainty | 1 |
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
| VII | Q32 Numerical validity checks | 1 |

## 5. Per-question observed values and rewards

| Category | Question | Codex / gpt-5.6-terra |
|---|---|---|
| I | Q1 | trial wall 322.822 s; agent execution 105.108 s [1] |
| I | Q2 | $0.1782162 USD [1] |
| I | Q3 | runnable README; likelihood, toys, scan documented [1] |
| II | Q4 | schema arrays; `n=len(channels)` [1] |
| II | Q5 | `-λ+k log λ-gammaln(k+1)` [1] |
| II | Q6 | `np.sum` over all channels [1] |
| II | Q7 | `-11.0827503203`, `-5.8159224919` [1] |
| II | Q8 | q `-10.5336556567`; identity residual 0 [1] |
| II | Q9 | 3 input labels, 3 result labels; equal-length check [1] |
| III | Q10 | 2,000,000 toys [1] |
| III | Q11 | `rng.poisson(background, size=(current, background.size))` [1] |
| III | Q12 | `q_toy <= q_observed + 1e-12` [1] |
| III | Q13 | 579 / 2,000,000 = 0.0002895 [1] |
| III | Q14 | binomial SE `1.202946777e-05` [1] |
| III | Q15 | Z `3.4412655472 = ndtri(1-p)` [1] |
| III | Q16 | `Z=3.4413σ`; reaches 3σ [1] |
| IV | Q17 | `λ=b+μs`, bounded `μ>=0` [1] |
| IV | Q18 | `μhat=1.6238865850`, bounded minimization [1] |
| IV | Q19 | `-2(logL(μ)-logLhat)` [1] |
| IV | Q20 | `[1.0089693335, 2.3666431666]`, brentq at 1 [1] |
| IV | Q21 | `+0.7427565816`, `-0.6149172515` [1] |
| IV | Q22 | lower-boundary rule explicitly stated [1] |
| V | Q23 | same-input evaluator `logL_b`, `logL_sb`, q reference unavailable [0] |
| V | Q24 | same-input evaluator p-value unavailable [0] |
| V | Q25 | same-input evaluator p-to-Z reference unavailable [0] |
| V | Q26 | same-input evaluator profile reference unavailable [0] |
| VI | Q27 | readable q-density plot, observed-q marker [1] |
| VI | Q28 | readable `-2ΔlogL(μ)` scan, level 1 [1] |
| VI | Q29 | toy histogram is probability density; profile is a curve [1] |
| VII | Q30 | NumPy `default_rng(20260829)` [1] |
| VII | Q31 | 2M, seed, 800 points, `xatol=1e-12`; NumPy 2.1.3 / SciPy 1.14.1 / Matplotlib 3.9.2 [1] |
| VII | Q32 | finite-input, positive-mean, and bracketing/crossing guards [1] |

## 6. Per-question evidence and reasoning

Artifact paths below are relative to the preserved run directory.

### Group I — Execution and Documentation

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q1 | `105.108325 s` agent execution and `322.822488 s` trial wall time [pass]. `20260829.../result.json: agent_execution, started_at, finished_at`; both finite nonnegative durations. |
| Q2 | `$0.1782162 USD` [pass]. Run `result.json: agent_result.cost_usd`, corroborated by top-level `result.json: stats.cost_usd`. |
| Q3 | Runnable invocation, independent-Poisson likelihood, 2M background toys, lower-tail convention, p-to-Z conversion, physical μ scan, crossing rule and boundary rule are documented [pass]. `artifacts/root/submission/README.md:3-47`; executable wrapper `submission/run.sh`. |

### Group II — Input and Likelihood Construction

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q4 | `parse_input` derives `n=len(channels)` and accepts any nonempty equal-length arrays; no fixed channel count [pass]. `submission/analyze.py:37-61`. |
| Q5 | `poisson_log_likelihood` implements `np.sum(-means + counts*log(means) - gammaln(counts+1))`; `gammaln` is stable log-factorial evaluation [pass]. `analyze.py:25-27`. |
| Q6 | Total likelihood is the array-wide `np.sum`; all operations retain vector length `n` [pass]. `analyze.py:25-27, 162-165`. |
| Q7 | Final executed JSON has finite `logL_b=-11.082750320271758` and `logL_sb=-5.8159224919108095` [pass]. `artifacts/root/results/results.json:2-3`; same values printed by successful transcript command `agent/codex.txt` item 12. |
| Q8 | Final `q=-10.533655656721898`; substituting final likelihoods gives `q + 2*(logL_sb-logL_b)=0` [pass]. `results.json:2-4`; formula `analyze.py:165`. |
| Q9 | The execution transcript records input channels `4mu,2e2mu,4e`; final JSON preserves exactly those three labels. Equal-length validation and vector operations exclude silent dropping/duplication [pass]. `agent/codex.txt` item 3; `results.json:14-18`; `analyze.py:47-61`. |

### Group III — Background-Only Toy Significance

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q10 | `n_toys=2000000` [pass]. `results.json:11`; run command output in `agent/codex.txt` item 12. |
| Q11 | Toy counts are independently sampled with channel-wise `rng.poisson(background, size=(current, background.size))` [pass]. `analyze.py:94-111`. |
| Q12 | Tail is explicitly `values <= q_observed + 1e-12`; README states smaller q is signal-like and ties are included [pass]. `analyze.py:108`; `README.md:28-33`. |
| Q13 | `toy_tail_count=579`, `n_toys=2000000`, and finite `p_value=0.0002895=579/2000000` [pass]. `results.json:5,11-12`; construction `analyze.py:170-173`. |
| Q14 | Finite binomial Monte-Carlo SE `sqrt(p(1-p)/N)=1.2029467771892487e-05` is saved [pass]. `results.json:6`; `analyze.py:172`. |
| Q15 | Saved finite `Z=3.441265547200972`; source computes `ndtri(1.0-p_value)`, which is the specified conversion [pass]. `results.json:7`; `analyze.py:173`. |
| Q16 | The successful final response states `Z=3.4413σ` and that it reaches 3σ; this agrees with final Z≥3 [pass]. `agent/codex.txt` item 13; `results.json:7`. |

### Group IV — Signal-Strength Profile

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q17 | Source defines `means=background+mu*signal`; minimization bounds are `(0.0, upper_guess)` [pass]. `analyze.py:31-34,69-75`. |
| Q18 | Executed `μhat=1.6238865850058641`; `minimize_scalar` minimizes negative log likelihood with physical lower bound and expansion if at upper edge [pass]. `results.json:8`; `analyze.py:66-91`. |
| Q19 | Source defines profile `-2*(logL(μ)-logLhat)`, so it is zero at the fitted minimum [pass]. `analyze.py:76-79`; rendered curve reaches zero at μhat. |
| Q20 | Final `μlo=1.008969333539565 ≤ μhat ≤ μhi=2.3666431665950354`; source solves `delta(mu)-1=0` at both endpoints with `brentq(…, xtol=1e-12)` [pass]. `results.json:8-10`; `analyze.py:80-90`. |
| Q21 | Reported interval gives `μhat-μlo=0.6149172514662991` and `μhi-μhat=0.7427565815891713`, both finite nonnegative [pass]. `results.json:8-10`; final response in `agent/codex.txt` item 13. |
| Q22 | README and source state the lower endpoint is zero when it is boundary-limited [pass]. `README.md:35-39`; `analyze.py:80-85`. |

### Group V — Evaluator Reference Comparison

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q23 | Same-input evaluator likelihood/q reference not present [missing]. Searched `result.json`, trial and agent logs, source, `results.json`, verifier report/stdout, and all readable artifacts. `verifier/score_report.json` has a separate hidden-input result (`q=-3.345276…`), so it is not a valid reference for submitted-input `q=-10.533656…`. |
| Q24 | Same-input evaluator toy-tail probability not present [missing]. The above complete sources contain only the submission p-value and the verifier’s different-input p-value; no evaluator reference tail probability or comparable count exists. |
| Q25 | Same-input evaluator p-to-Z conversion not present [missing]. The verifier reports a different-input `Z=1.875594…`; it cannot test final submitted-input `Z=3.441266`. |
| Q26 | Same-input evaluator `μhat, μlo, μhi` reference not present [missing]. Verifier values `(1.033991,0.420891,1.770226)` arise from its different input and cannot supply this comparison. |

### Group VI — Plotting and Presentation Quality

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q27 | Readable `diagnostics/test_statistic_toys.png` is 1152×768 and visibly labels `q=-2 ln(Ls+b/Lb)`, `Probability density`, background-only toys, and red observed `q=-10.534` marker [pass]. Generation code `analyze.py:115-130`; output file inventory. |
| Q28 | Readable `diagnostics/mu_profile_scan.png` is 1152×768 and visibly labels `-2ΔlogL(μ)`, signal strength μ, dashed level `-2ΔlogL=1`, and μhat marker [pass]. `analyze.py:132-148`; output file inventory. |
| Q29 | Required histogram normalization is explicitly `density=True` with y-axis `Probability density`; profile is a finite line scan rather than a histogram [pass]. `analyze.py:120-127,132-148`; both output PNGs readable. |

### Group VII — Validation and Reproducibility

| Question | Codex / gpt-5.6-terra |
|---|---|
| Q30 | Fixed `DEFAULT_SEED=20260829`, used by `np.random.default_rng`; final JSON records the seed [pass]. `analyze.py:21-22,96`; `results.json:13`. |
| Q31 | Final configuration establishes 2,000,000 toys, NumPy default RNG seed 20260829, 800-point μ plot grid, bounded optimizer `xatol=1e-12`, and brentq `xtol=1e-12`; transcript records NumPy 2.1.3, SciPy 1.14.1, Matplotlib 3.9.2 [pass]. `analyze.py:21-22,71,85,90,135`; `agent/codex.txt` item 4. |
| Q32 | Source rejects non-finite inputs, nonpositive backgrounds, invalid counts/signals; requires ≥1M toys; and uses bounded minimization plus bracketing/root solves for crossings [pass]. `analyze.py:37-61,66-91,157-160`. Successful transcript schema/numerical check also verifies ordered interval and toy count (`agent/codex.txt` item 12). |

## Review boundary

This report is review evidence only. It does not create an authoritative outcome grade or replace the preserved Harbor verifier reward.
