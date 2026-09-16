# Manual evidence review — higgs-4l

Non-authoritative single-run review under `evaluation/higgs_4l.md` and `evaluation/evaluation_rubric.md`, reviewed 2026-09-09. Run: `higgs-4l / terminus-2 / openai/lbl/cborg-coder / 20260902T192401Z-higgs-4l-significance-terminus-2-1410561`. This is review evidence, not an outcome grade.

Complete bounded bundle audit: job and trial metadata/logs, terminal pane and trajectory, submitted README/launcher/source, executed `results.json`, verifier JSON/CTRF/stdout/reward, and both PNG diagnostics were readable. The inventory contains no CSV, Parquet, ROOT workspace, table, or separate report. Verifier calculations use a distinct hidden input (e.g. verifier `logL_b=-7.9512456802` versus submitted `-11.0827503203`) and therefore are not same-input evaluator references for Q23–Q26.

## 1. Status Summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus 2 / openai/lbl/cborg-coder | 20 | 1 | 11 | completed / 0.700000 |

## 2. Total Reward (Raw, No Averaging)

| Summary | Terminus 2 / openai/lbl/cborg-coder |
|---|---:|
| Total reward | 20 / 32 |

## 3. Overall Equal-Category Reward

| Summary | Terminus 2 / openai/lbl/cborg-coder |
|---|---:|
| Overall equal-category reward | 0.581633 |

`(2/3 + 6/6 + 4/7 + 5/6 + 0/4 + 3/3 + 0/3) / 7`.

## 4. Per-Question Binary Rewards

| Category | Question | Terminus 2 / openai/lbl/cborg-coder |
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
| III | Q13 Toy p-value | 1 |
| III | Q14 Toy statistical uncertainty | 0 |
| III | Q15 Gaussian significance | 1 |
| III | Q16 Evidence conclusion | 0 |
| IV | Q17 Signal-strength model | 1 |
| IV | Q18 Best-fit strength | 1 |
| IV | Q19 Profile definition | 1 |
| IV | Q20 One-sigma crossings | 1 |
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

## 5. Per-Question Observed Values and Rewards

| Category | Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|---|
| I | Q1 | wall 201.626 s; agent 74.742 s [1] |
| I | Q2 | `cost_usd=null` [0] |
| I | Q3 | README plus runnable launcher/source [1] |
| II | Q4 | `len(obs)` channels [1] |
| II | Q5 | `-λ+k log λ-lgamma(k+1)` [1] |
| II | Q6 | `np.sum` over `zip` [1] |
| II | Q7 | −11.0827503203; −5.8159224919 [1] |
| II | Q8 | q=−10.5336556567; identity residual 0 [1] |
| II | Q9 | all 3 transcript channels consumed once [1] |
| III | Q10 | N=1,000,000 [1] |
| III | Q11 | `np.random.poisson(bkg,(N,len(obs)))` [1] |
| III | Q12 | implemented `q_toys >= q_obs`; required `<=` [0] |
| III | Q13 | 999,741 / 1,000,000 = 0.999741 [1] |
| III | Q14 | no binomial uncertainty/interval [0] |
| III | Q15 | Z=−3.4712714882; `norm.ppf(1-p)` [1] |
| III | Q16 | no 3σ/evidence conclusion [0] |
| IV | Q17 | `λ=μs+b`, optimization [0,10] [1] |
| IV | Q18 | μhat=1.6238866986 [1] |
| IV | Q19 | `-2(logL(μ)-logL(μhat))` [1] |
| IV | Q20 | μlo=1.0089694772 (0.99999948); μhi=2.3666424564 (0.99999824) [1] |
| IV | Q21 | −0.6149172214, +0.7427557578 [1] |
| IV | Q22 | no boundary-limited statement [0] |
| V | Q23 | same-input evaluator reference unavailable [0] |
| V | Q24 | same-input evaluator tail reference unavailable [0] |
| V | Q25 | same-input evaluator Z reference unavailable [0] |
| V | Q26 | same-input evaluator profile reference unavailable [0] |
| VI | Q27 | 100-bin density toy-q histogram and q marker [1] |
| VI | Q28 | 200-point μ∈[0,10] profile and y=1 [1] |
| VI | Q29 | `density=True`: probability density [1] |
| VII | Q30 | no seed/RNG state saved [0] |
| VII | Q31 | N and scan stated; seed, package versions absent [0] |
| VII | Q32 | no finite/mean/crossing validation checks [0] |

## 6. Per-Question Evidence and Reasoning

### Group I — Execution and Documentation

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q1 | `201.626265 s` trial wall time (`result.json` top level, 12:24:17.566529–12:27:54.622794) and `74.742485 s` agent execution (trial `result.json:agent_execution`) are finite [pass]. |
| Q2 | Both top-level `result.json:stats.cost_usd` and trial `result.json:agent_result.cost_usd` are `null`; no finite USD total exists [missing]. |
| Q3 | Runnable command plus likelihood, toys, profile and scan assumptions are described [pass]. `artifacts/root/submission/{README.md,run.sh,analysis.py}`. |

