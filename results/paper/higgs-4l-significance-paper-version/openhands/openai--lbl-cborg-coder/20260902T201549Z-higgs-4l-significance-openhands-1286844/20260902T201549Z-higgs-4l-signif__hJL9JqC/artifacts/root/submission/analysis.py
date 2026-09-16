
import json
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from scipy.special import gammaln
import matplotlib.pyplot as plt
import sys

def log_poisson(k, lam):
    return -lam + k * np.log(lam) - gammaln(k + 1)

def calculate_log_likelihood(observed, expected):
    return np.sum(log_poisson(observed, expected))

def run_analysis(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    observed = np.array(data['observed'])
    background = np.array(data['background'])
    signal = np.array(data['signal'])

    logL_b = calculate_log_likelihood(observed, background)
    logL_sb = calculate_log_likelihood(observed, signal + background)

    q_obs = -2 * (logL_sb - logL_b)

    n_toys = 1_000_000
    toy_obs = np.random.poisson(background, (n_toys, len(observed)))

    s = signal
    b = background
    term1 = np.sum(s)
    term2 = np.sum(toy_obs * np.log((s+b)/b), axis=1)
    q_toys = 2 * (term1 - term2)

    # "at least as signal-like" means q_toy <= q_obs
    p_value = np.mean(q_toys <= q_obs)
    z_significance = norm.ppf(1 - p_value)

    def negative_log_likelihood(mu):
        expected = mu * signal + background
        if np.any(expected <= 0):
            return 1e18
        return -calculate_log_likelihood(observed, expected)

    res = minimize_scalar(negative_log_likelihood, bounds=(0, 100), method='bounded')
    mu_hat = res.x
    min_nll = res.fun

    def delta_nll(mu):
        return 2 * (negative_log_likelihood(mu) - min_nll)

    mu_range = np.linspace(0, 100, 2000)
    nll_vals = np.array([delta_nll(mu) for mu in mu_range])
    crossings = np.where(np.diff(np.sign(nll_vals - 1)))[0]

    if len(crossings) >= 2:
        mu_lo = np.interp(1, nll_vals[crossings[0]:crossings[0]+2], mu_range[crossings[0]:crossings[0]+2])
        mu_hi = np.interp(1, nll_vals[crossings[-1]:crossings[-1]+2], mu_range[crossings[-1]:crossings[-1]+2])
    elif len(crossings) == 1:
        if crossings[0] < np.argmin(nll_vals):
            mu_lo = np.interp(1, nll_vals[crossings[0]:crossings[0]+2], mu_range[crossings[0]:crossings[0]+2])
            mu_hi = mu_hat + 1.0 
        else:
            mu_hi = np.interp(1, nll_vals[crossings[0]:crossings[0]+2], mu_range[crossings[0]:crossings[0]+2])
            mu_lo = mu_hat - 1.0
    else:
        mu_lo, mu_hi = mu_hat - 1.0, mu_hat + 1.0

    results = {
        "logL_b": float(logL_b),
        "logL_sb": float(logL_sb),
        "test_statistic": float(q_obs),
        "p_value": float(p_value),
        "significance": float(z_significance),
        "mu_hat": float(mu_hat),
        "mu_lo": float(mu_lo),
        "mu_hi": float(mu_hi)
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    plt.figure()
    plt.hist(q_toys, bins=100, density=True, alpha=0.7, label='Background toys')
    plt.axvline(q_obs, color='r', linestyle='--', label=f'Observed q={q_obs:.2f}')
    plt.xlabel('q')
    plt.ylabel('Probability Density')
    plt.title('Distribution of Test Statistic q')
    plt.legend()
    plt.savefig('/root/submission/diagnostics/q_distribution.png')
    plt.close()

    plt.figure()
    plt.plot(mu_range, nll_vals)
    plt.axhline(1, color='r', linestyle='--', label='-2DeltaLogL = 1')
    plt.axvline(mu_hat, color='g', linestyle='-', label=f'mu_hat={mu_hat:.2f}')
    plt.xlabel('mu')
    plt.ylabel('-2DeltaLogL')
    plt.title('Likelihood Scan for Signal Strength mu')
    plt.legend()
    plt.savefig('/root/submission/diagnostics/mu_scan.png')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analysis.py INPUT_JSON OUTPUT_JSON")
        sys.exit(1)
    run_analysis(sys.argv[1], sys.argv[2])
