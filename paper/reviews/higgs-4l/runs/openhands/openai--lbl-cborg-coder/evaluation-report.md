# Manual higgs-4l rubric evaluation

Manual evidence-backed, non-authoritative review of exactly `20260902T201549Z-higgs-4l-significance-openhands-1286844` / `20260902T201549Z-higgs-4l-signif__hJL9JqC` (OpenHands / `openai/lbl/cborg-coder`); it is not an indexed outcome grade. Self-run artifacts and verifier execution have different inputs, so their values are not combined. The verifier references are used only for Q23--Q26. Searched: metadata, trial/agent logs and trajectory, source/wrapper/README, results JSON, verifier JSON/stdout, artifact manifest, PNGs, workspace/session events, and readable tables/outputs.

## 1. Status summary
### Unspecified
| Status | OpenHands / openai/lbl/cborg-coder |
|---|---:|
| P | 23 |
| F | 2 |
| N | 0 |
| M | 7 |
| A | 0 |
| E | 0 |
| Harbor status / verifier reward | completed / 0.950000 |

## 2. Total reward (raw, no averaging)
| Cohort | OpenHands / openai/lbl/cborg-coder |
|---|---:|
| Unspecified | 23 / 32 |

## 3. Overall equal-category reward
| Cohort | OpenHands / openai/lbl/cborg-coder |
|---|---:|
| Unspecified | 0.658163 |

Fractions by rubric group: `2/3, 6/6, 6/7, 4/6, 3/4, 2/3, 0/3`; arithmetic mean `0.658163`.

## 4. Per-question binary rewards
### Unspecified
| Category | Question | OpenHands / openai/lbl/cborg-coder |
|---|---|---:|
| Execution and Documentation | Q1. Run timing | 1 |
| Execution and Documentation | Q2. Run cost | 0 |
| Execution and Documentation | Q3. Analysis documentation | 1 |
| Input and Likelihood Construction | Q4. Input generality | 1 |
| Input and Likelihood Construction | Q5. Poisson likelihood | 1 |
| Input and Likelihood Construction | Q6. Channel combination | 1 |
| Input and Likelihood Construction | Q7. Likelihood values | 1 |
| Input and Likelihood Construction | Q8. Observed test statistic | 1 |
| Input and Likelihood Construction | Q9. Input preservation | 1 |
| Background-Only Toy Significance | Q10. Toy count | 1 |
| Background-Only Toy Significance | Q11. Toy hypothesis | 1 |
| Background-Only Toy Significance | Q12. Tail convention | 1 |
| Background-Only Toy Significance | Q13. Toy p-value | 1 |
| Background-Only Toy Significance | Q14. Toy statistical uncertainty | 0 |
| Background-Only Toy Significance | Q15. Gaussian significance | 1 |
| Background-Only Toy Significance | Q16. Evidence conclusion | 1 |
| Signal-Strength Profile | Q17. Signal-strength model | 1 |
| Signal-Strength Profile | Q18. Best-fit strength | 1 |
| Signal-Strength Profile | Q19. Profile definition | 1 |
| Signal-Strength Profile | Q20. One-sigma crossings | 0 |
| Signal-Strength Profile | Q21. Asymmetric interval | 1 |
| Signal-Strength Profile | Q22. Boundary handling | 0 |
| Evaluator Reference Comparison | Q23. Likelihood reference agreement | 1 |
| Evaluator Reference Comparison | Q24. Toy p-value consistency | 1 |
| Evaluator Reference Comparison | Q25. Significance reference agreement | 1 |
| Evaluator Reference Comparison | Q26. Signal-strength reference agreement | 0 |
| Plotting and Presentation Quality | Q27. Toy-test-statistic diagnostic | 1 |
| Plotting and Presentation Quality | Q28. Profile diagnostic | 0 |
| Plotting and Presentation Quality | Q29. Plot normalization | 1 |
| Validation and Reproducibility | Q30. Randomness control | 0 |
| Validation and Reproducibility | Q31. Final configuration | 0 |
| Validation and Reproducibility | Q32. Numerical validity checks | 0 |

