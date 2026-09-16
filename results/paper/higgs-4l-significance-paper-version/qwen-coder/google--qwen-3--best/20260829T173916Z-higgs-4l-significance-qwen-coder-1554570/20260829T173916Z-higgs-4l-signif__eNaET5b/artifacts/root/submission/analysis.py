#!/usr/bin/env python3
"""
Statistical analysis for four-lepton Higgs search data.
Performs likelihood analysis, significance calculation, and signal strength measurement.
"""

import json
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
import sys
import os


def log_poisson(k, lam):
    """Compute the log of the Poisson probability P(k | λ)."""
    if lam <= 0:
        return -np.inf
    if k == 0:
        return -lam
    return -lam + k * np.log(lam) - np.log(np.arange(1, k+1)).sum()

def total_log_likelihood(observed, expected):
    """Compute total log-likelihood for all channels."""
    return sum(log_poisson(k, lam) for k, lam in zip(observed, expected))

def test_statistic(observed, background, signal):
    """Compute the likelihood-ratio test statistic q = -2*(logL_sb - logL_b)."""
    logL_b = total_log_likelihood(observed, background)
    logL_sb = total_log_likelihood(observed, [b + s for b, s in zip(background, signal)])
    return -2 * (logL_sb - logL_b)

def pseudo_experiments(background, signal, observed, n_toys=1000000):
    """Run pseudo-experiments to estimate the background-only p-value."""
    # Compute observed test statistic
    q_obs = test_statistic(observed, background, signal)
    
    # Generate toy datasets and compute test statistics
    q_toys = []
    for _ in range(n_toys):
        # Draw Poisson counts from background-only hypothesis
        toy_data = [np.random.poisson(b) for b in background]
        
        # Compute test statistic for this toy
        q_toy = test_statistic(toy_data, background, signal)
        q_toys.append(q_toy)
    
    # Estimate p-value as fraction of toys with q >= q_obs
    p_value = np.mean([q >= q_obs for q in q_toys])
    
    # Convert to Gaussian significance
    significance = stats.norm.ppf(1 - p_value) if p_value < 1 else 0
    
    return q_obs, q_toys, p_value, significance

def signal_strength_scan(observed, background, signal, n_points=1000):
    """Scan signal strength μ and compute -2ΔlogL(μ)."""
    # Define log-likelihood as a function of μ
    def log_likelihood(mu):
        expected = [mu * s + b for s, b in zip(signal, background)]
        return total_log_likelihood(observed, expected)
    
    # Find the best-fit μ that maximizes the log-likelihood
    result = minimize_scalar(lambda mu: -log_likelihood(mu), bounds=(0, 10), method='bounded')
    mu_hat = result.x
    
    # Compute -2ΔlogL(μ) = q(μ) - min_μ q(μ)
    # where q(μ) = -2*(logL(μ) - logL_b)
    logL_b = total_log_likelihood(observed, background)
    min_q = -2 * (log_likelihood(mu_hat) - logL_b)
    
    # Scan over a range of μ values
    mu_values = np.linspace(0, 5, n_points)
    delta_logL2 = []
    for mu in mu_values:
        q_mu = -2 * (log_likelihood(mu) - logL_b)
        delta_logL2.append(q_mu - min_q)
    
    # Find the ±1σ interval (where -2ΔlogL = 1)
    # Interpolate to find the precise values
    mu_lo = 0.0
    mu_hi = 5.0
    
    # Find lower bound
    for i in range(len(mu_values) - 1):
        if mu_values[i] >= mu_hat:
            break
        if delta_logL2[i] <= 1 and delta_logL2[i+1] > 1:
            # Linear interpolation
            frac = (1 - delta_logL2[i]) / (delta_logL2[i+1] - delta_logL2[i])
            mu_lo = mu_values[i] + frac * (mu_values[i+1] - mu_values[i])
            break
    
    # Find upper bound
    for i in range(len(mu_values) - 1):
        if mu_values[i] > mu_hat and delta_logL2[i] > 1:
            # Linear interpolation
            frac = (1 - delta_logL2[i-1]) / (delta_logL2[i] - delta_logL2[i-1])
            mu_hi = mu_values[i-1] + frac * (mu_values[i] - mu_values[i-1])
            break
    
    return mu_hat, mu_lo, mu_hi, mu_values, delta_logL2, min_q

def main(input_json, output_json):
    """Main function to run the complete analysis."""
    # Read input data
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    observed = data['observed']
    background = data['background']
    signal = data['signal']
    
    # 1. Compute log-likelihoods
    logL_b = total_log_likelihood(observed, background)
    logL_sb = total_log_likelihood(observed, [b + s for b, s in zip(background, signal)])
    
    # 2. Compute test statistic
    q_obs = test_statistic(observed, background, signal)
    
    # 3. Run pseudo-experiments
    print("Running pseudo-experiments (this may take a while)...")
    q_obs, q_toys, p_value, significance = pseudo_experiments(background, signal, observed, n_toys=1000000)
    
    # 4. Signal strength measurement
    mu_hat, mu_lo, mu_hi, mu_values, delta_logL2, min_q = signal_strength_scan(observed, background, signal)
    
    # Create results dictionary
    results = {
        "logL_b": logL_b,
        "logL_sb": logL_sb,
        "test_statistic": q_obs,
        "p_value": p_value,
        "significance": significance,
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi
    }
    
    # Save results
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Create diagnostics directory if it doesn't exist
    diagnostics_dir = os.path.join(os.path.dirname(output_json), "diagnostics")
    os.makedirs(diagnostics_dir, exist_ok=True)
    
    # Save diagnostic data for plotting
    diagnostics = {
        "mu_values": mu_values.tolist(),
        "delta_logL2": delta_logL2,
        "q_toys": q_toys,
        "q_obs": q_obs
    }
    
    with open(os.path.join(diagnostics_dir, "diagnostics.json"), 'w') as f:
        json.dump(diagnostics, f)
    
    return results

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analysis.py INPUT_JSON OUTPUT_JSON")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    
    results = main(input_json, output_json)
    
    # Print summary
    print(f"\nAnalysis complete!")
    print(f"Background-only log-likelihood: {results['logL_b']:.3f}")
    print(f"Signal+background log-likelihood: {results['logL_sb']:.3f}")
    print(f"Test statistic (q): {results['test_statistic']:.3f}")
    print(f"p-value: {results['p_value']:.6f}")
    print(f"Significance: {results['significance']:.3f}σ")
    print(f"Best-fit signal strength (μ̂): {results['mu_hat']:.3f}")
    print(f"1σ interval: [{results['mu_lo']:.3f}, {results['mu_hi']:.3f}]")
    
    # Check if significance reaches 3σ "evidence" level
    if results['significance'] >= 3:
        print(f"\nRESULT: The analysis reaches the 3σ 'evidence' level.")
    else:
        print(f"\nRESULT: The analysis does not reach the 3σ 'evidence' level.")
