#!/usr/bin/env python3
import json
import math
import os
import sys
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.special import gammaln
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N_TOYS = 1_000_000
SEED = 123456789

def validate(data):
    for key in ('channels', 'observed', 'background', 'signal'):
        if key not in data:
            raise ValueError(f'missing required field: {key}')
    n = len(data['channels'])
    if n == 0 or any(len(data[k]) != n for k in ('observed','background','signal')):
        raise ValueError('channel arrays must be nonempty and have equal lengths')
    obs = np.asarray(data['observed'], dtype=float)
    bkg = np.asarray(data['background'], dtype=float)
    sig = np.asarray(data['signal'], dtype=float)
    if np.any(~np.isfinite(obs)) or np.any(obs < 0) or np.any(obs != np.floor(obs)):
        raise ValueError('observed counts must be finite nonnegative integers')
    if np.any(~np.isfinite(bkg)) or np.any(bkg <= 0):
        raise ValueError('background expectations must be finite and strictly positive')
    if np.any(~np.isfinite(sig)) or np.any(sig < 0) or not np.any(sig > 0):
        raise ValueError('signal expectations must be finite, nonnegative, and not all zero')
    return obs.astype(np.int64), bkg, sig

def loglike(counts, means):
    return float(np.sum(-means + counts*np.log(means) - gammaln(counts+1)))

def main(inp, out):
    with open(inp) as f:
        data = json.load(f)
    obs, bkg, sig = validate(data)

    logL_b = loglike(obs, bkg)
    logL_sb = loglike(obs, bkg + sig)
    q_obs = -2.0*(logL_sb - logL_b)

    # For fixed hypotheses q = 2 sum[s_i - n_i log((b_i+s_i)/b_i)].
    # Thus smaller q is more signal-like.
    weights = np.log1p(sig/bkg)
    rng = np.random.default_rng(SEED)
    toy_q_parts = []
    batch = 100_000
    n_extreme = 0
    for start in range(0, N_TOYS, batch):
        m = min(batch, N_TOYS-start)
        counts = rng.poisson(bkg, size=(m, len(bkg)))
        qvals = 2.0*(np.sum(sig) - counts @ weights)
        n_extreme += int(np.count_nonzero(qvals <= q_obs + 1e-12))
        toy_q_parts.append(qvals)
    toy_q = np.concatenate(toy_q_parts)
    p_value = n_extreme/N_TOYS
    significance = float(norm.isf(p_value)) if p_value > 0 else float(norm.isf(0.5/N_TOYS))

    def nll2(mu):
        means = bkg + mu*sig
        return -2.0*loglike(obs, means)

    # Physical signal strength constraint mu >= 0.
    upper = max(5.0, 2.0*(np.sum(obs)/np.sum(sig)))
    fit = minimize_scalar(nll2, bounds=(0.0, upper), method='bounded',
                          options={'xatol': 1e-12})
    mu_hat = float(fit.x)
    # Explicitly compare the boundary in case the numerical optimizer sits nearby.
    if nll2(0.0) <= nll2(mu_hat):
        mu_hat = 0.0
    min_nll2 = nll2(mu_hat)
    def delta(mu):
        return nll2(mu) - min_nll2 - 1.0

    if mu_hat > 0 and delta(0.0) >= 0:
        mu_lo = float(brentq(delta, 0.0, mu_hat, xtol=1e-12))
    else:
        # If no lower unit crossing exists in the physical region, report boundary.
        mu_lo = 0.0
    hi = max(1.0, mu_hat*1.5 + 0.5)
    while delta(hi) < 0:
        hi *= 2.0
        if hi > 1e7:
            raise RuntimeError('failed to bracket upper likelihood crossing')
    mu_hi = float(brentq(delta, mu_hat, hi, xtol=1e-12))

    result = {
        'logL_b': logL_b,
        'logL_sb': logL_sb,
        'test_statistic': q_obs,
        'p_value': p_value,
        'significance': significance,
        'mu_hat': mu_hat,
        'mu_lo': mu_lo,
        'mu_hi': mu_hi,
        'mu_err_minus': mu_hat-mu_lo,
        'mu_err_plus': mu_hi-mu_hat,
        'n_toys': N_TOYS,
        'n_extreme_toys': n_extreme,
        'toy_seed': SEED,
        'reaches_3sigma_evidence': bool(significance >= 3.0)
    }
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')

    diag = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagnostics')
    os.makedirs(diag, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7,5))
    ax.hist(toy_q, bins=100, histtype='stepfilled', alpha=.7, color='steelblue')
    ax.axvline(q_obs, color='crimson', lw=2, label=f'observed q = {q_obs:.3f}')
    ax.set_xlabel(r'$q=-2\log(L_{s+b}/L_b)$')
    ax.set_ylabel('Background-only toys / bin')
    ax.set_title(f'Background-only toy distribution ({N_TOYS:,} toys)')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(diag, 'test_statistic_distribution.png'), dpi=160)
    plt.close(fig)

    scan_hi = max(mu_hi*1.35, mu_hat+1.0)
    mus = np.linspace(0, scan_hi, 600)
    ds = np.array([nll2(x)-min_nll2 for x in mus])
    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(mus, ds, color='navy', lw=2)
    ax.axhline(1, color='gray', ls='--', label=r'$-2\Delta\log L=1$')
    ax.axvline(mu_hat, color='crimson', ls='-', label=rf'$\hat\mu={mu_hat:.3f}$')
    ax.axvline(mu_lo, color='crimson', ls=':')
    ax.axvline(mu_hi, color='crimson', ls=':')
    ax.set_ylim(0, max(4, min(12, float(ds[-1])*1.05)))
    ax.set_xlim(0, scan_hi)
    ax.set_xlabel(r'Signal strength $\mu$')
    ax.set_ylabel(r'$-2\Delta\log L(\mu)$')
    ax.set_title('Signal-strength profile likelihood')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(diag, 'mu_profile_likelihood.png'), dpi=160)
    plt.close(fig)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} INPUT_JSON OUTPUT_JSON', file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