## 5. Per-question observed values and rewards
### Unspecified
| Category | Question | OpenHands / openai/lbl/cborg-coder |
|---|---|---|
| Execution and Documentation | Q1. Run timing | `321.438250 s`; `192.860688 s` [1] |
| Execution and Documentation | Q2. Run cost | `N/A` cost null [0] |
| Execution and Documentation | Q3. Analysis documentation | runnable README/method [1] |
| Input and Likelihood Construction | Q4. Input generality | input arrays; `len(observed)` [1] |
| Input and Likelihood Construction | Q5. Poisson likelihood | `-lambda+k log(lambda)-gammaln(k+1)` [1] |
| Input and Likelihood Construction | Q6. Channel combination | `np.sum` [1] |
| Input and Likelihood Construction | Q7. Likelihood values | `-11.0827503203`, `-5.8159224919` [1] |
| Input and Likelihood Construction | Q8. Observed test statistic | `q=-10.5336556567`; residual 0 [1] |
| Input and Likelihood Construction | Q9. Input preservation | all array elements vectorized [1] |
| Background-Only Toy Significance | Q10. Toy count | `1,000,000` [1] |
| Background-Only Toy Significance | Q11. Toy hypothesis | `Poisson(background)` [1] |
| Background-Only Toy Significance | Q12. Tail convention | `q_toy <= q_obs` [1] |
| Background-Only Toy Significance | Q13. Toy p-value | `0.000223=223/1,000,000` [1] |
| Background-Only Toy Significance | Q14. Toy statistical uncertainty | `N/A` [0] |
| Background-Only Toy Significance | Q15. Gaussian significance | `3.5112528289` [1] |
| Background-Only Toy Significance | Q16. Evidence conclusion | `Z>=3`, evidence stated [1] |
| Signal-Strength Profile | Q17. Signal-strength model | `mu*s+b`, `mu in [0,100]` [1] |
| Signal-Strength Profile | Q18. Best-fit strength | `1.6238873670` [1] |
| Signal-Strength Profile | Q19. Profile definition | `2*(NLL-min_NLL)` [1] |
| Signal-Strength Profile | Q20. One-sigma crossings | endpoints only; ordinates absent [0] |
| Signal-Strength Profile | Q21. Asymmetric interval | `+0.742485/-0.573362` [1] |
| Signal-Strength Profile | Q22. Boundary handling | `N/A` [0] |
| Evaluator Reference Comparison | Q23. Likelihood reference agreement | exact verifier equality [1] |
| Evaluator Reference Comparison | Q24. Toy p-value consistency | delta `-0.0001345`, 3-sigma interval contains ref [1] |
| Evaluator Reference Comparison | Q25. Significance reference agreement | delta `0.0019620` [1] |
| Evaluator Reference Comparison | Q26. Signal-strength reference agreement | lower delta `0.029225>0.02` [0] |
| Plotting and Presentation Quality | Q27. Toy-test-statistic diagnostic | density plus observed line [1] |
| Plotting and Presentation Quality | Q28. Profile diagnostic | `N/A` scan ordinates absent [0] |
| Plotting and Presentation Quality | Q29. Plot normalization | probability density [1] |
| Validation and Reproducibility | Q30. Randomness control | `N/A` no seed/state [0] |
| Validation and Reproducibility | Q31. Final configuration | `N/A` package versions absent [0] |
| Validation and Reproducibility | Q32. Numerical validity checks | missing required checks/fallback [0] |

