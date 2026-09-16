# Higgs Search Statistical Analysis

This tool performs a statistical analysis of 4-lepton Higgs search data.

## Method
1.  **Likelihood calculation**: Poisson log-likelihood is computed for background-only ($H_b$) and signal-plus-background ($H_{sb}$) hypotheses.
2.  **Test statistic**: $q = -2(\log L_{sb} - \log L_b)$ is used to quantify the signal-likeness.
3.  **P-value**: Estimated using $10^6$ pseudo-experiments drawn from the background-only expectation. The p-value is the fraction of toys where $q_{toy} \le q_{obs}$.
4.  **Significance**: Gaussian significance $Z = \Phi^{-1}(1 - p)$.
5.  **Signal Strength**: Best-fit $\hat{\mu}$ is found by minimizing $-2\log L(\mu)$. The $1\sigma$ interval is derived from the points where $-2\Delta\log L = 1$.

## How to run
Run the following bash script:
\`\`\`/root/submission/run.sh INPUT_JSON OUTPUT_JSON\`\`\`

## Diagnostics
Plots of the test statistic distribution and the likelihood scan are saved in `/root/submission/diagnostics/`.
