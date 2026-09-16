# Higgs Signal Strength Analysis

This package provides a statistical analysis of a four-lepton counting experiment to measure the signal strength $\mu$ of the Higgs boson.

## Methodology

1. **Likelihoods**: We use the Poisson log-likelihood for each channel $i$: 
   $$\log P(k_i | \lambda_i) = -\lambda_i + k_i \log(\lambda_i) - \log(k_i!)$$
   where $\lambda_i$ is either the background-only expectation ($B_i$) or the signal-plus-background expectation ($\mu S_i + B_i$).

2. **Test Statistic**: The observed likelihood-ratio test statistic is computed as:
   $$q = -2 \log \frac{L(\text{data} | S+B)}{L(\text{data} | B)} = -2 (\log L_{sb} - \log L_b)$$

3. **Significance**: We estimate the p-value by generating $10^6$ toy datasets from the background-only hypothesis. The p-value is the fraction of toys with $q_{toy} \ge q_{obs}$. The significance $Z$ is calculated as $\Phi^{-1}(1-p)$.

4. **Signal Strength $\mu$**: 
   - The best-fit $\hat{\mu}$ is the value that maximizes the likelihood (minimizes $-2\log L(\mu)$).
   - The $\pm 1\sigma$ interval is found by searching for $\mu$ values where $-2\Delta \log L(\mu) = q(\mu) - q(\hat{\mu}) = 1$.

## How to Run

Execute the `run.sh` script with the input JSON file and the desired output JSON path:

```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

## Diagnostics

Plots of the test statistic distribution and the profile likelihood scan are saved in the `diagnostics/` directory.
