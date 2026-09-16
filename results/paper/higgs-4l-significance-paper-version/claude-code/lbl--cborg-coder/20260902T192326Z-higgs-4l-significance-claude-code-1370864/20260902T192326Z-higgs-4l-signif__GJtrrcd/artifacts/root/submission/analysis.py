import json
import numpy as np
from scipy.stats import norm, poisson
from scipy.special import gammaln
import matplotlib.pyplot as plt
import sys
import os

def log_poisson(k, lamb):
    # logPoisson(k, λ) = -λ + k·log(λ) - log(k!)
    # We use gammaln(k+1) for log(k!)
    return -lamb + k * np.log(lamb) - gammaln(k + 1)

def calculate_log_likelihood(observed, expected):
    total_ll = 0
    for k, lamb in zip(observed, expected):
        total_ll += log_poisson(k, lamb)
    return total_ll

def run_analysis(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    observed = np.array(data['observed'])
    background = np.array(data['background'])
    signal = np.array(data['signal'])

    # 1. Likelihoods
    logL_b = calculate_log_likelihood(observed, background)
    logL_sb = calculate_log_likelihood(observed, signal + background)

    # 2. Test statistic
    # q = -2 * (logL_sb - logL_b)
    q_obs = -2 * (logL_sb - logL_b)

    # 3. Significance via pseudo-experiments
    num_toys = 10**6
    q_toys = []

    # To speed up toy generation, we can vectorise.
    # For each channel, generate num_toys samples.
    # Then for each sample index i, compute logL_b and logL_sb.

    # samples[channel][toy_index]
    samples = np.array([np.random.poisson(b, num_toys) for b in background])

    # Calculate logL_b and logL_sb for all toys
    # logL_b_toys = sum_channels (-b + k*log(b) - log(k!))
    # logL_sb_toys = sum_channels (-(s+b) + k*log(s+b) - log(k!))
    # q_toy = -2 * (logL_sb_toy - logL_b_toy)
    # q_toy = -2 * sum_channels ( (-(s+b) + k*log(s+b) - log(k!)) - (-b + k*log(b) - log(k!)) )
    # q_toy = -2 * sum_channels ( -s + k*(log(s+b) - log(b)) )

    # Vectorized calculation of q_toy
    q_toys = np.zeros(num_toys)
    for i in range(len(background)):
        s = signal[i]
        b = background[i]
        k = samples[i]
        q_toys += -2 * (-s + k * (np.log(s + b) - np.log(b)))

    p_value = np.mean(q_toys <= q_obs)
    significance = norm.ppf(1 - p_value)

    # 4. Signal-strength measurement
    # Scan mu to find best-fit mu_hat
    mu_range = np.linspace(0, 10, 1000)
    logL_mu = []
    for mu in mu_range:
        expected = mu * signal + background
        logL_mu.append(calculate_log_likelihood(observed, expected))

    logL_mu = np.array(logL_mu)
    idx_best = np.argmax(logL_mu)
    mu_hat = mu_range[idx_best]
    max_logL = logL_mu[idx_best]

    # Refine mu_hat if needed (simple search or just dense range)
    # Let's do a finer search around mu_hat
    mu_fine = np.linspace(max(0, mu_hat - 0.1), mu_hat + 0.1, 1000)
    logL_fine = []
    for mu in mu_fine:
        expected = mu * signal + background
        logL_fine.append(calculate_log_likelihood(observed, expected))

    idx_best_fine = np.argmax(logL_fine)
    mu_hat = mu_fine[idx_best_fine]
    max_logL = logL_fine[idx_best_fine]

    # Find mu_lo and mu_hi where -2*delta logL = 1
    # -2*delta logL = -2 * (logL(mu) - max_logL)
    # we want -2 * (logL(mu) - max_logL) = 1  => logL(mu) = max_logL - 0.5

    # Scan a wider range for the interval
    mu_scan = np.linspace(0, 20, 10000)
    logL_scan = []
    for mu in mu_scan:
        expected = mu * signal + background
        logL_scan.append(calculate_log_likelihood(observed, expected))
    logL_scan = np.array(logL_scan)

    delta_logL_2 = -2 * (logL_scan - max_logL)

    # Finding intersections with 1
    # mu_lo is the point < mu_hat where delta_logL_2 = 1
    # mu_hi is the point > mu_hat where delta_logL_2 = 1

    # Simple linear interpolation for precision
    def find_intersection(mu_vals, y_vals, target, side='lo'):
        # target = 1
        # find index where y_vals crosses target
        if side == 'lo':
            # look for y_vals crossing target from below to above as mu increases?
            # No, delta_logL_2 is convex. it decreases to 0 at mu_hat, then increases.
            # So for mu < mu_hat, delta_logL_2 is decreasing.
            # we want the point where it equals 1.
            idx = np.where(mu_vals < mu_hat)[0]
            # delta_logL_2[idx] is decreasing. Find where it crosses 1.
            # Since it's convex, it'll be one point.
            for i in range(len(idx)-1, -1, -1):
                curr_idx = idx[i]
                next_idx = curr_idx + 1
                if (y_vals[curr_idx] - target) * (y_vals[next_idx] - target) <= 0:
                    # linear interpolation
                    m = (y_vals[next_idx] - y_vals[curr_idx]) / (mu_vals[next_idx] - mu_vals[curr_idx])
                    return mu_vals[curr_idx] + (target - y_vals[curr_idx]) / m
        else:
            # look for mu > mu_hat
            idx = np.where(mu_vals > mu_hat)[0]
            for i in range(len(idx)-1):
                curr_idx = idx[i]
                next_idx = idx[i+1]
                if (y_vals[curr_idx] - target) * (y_vals[next_idx] - target) <= 0:
                    m = (y_vals[next_idx] - y_vals[curr_idx]) / (mu_vals[next_idx] - mu_vals[curr_idx])
                    return mu_vals[curr_idx] + (target - y_vals[curr_idx]) / m
        return None

    mu_lo = find_intersection(mu_scan, delta_logL_2, 1, side='lo')
    mu_hi = find_intersection(mu_scan, delta_logL_2, 1, side='hi')

    # If not found, it might be because mu_lo < 0.
    # The signal strength is physically >= 0.
    if mu_lo is None:
        # check if delta_logL_2(0) < 1. If so, mu_lo is effectively 0 or we can't bound it.
        # For the purpose of reporting an interval, we usually cap at 0.
        if delta_logL_2[0] < 1:
            mu_lo = 0.0
        else:
            # This should not happen if we scanned 0-20 and mu_hat is reasonable
            mu_lo = 0.0

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

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    # Diagnostics
    # Plot test statistic
    plt.figure(figsize=(10, 6))
    plt.hist(q_toys, bins=100, density=True, alpha=0.7, label='Background Toys')
    plt.axvline(q_obs, color='r', linestyle='--', label=f'Observed q = {q_obs:.3f}')
    plt.title('Distribution of Test Statistic q under Background-Only Hypothesis')
    plt.xlabel('q = -2(logL_sb - logL_b)')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.savefig('/root/submission/diagnostics/q_distribution.png')
    plt.close()

    # Plot -2Delta Log L
    plt.figure(figsize=(10, 6))
    plt.plot(mu_scan, delta_logL_2)
    plt.axhline(1, color='g', linestyle='--', label='1$\sigma$ boundary')
    plt.axvline(mu_hat, color='r', linestyle=':', label=f'$\hat{{\mu}} = {mu_hat:.3f}$')
    plt.title('Profile Likelihood $-2\Delta\log L(\mu)$')
    plt.xlabel('Signal Strength $\mu$')
    plt.ylabel('$-2\Delta\log L$')
    plt.legend()
    plt.grid(True)
    plt.savefig('/root/submission/diagnostics/mu_scan.png')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analysis.py INPUT_JSON OUTPUT_JSON")
        sys.exit(1)
    run_analysis(sys.argv[1], sys.argv[2])
