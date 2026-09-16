# Manual Evaluation Report — higgs-4l

Non-authoritative manual evidence review; no authoritative outcome grade. Evidence root below is `20260829T164001Z-higgs-4l-signif__CqRrCvf`.

## 1. Status Summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| OpenHands / gpt-5.6-terra | 1 | 0 | 31 | completed / 0.000000 |

## 2. Total Reward (Raw, No Averaging)

| Summary | OpenHands / gpt-5.6-terra |
|---|---:|
| Total reward | 1 / 32 |

## 3. Overall Equal-Category Reward

| Summary | OpenHands / gpt-5.6-terra |
|---|---:|
| Overall equal-category reward | 0.047619 |

Category fractions: `1/3, 0/6, 0/7, 0/6, 0/4, 0/3, 0/3`; arithmetic mean `1/21`.

## 4. Per-Question Binary Rewards

| Category | Question | OpenHands / gpt-5.6-terra |
|---|---|---:|
| Execution | Q1. Run timing | 1 |
| Execution | Q2. Run cost | 0 |
| Execution | Q3. Analysis documentation | 0 |
| Likelihood | Q4. Input generality | 0 |
| Likelihood | Q5. Poisson likelihood | 0 |
| Likelihood | Q6. Channel combination | 0 |
| Likelihood | Q7. Likelihood values | 0 |
| Likelihood | Q8. Observed test statistic | 0 |
| Likelihood | Q9. Input preservation | 0 |
| Toys | Q10. Toy count | 0 |
| Toys | Q11. Toy hypothesis | 0 |
| Toys | Q12. Tail convention | 0 |
| Toys | Q13. Toy p-value | 0 |
| Toys | Q14. Toy statistical uncertainty | 0 |
| Toys | Q15. Gaussian significance | 0 |
| Toys | Q16. Evidence conclusion | 0 |
| Profile | Q17. Signal-strength model | 0 |
| Profile | Q18. Best-fit strength | 0 |
| Profile | Q19. Profile definition | 0 |
| Profile | Q20. One-sigma crossings | 0 |
| Profile | Q21. Asymmetric interval | 0 |
| Profile | Q22. Boundary handling | 0 |
| Reference | Q23. Likelihood reference agreement | 0 |
| Reference | Q24. Toy p-value consistency | 0 |
| Reference | Q25. Significance reference agreement | 0 |
| Reference | Q26. Signal-strength reference agreement | 0 |
| Plots | Q27. Toy-test-statistic diagnostic | 0 |
| Plots | Q28. Profile diagnostic | 0 |
| Plots | Q29. Plot normalization | 0 |
| Validation | Q30. Randomness control | 0 |
| Validation | Q31. Final configuration | 0 |
| Validation | Q32. Numerical validity checks | 0 |

## 5. Per-Question Observed Values and Rewards

| Category | Question | OpenHands / gpt-5.6-terra |
|---|---|---|
| Execution | Q1 | trial `226.232730 s`; agent `25.292952 s` [1] |
| Execution | Q2 | `cost_usd: null` [0] |
| Execution | Q3 | no README/method [0] |
| Likelihood | Q4 | no executable [0] |
| Likelihood | Q5 | no Poisson implementation [0] |
| Likelihood | Q6 | no sum implementation [0] |
| Likelihood | Q7 | no `logL_b`/`logL_sb` [0] |
| Likelihood | Q8 | no observed q [0] |
| Likelihood | Q9 | no input execution [0] |
| Toys | Q10 | no toy count [0] |
| Toys | Q11 | no toy hypothesis [0] |
| Toys | Q12 | no tail convention [0] |
| Toys | Q13 | no p-value/count [0] |
| Toys | Q14 | no uncertainty [0] |
| Toys | Q15 | no Z [0] |
| Toys | Q16 | no conclusion [0] |
| Profile | Q17 | no mu model [0] |
| Profile | Q18 | no `mu_hat` [0] |
| Profile | Q19 | no profile [0] |
| Profile | Q20 | no crossings [0] |
| Profile | Q21 | no uncertainties [0] |
| Profile | Q22 | no boundary statement [0] |
| Reference | Q23 | agent values unavailable [0] |
| Reference | Q24 | agent toys unavailable [0] |
| Reference | Q25 | agent Z unavailable [0] |
| Reference | Q26 | agent profile unavailable [0] |
| Plots | Q27 | no toy plot [0] |
| Plots | Q28 | no profile plot [0] |
| Plots | Q29 | no normalization [0] |
| Validation | Q30 | no seed/RNG state [0] |
| Validation | Q31 | no numerical settings [0] |
| Validation | Q32 | no validity checks [0] |

