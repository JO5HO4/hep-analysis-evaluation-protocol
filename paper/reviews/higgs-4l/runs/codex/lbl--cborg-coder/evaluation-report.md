# Manual evidence review — higgs-4l

Run: `20260902T192326Z-higgs-4l-significance-codex-1785193/20260902T192326Z-higgs-4l-signif__Mmua7tm`  
Agent/model: `Codex / lbl/cborg-coder`  
Review date: 2026-09-09  
Scope: one preserved run only. This is non-authoritative manual review evidence, not an outcome grade. Harbor execution completed with verifier reward `0.950000` (five verifier tests: four passed, diagnostics failed).

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / lbl/cborg-coder | 22 | 2 | 8 | completed / 0.950000 |

## Total reward (raw, no averaging)

| Summary | Codex / lbl/cborg-coder |
|---|---:|
| Total reward | 22 / 32 |

## Overall equal-category reward

| Summary | Codex / lbl/cborg-coder |
|---|---:|
| Overall equal-category reward | 0.622449 |

Arithmetic: `(2/3 + 6/6 + 6/7 + 5/6 + 0/4 + 3/3 + 0/3) / 7`.

## Per-question binary rewards

| Category | Question | Codex / lbl/cborg-coder |
|---|---|---:|
| Execution and Documentation | Q1 Run timing | 1 |
| Execution and Documentation | Q2 Run cost | 0 |
| Execution and Documentation | Q3 Analysis documentation | 1 |
| Input and Likelihood Construction | Q4 Input generality | 1 |
| Input and Likelihood Construction | Q5 Poisson likelihood | 1 |
| Input and Likelihood Construction | Q6 Channel combination | 1 |
| Input and Likelihood Construction | Q7 Likelihood values | 1 |
| Input and Likelihood Construction | Q8 Observed test statistic | 1 |
| Input and Likelihood Construction | Q9 Input preservation | 1 |
| Background-Only Toy Significance | Q10 Toy count | 1 |
| Background-Only Toy Significance | Q11 Toy hypothesis | 1 |
| Background-Only Toy Significance | Q12 Tail convention | 1 |
| Background-Only Toy Significance | Q13 Toy p-value | 1 |
| Background-Only Toy Significance | Q14 Toy statistical uncertainty | 0 |
| Background-Only Toy Significance | Q15 Gaussian significance | 1 |
| Background-Only Toy Significance | Q16 Evidence conclusion | 1 |
| Signal-Strength Profile | Q17 Signal-strength model | 1 |
| Signal-Strength Profile | Q18 Best-fit strength | 1 |
| Signal-Strength Profile | Q19 Profile definition | 1 |
| Signal-Strength Profile | Q20 One-sigma crossings | 1 |
| Signal-Strength Profile | Q21 Asymmetric interval | 1 |
| Signal-Strength Profile | Q22 Boundary handling | 0 |
| Evaluator Reference Comparison | Q23 Likelihood reference agreement | 0 |
| Evaluator Reference Comparison | Q24 Toy p-value consistency | 0 |
| Evaluator Reference Comparison | Q25 Significance reference agreement | 0 |
| Evaluator Reference Comparison | Q26 Signal-strength reference agreement | 0 |
| Plotting and Presentation Quality | Q27 Toy-test-statistic diagnostic | 1 |
| Plotting and Presentation Quality | Q28 Profile diagnostic | 1 |
| Plotting and Presentation Quality | Q29 Plot normalization | 1 |
| Validation and Reproducibility | Q30 Randomness control | 0 |
| Validation and Reproducibility | Q31 Final configuration | 0 |
| Validation and Reproducibility | Q32 Numerical validity checks | 0 |

## Per-question observed values and rewards

