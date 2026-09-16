# Four-Lepton Higgs Search Statistical Analysis

This directory contains the analysis code for a counting experiment in the $H \to ZZ^* \to 4\ell$ channel.

## Method

The analysis performs a Poisson likelihood ratio test to determine the significance of the signal relative to the background-only hypothesis.

### 1. Likelihood Calculation
For each channel $i$, the Poisson log-likelihood is:
$$\log \mathcal{L}(k_i, \lambda_i) = -\lambda_i + k_i \ln(\lambda_i) - \ln(k_i!)$$
The total log-likelihood is the sum over all channels.

### 2. Test Statistic
The test statistic is defined as:
$$q = -2 (\log \mathcal{L}_{s+b} - \log \mathcal{L}_b)$$
A more negative value of $q$ indicates a result that is more compatible with the signal-plus-background hypothesis than with the background-only hypothesis.

### 3. Significance (Toy Monte Carlo)
The background-only $p$-value is estimated by generating $10^6$ pseudo-experiments. For each toy:
1. Observed counts are drawn from a Poisson distribution with the background-only mean $\lambda_i = b_i$.
2. The test statistic $q_{toy}$ is computed.
3. $p = P(q_{toy} \le q_{obs} | H_b)$.
The Gaussian significance is then $Z = \Phi^{-1}(1 - p)$.

### 4. Signal Strength Measurement
We introduce a signal strength parameter $\mu$ such that the mean in channel $i$ is $\lambda_i(\mu) = \mu s_i + b_i$.
The best-fit $\hat{\mu}$ is the value that maximizes the total log-likelihood.
The $1\sigma$ confidence interval is found by identifying $\mu_{lo}$ and $\mu_{hi}$ such that:
$$-2(\log \mathcal{L}(\mu) - \log \mathcal{L}(\hat{\mu})) = 1$$

## How to Run

The analysis is executed via a shell script:
```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

## Deliverables
- `analysis.py`: The Python script implementing the statistical logic.
- `run.sh`: Wrapper script for execution.
- `diagnostics/`: Contains plots of the $q$ distribution and the profile likelihood scan.
