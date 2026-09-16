# Manual evidence review — Higgs → 4l

Non-authoritative review, completed 2026-09-09. This applies `evaluation/higgs_4l.md` and the shared evidence policy, not an outcome grader. Run: `20260902T192318Z-higgs-4l-significance-qwen-coder-1513207 / 20260902T192318Z-higgs-4l-signif__D2WKKsA`; task `haichenwangberkeley/higgs-4l-significance`; agent/model `qwen-coder / lbl/cborg-coder`.

## Evidence audit

The complete preserved readable bundle was inventoried: top-level and trial `config.json`, `result.json`, `job.log`, `trial.log`, verifier reward/report/stdout/CTRF, artifact manifest, agent transcript/session/trajectory, submitted `run.sh`, `run_analysis.py`, `README.md`, produced `results.json`, and both PNG diagnostics. The source and executed `results.json` are consistent with the session trace; the verifier's numeric reference record is a rerun on different counts (for example its `logL_b=-7.9512456802`, versus submitted `-11.0827503203`), so it is not a same-input evaluator reference for Q23–Q26.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| qwen-coder / lbl-cborg-coder | 19 | 1 | 12 | completed / 0.687500 |

## Total reward (raw, no averaging)

| Summary | qwen-coder / lbl-cborg-coder |
|---|---:|
| Total reward | 19 / 32 |

## Overall equal-category reward

| Summary | qwen-coder / lbl-cborg-coder |
|---|---:|
| Overall equal-category reward | 0.558 |

This is the mean of group pass fractions: 2/3, 6/6, 4/7, 4/6, 0/4, 3/3, and 0/3.

## Per-question binary rewards

| Category | Question | qwen-coder / lbl-cborg-coder |
|---|---|---:|
| Execution/documentation | Q1 Run timing | 1 |
| Execution/documentation | Q2 Run cost | 0 |
| Execution/documentation | Q3 Analysis documentation | 1 |
| Input/likelihood | Q4 Input generality | 1 |
| Input/likelihood | Q5 Poisson likelihood | 1 |
| Input/likelihood | Q6 Channel combination | 1 |
| Input/likelihood | Q7 Likelihood values | 1 |
| Input/likelihood | Q8 Observed test statistic | 1 |
| Input/likelihood | Q9 Input preservation | 1 |
| Toys/significance | Q10 Toy count | 1 |
| Toys/significance | Q11 Toy hypothesis | 1 |
| Toys/significance | Q12 Tail convention | 0 |
| Toys/significance | Q13 Toy p-value | 1 |
| Toys/significance | Q14 Toy statistical uncertainty | 0 |
| Toys/significance | Q15 Gaussian significance | 1 |
| Toys/significance | Q16 Evidence conclusion | 0 |
| Signal strength | Q17 Signal-strength model | 1 |
| Signal strength | Q18 Best-fit strength | 1 |
| Signal strength | Q19 Profile definition | 1 |
| Signal strength | Q20 One-sigma crossings | 0 |
| Signal strength | Q21 Asymmetric interval | 1 |
| Signal strength | Q22 Boundary handling | 0 |
| Evaluator reference | Q23 Likelihood reference agreement | 0 |
| Evaluator reference | Q24 Toy p-value consistency | 0 |
| Evaluator reference | Q25 Significance reference agreement | 0 |
| Evaluator reference | Q26 Signal-strength reference agreement | 0 |
| Plotting | Q27 Toy-test-statistic diagnostic | 1 |
| Plotting | Q28 Profile diagnostic | 1 |
| Plotting | Q29 Plot normalization | 1 |
| Validation/reproducibility | Q30 Randomness control | 0 |
| Validation/reproducibility | Q31 Final configuration | 0 |
| Validation/reproducibility | Q32 Numerical validity checks | 0 |

## Per-question observed values, status, and evidence