| Category | Question | Codex / lbl/cborg-coder |
|---|---|---|
| Execution and Documentation | Q1 | `338.093 s` trial wall clock; `224.884 s` agent execution [1] |
| Execution and Documentation | Q2 | `null USD` [0] |
| Execution and Documentation | Q3 | README documents invocation, likelihood, toys, scan [1] |
| Input and Likelihood Construction | Q4 | `len(observed)` channels; three observed channels in executed input [1] |
| Input and Likelihood Construction | Q5 | `-lambda + k log(lambda) - gammaln(k+1)` [1] |
| Input and Likelihood Construction | Q6 | `np.sum(...)` across channel axis [1] |
| Input and Likelihood Construction | Q7 | `logL_b=-11.0827503203`, `logL_sb=-5.8159224919` [1] |
| Input and Likelihood Construction | Q8 | `q=-10.5336556567`; `q + 2(logL_sb-logL_b)=0` [1] |
| Input and Likelihood Construction | Q9 | executed arrays `observed=[6,5,2]`, all three indexed once [1] |
| Background-Only Toy Significance | Q10 | `N=1,000,000` [1] |
| Background-Only Toy Significance | Q11 | `np.random.poisson(background, size=(N,len(observed)))` [1] |
| Background-Only Toy Significance | Q12 | final expression `q_toys <= q_obs` [1] |
| Background-Only Toy Significance | Q13 | `p=0.000247 = 247/1,000,000` [1] |
| Background-Only Toy Significance | Q14 | no saved binomial uncertainty or interval [0] |
| Background-Only Toy Significance | Q15 | `Z=3.4839888865 = Phi^-1(1-0.000247)` [1] |
| Background-Only Toy Significance | Q16 | `Z=3.48 sigma`; stated “evidence” [1] |
| Signal-Strength Profile | Q17 | `lambda_i(mu)=mu*s_i+b_i`; fit bounded `[0,10]` [1] |
| Signal-Strength Profile | Q18 | `mu_hat=1.6238866986`, bounded scalar likelihood optimum [1] |
| Signal-Strength Profile | Q19 | `2(logL_max-logL(mu))`, zero at `mu_hat` [1] |
| Signal-Strength Profile | Q20 | `mu_lo=1.0089693297`, `mu_hi=2.3666431655`; target `logL_max-0.5` [1] |
| Signal-Strength Profile | Q21 | `-0.6149173689`, `+0.7427564669` [1] |
| Signal-Strength Profile | Q22 | no statement whether a `mu_lo=0` endpoint is boundary-limited [0] |
| Evaluator Reference Comparison | Q23 | same-input evaluator reference unavailable [0] |
| Evaluator Reference Comparison | Q24 | same-input evaluator tail probability unavailable [0] |
| Evaluator Reference Comparison | Q25 | same-input evaluator p-to-Z reference unavailable [0] |
| Evaluator Reference Comparison | Q26 | same-input evaluator profile reference unavailable [0] |
| Plotting and Presentation Quality | Q27 | q-toy density, 100 bins, observed-q line [1] |
| Plotting and Presentation Quality | Q28 | 500-point `-2 Delta log L(mu)` scan and horizontal 1 line [1] |
| Plotting and Presentation Quality | Q29 | q histogram is `density=True` / probability density [1] |
| Validation and Reproducibility | Q30 | unseeded `np.random.poisson`; no seed/state [0] |
| Validation and Reproducibility | Q31 | N/scan/optimizer visible; RNG seed and package versions absent [0] |
| Validation and Reproducibility | Q32 | means clamped; no finite-state or crossing-failure checks [0] |

## Per-question evidence and reasoning

### Execution and Documentation

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q1 Run timing | **pass** — `trial/result.json` gives `2026-09-02T19:24:08.120654Z` to `19:29:46.213682Z` (338.093028 s) and agent execution `19:24:28.639199Z` to `19:28:13.523418Z` (224.884219 s). |
| Q2 Run cost | **missing** — job `result.json: stats.cost_usd` and trial `result.json: agent_result.cost_usd` are both `null`; `job.log` says no LiteLLM pricing entry. |
| Q3 Analysis documentation | **pass** — `artifacts/root/submission/README.md` supplies runnable command, Poisson likelihood, 10^6 toys, tail, p-to-Z, and profile/scan definitions; `run.sh` is executable wrapper. |

### Input and Likelihood Construction

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q4 Input generality | **pass** — `analysis.py` reads arrays from the input schema and constructs toys with `len(observed)`, with no literal channel count; `agent/trajectory.json` records the three-channel executed input. |
| Q5 Poisson likelihood | **pass** — `analysis.py: log_poisson` implements `-lam + k*np.log(lam) - gammaln(k+1)`; `gammaln` is a stable log-factorial. |
| Q6 Channel combination | **pass** — `total_log_likelihood` returns `np.sum(log_poisson(...))`; toy likelihood differences also sum channel axis 1. |
| Q7 Likelihood values | **pass** — `artifacts/root/results/results.json` contains finite `logL_b=-11.082750320271758` and `logL_sb=-5.8159224919108095`. |
| Q8 Observed test statistic | **pass** — same JSON gives `q=-10.533655656721898`; substituting the two saved likelihoods into the required identity gives zero residual at displayed precision. |
| Q9 Input preservation | **pass** — transcript records observed/background/signal triples of length three; `analysis.py` vectorizes those full arrays and sums them, without selection, slice, or duplication. |

### Background-Only Toy Significance

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q10 Toy count | **pass** — final executed `analysis.py` sets `n_toys=10**6`; the transcript records the final wrapper execution succeeded and produced the saved JSON. |
| Q11 Toy hypothesis | **pass** — final source uses `np.random.poisson(background, size=(n_toys, len(observed)))`, independently drawing each channel at its background mean; final execution is recorded in `agent/trajectory.json` steps 12–13. |
| Q12 Tail convention | **pass** — final source and README use `np.sum(q_toys <= q_obs) / n_toys`. The transcript preserves the prior `>=` result, then the explicit source correction and successful rerun. |
| Q13 Toy p-value | **pass** — final results JSON gives `0.000247`; with executed source `N=1,000,000` and direct division form this is tail count 247 / 1,000,000, finite and in `(0,1]`. |
| Q14 Toy statistical uncertainty | **missing** — searched final JSON, README, source, trajectory, trial log, verifier stdout/report, and plots; none saves or reports a binomial standard error/confidence interval. |
| Q15 Gaussian significance | **pass** — results JSON gives `p=0.000247`, `Z=3.4839888865278295`; final source calls `norm.ppf(1-p_value)`, agreeing within criterion tolerance. |
| Q16 Evidence conclusion | **pass** — `agent/trajectory.json` final message says the 3.48-sigma result reaches the 3-sigma “evidence” level; the saved Z is above 3. |