### Group II — Input and Likelihood Construction

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q4 | Source reads arrays and sizes toys with `len(obs)`, not a fixed channel count [pass]. `submission/analysis.py:run_analysis`. |
| Q5 | `log_poisson` implements `-lam+k*np.log(lam)-lgamma(k+1)` [pass]. `submission/analysis.py:log_poisson`. |
| Q6 | `calculate_logL` sums the list comprehension spanning `zip(observed, expected)` [pass]. `submission/analysis.py:calculate_logL`. |
| Q7 | Executed saved output contains finite `logL_b=-11.082750320271757`, `logL_sb=-5.815922491910811` [pass]. `artifacts/root/results/results.json`. |
| Q8 | Saved q is `-10.53365565672189`; `q+2*(logL_sb-logL_b)=0` to displayed precision [pass]. `results.json`. |
| Q9 | Transcript shows three channel arrays; each likelihood and toy expression consumes each aligned array element once [pass]. `agent/terminus_2.pane`, `submission/analysis.py`. |

### Group III — Background-Only Toy Significance

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q10 | Submitted source fixes `n_toys=10**6`, and the transcript records execution of that source before the saved result [pass]. `agent/terminus_2.pane`, `submission/analysis.py`. |
| Q11 | Source generates the `(N,len(obs))` toys from channel-wise `bkg` Poisson means [pass]. `submission/analysis.py`. |
| Q12 | Direct contradiction: source and README use `q_toys >= q_obs`; this rubric requires the signal-like `q_toy <= q_observed` tail for its q definition [fail]. `submission/analysis.py`, `README.md`. |
| Q13 | Executed p-value is finite and in range. With executed source `N=1,000,000`, its exact six-decimal value establishes tail count 999,741 [pass]. `results.json`, source/transcript. |
| Q14 | No binomial standard error or interval appears after searching source, README, terminal pane/trajectory, saved JSON, verifier output, logs, or plots [missing]. |
| Q15 | `norm.ppf(1-0.999741)=-3.4712714882`, matching saved Z within 1e-6 [pass]. `results.json`, `submission/analysis.py`. |
| Q16 | No artifact states whether the result reaches 3σ evidence; source only writes numeric outputs. Searched README, source, pane/trajectory, result and verifier files [missing]. |

### Group IV — Signal-Strength Profile

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q17 | `expected=mu*sig+bkg`; `minimize_scalar(...bounds=(0,10))` supplies the μ≥0 model/domain [pass]. `submission/analysis.py`. |
| Q18 | Executed μhat is finite and source minimizes negative log likelihood [pass]. `results.json`; `analysis.py:minimize_scalar`. |
| Q19 | Source defines profile as `-2*(logL(mu)-logL(mu_hat))`, exactly zero at μhat [pass]. `submission/analysis.py:profile_likelihood`. |
| Q20 | Saved endpoints bracket μhat; recomputing the submitted defined profile from transcript input gives 0.99999948 and 0.99999824 at lower/upper endpoints [pass]. `results.json`, pane input, source. |
| Q21 | Saved endpoints establish finite asymmetric uncertainties μhat−μlo=0.6149172214 and μhi−μhat=0.7427557578 [pass]. `results.json`. |
| Q22 | No source, README, result, transcript, log, or plot says whether `mu_lo=0` denotes a boundary-limited endpoint [missing]. |

### Group V — Evaluator Reference Comparison

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q23 | Same-input evaluator reference is unavailable [missing]. All readable sources were searched; verifier values are from a different input, so cannot support this comparison. |
| Q24 | Same-input evaluator tail probability is unavailable [missing]. Verifier p=0.969651 is distinct-input evidence, not a reference interval check. |
| Q25 | Same-input evaluator p-to-Z reference is unavailable [missing]. Verifier Z=−1.87568898 is distinct-input evidence. |
| Q26 | Same-input evaluator profile reference is unavailable [missing]. Verifier `(1.0339908,0.4208909,1.7702262)` is distinct-input evidence. |

### Group VI — Plotting and Presentation Quality

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q27 | The readable 640×480 `q_dist.png` is generated by source as a 100-bin background-toy q distribution, normalized density, with observed-q vertical marker [pass]. `submission/analysis.py`; `diagnostics/q_dist.png`. |
| Q28 | The readable 640×480 `mu_scan.png` is generated from 200 finite μ points on [0,10], with `-2 Delta log L` and y=1 line [pass]. `analysis.py`; `diagnostics/mu_scan.png`. |
| Q29 | Required toy histogram unit is explicit: `density=True` and y label `Probability Density` [pass]. `submission/analysis.py`. |

### Group VII — Validation and Reproducibility

| Question | Terminus 2 / openai/lbl/cborg-coder |
|---|---|
| Q30 | `np.random.poisson` is unseeded; no seed/state is recorded in all inspected files [missing]. |
| Q31 | Source gives N and scan [0,10]/200 points, but no RNG seed/algorithm state, optimizer tolerance, or package versions; criterion is incomplete [missing]. |
| Q32 | Source contains no explicit checks for non-finite likelihoods, invalid Poisson means, or failed interval crossings; searched source, README, transcript, JSON/log/verifier records [missing]. |
