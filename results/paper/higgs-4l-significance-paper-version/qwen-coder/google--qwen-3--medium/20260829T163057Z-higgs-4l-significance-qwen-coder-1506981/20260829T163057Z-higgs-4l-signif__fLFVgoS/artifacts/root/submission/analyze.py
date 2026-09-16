#!/usr/bin/env python3
"""
Statistical analysis for four-lepton Higgs search.
Performs likelihood analysis, significance calculation, and signal-strength measurement.
"""

import json
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import argparse


def log_poisson(k, lam):
    """Compute log(Poisson(k|lambda)) = -lambda + k*log(lambda) - log(k!)"""
    if lam <= 0:
        return -np.inf
    if k == 0:
        return -lam
    return -lam + k * np.log(lam) - np.sum(np.log(np.arange(1, k+1)))


def total_log_likelihood(observed, expected):
    """Compute total log-likelihood for all channels"""
    return sum(log_poisson(k, lam) for k, lam in zip(observed, expected))


def test_statistic(observed, background, signal):
    """Compute test statistic q = -2*(logL_sb - logL_b)"""
    logL_b = total_log_likelihood(observed, background)
    logL_sb = total_log_likelihood(observed, [b + s for b, s in zip(background, signal)])
    return -2 * (logL_sb - logL_b)


def pseudo_experiments(background, signal, observed, n_toys=1000000):
    """Estimate p-value using pseudo-experiments"""
    # Calculate observed test statistic
    q_obs = test_statistic(observed, background, signal)
    
    # Generate toy datasets and compute test statistics
    q_toys = []
    for _ in range(n_toys):
        # Draw Poisson counts from background-only hypothesis
        toy_data = [np.random.poisson(b) for b in background]
        # Calculate test statistic for this toy
        q_toy = test_statistic(toy_data, background, signal)
        q_toys.append(q_toy)
    
    # Calculate p-value: fraction of toys with q >= q_obs
    p_value = np.mean([q >= q_obs for q in q_toys])
    
    # Convert to Gaussian significance
    significance = stats.norm.ppf(1 - p_value) if p_value < 0.5 else -stats.norm.ppf(p_value)
    
    return p_value, significance, q_obs, q_toys


def signal_strength_scan(observed, background, signal, n_points=1000):
    """Scan signal strength parameter μ and find best-fit value and uncertainties"""
    # Define -2ΔlogL(μ) = q(μ) - min_μ q(μ)
    def q_mu(mu):
        # Expected counts under signal strength μ
        expected = [mu * s + b for s, b in zip(signal, background)]
        # log-likelihood under background-only hypothesis
        logL_b = total_log_likelihood(observed, background)
        # log-likelihood under signal hypothesis with strength μ
        logL_mu = total_log_likelihood(observed, expected)
        # Test statistic
        return -2 * (logL_mu - logL_b)
    
    # Find the minimum of q(μ)
    result = minimize_scalar(q_mu, bounds=(0, 5), method='bounded')
    mu_hat = result.x
    min_q = result.fun
    
    # Calculate -2ΔlogL(μ) = q(μ) - min_q
    def delta_q(mu):
        return q_mu(mu) - min_q
    
    # Scan μ values to find where -2ΔlogL = 1
    mu_values = np.linspace(0, 5, n_points)
    delta_q_values = [delta_q(mu) for mu in mu_values]
    
    # Find the two points where -2ΔlogL = 1 (one on each side of mu_hat)
    # Lower bound
    mu_lo = 0
    for i in range(len(mu_values)):
        if mu_values[i] >= mu_hat:
            break
        if delta_q_values[i] >= 1:
            mu_lo = mu_values[i]
    
    # Upper bound
    mu_hi = 5
    for i in range(len(mu_values)-1, -1, -1):
        if mu_values[i] <= mu_hat:
            break
        if delta_q_values[i] >= 1:
            mu_hi = mu_values[i]
    
    return mu_hat, mu_lo, mu_hi, mu_values, delta_q_values


