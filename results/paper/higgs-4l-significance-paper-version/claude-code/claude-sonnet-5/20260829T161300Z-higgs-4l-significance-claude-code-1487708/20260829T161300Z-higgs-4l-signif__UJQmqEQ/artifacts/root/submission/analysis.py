#!/usr/bin/env python3
"""
Statistical analysis of a multi-channel Poisson counting experiment
(H -> ZZ* -> 4l style search).

Usage:
    python3 analysis.py INPUT_JSON OUTPUT_JSON [--diagnostics DIR] [--ntoys N] [--seed S]
"""
import argparse
import json
import os
import sys

import numpy as np
from scipy.stats import poisson, norm
from scipy.optimize import minimize_scalar, brentq

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def total_logL(obs, lam):
    """Total log-likelihood for a single toy/observation vector (1-D arrays)."""
    return np.sum(poisson.logpmf(obs, lam))


def total_logL_batch(obs_batch, lam):
    """Total log-likelihood over channels for a batch of toy datasets.
    obs_batch: shape (N, C). lam: shape (C,). Returns shape (N,)."""
    return poisson.logpmf(obs_batch, lam).sum(axis=1)


def neg_logL_mu(mu, obs, sig, bkg):
    lam = mu * sig + bkg
    if np.any(lam <= 0):
        return 1e10
    return -total_logL(obs, lam)


