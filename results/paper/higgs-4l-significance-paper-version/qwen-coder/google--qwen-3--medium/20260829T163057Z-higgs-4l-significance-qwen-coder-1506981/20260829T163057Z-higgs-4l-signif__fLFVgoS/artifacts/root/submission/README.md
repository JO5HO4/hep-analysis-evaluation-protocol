# Four-Lepton Higgs Search Statistical Analysis

This repository contains code for the statistical analysis of a four-lepton (H→ZZ*→4l) Higgs search. The analysis follows the requirements specified in the task description, performing a complete statistical analysis of the dataset to determine the significance of any potential Higgs signal and to measure the signal strength.

## Methodology

The analysis implements the following steps:

1. **Likelihoods**: Using the Poisson log-likelihood function, we compute the total log-likelihood of the observed data under the background-only hypothesis and under the signal-plus-background hypothesis (summed over channels).

2. **Test Statistic**: We form the likelihood-ratio test statistic q = -2·(logL_sb - logL_b) for the observed data, where logL_sb and logL_b are the signal-plus-background and background-only log-likelihoods.

3. **Significance via Pseudo-experiments**: We estimate the background-only p-value of the observed result using pseudo-experiments (toy Monte Carlo). We generate 10^6 toy datasets by drawing Poisson counts from the background-only expectation, compute the test statistic for each toy, and measure the fraction that are at least as signal-like as the observed data. This p-value is then converted into a Gaussian significance Z = Φ⁻¹(1 - p).

4. **Signal-strength Measurement**: We introduce a signal-strength parameter μ that scales the signal expectation. We scan μ, build the profile -2ΔlogL(μ) = q(μ) - min_μ q(μ), find the best-fit μ̂ (the minimum), and determine the asymmetric ±1σ interval from the two points where -2ΔlogL = 1.

## Directory Structure

- `run.sh`: Main entry point script that runs the analysis
- `analyze.py`: Python script implementing the full statistical analysis
- `diagnostics/`: Directory containing diagnostic plots
  - `test_statistic_distribution.png`: Distribution of test statistic from pseudo-experiments
  - `signal_strength_scan.png`: Signal strength scan showing -2ΔlogL(μ)

## Requirements

- Python 3
- NumPy
- SciPy
- Matplotlib

## How to Run

The analysis is executed through the `run.sh` script, which takes two arguments:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

Where:
- `INPUT_JSON` is the path to the input JSON file containing the event counts
- `OUTPUT_JSON` is the path where the results JSON file will be written

For example:

```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

The script will perform the complete analysis and write the results to the specified output file. Diagnostic plots will be saved in the `diagnostics` directory.

## Output

The results JSON file contains the following fields:
- `logL_b`: total background-only log-likelihood of the observed data
- `logL_sb`: total signal-plus-background log-likelihood of the observed data
- `test_statistic`: observed q = -2·(logL_sb - logL_b)
- `p_value`: background-only p-value from pseudo-experiments
- `significance`: the Gaussian significance Z
- `mu_hat`: best-fit signal strength μ̂
- `mu_lo`: lower edge of the ±1σ interval
- `mu_hi`: upper edge of the ±1σ interval

## References

This analysis follows standard statistical methods used in high-energy physics, particularly the profile likelihood method for parameter estimation and the use of pseudo-experiments for significance calculation.