import json
import numpy as np
from scipy.stats import poisson, norm
from scipy.optimize import minimize_scalar
import sys
import matplotlib.pyplot as plt

def log_poisson(k, lam):
    # log(k! ) is handled by log_factorial
    from math import lgamma
    return -lam + k * np.log(lam) - lgamma(k + 1)

def calculate_logL(observed, expected):
    return np.sum([log_poisson(k, lam) for k, lam in zip(observed, expected)])

def run_analysis(input_json, output_json, diag_dir):
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    obs = np.array(data['observed'])
    bkg = np.array(data['background'])
    sig = np.array(data['signal'])

    # 1. Likelihoods
    logL_b = calculate_logL(obs, bkg)
    logL_sb = calculate_logL(obs, sig + bkg)

    # 2. Test statistic
    q_obs = -2 * (logL_sb - logL_b)

    # 3. Significance via pseudo-experiments
    n_toys = 10**6
    # Generate toys: for each channel, draw from Poisson(bkg)
    # Shape: (n_toys, n_channels)
    toys = np.random.poisson(bkg, (n_toys, len(obs)))
    
    # Calculate q for each toy
    # q_toy = -2 * (logL_sb_toy - logL_b_toy)
    # logL_b_toy = sum(-bkg + k*log(bkg) - log(k!))
    # logL_sb_toy = sum(-(sig+bkg) + k*log(sig+bkg) - log(k!))
    # q_toy = -2 * [ sum(-(sig+bkg) + k*log(sig+bkg)) - sum(-bkg + k*log(bkg)) ]
    # q_toy = -2 * [ sum(-sig + k*log((sig+bkg)/bkg)) ]
    # q_toy = 2 * sum(sig) - 2 * sum(k * log((sig+bkg)/bkg))
    
    log_ratio = np.log((sig + bkg) / bkg)
    sum_sig = np.sum(sig)
    # Vectorized q calculation
    # toys: (10^6, 3), log_ratio: (3,) -> product: (10^6,)
    q_toys = 2 * sum_sig - 2 * np.sum(toys * log_ratio, axis=1)
    
    p_value = np.sum(q_toys >= q_obs) / n_toys
    significance = norm.ppf(1 - p_value)

    # 4. Signal-strength measurement
    def get_logL_mu(mu):
        expected = mu * sig + bkg
        return calculate_logL(obs, expected)

    def profile_likelihood(mu):
        return -2 * (get_logL_mu(mu) - get_logL_mu(mu_hat))

    # Find mu_hat
    res = minimize_scalar(lambda mu: -get_logL_mu(mu), bounds=(0, 10), method='bounded')
    mu_hat = res.x

    # Find 1-sigma interval: profile_likelihood(mu) = 1
    # Lower bound
    res_lo = minimize_scalar(lambda mu: (profile_likelihood(mu) - 1)**2, bounds=(0, mu_hat), method='bounded')
    mu_lo = res_lo.x
    # Upper bound
    res_hi = minimize_scalar(lambda mu: (profile_likelihood(mu) - 1)**2, bounds=(mu_hat, 10), method='bounded')
    mu_hi = res_hi.x

    # Results
    results = {
        "logL_b": float(logL_b),
        "logL_sb": float(logL_sb),
        "test_statistic": float(q_obs),
        "p_value": float(p_value),
        "significance": float(significance),
        "mu_hat": float(mu_hat),
        "mu_lo": float(mu_lo),
        "mu_hi": float(mu_hi)
    }

    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)

    # Diagnostics
    plt.figure()
    plt.hist(q_toys, bins=100, density=True, alpha=0.5, label='Background-only toys')
    plt.axvline(q_obs, color='red', linestyle='--', label=f'Observed q={q_obs:.2f}')
    plt.title('Distribution of Test Statistic q')
    plt.xlabel('q')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.savefig(f'{diag_dir}/q_dist.png')
    plt.close()

    plt.figure()
    mu_range = np.linspace(0, 10, 200)
    q_mu = [profile_likelihood(mu) for mu in mu_range]
    plt.plot(mu_range, q_mu)
    plt.axvline(mu_hat, color='red', linestyle='--', label=f'mu_hat={mu_hat:.2f}')
    plt.axhline(1, color='green', linestyle=':', label='1-sigma level')
    plt.title('Profile Likelihood Scan')
    plt.xlabel('mu')
    plt.ylabel('-2 Delta log L')
    plt.legend()
    plt.savefig(f'{diag_dir}/mu_scan.png')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analysis.py INPUT_JSON OUTPUT_JSON")
        sys.exit(1)
    run_analysis(sys.argv[1], sys.argv[2], '/root/submission/diagnostics/')
