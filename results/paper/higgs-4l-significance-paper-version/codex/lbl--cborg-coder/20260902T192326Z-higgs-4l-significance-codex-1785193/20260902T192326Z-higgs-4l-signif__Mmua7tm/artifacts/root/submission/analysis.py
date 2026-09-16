import json
import sys
import numpy as np
from scipy.special import gammaln
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

def log_poisson(k, lam):
    # lam must be > 0
    return -lam + k * np.log(lam) - gammaln(k + 1)

def total_log_likelihood(mu, observed, signal, background):
    # Mean for each channel: mu * signal + background
    lam = mu * np.array(signal) + np.array(background)
    # Handle cases where lam <= 0 if necessary, though signal and background are > 0
    lam = np.maximum(lam, 1e-10)
    return np.sum(log_poisson(np.array(observed), lam))

def main():
    if len(sys.argv) != 3:
        print("Usage: python analysis.py <input_json> <output_json>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r') as f:
        data = json.load(f)

    observed = np.array(data['observed'])
    background = np.array(data['background'])
    signal = np.array(data['signal'])

    # 1. Likelihoods
    # Background-only: mu = 0
    logL_b = total_log_likelihood(0, observed, signal, background)
    # Signal-plus-background: mu = 1
    logL_sb = total_log_likelihood(1, observed, signal, background)

    # 2. Test statistic
    q_obs = -2 * (logL_sb - logL_b)

    # 3. Significance via pseudo-experiments
    n_toys = 10**6
    # Generate toy data: for each channel, draw from Poisson(background)
    # toy_data shape: (n_toys, n_channels)
    toy_data = np.random.poisson(background, size=(n_toys, len(observed)))
    
    # Compute q for each toy
    # Vectorized log-likelihood for toys
    # logL_b_toy: for each toy, sum(log_poisson(k_toy, b))
    # logL_sb_toy: for each toy, sum(log_poisson(k_toy, s + b))
    
    # Use broadcasting to compute log_poisson for all toys and channels
    # toy_data: (n_toys, n_channels)
    # background: (n_channels,)
    # signal + background: (n_channels,)
    
    # logL = -lam + k*log(lam) - log(k!)
    # b_lam = background
    # sb_lam = signal + background
    
    b_lam = background
    sb_lam = signal + background
    
    # Log-likelihood for background
    # We can precompute log(b_lam) and log(sb_lam)
    log_b_lam = np.log(b_lam)
    log_sb_lam = np.log(sb_lam)
    
    # Vectorized log_poisson:
    # logL_b = sum_i (-b_lam_i + k_toy_i * log_b_lam_i - gammaln(k_toy_i + 1))
    # logL_sb = sum_i (-sb_lam_i + k_toy_i * log_sb_lam_i - gammaln(k_toy_i + 1))
    # q = -2 * (logL_sb - logL_b) = -2 * sum_i [ (-sb_lam_i + b_lam_i) + k_toy_i * (log_sb_lam_i - log_b_lam_i) ]
    # Note: gammaln(k+1) cancels out.
    
    diff_lam = b_lam - sb_lam
    diff_log_lam = log_sb_lam - log_b_lam
    
    # q_toys = -2 * ( (diff_lam * 1).sum() + (toy_data * diff_log_lam).sum(axis=1) )
    # Wait, check signs.
    # logL_sb - logL_b = sum [ -sb_lam + k*log(sb_lam) - log(k!) - (-b_lam + k*log(b_lam) - log(k!)) ]
    # = sum [ (b_lam - sb_lam) + k * (log(sb_lam) - log(b_lam)) ]
    # q = -2 * (logL_sb - logL_b) = -2 * sum [ (b_lam - sb_lam) + k * (log(sb_lam) - log(b_lam)) ]
    
    q_toys = -2 * ( np.sum(diff_lam) + np.sum(toy_data * diff_log_lam, axis=1) )
    
    p_value = np.sum(q_toys <= q_obs) / n_toys
    significance = norm.ppf(1 - p_value)
    
    # 4. Signal-strength measurement
    # Find mu_hat: minimize -logL(mu)
    # mu must be >= 0 usually, but the problem says scan mu.
    # Let's use minimize_scalar for mu_hat.
    res = minimize_scalar(lambda m: -total_log_likelihood(m, observed, signal, background), 
                          bounds=(0, 10), method='bounded')
    mu_hat = res.x
    logL_max = total_log_likelihood(mu_hat, observed, signal, background)
    
    # Find mu_lo and mu_hi where -2 * (logL(mu) - logL(mu_hat)) = 1
    # -2 * deltaLogL = 1  =>  logL(mu) = logL(mu_hat) - 0.5
    
    def find_mu_edge(target_logL, direction):
        # direction = -1 for lo, 1 for hi
        # We search from mu_hat outwards.
        # Since logL(mu) is concave, we can use a simple root finding or scan.
        mu_start = mu_hat
        step = 0.01 * direction
        # Crude but effective for this 1D problem:
        mu = mu_start
        while True:
            mu += step
            if total_log_likelihood(mu, observed, signal, background) < target_logL:
                # We passed the edge, let's refine with binary search
                lo = mu - step
                hi = mu
                for _ in range(20):
                    mid = (lo + hi) / 2
                    if total_log_likelihood(mid, observed, signal, background) > target_logL:
                        lo = mid
                    else:
                        hi = mid
                return (lo + hi) / 2
            if abs(mu) > 100: # safety break
                return mu

    target_logL = logL_max - 0.5
    mu_lo = find_mu_edge(target_logL, -1)
    mu_hi = find_mu_edge(target_logL, 1)
    
    # To handle the case where mu_lo might go below 0, the problem asks for mu_lo.
    # In Higgs physics, we often constrain mu >= 0. Let's see if it's negative.
    # The prompt says "find the best-fit mu_hat... and determine the asymmetric +/-1sigma interval".
    # I'll keep mu_lo as it is, but if it's below 0, I'll report it.
    
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
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    # Diagnostics
    plt.figure(figsize=(10, 6))
    plt.hist(q_toys, bins=100, density=True, alpha=0.7, label='Background Toys')
    plt.axvline(q_obs, color='r', linestyle='--', label=f'Observed q = {q_obs:.2f}')
    plt.title('Distribution of Test Statistic $q$ under Background-only Hypothesis')
    plt.xlabel('$q$')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.savefig('/root/submission/diagnostics/q_distribution.png')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    mu_scan = np.linspace(max(0, mu_hat - 5), mu_hat + 5, 500)
    neg_2deltaLogL = [2 * (logL_max - total_log_likelihood(m, observed, signal, background)) for m in mu_scan]
    plt.plot(mu_scan, neg_2deltaLogL)
    plt.axhline(1, color='g', linestyle='--', label='-2$\Delta$logL = 1')
    plt.axvline(mu_hat, color='r', linestyle='--', label=f'mu_hat = {mu_hat:.2f}')
    plt.title('Profile Likelihood Scan')
    plt.xlabel('Signal Strength $\mu$')
    plt.ylabel('$-2\Delta\log L(\mu)$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('/root/submission/diagnostics/mu_scan.png')
    plt.close()

if __name__ == "__main__":
    main()
