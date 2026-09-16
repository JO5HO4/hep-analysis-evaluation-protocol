import json
import math
import numpy as np
from scipy.stats import poisson, norm
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import sys
import os

def log_poisson(k, lambd):
    """Compute log(Poisson(k; lambd)) = -lambd + k*log(lambd) - log(k!)"""
    if lambd <= 0:
        return -float('inf')
    # Use math.lgamma for log(k!)
    return -lambd + k * math.log(lambd) - math.lgamma(k + 1)

def compute_log_likelihood(observed, expected):
    total_ll = 0.0
    for k, lambd in zip(observed, expected):
        total_ll += log_poisson(k, lambd)
    return total_ll

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_analysis.py <INPUT_JSON> <OUTPUT_JSON>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r') as f:
        data = json.load(f)

    observed = np.array(data['observed'])
    background = np.array(data['background'])
    signal = np.array(data['signal'])

    # 1. Likelihoods
    # Background-only hypothesis: mean = background
    logL_b = compute_log_likelihood(observed, background)
    
    # Signal-plus-background hypothesis: mean = signal + background
    sb_expected = signal + background
    logL_sb = compute_log_likelihood(observed, sb_expected)

    # 2. Test statistic
    # q = -2 * (logL_sb - logL_b)
    # Note: In H->ZZ, usually q is defined such that larger q = more signal-like.
    # Let's stick to the formula: q = -2 * (logL_sb - logL_b)
    # Wait, usually q = -2 * (LL(b) - LL(sb)) = 2 * (LL(sb) - LL(b))
    # The prompt says q = -2 * (logL_sb - logL_b), which is 2 * (logL_b - logL_sb)
    # If signal is present, logL_sb > logL_b, so q would be negative.
    # However, typically the test statistic for discovery is q_0 = -2 log( L(b)/L(sb|mu_hat) )
    # Let's use the EXACT formula provided: q = -2 * (logL_sb - logL_b)
    observed_q = -2 * (logL_sb - logL_b)

    # 3. Significance via pseudo-experiments
    n_toys = 10**6
    toy_qs = []
    
    # Generate toys based on background-only expectation
    # For each channel, draw Poisson(background[i])
    # Use numpy for speed
    toy_observed = np.random.poisson(background[:, np.newaxis], (len(observed), n_toys))
    
    # To compute toy_qs efficiently:
    # toy_logL_b = sum_i [ -b_i + k_i * log(b_i) - log(k_i!) ]
    # toy_logL_sb = sum_i [ -(s_i + b_i) + k_i * log(s_i + b_i) - log(k_i!) ]
    # toy_q = -2 * (toy_logL_sb - toy_logL_b)
    # toy_q = -2 * sum_i [ -s_i + k_i * (log(s_i + b_i) - log(b_i)) ]
    # toy_q = 2 * sum_i [ s_i - k_i * log((s_i + b_i)/b_i) ]
    
    log_ratio = np.log((signal + background) / background)
    # toy_observed is (n_channels, n_toys)
    # signal is (n_channels,)
    # result of (toy_observed * log_ratio[:, np.newaxis]) is (n_channels, n_toys)
    # sum over axis 0: (n_toys,)
    term2 = np.sum(toy_observed * log_ratio[:, np.newaxis], axis=0)
    term1 = np.sum(signal)
    toy_qs = 2 * (term1 - term2)

    p_value = np.sum(toy_qs >= observed_q) / n_toys
    significance = norm.ppf(1 - p_value)

    # 4. Signal-strength measurement
    def get_q_mu(mu):
        expected_mu = mu * signal + background
        logL_mu = compute_log_likelihood(observed, expected_mu)
        # We want to minimize -logL_mu, or maximize logL_mu
        # Since q_mu = -2 * (logL_mu - logL_b) is often used, 
        # but we need the best fit mu_hat first.
        return -logL_mu

    # Find best fit mu_hat
    # Use a scalar optimizer. Mu should be non-negative.
    res = minimize_scalar(get_q_mu, bounds=(0, 10), method='bounded')
    mu_hat = res.x
    min_q_mu = res.fun
    
    # Profile likelihood: -2Delta logL(mu) = 2 * (logL(mu_hat) - logL(mu))
    def delta_logL(mu):
        logL_mu = compute_log_likelihood(observed, mu * signal + background)
        # logL(mu_hat) = -min_q_mu
        return 2 * (-min_q_mu - logL_mu)

    # Find mu_lo and mu_hi where -2Delta logL = 1
    # Use a simple scan or binary search since it's monotonic on either side of mu_hat
    mu_range = np.linspace(0, 10, 1000)
    dlogL_vals = [delta_logL(m) for m in mu_range]
    
    # Find crossing points
    mu_lo = mu_hat
    mu_hi = mu_hat
    
    # Simple search for boundaries
    for m, val in zip(mu_range, dlogL_vals):
        if m < mu_hat and val >= 1:
            mu_lo = m
            break
    
    for m, val in reversed(list(zip(mu_range, dlogL_vals))):
        if m > mu_hat and val >= 1:
            mu_hi = m
            break
            
    # Refine with a bit more precision? For 1000 points in [0,10], step is 0.01. Good enough?
    # Let's refine with bisection for better precision.
    def find_crossing(f, a, b, target=1.0):
        for _ in range(20):
            mid = (a + b) / 2
            if f(mid) < target:
                if a < b: a = mid
                else: b = mid
            else:
                if a < b: b = mid
                else: a = mid
        return (a + b) / 2

    # Refine mu_lo
    # Search between some point < mu_hat and mu_hat
    # Since f(mu_hat) = 0 and f(0) might be > 1 or < 1
    # If f(0) < 1, mu_lo = 0 (bounded)
    if delta_logL(0) < 1:
        mu_lo = 0
    else:
        mu_lo = find_crossing(delta_logL, 0, mu_hat)

    # Refine mu_hi
    # Search between mu_hat and 10
    if delta_logL(10) < 1:
        mu_hi = 10 # Upper bound
    else:
        mu_hi = find_crossing(delta_logL, mu_hat, 10)

    # Results
    results = {
        "logL_b": logL_b,
        "logL_sb": logL_sb,
        "test_statistic": observed_q,
        "p_value": p_value,
        "significance": significance,
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi
    }

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    # Diagnostics
    diag_dir = "/root/submission/diagnostics"
    if not os.path.exists(diag_dir):
        os.makedirs(diag_dir)

    # Plot test statistic
    plt.figure()
    plt.hist(toy_qs, bins=50, density=True, alpha=0.7, label='Bkg toys')
    plt.axvline(observed_q, color='r', linestyle='--', label=f'Observed q={observed_q:.2f}')
    plt.title("Test Statistic Distribution")
    plt.xlabel("q")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.savefig(os.path.join(diag_dir, "test_statistic.png"))
    plt.close()

    # Plot -2Delta logL
    plt.figure()
    mu_scan = np.linspace(0, 10, 200)
    dlogL_scan = [delta_logL(m) for m in mu_scan]
    plt.plot(mu_scan, dlogL_scan)
    plt.axvline(mu_hat, color='g', label=f'mu_hat={mu_hat:.2f}')
    plt.axhline(1, color='r', linestyle='--', label='1-sigma')
    plt.title("-2 Delta Log-Likelihood Profile")
    plt.xlabel("mu")
    plt.ylabel("-2 Delta logL")
    plt.legend()
    plt.savefig(os.path.join(diag_dir, "likelihood_profile.png"))
    plt.close()

if __name__ == "__main__":
    main()
