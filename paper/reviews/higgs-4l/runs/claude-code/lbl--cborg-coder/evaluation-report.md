# Manual evidence review — higgs-4l

Non-authoritative natural-language rubric review. Reviewed 2026-09-09 from the complete preserved bundle `20260902T192326Z-higgs-4l-significance-claude-code-1370864`, trial `20260902T192326Z-higgs-4l-signif__GJtrrcd`. Harbor completion and verifier reward are execution context, not an outcome grade.

## 1. Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / lbl/cborg-coder | 28 | 2 | 2 | completed / 0.950000 |

## 2. Total reward (raw, no averaging)

| Summary | Claude Code / lbl/cborg-coder |
|---|---:|
| Total reward | 28 / 32 |

## 3. Overall equal-category reward

| Summary | Claude Code / lbl/cborg-coder |
|---|---:|
| Overall equal-category reward | 0.837 |

The value is `(3/3 + 6/6 + 6/7 + 6/6 + 4/4 + 3/3 + 0/3) / 7`. No authoritative outcome grade is assigned.

## 4. Per-question binary rewards

| Category | Question | Claude Code / lbl/cborg-coder |
|---|---|---:|
| Execution and Documentation | Q1–Q3 | 1, 1, 1 |
| Input and Likelihood Construction | Q4–Q9 | 1, 1, 1, 1, 1, 1 |
| Background-Only Toy Significance | Q10–Q16 | 1, 1, 1, 1, 0, 1, 1 |
| Signal-Strength Profile | Q17–Q22 | 1, 1, 1, 1, 1, 1 |
| Evaluator Reference Comparison | Q23–Q26 | 1, 1, 1, 1 |
| Plotting and Presentation Quality | Q27–Q29 | 1, 1, 1 |
| Validation and Reproducibility | Q30–Q32 | 0, 0, 0 |

## 5. Per-question observed values and rewards

| Category | Question | Claude Code / lbl/cborg-coder |
|---|---|---|
| Execution | Q1 timing | wall 319.600 s; agent 203.155 s [1] |
| Execution | Q2 cost | $0.914473 USD [1] |
| Execution | Q3 documentation | README run command, likelihood, toys, mu scan [1] |
| Input/likelihood | Q4–Q6 | arbitrary NumPy arrays; Poisson with `gammaln`; sum over arrays [1,1,1] |
| Input/likelihood | Q7–Q9 | logL_b=-11.0827503203; logL_sb=-5.8159224919; q=-10.5336556567; 3/3 channels [1,1,1] |
| Toys | Q10–Q13 | N=1,000,000; background Poisson; `q_toy <= q_obs`; p=0.000276=276/1,000,000 [1,1,1,1] |
| Toys | Q14–Q16 | binomial uncertainty not reported [0]; Z=3.4541647741 [1]; stated 3σ evidence [1] |
| Profile | Q17–Q22 | lambda=mu*s+b, mu>=0; muhat=1.6239239239; profile target 1; lo=1.0089704113, hi=2.3666428349; -0.6149535126/+0.7427189110; non-boundary [1,1,1,1,1,1] |
| Reference | Q23–Q26 | verifier: exact likelihood/q; p 0.030110 vs 0.0303385; Z 1.879179 vs 1.875842; mu 1.033934/0.420892/1.770226 vs 1.034/0.421/1.770 [1,1,1,1] |
| Plots | Q27–Q29 | q density + observed marker; profile + y=1; q normalization=density [1,1,1] |
| Validation | Q30–Q32 | no seed [0]; settings/version set incomplete [0]; no invalid-state checks [0] |

## 6. Per-question evidence and reasoning

Artifact shorthand: `R` = `artifacts/root/results/results.json`; `A` = `artifacts/root/submission/analysis.py`; `README` = `artifacts/root/submission/README.md`; `T` = `agent/claude-code.txt`; `V` = `verifier/score_report.json`; `trial-result` = trial `result.json`.

### I. Execution and documentation

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q1 | **pass [1]** — `trial-result: started_at/finished_at` gives 2026-09-02T19:24:08.126279Z to 19:29:27.726041Z = 319.599762 s; `agent_execution` gives 203.154581 s. Both are finite nonnegative seconds. |
| Q2 | **pass [1]** — `trial-result: agent_result.cost_usd=0.914473`; also `T` terminal summary reports the same USD total. |
| Q3 | **pass [1]** — `README` supplies the runnable `run.sh INPUT_JSON OUTPUT_JSON` command and describes the likelihood, 10^6 toys, tail, p-to-Z conversion, mu model, and scan. |

### II. Input and likelihood construction

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q4 | **pass [1]** — `A:22-31` reads `observed`, `background`, and `signal` arrays from JSON; its loops use their lengths, with no literal channel count. `T` records the actual three-channel schema. |
| Q5 | **pass [1]** — `A:9-12` implements `-lambda + k*log(lambda) - gammaln(k+1)`, the stable log-factorial term. |
| Q6 | **pass [1]** — `A:14-18` accumulates every pair from `zip(observed, expected)` into `total_ll`; the executed three-element input in `T` has equal arrays. |
| Q7 | **pass [1]** — `R` records finite `logL_b=-11.082750320271758` and `logL_sb=-5.8159224919108095`; `T` shows this file immediately after the successful run. |
| Q8 | **pass [1]** — `R` gives q=-10.533655656721898. From its two log likelihoods, `-2*(-5.8159224919108095 + 11.082750320271758)=-10.533655656721898`, zero delta. |
| Q9 | **pass [1]** — `T` shows observed/background/signal each have three entries; `A:16`, `A:45`, and `A:57-60` each iterate all three equal-length entries once for likelihoods and toys. |