def fit_mu(obs, sig, bkg, mu_max=50.0):
    """Find best-fit mu (unconstrained sign, but lambda_i>0 required) and
    the +/-1 sigma interval from -2*DeltaLogL = 1."""
    # Domain: mu*sig + bkg > 0 for every channel => mu > -bkg/sig (for sig_i>0)
    with np.errstate(divide="ignore", invalid="ignore"):
        lower_bounds = np.where(sig > 0, -bkg / sig, -np.inf)
    mu_domain_min = np.max(lower_bounds) + 1e-9

    res = minimize_scalar(
        neg_logL_mu,
        bounds=(mu_domain_min, mu_max),
        args=(obs, sig, bkg),
        method="bounded",
        options={"xatol": 1e-12},
    )
    mu_hat = res.x
    logL_max = -res.fun

    def two_dlogl(mu):
        return 2.0 * (logL_max - (-neg_logL_mu(mu, obs, sig, bkg)))

    def root_fn(mu):
        return two_dlogl(mu) - 1.0

    # lower edge
    lo = mu_domain_min
    if root_fn(lo) < 0:
        # -2dlogL doesn't cross 1 within domain (rare); clip
        mu_lo = lo
    else:
        mu_lo = brentq(root_fn, lo, mu_hat, xtol=1e-10)

    # upper edge - expand search until root bracketed
    hi = mu_hat + 1.0
    while root_fn(hi) < 0 and hi < mu_max:
        hi *= 2.0
    hi = min(hi, mu_max)
    mu_hi = brentq(root_fn, mu_hat, hi, xtol=1e-10)

    return mu_hat, mu_lo, mu_hi, mu_domain_min, logL_max


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_json")
    ap.add_argument("output_json")
    ap.add_argument("--diagnostics", default=None, help="directory for diagnostic plots")
    ap.add_argument("--ntoys", type=int, default=5_000_000)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()

    with open(args.input_json) as f:
        data = json.load(f)

    channels = data["channels"]
    obs = np.array(data["observed"], dtype=float)
    bkg = np.array(data["background"], dtype=float)
    sig = np.array(data["signal"], dtype=float)
    nch = len(channels)
    assert len(obs) == len(bkg) == len(sig) == nch

    # ---------------------------------------------------------------
    # 1) Likelihoods and observed test statistic
    # ---------------------------------------------------------------
    logL_b = total_logL(obs, bkg)
    logL_sb = total_logL(obs, sig + bkg)
    q_obs = -2.0 * (logL_sb - logL_b)

    # ---------------------------------------------------------------
    # 2) Pseudo-experiments under background-only hypothesis
    # ---------------------------------------------------------------
    rng = np.random.default_rng(args.seed)
    ntoys = args.ntoys
    toys = rng.poisson(lam=bkg, size=(ntoys, nch))

    logLb_t = total_logL_batch(toys, bkg)
    logLsb_t = total_logL_batch(toys, sig + bkg)
    q_t = -2.0 * (logLsb_t - logLb_t)

    # "at least as signal-like as observed" -> q_toy <= q_obs (more negative = more signal-like)
    n_as_extreme = int(np.sum(q_t <= q_obs))
    p_value = n_as_extreme / ntoys
    # guard against p=0 (no toy at least as extreme): report a conservative
    # upper bound using the smallest resolvable value 1/ntoys.
    p_reported = p_value if p_value > 0 else 1.0 / ntoys
    significance = float(norm.isf(p_reported))
    p_is_bound = p_value == 0.0

    # ---------------------------------------------------------------
    # 3) Signal-strength fit
    # ---------------------------------------------------------------
    mu_hat, mu_lo, mu_hi, mu_domain_min, logL_max = fit_mu(obs, sig, bkg)

    # scan for diagnostics
    mu_scan = np.linspace(max(mu_domain_min, mu_lo - 3 * (mu_hat - mu_lo) - 0.5),
                           mu_hi + 3 * (mu_hi - mu_hat) + 0.5, 400)
    mu_scan = mu_scan[mu_scan > mu_domain_min]
    twodll_scan = np.array([2.0 * (logL_max - (-neg_logL_mu(m, obs, sig, bkg))) for m in mu_scan])

    results = {
        "channels": channels,
        "observed": obs.tolist(),
        "background": bkg.tolist(),
        "signal": sig.tolist(),
        "logL_b": float(logL_b),
        "logL_sb": float(logL_sb),
        "test_statistic": float(q_obs),
        "n_toys": int(ntoys),
        "n_toys_as_extreme": n_as_extreme,
        "p_value": float(p_value),
        "p_value_is_upper_bound": bool(p_is_bound),
        "significance": significance,
        "reaches_3sigma_evidence": bool(significance >= 3.0),
        "mu_hat": float(mu_hat),
        "mu_lo": float(mu_lo),
        "mu_hi": float(mu_hi),
        "mu_err_minus": float(mu_hat - mu_lo),
        "mu_err_plus": float(mu_hi - mu_hat),
    }

    with open(args.output_json, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))

    # ---------------------------------------------------------------
    # Diagnostic plots
    # ---------------------------------------------------------------
    if args.diagnostics:
        os.makedirs(args.diagnostics, exist_ok=True)

        # (a) test-statistic distribution from toys
        plt.figure(figsize=(7, 5))
        lo_plot = min(q_t.min(), q_obs) - 1
        hi_plot = max(q_t.max(), q_obs) + 1
        plt.hist(q_t, bins=200, range=(lo_plot, hi_plot), histtype="stepfilled",
                 color="steelblue", alpha=0.7, label=f"background-only toys (N={ntoys:,})")
        plt.axvline(q_obs, color="crimson", lw=2,
                    label=f"observed q = {q_obs:.2f}")
        plt.yscale("log")
        plt.xlabel(r"$q = -2(\log L_{s+b} - \log L_b)$")
        plt.ylabel("toy experiments / bin")
        plt.title("Background-only test-statistic distribution")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(args.diagnostics, "test_statistic_distribution.png"), dpi=150)
        plt.close()

        # (b) -2*DeltaLogL(mu) scan
        plt.figure(figsize=(7, 5))
        plt.plot(mu_scan, twodll_scan, color="darkorange", lw=2)
        plt.axhline(1.0, color="gray", ls="--", lw=1, label=r"$-2\Delta\log L = 1$ (68% CL)")
        plt.axvline(mu_hat, color="black", ls=":", lw=1,
                    label=rf"$\hat\mu$ = {mu_hat:.2f}$^{{+{mu_hi-mu_hat:.2f}}}_{{-{mu_hat-mu_lo:.2f}}}$")
        plt.axvline(mu_lo, color="gray", ls=":", lw=1)
        plt.axvline(mu_hi, color="gray", ls=":", lw=1)
        plt.ylim(0, max(5, np.nanmax(twodll_scan[np.isfinite(twodll_scan)]) * 0.2))
        plt.xlabel(r"signal strength $\mu$")
        plt.ylabel(r"$-2\Delta\log L(\mu)$")
        plt.title("Profile likelihood scan for signal strength")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(args.diagnostics, "mu_scan.png"), dpi=150)
        plt.close()


if __name__ == "__main__":
    main()
