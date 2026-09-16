# Higgs Search Statistical Analysis

This project implements a statistical analysis of a four-lepton Higgs search counting experiment.

## Method

1. **Likelihood Calculation**: 
   The total log-likelihood is computed as the sum of Poisson log-likelihoods across all channels:
   $$\log L(\mu) = \sum_i [ -\lambda_i + k_i \ln \lambda_i - \ln(k_i!) ]$$
   where $\lambda_i = \mu \cdot s_i + b_i$.
   - Background-only hypothesis: $\mu = 0$.
   - Signal-plus-background hypothesis: $\mu = 1$.

2. **Test Statistic**:
   The test statistic is defined as $q = -2(\log L_{sb} - \log L_b)$.
   Under this definition, a more negative $q$ indicates data that is more signal-like.

3. **P-value and Significance**:
   We generate $10^6$ pseudo-experiments (toys) where event counts are drawn from $\text{Poisson}(b_i)$.
   The p-value is the fraction of toys where $q_{toy} \le q_{obs}$.
   The significance $Z$ is computed as $Z = \Phi^{-1}(1 - p)$.

4. **Signal Strength $\mu$**:
   - The best-fit $\hat{\mu}$ is found by maximizing $\log L(\mu)$.
   - The $\pm 1\sigma$ interval is determined by finding $\mu$ values where $-2\Delta \log L(\mu) = 2(\log L(\hat{\mu}) - \log L(\mu)) = 1$.

## How to Run

Execute the provided shell script with the input and output JSON paths:

```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

## Diagnostics

Plots of the test statistic distribution and the profile likelihood scan are saved in `/root/submission/diagnostics/`.