### III. Background-only toy significance

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q10 | **pass [1]** — `A:37` fixes `num_toys=10**6`; the successful execution and saved `R` result are recorded by `T`. |
| Q11 | **pass [1]** — `A:45` independently draws `np.random.poisson(b, num_toys)` for each background expectation. |
| Q12 | **pass [1]** — `A:62` uses `np.mean(q_toys <= q_obs)`; README states the same signal-like tail convention. |
| Q13 | **pass [1]** — `R:p_value=0.000276`, finite and in (0,1]. With executed `N=1,000,000` and the source's exact mean-of-Boolean estimator, this is 276 tail toys / 1,000,000. |
| Q14 | **missing [0]** — searched `R`, `T`, `README`, `A`, verifier report, plots, and session: none reports a binomial uncertainty or interval. The p value and N alone do not make it reported evidence. |
| Q15 | **pass [1]** — `R` gives p=0.000276 and Z=3.454164774097414; `A:63` uses `norm.ppf(1-p_value)`, consistent with Phi inverse. |
| Q16 | **pass [1]** — `T` final result states Z=3.45σ and “reaches the 3σ evidence level”; the saved Z=3.4541647741 is >=3. |

### IV. Signal-strength profile

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q17 | **pass [1]** — `A:69-73` uses `expected=mu*signal+background`; all scans begin at 0 (`A:68, 78, 87`) and the fallback enforces 0 (`A:143-150`). |
| Q18 | **pass [1]** — `R:mu_hat=1.623923923923924`; `A:68-85` maximizes the profile likelihood then refines around that maximum. |
| Q19 | **pass [1]** — `A:94-96` defines `-2*(logL_scan-max_logL)`; it is zero at the fitted maximum by construction. |
| Q20 | **pass [1]** — `R:mu_lo=1.0089704112810363`, `mu_hat=1.623923923923924`, `mu_hi=2.366642834891338`. `A:90-139` linearly interpolates both crossings at target 1. |
| Q21 | **pass [1]** — from `R`, lower uncertainty=0.6149535126428877 and upper=0.742718911? (2.366642834891338-1.623923923923924=0.742718910967414), both finite nonnegative; `T` reports 1.62 +0.75/-0.61. |
| Q22 | **pass [1]** — `R:mu_lo=1.0089704113`, so this result is not lower-bound limited; `A:141-150` explicitly documents and implements the zero-boundary fallback if a crossing is absent. |

### V. Evaluator reference comparison

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q23 | **pass [1]** — `V:test_statistic` records agent and reference logL_b=-7.951245680204405, logL_sb=-6.278607590251635, q=-3.3452761799055395; all deltas 0. |
| Q24 | **pass [1]** — `V:significance` records p=0.030110 versus reference 0.0303385. With N=1e6, the two-sided 99.7% binomial half-width is about 0.000512, so delta=0.0002285 is inside. |
| Q25 | **pass [1]** — `V:significance` gives agent Z=1.879179410565057 and reference p-converted Z=1.8758418459887942; absolute delta=0.003337564576263 <0.02. |
| Q26 | **pass [1]** — `V:signal_strength`: agent/reference deltas are -0.0000661 (muhat), -0.0001081 (lo), +0.0002256 (hi), each <0.02. |

### VI. Plotting and presentation

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q27 | **pass [1]** — `A:166-176` plots `q_toys`, labels its q definition, and draws the observed-q vertical marker; `diagnostics/q_distribution.png` is a readable 1000x600 PNG. |
| Q28 | **pass [1]** — `A:179-190` plots the finite `delta_logL_2` scan and horizontal y=1 boundary; `diagnostics/mu_scan.png` is a readable 1000x600 PNG. |
| Q29 | **pass [1]** — `A:169` explicitly uses `density=True` and `A:173` labels “Probability Density”, establishing the toy histogram normalization. |

### VII. Validation and reproducibility

| Question | Evidence, observed value, status, and reason |
|---|---|
| Q30 | **fail [0]** — `A` calls `np.random.poisson` (`A:45`) but contains no `seed`, RNG object/state capture, or reproducible generator; `R`, `README`, and `T` supply none. This directly contradicts reproducible randomness control. |
| Q31 | **missing [0]** — `A` establishes N=1e6 and scan grids 0–10/1000, local refinement/1000, 0–20/10000; it does not identify RNG algorithm/seed or numerical package versions. `T` only says imports succeeded. The required complete configuration is therefore not established. |
| Q32 | **fail [0]** — `A` has no checks for non-finite likelihoods or invalid Poisson means. Its only crossing contingency silently sets `mu_lo=0` (`A:141-150`) rather than checking/reporting failed crossings. This directly shows the required checks were not implemented. |

