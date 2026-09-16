#!/usr/bin/env python3
"""Likelihood analysis for independent Poisson counting channels."""
import json
import math
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, brentq
from scipy.special import gammaln, ndtri

N_TOYS = 1_000_000
SEED = 20250308


def loglike(mu, observed, background, signal):
    mean = background + mu * signal
    if np.any(mean <= 0):
        return -np.inf
    return float(np.sum(-mean + observed * np.log(mean) - gammaln(observed + 1)))


def main(infile, outfile):
    with open(infile) as f:
        d = json.load(f)
    observed = np.asarray(d['observed'], dtype=float)
    background = np.asarray(d['background'], dtype=float)
    signal = np.asarray(d['signal'], dtype=float)
    n = len(observed)
    if n == 0 or len(background) != n or len(signal) != n:
        raise ValueError('observed, background, and signal must be equal-length nonempty arrays')
    if np.any(observed < 0) or np.any(observed != np.floor(observed)):
        raise ValueError('observed counts must be nonnegative integers')
    if np.any(background <= 0) or np.any(signal < 0):
        raise ValueError('background must be positive and signal nonnegative')

    logL_b = loglike(0.0, observed, background, signal)
    logL_sb = loglike(1.0, observed, background, signal)
    q_obs = -2.0 * (logL_sb - logL_b)

    # For fixed b versus fixed s+b, a lower q favors s+b and is more signal-like.
    rng = np.random.default_rng(SEED)
    q_toys = np.empty(N_TOYS, dtype=np.float64)
    done = 0
    logratio_const = -2.0 * (-(background + signal).sum() + background.sum())
    # q = -2[sum(k log((b+s)/b)) - sum(s)]
    weights = np.log((background + signal) / background)
    batch = 100_000
    while done < N_TOYS:
        m = min(batch, N_TOYS - done)
        toys = rng.poisson(background, size=(m, n))
        q_toys[done:done+m] = -2.0 * (toys @ weights - signal.sum())
        done += m
    n_extreme = int(np.count_nonzero(q_toys <= q_obs))
    # Conservative finite-toy estimate avoids exactly zero p-values.
    p_value = (n_extreme + 1.0) / (N_TOYS + 1.0)
    significance = float(ndtri(1.0 - p_value))

    # Profile over the physical signal-strength domain mu >= 0.
    # Expand a bracket until its high end lies below the maximum likelihood.
    upper = max(5.0, 2.0 * (float(observed.sum()) / max(float(signal.sum()), 1e-12) + 1.0))
    while loglike(upper, observed, background, signal) > loglike(upper * 0.8, observed, background, signal):
        upper *= 2.0
    fit = minimize_scalar(lambda x: -loglike(x, observed, background, signal), bounds=(0.0, upper), method='bounded', options={'xatol': 1e-12})
    mu_hat = float(fit.x)
    ll_hat = -float(fit.fun)
    target = ll_hat - 0.5
    fprof = lambda x: loglike(x, observed, background, signal) - target
    # If the likelihood at physical boundary remains within one unit, quote boundary.
    mu_lo = 0.0 if fprof(0.0) >= 0 else float(brentq(fprof, 0.0, mu_hat, xtol=1e-12))
    hi_bracket = max(upper, mu_hat + 1.0)
    while fprof(hi_bracket) > 0:
        hi_bracket *= 2.0
    mu_hi = float(brentq(fprof, mu_hat, hi_bracket, xtol=1e-12))

    outdir = os.path.dirname(os.path.abspath(outfile))
    os.makedirs(outdir, exist_ok=True)
    diagnostics = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagnostics')
    os.makedirs(diagnostics, exist_ok=True)

    # Distribution of the fixed-hypothesis likelihood-ratio statistic.
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(q_toys, bins=100, density=True, color='#4c78a8', alpha=0.8, label='Background-only toys')
    ax.axvline(q_obs, color='#e45756', lw=2, label=f'Observed q = {q_obs:.3f}')
    ax.set(xlabel=r'$q=-2\ln(L_{s+b}/L_b)$', ylabel='Density', title='Background-only pseudo-experiment distribution')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(diagnostics, 'test_statistic_toys.png'), dpi=150)
    plt.close(fig)

    scan_max = max(mu_hi * 1.25, 2.0)
    mu_scan = np.linspace(0.0, scan_max, 800)
    profile = np.array([-2.0 * (loglike(x, observed, background, signal) - ll_hat) for x in mu_scan])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(mu_scan, profile, color='#4c78a8', lw=2)
    ax.axhline(1.0, color='gray', ls='--', label=r'$1\sigma$ threshold')
    ax.axvline(mu_hat, color='#e45756', ls='-', label=rf'$\hat{{\mu}}={mu_hat:.3f}$')
    ax.scatter([mu_lo, mu_hi], [1, 1], color='#e45756', zorder=3)
    ax.set(xlabel=r'Signal strength $\mu$', ylabel=r'$-2\Delta\log L(\mu)$', ylim=(0, max(3.0, min(float(profile.max()) * 1.05, 10.0))), title='Signal-strength likelihood profile')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(diagnostics, 'mu_profile.png'), dpi=150)
    plt.close(fig)

    result = {
        'logL_b': logL_b,
        'logL_sb': logL_sb,
        'test_statistic': q_obs,
        'p_value': p_value,
        'significance': significance,
        'mu_hat': mu_hat,
        'mu_lo': mu_lo,
        'mu_hi': mu_hi,
        'n_toys': N_TOYS,
        'n_signal_like_toys': n_extreme,
        'toy_seed': SEED,
    }
    with open(outfile, 'w') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} INPUT_JSON OUTPUT_JSON', file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