## 6. Per-Question Evidence and Reasoning

`result.json` establishes Harbor completion and timings. `agent/openhands.txt:41-64` establishes the pre-action `AssertionError`. `agent/trajectory.json: steps` has only four context steps and no action. `artifacts/manifest.json` records an empty exported submission directory and failed `/root/results/results.json`; `verifier/score_report.json` names missing `run.sh` and results. The readable root was enumerated with `rg --files`; logs, trajectory, metadata, verifier files, artifact manifest, session events, tables/outputs, plots, workspaces, and the empty `artifacts/root/submission/` were inspected. No source, report, JSON/CSV/Parquet output, plot, or workspace was present. Each `missing` below is absence after that concrete search, not an inference from a preferred filename.

| Question | OpenHands / gpt-5.6-terra |
|---|---|
| Q1 | `pass`; trial `result.json: started_at/finished_at` gives 226.232730 s; `agent_execution` gives 25.292952 s. |
| Q2 | `missing`; top-level `stats.cost_usd` and trial `agent_result.cost_usd` are both null. |
| Q3 | `missing`; no README or runnable method in transcript or empty submission. |
| Q4 | `missing`; no executable source establishes arbitrary channel handling. |
| Q5 | `missing`; no source/output establishes the Poisson formula. |
| Q6 | `missing`; no source/output establishes channel summation. |
| Q7 | `missing`; failed results artifact contains no finite likelihoods. |
| Q8 | `missing`; no finite observed q in logs/source/output. |
| Q9 | `missing`; no input-processing execution evidence. |
| Q10 | `missing`; no reported integer toy count. |
| Q11 | `missing`; no toy-generation implementation. |
| Q12 | `missing`; no tail comparison definition. |
| Q13 | `missing`; no p-value numerator/denominator. |
| Q14 | `missing`; no binomial uncertainty/interval. |
| Q15 | `missing`; no p-value or finite Z. |
| Q16 | `missing`; no evidence conclusion. |
| Q17 | `missing`; no mu model/domain implementation. |
| Q18 | `missing`; no finite profile minimum. |
| Q19 | `missing`; no relative profile definition/values. |
| Q20 | `missing`; no finite one-sigma crossings. |
| Q21 | `missing`; no asymmetric uncertainties. |
| Q22 | `missing`; no physical-boundary statement. |
| Q23 | `missing`; no agent likelihood/q values for evaluator comparison. |
| Q24 | `missing`; no agent tail count/toy count for interval comparison. |
| Q25 | `missing`; no agent Z for reference conversion. |
| Q26 | `missing`; no agent profile values for reference comparison. |
| Q27 | `missing`; empty submission and empty `/logs/artifacts`; no toy diagnostic/marker. |
| Q28 | `missing`; no profile scan/one-sigma diagnostic. |
| Q29 | `missing`; no histogram/table identifies a statistical unit. |
| Q30 | `missing`; no pseudo-experiment seed or RNG state. |
| Q31 | `missing`; no toy/RNG/scan/package configuration. |
| Q32 | `missing`; no checks for invalid means, non-finite likelihoods, or failed crossings. |
