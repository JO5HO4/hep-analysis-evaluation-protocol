#!/usr/bin/env python3
"""
Plot diagnostic plots for the four-lepton Higgs search analysis.
Creates plots of the test-statistic distribution and the -2ΔlogL(μ) scan.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_test_statistic_distribution(diagnostics_file, output_dir):
    """Plot the distribution of test statistics from pseudo-experiments."""
    # Read diagnostic data
    with open(diagnostics_file, 'r') as f:
        data = json.load(f)
    
    q_toys = data['q_toys']
    q_obs = data['q_obs']
    
    # Create histogram of test statistics
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(q_toys, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    
    # Mark the observed test statistic
    plt.axvline(q_obs, color='red', linestyle='--', linewidth=2, label=f'Observed q = {q_obs:.3f}')
    
    # Calculate and mark the 95% quantile
    q_95 = np.percentile(q_toys, 95)
    plt.axvline(q_95, color='orange', linestyle=':', linewidth=2, label=f'95% quantile = {q_95:.3f}')
    
    plt.xlabel('Test Statistic (q)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title('Distribution of Test Statistic under Background-Only Hypothesis', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save plot
    output_file = os.path.join(output_dir, 'test_statistic_distribution.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Test statistic distribution plot saved to {output_file}")


def plot_delta_logL_scan(diagnostics_file, output_dir):
    """Plot the -2ΔlogL(μ) scan."""
    # Read diagnostic data
    with open(diagnostics_file, 'r') as f:
        data = json.load(f)
    
    mu_values = np.array(data['mu_values'])
    delta_logL2 = np.array(data['delta_logL2'])
    
    # Find minimum and 1σ interval
    min_idx = np.argmin(delta_logL2)
    mu_hat = mu_values[min_idx]
    
    # Find 1σ interval (where -2ΔlogL = 1)
    mu_lo = 0.0
    mu_hi = mu_values[-1]
    
    for i in range(len(mu_values) - 1):
        if mu_values[i] >= mu_hat:
            break
        if delta_logL2[i] <= 1 and delta_logL2[i+1] > 1:
            frac = (1 - delta_logL2[i]) / (delta_logL2[i+1] - delta_logL2[i])
            mu_lo = mu_values[i] + frac * (mu_values[i+1] - mu_values[i])
            break
    
    for i in range(len(mu_values) - 1):
        if mu_values[i] > mu_hat and delta_logL2[i] > 1:
            frac = (1 - delta_logL2[i-1]) / (delta_logL2[i] - delta_logL2[i-1])
            mu_hi = mu_values[i-1] + frac * (mu_values[i] - mu_values[i-1])
            break
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(mu_values, delta_logL2, 'b-', linewidth=2, label='-2ΔlogL(μ)')
    
    # Mark minimum and 1σ interval
    plt.axhline(y=1, color='green', linestyle='-', linewidth=2, alpha=0.7, label='1σ (ΔlogL = 0.5)')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    plt.axvline(x=mu_hat, color='red', linestyle='--', linewidth=2, label=f'μ̂ = {mu_hat:.3f}')
    plt.axvline(x=mu_lo, color='orange', linestyle=':', linewidth=2, label=f'μ = {mu_lo:.3f}')
    plt.axvline(x=mu_hi, color='orange', linestyle=':', linewidth=2, label=f'μ = {mu_hi:.3f}')
    
    plt.xlabel('Signal Strength (μ)', fontsize=12)
    plt.ylabel('-2ΔlogL(μ)', fontsize=12)
    plt.title('Signal Strength Scan: -2ΔlogL(μ) vs μ', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Set y-axis to show from 0 to an appropriate maximum
    max_y = max(delta_logL2)
    if max_y > 5:
        # Find the first index where delta_logL2 exceeds 5
        try:
            max_idx = np.argmax(delta_logL2 > 5)
            max_y = max(delta_logL2[:max_idx])
        except:
            pass
    
    plt.ylim(0, max_y)
    
    # Save plot
    output_file = os.path.join(output_dir, 'delta_logL_scan.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"-2ΔlogL(μ) scan plot saved to {output_file}")


def main():
    """Main function to create diagnostic plots."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    diagnostics_file = os.path.join(script_dir, "diagnostics", "diagnostics.json")
    # If the file doesn't exist in the script directory, try the results directory
    if not os.path.exists(diagnostics_file):
        diagnostics_file = os.path.join("/root/results", "diagnostics", "diagnostics.json")
    
    # Use the output directory from the results
    output_dir = os.path.dirname(diagnostics_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if diagnostics file exists
    if not os.path.exists(diagnostics_file):
        print(f"Error: Diagnostics file not found at {diagnostics_file}")
        return
    
    # Create plots
    plot_test_statistic_distribution(diagnostics_file, output_dir)
    plot_delta_logL_scan(diagnostics_file, output_dir)

if __name__ == "__main__":
    main()