### Signal-Strength Profile

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q17 Signal-strength model | **pass** — `analysis.py` forms `lam = mu*signal + background`; best-fit optimizer bounds are `(0,10)`, directly establishing the physical fit domain. |
| Q18 Best-fit strength | **pass** — results JSON gives finite `mu_hat=1.6238866986292637`; source obtains it by bounded minimization of negative total log likelihood. |
| Q19 Profile definition | **pass** — source computes `2*(logL_max-total_log_likelihood(m,...))`; at saved `mu_hat`, this is zero by construction. |
| Q20 One-sigma crossings | **pass** — final JSON gives `1.0089693297404083 <= 1.6238866986292637 <= 2.3666431654947955`; source solves each direction at `logL_max-0.5` by 20 bisections, equivalent to profile 1. |
| Q21 Asymmetric interval | **pass** — direct subtraction of saved endpoints gives lower uncertainty `0.6149173688888554` and upper `0.7427564668655318`, both finite/nonnegative. |
| Q22 Boundary handling | **missing** — README states the `mu>=0` model and source bounds the optimizer, but source explicitly allows the lower crossing to go negative and neither saved result nor documentation states whether a zero lower endpoint would be boundary-limited. |

### Evaluator Reference Comparison

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q23 Likelihood reference agreement | **missing** — searched preserved result JSON, submitted source/README, trajectory input, verifier `score_report.json`, CTRF, stdout, and task-local evaluation materials. No evaluator-owned reference for the executed counts `[6,5,2]` is readable. `score_report.json` references different values (`logL_b=-7.951...`, `q=-3.345...`), so it cannot be substituted. |
| Q24 Toy p-value consistency | **missing** — same searched sources contain no same-input evaluator tail probability/interval. Verifier p-value `0.030159` differs from saved `0.000247` and is associated with the verifier’s different evaluation input. |
| Q25 Significance reference agreement | **missing** — no same-input evaluator reference p-to-Z conversion is available; verifier significance `1.87846` corresponds to its different p-value/input. |
| Q26 Signal-strength reference agreement | **missing** — no same-input evaluator `mu_hat, mu_lo, mu_hi` is readable. Verifier profile values (`1.03399, 0.42089, 1.77023`) are demonstrably not the saved run values and cannot support this rubric comparison. |

### Plotting and Presentation Quality

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q27 Toy-test-statistic diagnostic | **pass** — `analysis.py` makes a 100-bin `q_toys` histogram with `density=True` and `axvline(q_obs)`; artifact `submission/diagnostics/q_distribution.png` is readable PNG (1000×600). |
| Q28 Profile diagnostic | **pass** — source makes a 500-point `mu_scan`, plots `2*(logL_max-logL(mu))`, and draws `axhline(1)`; `submission/diagnostics/mu_scan.png` is readable PNG (1000×600). |
| Q29 Plot normalization | **pass** — q diagnostic explicitly requests `density=True` and labels y axis “Probability Density”; the profile is a continuous ordinate rather than a histogram. |

### Validation and Reproducibility

| Question | Codex / lbl/cborg-coder |
|---|---|
| Q30 Randomness control | **fail** — final source invokes global `np.random.poisson` without `seed`, `default_rng`, or serialized RNG state; README/results/trajectory add no reproducibility state. |
| Q31 Final configuration | **missing** — source establishes 1,000,000 toys, optimizer bounds `(0,10)`, 500 scan points and scan extent, but the searched bundle has neither RNG seed/algorithm nor numerical package versions; the required complete configuration is therefore incomplete. |
| Q32 Numerical validity checks | **fail** — `analysis.py` clamps nonpositive means with `np.maximum(lam,1e-10)` rather than validating/rejecting them, has no `isfinite` checks, and `find_mu_edge` returns a safety value at `abs(mu)>100` without a failed-crossing status. |

## Evidence inventory audited

Audited all readable files under the preserved run: job/trial result, config, lock and log files; agent transcript, `codex.txt`, session and trajectory; verifier reward, score report, CTRF and stdout; artifact manifest; submitted `analysis.py`, `run.sh`, README, both diagnostic PNGs; and saved `results.json`. No tables, CSV, Parquet, ROOT workspace, or additional report/workspace artifact exists in this bundle inventory.
