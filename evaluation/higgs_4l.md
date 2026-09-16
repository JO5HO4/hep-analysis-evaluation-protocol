# Higgs to Four-Lepton Significance Evaluation Rubric

Each criterion follows the shared evaluation status, binary-reward, and flexible evidence policy in [evaluation_rubric.md](evaluation_rubric.md). This is a natural-language review rubric, not an authoritative outcome grader. Workflow behavior is reported separately under the non-scoring [workflow-characterization protocol](workflow-characterization.md).

The statistical convention is the physical domain `mu >= 0`. Reference comparisons use an evaluator-owned calculation on the same input counts and are development evidence unless an indexed evaluation spec selects them.

## Group I: Execution and Documentation

| Criterion | Desired answer | Scoring |
|---|---|---|
| 1. Run timing | Both trial wall-clock and pure agent execution time established | 1 if direct evidence establishes both times as finite nonnegative values with units; otherwise 0. |
| 2. Run cost | Total cost established in USD | 1 if direct evidence establishes one finite nonnegative USD total, including `$0.00`; otherwise 0. |
| 3. Analysis documentation | Runnable method and statistical assumptions described | 1 if direct evidence describes how to run the analysis, the likelihood, toys, and signal-strength scan; otherwise 0. |

## Group II: Input and Likelihood Construction

| Criterion | Desired answer | Scoring |
|---|---|---|
| 4. Input generality | Arbitrary valid channel count supported | 1 if direct evidence establishes that the executable reads the specified count schema without a hard-coded channel count; otherwise 0. |
| 5. Poisson likelihood | Correct per-channel log likelihood | 1 if direct evidence establishes `-lambda + k*log(lambda) - log(k!)` for every channel and a numerically stable factorial term; otherwise 0. |
| 6. Channel combination | Independent-channel sum used | 1 if direct evidence establishes that total log likelihood is summed over all input channels; otherwise 0. |
| 7. Likelihood values | Finite `logL_b` and `logL_sb` reported | 1 if direct execution evidence gives both finite values; otherwise 0. |
| 8. Observed test statistic | Exact likelihood-ratio definition used | 1 if direct execution evidence gives finite `q` satisfying `abs(q + 2*(logL_sb-logL_b)) <= 1e-8 * max(1, abs(q))`; otherwise 0. |
| 9. Input preservation | All input channels used once | 1 if direct evidence establishes that no input channel was silently dropped or duplicated; otherwise 0. |

## Group III: Background-Only Toy Significance

| Criterion | Desired answer | Scoring |
|---|---|---|
| 10. Toy count | At least one million toys | 1 if direct execution evidence gives an integer toy count `N >= 1,000,000`; otherwise 0. |
| 11. Toy hypothesis | Background-only Poisson means used | 1 if direct evidence establishes independent channel counts drawn from each channel's background expectation; otherwise 0. |
| 12. Tail convention | Signal-like tail defined correctly | 1 if direct evidence establishes the background-tail count uses `q_toy <= q_observed` for the task-defined q statistic; otherwise 0. |
| 13. Toy p-value | Finite p-value with numerator and denominator established | 1 if direct execution evidence gives finite `0 < p_value <= 1`, toy count, and tail-count or equivalent direct calculation; otherwise 0. |
| 14. Toy statistical uncertainty | Binomial uncertainty established | 1 if direct evidence gives the binomial uncertainty or interval corresponding to the reported toy count and p-value; otherwise 0. |
| 15. Gaussian significance | Correct p-to-Z conversion used | 1 if direct evidence gives finite `Z` equal to `Phi^-1(1-p_value)` within `1e-6`; otherwise 0. |
| 16. Evidence conclusion | 3-sigma statement agrees with Z | 1 if the stated conclusion is “evidence” exactly when `Z >= 3`; otherwise 0. |

## Group IV: Signal-Strength Profile

| Criterion | Desired answer | Scoring |
|---|---|---|
| 17. Signal-strength model | `lambda_i(mu) = mu*s_i + b_i`, with `mu >= 0` | 1 if direct evidence establishes this model and domain; otherwise 0. |
| 18. Best-fit strength | Finite profile minimum found | 1 if direct execution evidence gives finite `mu_hat >= 0` and establishes it minimizes the profile; otherwise 0. |
| 19. Profile definition | `-2 Delta log L` relative to the minimum | 1 if direct evidence establishes the profile is zero at `mu_hat` and is defined relative to the fitted minimum; otherwise 0. |
| 20. One-sigma crossings | Both profile crossings solved | 1 if direct execution evidence gives finite `mu_lo <= mu_hat <= mu_hi` and profile values within `0.01` of 1 at both endpoints; otherwise 0. |
| 21. Asymmetric interval | Both uncertainties reported | 1 if direct evidence gives `mu_hat-mu_lo` and `mu_hi-mu_hat` as finite nonnegative uncertainties; otherwise 0. |
| 22. Boundary handling | Physical-boundary behavior stated | 1 if direct evidence states whether `mu_lo=0` is a boundary-limited interval endpoint; otherwise 0. |

## Group V: Evaluator Reference Comparison

| Criterion | Desired answer | Scoring |
|---|---|---|
| 23. Likelihood reference agreement | Likelihoods and q agree with reference | 1 if `logL_b`, `logL_sb`, and q each agree with evaluator reference within `1e-6 * max(1, abs(reference))`; otherwise 0. |
| 24. Toy p-value consistency | Toy result statistically agrees with reference tail probability | 1 if the evaluator reference p-value lies within the agent's two-sided 99.7% binomial interval for its reported tail count and toy count; otherwise 0. |
| 25. Significance reference agreement | Z agrees with reference p-value conversion | 1 if agent Z agrees with the reference p-to-Z conversion within `0.02`; otherwise 0. |
| 26. Signal-strength reference agreement | Profile results agree with reference | 1 if `mu_hat`, `mu_lo`, and `mu_hi` each agree with evaluator reference within `0.02`; otherwise 0. |

## Group VI: Plotting and Presentation Quality

| Criterion | Desired answer | Scoring |
|---|---|---|
| 27. Toy-test-statistic diagnostic | Quantity and observed marker established | 1 if direct evidence establishes the toy test-statistic distribution, its statistical unit or normalization, and the observed-q marker; otherwise 0. |
| 28. Profile diagnostic | Profile quantity and one-sigma level established | 1 if direct evidence establishes a `-2 Delta log L(mu)` scan with the `1` crossing level and finite plotted values; otherwise 0. |
| 29. Plot normalization | Statistical unit established | 1 if direct evidence identifies each required histogram as count, normalized density, or fraction; otherwise 0. |

## Group VII: Validation and Reproducibility

| Criterion | Desired answer | Scoring |
|---|---|---|
| 30. Randomness control | Toy generator seed or RNG state established | 1 if direct evidence identifies the pseudo-experiment RNG seed or reproducible RNG state; otherwise 0. |
| 31. Final configuration | Required numerical settings established | 1 if direct evidence gives toy count, RNG algorithm/seed, mu scan range and resolution or optimizer tolerance, and numerical package versions; otherwise 0. |
| 32. Numerical validity checks | Invalid numerical states checked | 1 if direct evidence establishes checks for non-finite likelihoods, invalid Poisson means, and failed interval crossings; otherwise 0. |