def plot_diagnostics(q_toys, q_obs, mu_values, delta_q_values, mu_hat, mu_lo, mu_hi, output_dir):
    """Create diagnostic plots"""
    # Plot 1: Test statistic distribution from pseudo-experiments
    plt.figure(figsize=(10, 6))
    plt.hist(q_toys, bins=50, density=True, alpha=0.7, label='Background-only toys')
    plt.axvline(q_obs, color='red', linestyle='--', linewidth=2, label=f'Observed q = {q_obs:.3f}')
    plt.xlabel('Test Statistic q')
    plt.ylabel('Density')
    plt.title('Distribution of Test Statistic under Background-only Hypothesis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{output_dir}/test_statistic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: -2ΔlogL(μ) scan
    plt.figure(figsize=(10, 6))
    plt.plot(mu_values, delta_q_values, 'b-', linewidth=2, label='-2ΔlogL(μ)')
    plt.axhline(1, color='green', linestyle='--', linewidth=2, label='1σ level')
    plt.axvline(mu_hat, color='red', linestyle='-', linewidth=2, label=f'Best-fit μ = {mu_hat:.3f}')
    plt.axvline(mu_lo, color='orange', linestyle=':', linewidth=2, label=f'Lower 1σ = {mu_lo:.3f}')
    plt.axvline(mu_hi, color='orange', linestyle=':', linewidth=2, label=f'Upper 1σ = {mu_hi:.3f}')
    plt.xlabel('Signal Strength μ')
    plt.ylabel('-2ΔlogL(μ)')
    plt.title('Signal Strength Scan')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{output_dir}/signal_strength_scan.png', dpi=300, bbox_inches='tight')
    plt.close()


def main(input_json, output_json):
    """Main function to run the complete analysis"""
    # Read input data
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    channels = data['channels']
    observed = data['observed']
    background = data['background']
    signal = data['signal']
    
    # 1. Likelihoods
    logL_b = total_log_likelihood(observed, background)
    logL_sb = total_log_likelihood(observed, [b + s for b, s in zip(background, signal)])
    
    # 2. Test statistic
    test_stat = test_statistic(observed, background, signal)
    
    # 3. Significance via pseudo-experiments
    p_value, significance, q_obs, q_toys = pseudo_experiments(background, signal, observed, n_toys=1000000)
    
    # 4. Signal-strength measurement
    mu_hat, mu_lo, mu_hi, mu_values, delta_q_values = signal_strength_scan(observed, background, signal)
    
    # Create diagnostic plots
    plot_diagnostics(q_toys, q_obs, mu_values, delta_q_values, mu_hat, mu_lo, mu_hi, '/root/submission/diagnostics')
    
    # Prepare results
    results = {
        'logL_b': logL_b,
        'logL_sb': logL_sb,
        'test_statistic': test_stat,
        'p_value': p_value,
        'significance': significance,
        'mu_hat': mu_hat,
        'mu_lo': mu_lo,
        'mu_hi': mu_hi
    }
    
    # Write results to output file
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"Background-only log-likelihood: {logL_b:.3f}")
    print(f"Signal+background log-likelihood: {logL_sb:.3f}")
    print(f"Test statistic q: {test_stat:.3f}")
    print(f"p-value: {p_value:.6f}")
    print(f"Significance: {significance:.3f}σ")
    print(f"Best-fit signal strength: μ = {mu_hat:.3f} (+{mu_hi-mu_hat:.3f}/-{mu_hat-mu_lo:.3f})")
    
    if significance >= 3:
        print("Result reaches 3σ 'evidence' level.")
    else:
        print("Result does not reach 3σ 'evidence' level.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Four-lepton Higgs search statistical analysis')
    parser.add_argument('input_json', help='Input JSON file with event counts')
    parser.add_argument('output_json', help='Output JSON file for results')
    args = parser.parse_args()
    
    main(args.input_json, args.output_json)