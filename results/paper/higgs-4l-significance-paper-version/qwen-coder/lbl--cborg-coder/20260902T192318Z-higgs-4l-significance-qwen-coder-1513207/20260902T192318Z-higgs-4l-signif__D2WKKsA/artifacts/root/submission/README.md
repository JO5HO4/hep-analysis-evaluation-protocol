# Statistical Analysis of H->ZZ*->4l Search

This directory contains the tools to perform a Poisson likelihood analysis of event counts across multiple channels.

## Methodology

1.  **Likelihood Calculation**: 
    The analysis uses the Poisson log-likelihood summed over all channels:
    `logL = sum(-λ_i + k_i * log(λ_i) - log(k_i!))`
    where `k_i` is the observed count and `λ_i` is the expected count.

2.  **Test Statistic**:
    The test statistic is computed as `q = -2 * (logL_sb - logL_b)`, where `logL_sb` is the log-likelihood under the signal-plus-background hypothesis and `logL_b` is under the background-only hypothesis.

3.  **P-value and Significance**:
    The background-only p-value is estimated using $10^6$ pseudo-experiments. For each toy dataset, event counts are drawn from a Poisson distribution with the background-only expectation. The p-value is the fraction of toy test statistics that are at least as signal-like as the observed `q`. This is converted to a Gaussian significance $Z = \Phi^{-1}(1-p)$.

4.  **Signal Strength μ**:
    The signal strength $\mu$ is the factor scaling the predicted signal. The best-fit $\hat{\mu}$ is found by minimizing $-logL(\mu)$. The $1\sigma$ interval is determined by finding the values of $\mu$ where $-2\Delta logL(\mu) = 1$, where $-2\Delta logL(\mu) = 2(logL(\hat{\mu}) - logL(\mu))$.

## How to Run

Run the analysis using the provided shell script:
```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

## Deliverables
- `run.sh`: Wrapper script.
- `run_analysis.py`: Main Python implementation.
- `diagnostics/`: Directory containing plots of the test statistic distribution and the likelihood profile.