## 6. Evidence and reasoning
### Execution and Documentation
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q1. Run timing | `321.438250 s`, `192.860688 s` [pass]; trial `result.json: started_at/finished_at, agent_execution`. |
| Q2. Run cost | `N/A` [missing]; top-level/trial `result.json: cost_usd` are null. |
| Q3. Analysis documentation | method/invocation [pass]; `artifacts/root/submission/README.md: Method, How to run`. |
### Input and Likelihood Construction
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q4. Input generality | [pass]; `analysis.py:18-20,30`, dynamic arrays/no fixed count. |
| Q5. Poisson likelihood | [pass]; `analysis.py:9-13`, formula plus `gammaln`. |
| Q6. Channel combination | [pass]; `analysis.py:12-13,24-25`, `np.sum`. |
| Q7. Likelihood values | [pass]; `results/results.json:2-3`, final execution recorded in trajectory. |
| Q8. Observed test statistic | [pass]; `results/results.json:4; analysis.py:27`, exact identity. |
| Q9. Input preservation | [pass]; `analysis.py:18-39`, no filtering/slicing/duplication. |
### Background-Only Toy Significance
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q10. Toy count | [pass]; `analysis.py:29`, executed final source. |
| Q11. Toy hypothesis | [pass]; `analysis.py:30`, background Poisson vector. |
| Q12. Tail convention | [pass]; `analysis.py:38-39`, final source corrects earlier opposite tail. |
| Q13. Toy p-value | [pass]; `results/results.json:5; analysis.py:29,39`, 223/1e6. |
| Q14. Toy statistical uncertainty | [missing]; no interval/uncertainty in results, README, source, logs, trajectory, or reports. |
| Q15. Gaussian significance | [pass]; `results/results.json:6; analysis.py:40`, inverse-normal conversion. |
| Q16. Evidence conclusion | [pass]; `events/73.json` final message and saved Z state 3-sigma evidence. |
### Signal-Strength Profile
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q17. Signal-strength model | [pass]; `analysis.py:43,48`, `mu*s+b`, lower bound zero. |
| Q18. Best-fit strength | [pass]; `results/results.json:7; analysis.py:48-50`, finite minimizer. |
| Q19. Profile definition | [pass]; `analysis.py:52-53`, relative to fitted minimum. |
| Q20. One-sigma crossings | [missing]; `results/results.json:8-9; analysis.py:57-70`, no saved profile values within 0.01 of one. |
| Q21. Asymmetric interval | [pass]; calculated from `results/results.json:7-9`. |
| Q22. Boundary handling | [missing]; no boundary-limited-endpoint statement in source outputs/reports. |
### Evaluator Reference Comparison
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q23. Likelihood reference agreement | [pass]; `verifier/score_report.json: test_statistic`, all values equal reference. |
| Q24. Toy p-value consistency | [pass]; `verifier/score_report.json: significance`, ref lies within 99.7% binomial interval. |
| Q25. Significance reference agreement | [pass]; same verifier section, delta 0.0019620. |
| Q26. Signal-strength reference agreement | [fail]; `verifier/score_report.json: signal_strength`, lower-edge delta 0.029225. |
### Plotting and Presentation Quality
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q27. Toy-test-statistic diagnostic | [pass]; `analysis.py:85-92`; readable `diagnostics/q_distribution.png`. |
| Q28. Profile diagnostic | [missing]; `analysis.py:96-103` implements it, but no saved finite scan values/crossing ordinate. |
| Q29. Plot normalization | [pass]; `analysis.py:87,90`, `density=True` and Probability Density. |
### Validation and Reproducibility
| Question | OpenHands / openai/lbl/cborg-coder |
|---|---|
| Q30. Randomness control | [missing]; no seed/RNG state in searched source/logs/outputs. |
| Q31. Final configuration | [missing]; count/range/resolution exist, but seed and package versions do not. |
| Q32. Numerical validity checks | [fail]; `analysis.py:43-45,57-70` lacks finite/input-Poisson checks and substitutes `mu_hat +/- 1` on failed crossings. |

### Exact artifact roots
- `results/paper/higgs-4l-significance-paper-version/openhands/openai--lbl-cborg-coder/20260902T201549Z-higgs-4l-significance-openhands-1286844/{result.json,job.log}`
- `results/paper/higgs-4l-significance-paper-version/openhands/openai--lbl-cborg-coder/20260902T201549Z-higgs-4l-significance-openhands-1286844/20260902T201549Z-higgs-4l-signif__hJL9JqC/{result.json,trial.log,agent,verifier,artifacts}`
