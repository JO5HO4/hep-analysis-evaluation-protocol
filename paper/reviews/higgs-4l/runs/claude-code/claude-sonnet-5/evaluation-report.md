# Manual evidence review — Higgs → 4ℓ

Non-authoritative review, generated 2026-09-09.  This review applies the
natural-language rubric only; it does not create an outcome grade.

Run: `higgs-4l / claude-code / claude-sonnet-5 /
20260829T161300Z-higgs-4l-signif__UJQmqEQ`.

## Evidence scope

The complete preserved root was enumerated before assigning missing status:
the job/trial `result.json` files, `config.json`, `lock.json`, `job.log` and
`trial.log`; `agent/claude-code.txt` and `agent/trajectory.json`; the artifact
manifest; submitted `analysis.py`, `run.sh`, and `README.md`; task output
`artifacts/root/results/results.json`; both PNG diagnostics; and verifier
`ctrf.json`, `test-stdout.txt`, `score_report.json`, and `reward.txt`.
`artifacts/logs/artifacts` is explicitly recorded empty.  No CSV, Parquet,
additional report/table, or workspace artifact is present in this readable
bundle.  Source is used for implementation facts and the saved JSON/verifier
report for executed numerical facts.

Harbor context: completed (one completed trial, zero trial errors), verifier
reward **1.000000**.  This is context, not the score below.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / claude-sonnet-5 | 26 | 1 | 5 | completed / 1.000000 |

## Total reward (raw, no averaging)

| Summary | Claude Code / claude-sonnet-5 |
|---|---:|
| Total reward | 26 / 32 |

## Overall equal-category reward

| Summary | Claude Code / claude-sonnet-5 |
|---|---:|
| Overall equal-category reward | 0.8010 |

This is the mean of section fractions: `3/3, 6/6, 6/7, 4/6, 3/4, 3/3, 1/3`.

## Per-question binary rewards

| Category | Question | Claude Code / claude-sonnet-5 |
|---|---|---:|
| Execution and documentation | Q1–Q3 | 1, 1, 1 |
| Input and likelihood construction | Q4–Q9 | 1, 1, 1, 1, 1, 1 |
| Background-only toy significance | Q10–Q16 | 1, 1, 1, 1, 0, 1, 1 |
| Signal-strength profile | Q17–Q22 | 0, 1, 1, 1, 1, 0 |
| Evaluator reference comparison | Q23–Q26 | 1, 0, 1, 1 |
| Plotting and presentation | Q27–Q29 | 1, 1, 1 |
| Validation and reproducibility | Q30–Q32 | 1, 0, 0 |

## Per-question observed values and evidence