| ID | Status / reward | Observed value | Evidence and reason |
|---|---|---|---|
| Q1 | pass / 1 | trial wall time 274.172 s; agent execution 162.980 s | Trial `result.json` timestamps establish both finite nonnegative durations. |
| Q2 | missing / 0 | cost USD: null | Top-level `result.json:stats.cost_usd` and trial `result.json:agent_result.cost_usd` are null; no other bundle artifact gives a USD total. |
| Q3 | pass / 1 | runnable wrapper; Poisson likelihood, 1,000,000 toys, μ scan described | `submission/README.md` Methodology and How to Run, corroborated by `run.sh` and `run_analysis.py`. |
| Q4 | pass / 1 | channel length is `len(observed)` | `run_analysis.py` reads arrays from JSON and creates toys with `(len(observed), n_toys)`; no fixed count. |
| Q5 | pass / 1 | `-λ+k log λ-lgamma(k+1)` | `run_analysis.py:log_poisson`; `math.lgamma` is the stable log-factorial term. |
| Q6 | pass / 1 | sum over `zip(observed, expected)` | `run_analysis.py:compute_log_likelihood` adds each channel contribution. |
| Q7 | pass / 1 | logL_b −11.082750320272; logL_sb −5.815922491911 | Executed `artifacts/root/results/results.json`. |
| Q8 | pass / 1 | q −10.533655656722; residual `q+2(logL_sb-logL_b)=0` to shown precision | Executed `results.json`; definition in `run_analysis.py`. |
| Q9 | pass / 1 | 3 observed/background/signal entries, each used in array calculation | Session input read shows three aligned arrays; source computes all likelihood/toy entries over these arrays once. |
| Q10 | pass / 1 | N = 1,000,000 toys | `run_analysis.py:n_toys=10**6`; successful `run.sh` invocation in trajectory. |
| Q11 | pass / 1 | `np.random.poisson(background[:, np.newaxis], ...)` | `run_analysis.py`; one independent Poisson row per background expectation. |
| Q12 | fail / 0 | implemented tail is `toy_qs >= observed_q`, required is `<=` | Direct contradictory source evidence: `run_analysis.py:p_value`; final agent message also acknowledges the sign/tail problem. |
| Q13 | pass / 1 | p = 0.999732 = 999,732 / 1,000,000 | Executed `results.json` plus direct `n_toys` and numerator expression in `run_analysis.py`. |
| Q14 | missing / 0 | no binomial uncertainty/interval reported | Searched results JSON, README, final transcript, source, and plots; none reports uncertainty or interval. |
| Q15 | pass / 1 | Z = −3.462088937902 = `norm.ppf(1−0.999732)` | Executed `results.json`; direct conversion in `run_analysis.py`. |
| Q16 | missing / 0 | Z < 3, but no explicit evidence/no-evidence conclusion | README/source and final message report the negative Z but never state the requested 3σ conclusion. |
| Q17 | pass / 1 | λ(μ)=μs+b; μ constrained to [0,10] | `run_analysis.py` expected mean and bounded optimizer. |
| Q18 | pass / 1 | μhat = 1.623886698632 | Executed `results.json`; `minimize_scalar(... bounds=(0,10), method='bounded')` minimizes −logL. |
| Q19 | pass / 1 | profile `2(logL(μhat)-logL(μ))`, zero by definition at μhat | `run_analysis.py:delta_logL`; corresponding profile plot saved. |
| Q20 | missing / 0 | μlo = 0.000000774330; μhi = 2.366646719038 | Executed endpoints exist, but no saved executed profile values at endpoints establish both are within 0.01 of 1; source alone is insufficient for this numeric-execution criterion. |
| Q21 | pass / 1 | −σ = 1.623885924302; +σ = 0.742760020406 | Arithmetic from finite executed μhat, μlo, μhi in `results.json`. |
| Q22 | missing / 0 | lower value near, but not equal to, zero | Source describes a possible boundary branch and final text rounds interval to `[0, 2.37]`; neither states whether this run is boundary-limited. |
| Q23 | missing / 0 | same-input evaluator reference unavailable | `verifier/score_report.json` references different likelihood values/input; no evaluator-owned same-count reference is in the readable bundle. |
| Q24 | missing / 0 | same-input reference p unavailable | Same search of verifier report, JSON, logs, source, and reports found only a different-input reference p. |
| Q25 | missing / 0 | same-input reference conversion unavailable | Same evidence limitation as Q23; no comparison is inferred. |
| Q26 | missing / 0 | same-input reference μ values unavailable | Verifier μ references pair with its different test values; not usable as this rubric's same-input reference. |
| Q27 | pass / 1 | density histogram of background toy q; observed q=−10.53 marked | `diagnostics/test_statistic.png` and plotting calls: `hist(... density=True)` and `axvline(observed_q)`. |
| Q28 | pass / 1 | finite −2ΔlogL scan; horizontal level 1 | `diagnostics/likelihood_profile.png` plus source uses 200 μ points and `axhline(1)`. |
| Q29 | pass / 1 | toy histogram is probability density | Plot y-axis says Probability Density; source explicitly uses `density=True`. |
| Q30 | missing / 0 | RNG seed/state not established | Source calls unseeded `np.random.poisson`; no seed/state in source, README, JSON, logs, or transcript. |
| Q31 | missing / 0 | N=1e6; μ range [0,10], scan 1000/200; seed/RNG algorithm and package versions absent | Source establishes some settings, but the required complete configuration is not preserved. |
| Q32 | missing / 0 | only `lambd <= 0 → -inf` is present | Complete submitted source lacks checks for non-finite likelihoods and failed crossings; the limited mean guard does not establish all required validity checks. |

The Harbor reward is retained only as execution context; this report neither assigns an authoritative outcome grade nor alters the preserved run.
