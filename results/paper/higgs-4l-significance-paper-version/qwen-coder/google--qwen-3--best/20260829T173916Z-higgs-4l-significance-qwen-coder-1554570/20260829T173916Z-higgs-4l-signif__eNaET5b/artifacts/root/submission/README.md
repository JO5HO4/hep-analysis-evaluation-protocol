# Four-Lepton Higgs Search Statistical Analysis

This repository contains code for the statistical analysis of four-lepton (H→ZZ*→4l) Higgs search data. The analysis performs a complete statistical evaluation of the dataset, including likelihood calculation, significance determination, and signal strength measurement.

## Analysis Method

### 1. Likelihoods
For each independent final-state channel, we model the observed event counts as Poisson-distributed. The Poisson log-likelihood is computed as:

    logPoisson(k, λ) = -λ + k·log(λ) - log(k!)

We calculate the total log-likelihood of the observed data under two hypotheses:
- **Background-only hypothesis**: λ = background[i]
- **Signal-plus-background hypothesis**: λ = signal[i] + background[i]

### 2. Test Statistic
We form the likelihood-ratio test statistic:

    q = -2·(logL_sb - logL_b)

where logL_sb and logL_b are the signal-plus-background and background-only log-likelihoods, respectively.

### 3. Significance via Pseudo-Experiments
To estimate the background-only p-value of the observed result, we use pseudo-experiments (toy Monte Carlo):
- Generate 10^6 toy datasets by drawing Poisson counts from the background-only expectation
- Compute the test statistic for each toy
- Measure the fraction of toys with test statistic at least as large as the observed value
- Convert this p-value to a Gaussian significance Z = Φ⁻¹(1 - p)

### 4. Signal-Strength Measurement
We introduce a signal-strength parameter μ that scales the signal expectation, so channel i has mean μ·signal[i] + background[i]. We:
- Scan μ values to build the profile -2ΔlogL(μ) = q(μ) - min_μ q(μ)
- Find the best-fit μ̂ (the minimum of -2ΔlogL)
- Determine the asymmetric ±1σ interval from the two points where -2ΔlogL = 1

## Usage

### Running the Analysis

The analysis is executed through the `run.sh` script:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

Where:
- `INPUT_JSON`: Path to the input data file (in the same schema as `/root/data/four_lepton_counts.json`)
- `OUTPUT_JSON`: Path where the results will be saved

For example:

```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

### Input Data Schema

The input JSON file should have the following structure:

```json
{
  "channels": ["4mu", "2e2mu", "4e"],
  "observed": [6, 5, 2],
  "background": [1.25, 2.07, 1.53],
  "signal": [2.09, 2.29, 0.9]
}
```

### Output Data

The analysis produces a JSON results file with the following fields:

- `logL_b`: Total background-only log-likelihood of the observed data
- `logL_sb`: Total signal-plus-background log-likelihood of the observed data
- `test_statistic`: Observed test statistic q
- `p_value`: Background-only p-value from pseudo-experiments
- `significance`: Gaussian significance Z
- `mu_hat`: Best-fit signal strength μ̂
- `mu_lo`: Lower edge of the ±1σ interval
- `mu_hi`: Upper edge of the ±1σ interval

Additionally, diagnostic plots are saved in the `diagnostics/` directory:
- `test_statistic_distribution.png`: Distribution of test statistics from pseudo-experiments with the observed value marked
- `delta_logL_scan.png`: Plot of -2ΔlogL(μ) vs μ showing the best-fit value and 1σ interval

## Code Structure

- `run.sh`: Main executable script that orchestrates the analysis
- `analysis.py`: Python script that performs the statistical analysis
- `plot_diagnostics.py`: Python script that generates diagnostic plots
- `README.md`: This documentation file

## Dependencies

The analysis requires the following Python packages:
- numpy
- scipy
- matplotlib

These can be installed with:

```bash
pip install numpy scipy matplotlib
```

## Reproducibility

All code needed to reproduce the analysis is included in the `/root/submission` directory. The analysis is designed to be reproducible with the same input data and random seed (though the pseudo-experiments use random sampling, so results will vary slightly between runs).