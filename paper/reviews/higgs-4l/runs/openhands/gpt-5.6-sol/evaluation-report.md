# Manual evidence review — Higgs four-lepton significance

Review date: 2026-09-09. Run: `20260829T174904Z-higgs-4l-significance-openhands-1563552 / 20260829T174904Z-higgs-4l-signif__V5CzXRE`. This is non-authoritative manual review evidence under `evaluation/higgs_4l.md`, not an outcome grade.

## Evidence audit

The complete readable preserved bundle was enumerated before scoring. It contains job/trial `config.json`, `lock.json`, `result.json`, `job.log`, `trial.log`, `artifacts/manifest.json`, agent transcript/trajectory/completion/session events, and verifier `reward.txt`, `score_report.json`, `ctrf.json`, and `test-stdout.txt`. It contains no preserved submitted source file, workspace file, task-output JSON/CSV/Parquet table, plot, or report: `artifacts/manifest.json` records `/root/submission` as a copied directory but has no files, and records `/root/results/results.json` with status `failed`; the verifier reports missing `/root/submission/run.sh` and `/root/results/results.json`, `readme: false`, and diagnostic `files: []`. Searches of the readable agent transcript, trajectory, and completion for the rubric quantities, definitions, configuration, implementation, outputs, plots, and reports found only the task prompt and a pre-action plan, followed by `AssertionError: Only one choice is supported for now`; no tool invocation or scientific result was recorded.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| OpenHands / gpt-5.6-sol | 2 | 4 | 26 | completed (1 completed trial, 0 trial errors) / 0.000000 |

## Total reward (raw, no averaging)

| Summary | OpenHands / gpt-5.6-sol |
|---|---:|
| Total reward | 2 / 32 |

## Overall equal-category reward

| Summary | OpenHands / gpt-5.6-sol |
|---|---:|
| Overall equal-category reward | 0.095238 |

This is the mean of Group I `2/3` and Groups II–VII `0` each; it is not a Harbor or authoritative physics score.

## Per-question binary rewards

| Category | Question | OpenHands / gpt-5.6-sol |
|---|---|---:|
| I Execution and Documentation | Q1 Run timing | 1 |
| I Execution and Documentation | Q2 Run cost | 1 |
| I Execution and Documentation | Q3 Analysis documentation | 0 |
| II Input and Likelihood Construction | Q4 Input generality | 0 |
| II Input and Likelihood Construction | Q5 Poisson likelihood | 0 |
| II Input and Likelihood Construction | Q6 Channel combination | 0 |
| II Input and Likelihood Construction | Q7 Likelihood values | 0 |
| II Input and Likelihood Construction | Q8 Observed test statistic | 0 |
| II Input and Likelihood Construction | Q9 Input preservation | 0 |
| III Background-Only Toy Significance | Q10 Toy count | 0 |
| III Background-Only Toy Significance | Q11 Toy hypothesis | 0 |
| III Background-Only Toy Significance | Q12 Tail convention | 0 |
| III Background-Only Toy Significance | Q13 Toy p-value | 0 |
| III Background-Only Toy Significance | Q14 Toy statistical uncertainty | 0 |
| III Background-Only Toy Significance | Q15 Gaussian significance | 0 |
| III Background-Only Toy Significance | Q16 Evidence conclusion | 0 |
| IV Signal-Strength Profile | Q17 Signal-strength model | 0 |
| IV Signal-Strength Profile | Q18 Best-fit strength | 0 |
| IV Signal-Strength Profile | Q19 Profile definition | 0 |
| IV Signal-Strength Profile | Q20 One-sigma crossings | 0 |
| IV Signal-Strength Profile | Q21 Asymmetric interval | 0 |
| IV Signal-Strength Profile | Q22 Boundary handling | 0 |
| V Evaluator Reference Comparison | Q23 Likelihood reference agreement | 0 |
| V Evaluator Reference Comparison | Q24 Toy p-value consistency | 0 |
| V Evaluator Reference Comparison | Q25 Significance reference agreement | 0 |
| V Evaluator Reference Comparison | Q26 Signal-strength reference agreement | 0 |
| VI Plotting and Presentation Quality | Q27 Toy-test-statistic diagnostic | 0 |
| VI Plotting and Presentation Quality | Q28 Profile diagnostic | 0 |
| VI Plotting and Presentation Quality | Q29 Plot normalization | 0 |
| VII Validation and Reproducibility | Q30 Randomness control | 0 |
| VII Validation and Reproducibility | Q31 Final configuration | 0 |
| VII Validation and Reproducibility | Q32 Numerical validity checks | 0 |

## Per-question observed values and rewards

`NE` means not established after the stated bundle-wide evidence search; each is a missing status, not a numerical zero. `Absent` is a direct verifier/artifact finding and is a fail only where it directly contradicts the requested deliverable.