| Q | Status / reward | Observed value | Evidence and reason |
|---:|---|---|---|
| 1 | pass / 1 | wall 451.886142 s; agent execution 289.637013 s | Trial `result.json` timestamps establish both finite durations. |
| 2 | pass / 1 | $2.2233186 USD | Job and trial `result.json: stats.cost_usd` / `agent_result.cost_usd`. |
| 3 | pass / 1 | runnable wrapper; likelihood, toys, scan documented | `submission/README.md`; `run.sh`; `analysis.py`. |
| 4 | pass / 1 | `nch=len(channels)` | `analysis.py: main` reads all four arrays and has no fixed channel count. |
| 5 | pass / 1 | `poisson.logpmf(obs,lam)` | `analysis.py: total_logL`; SciPy stable log-PMF implements the required term. |
| 6 | pass / 1 | sum over channels | `total_logL` and `total_logL_batch(...).sum(axis=1)`. |
| 7 | pass / 1 | logL_b −11.0827503203; logL_sb −5.8159224919 | Executed `artifacts/root/results/results.json`. |
| 8 | pass / 1 | q −10.5336556567 | Saved output and `q_obs=-2*(logL_sb-logL_b)`; identity holds to floating precision. |
| 9 | pass / 1 | 3 saved channels, each array length 3 | Output lists `4mu,2e2mu,4e`; source asserts all array lengths equal `nch` and evaluates full arrays. |
| 10 | pass / 1 | 5,000,000 toys | Executed output `n_toys`; `run.sh --ntoys 5000000`. |
| 11 | pass / 1 | independent `rng.poisson(lam=bkg,size=(ntoys,nch))` | `analysis.py`; executed output records the input background vector. |
| 12 | pass / 1 | `sum(q_t <= q_obs)` | `analysis.py` uses the correct signal-like tail for this q convention. |
| 13 | pass / 1 | 1,288 / 5,000,000 = 0.0002576 | Executed `results.json: n_toys_as_extreme,n_toys,p_value`. |
| 14 | missing / 0 | not established | Searched saved output, README, source, transcript, and verifier artifacts. They give N and p but no reported binomial uncertainty/interval. |
| 15 | pass / 1 | Z 3.4727265423 | `norm.isf(p_reported)` in source and saved p=0.0002576; equals Phi^-1(1−p). |
| 16 | pass / 1 | `reaches_3sigma_evidence=true`, Z=3.4727 | Executed output; the Boolean agrees with Z ≥ 3. |
| 17 | fail / 0 | fit domain `mu_domain_min=max(-bkg/sig)+1e-9`, not mu≥0 | `analysis.py: fit_mu` explicitly describes an “unconstrained sign” fit and bounds the optimizer below zero where permitted. This directly contradicts the rubric’s physical domain. |
| 18 | pass / 1 | mu_hat 1.6238865608 | Executed output plus bounded `minimize_scalar` in `fit_mu`. |
| 19 | pass / 1 | `2*(logL_max-logL(mu))`; zero at fitted maximum | `analysis.py: two_dlogl`; profile is referenced to `logL_max`. |
| 20 | pass / 1 | mu_lo 1.0089693335; mu_hat 1.6238865608; mu_hi 2.3666431666 | Executed values; source obtains both roots by `brentq(two_dlogl-1)`, hence their profile value is 1. |
| 21 | pass / 1 | −0.6149172273, +0.7427566058 | Executed `mu_err_minus` and `mu_err_plus`. |
| 22 | missing / 0 | not established | Source/output/transcript/verifier were searched. The output has mu_lo>0, but no artifact states physical-boundary handling; moreover Q17 shows the fit was not constrained to that boundary. |
| 23 | pass / 1 | verifier-input: logL_b −7.9512456802 vs −7.9512456802; logL_sb −6.2786075903 vs −6.2786075903; q −3.3452761799 vs −3.3452761799 | `verifier/score_report.json`; all deltas are within the specified tolerance. This is development comparison evidence, not an outcome grade. |
| 24 | missing / 0 | not established | `score_report.json` supplies the verifier-input p values (0.0302272 and 0.0303385), but no corresponding tail count/toy count. The saved 1,288/5M count is for a different saved task input, so it cannot establish the requested interval comparison. |
| 25 | pass / 1 | 1.8774649270 vs 1.8758418460; delta 0.0016230810 | `verifier/score_report.json`; delta <0.02. |
| 26 | pass / 1 | (1.0339913385, 0.4208908423, 1.7702256921) vs (1.034, 0.421, 1.770) | `verifier/score_report.json`; each absolute delta <0.02. |
| 27 | pass / 1 | toy experiments/bin; observed-q vertical marker | `analysis.py` plotting code and retained `diagnostics/test_statistic_distribution.png`. |
| 28 | pass / 1 | −2ΔlogL(mu), horizontal level 1, finite 400-point scan | `analysis.py` and retained `diagnostics/mu_scan.png`. |
| 29 | pass / 1 | toy histogram is “toy experiments / bin” | Plot code explicitly labels the statistical unit; profile plot labels its ordinate. |
| 30 | pass / 1 | NumPy default RNG seed 12345 | `run.sh --seed 12345`; `analysis.py: np.random.default_rng(args.seed)`. |
| 31 | missing / 0 | settings partly established; package versions not established | Source gives 5M toys, seed, 400-point scan, xatol 1e−12; searched config, logs, README, output, and verifier artifacts contain no numerical package versions. |
| 32 | missing / 0 | partial invalid-mean guard only | `neg_logL_mu` checks `lam<=0`, but the complete searched source/output/log/report set gives no check for non-finite likelihoods or failed interval crossings. |

The saved output (`results.json`) and the verifier report use different task
inputs, as shown by their distinct likelihood values.  They are therefore used
only for the facts each directly establishes; they are not mixed for a new
scientific calculation.