| Category | Question | OpenHands / gpt-5.6-sol |
|---|---|---|
| I | Q1 | `182.903882 s` trial wall-clock; `29.537057 s` agent execution [1] |
| I | Q2 | `$0.051794875 USD` one recorded completion; sole response and no invocations [1] |
| I | Q3 | `run.sh` and README absent [0] |
| II | Q4–Q6 | `NE` [0] |
| II | Q7–Q8 | `NE`; results JSON absent [0] |
| II | Q9 | `NE` [0] |
| III | Q10–Q16 | `NE` [0] |
| IV | Q17–Q22 | `NE` [0] |
| V | Q23–Q26 | `NE`; no agent values available for reference comparison [0] |
| VI | Q27–Q29 | diagnostics `files: []`; plots absent [0] |
| VII | Q30–Q32 | `NE` [0] |

## Per-question evidence and reasoning

| Question | Status, observed value, and evidence |
|---|---|
| Q1 | **pass** — trial wall-clock `182.903882 s` (`result.json: started_at` to `finished_at`); pure agent execution `29.537057 s` (`agent_execution` timestamps). |
| Q2 | **pass** — `$0.051794875 USD`, `agent/completions/gpt-5.6-sol-1788025845.0566354.json: cost`; it is the sole saved completion, while `trajectory.json` records no invocation. |
| Q3 | **fail** — `verifier/score_report.json: framework` says `readme: false` and missing `run.sh`; `artifacts/manifest.json` also says results-file collection failed. This directly contradicts runnable method documentation. |
| Q4 | **missing** — no submitted executable/source exists to inspect channel-count handling. Searched artifact manifest, agent transcript/trajectory/completion, verifier records, and all bundle files from inventory. |
| Q5 | **missing** — no source or executed likelihood output establishes the per-channel formula or stable factorial treatment; same sources searched. |
| Q6 | **missing** — no source or execution output establishes an independent-channel sum; same sources searched. |
| Q7 | **missing** — no finite `logL_b`/`logL_sb` output. `artifacts/manifest.json` and verifier both directly report absent results JSON. |
| Q8 | **missing** — no finite q or likelihood pair exists to check the stated identity; results JSON and source are absent. |
| Q9 | **missing** — no executable or run output establishes one-time use of every channel; sources searched as Q4. |
| Q10 | **missing** — no executed toy count; trajectory has no action and results JSON is absent. |
| Q11 | **missing** — no implementation/execution evidence for background-only Poisson means; sources searched as Q4. |
| Q12 | **missing** — no source or tail-count output establishes `q_toy <= q_observed`; sources searched as Q4. |
| Q13 | **missing** — no p-value, numerator, denominator, or equivalent calculation in any readable bundle artifact. |
| Q14 | **missing** — no binomial uncertainty/interval output; sources searched as Q4. |
| Q15 | **missing** — no p-value or finite Z output to test the conversion. |
| Q16 | **missing** — no Z or stated evidence conclusion was produced. |
| Q17 | **missing** — no submitted source/output establishes `lambda_i(mu)=mu*s_i+b_i` or `mu >= 0`. |
| Q18 | **missing** — no finite `mu_hat` or minimization result. |
| Q19 | **missing** — no profile scan/source establishes a zero-at-minimum definition. |
| Q20 | **missing** — no `mu_lo`, `mu_hi`, or crossing values. |
| Q21 | **missing** — no asymmetric uncertainties. |
| Q22 | **missing** — no boundary statement. |
| Q23 | **missing** — no agent likelihood/q values exist; evaluator reference comparison cannot be formed. |
| Q24 | **missing** — no agent tail count/toy count/p-value exists; reference interval comparison cannot be formed. |
| Q25 | **missing** — no agent Z exists; reference conversion comparison cannot be formed. |
| Q26 | **missing** — no agent profile values exist; reference comparison cannot be formed. |
| Q27 | **fail** — `verifier/score_report.json: diagnostics.files` is `[]` and `verifier/ctrf.json` marks diagnostics failed. No toy-distribution plot/observed marker was produced. |
| Q28 | **fail** — the same direct empty diagnostics finding leaves no profile scan/one-sigma plot. |
| Q29 | **fail** — the same direct empty diagnostics finding leaves no required histogram normalization to identify. |
| Q30 | **missing** — no source/config/output identifies RNG seed or state. |
| Q31 | **missing** — no source/config/output gives toy count, RNG algorithm/seed, scan/optimizer settings, or package versions. |
| Q32 | **missing** — no source/config/output establishes checks for non-finite likelihoods, invalid means, or failed crossings. |

The sole saved model text says it *intends* to inspect inputs and run at least one million toys, but this is an unsupported pre-action statement and is not used as evidence. The direct agent failure appears at `agent/openhands.txt:41-64`; the model response contains two choices and OpenHands raises `AssertionError: Only one choice is supported for now`. Harbor's completed state and zero verifier reward are retained as context only.
