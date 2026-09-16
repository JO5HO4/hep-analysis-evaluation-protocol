#!/usr/bin/env python3
"""
Counting-experiment analysis for H->ZZ*->4l.

Each channel i is an independent Poisson measurement of n_i events:
    background-only     :  lambda_i = b_i
    signal+background   :  lambda_i = mu * s_i + b_i   (mu = 1 for the SM)

Deliverables: log-likelihoods, the likelihood-ratio test statistic q, a
background-only p-value from toy Monte Carlo, the Gaussian significance Z,
and the best-fit signal strength mu-hat with its asymmetric +-1 sigma interval.

Usage:  python3 analysis.py INPUT_JSON OUTPUT_JSON [--ntoys N] [--seed S]
"""

import argparse
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import gammaln
from scipy.stats import norm, poisson

# ---------------------------------------------------------------------------
# likelihood
# ---------------------------------------------------------------------------


def log_poisson(k, lam):
    """log P(k | lam) = -lam + k log(lam) - log(k!), summed elementwise."""
    k = np.asarray(k, dtype=float)
    lam = np.asarray(lam, dtype=float)
    return -lam + k * np.log(lam) - gammaln(k + 1.0)


def total_logL(k, lam):
    return float(np.sum(log_poisson(k, lam)))


def q_of_mu(k, s, b, mu):
    """q(mu) = -2 [ logL(mu) - logL(0) ], with the log(k!) terms cancelling."""
    lam = mu * s + b
    return -2.0 * (total_logL(k, lam) - total_logL(k, b))


# ---------------------------------------------------------------------------
# test statistic
# ---------------------------------------------------------------------------
#
# For the fixed SM hypothesis (mu = 1) the factorials cancel and
#
#     q = -2 sum_i [ -s_i + n_i log(1 + s_i/b_i) ]
#       = 2 sum_i s_i  -  2 sum_i n_i w_i ,      w_i = log(1 + s_i/b_i) >= 0
#
# so q is an exact affine function of the counts.  More signal-like data give
# a *smaller* (more negative) q, hence the p-value is P(q_toy <= q_obs).
# The closed form makes 10^7 toys a couple of matrix products.


def weights(s, b):
    return np.log1p(s / b)


def q_from_counts(counts, s, b):
    """q for one or many datasets; `counts` has shape (..., nchan)."""
    w = weights(s, b)
    return 2.0 * np.sum(s) - 2.0 * np.asarray(counts, dtype=float) @ w


# ---------------------------------------------------------------------------
# p-value
# ---------------------------------------------------------------------------


def run_toys(s, b, q_obs, ntoys, seed, batch=2_000_000, rng_mean=None):
    """Throw Poisson toys from `rng_mean` (default: background-only) and count
    how many are at least as signal-like as the data.  Returns (n_pass, q_all)."""
    if rng_mean is None:
        rng_mean = b
    rng = np.random.default_rng(seed)
    w = weights(s, b)
    const = 2.0 * np.sum(s)
    # exact ties are physically meaningful (the statistic is lattice-valued);
    # a tiny tolerance keeps float round-off from dropping them.
    tol = 1e-9 * max(1.0, abs(q_obs))

    n_pass = 0
    chunks = []
    done = 0
    while done < ntoys:
        n = min(batch, ntoys - done)
        counts = rng.poisson(rng_mean, size=(n, len(b)))
        q = const - 2.0 * (counts @ w)
        n_pass += int(np.count_nonzero(q <= q_obs + tol))
        chunks.append(q.astype(np.float32))
        done += n
    return n_pass, np.concatenate(chunks)


def exact_pvalue(s, b, q_obs, tail_prob=1e-15):
    """Cross-check: sum the background-only Poisson probability over the count
    lattice directly.  Only attempted when the lattice is small enough."""
    w = weights(s, b)
    const = 2.0 * np.sum(s)
    kmaxes = [int(poisson.isf(tail_prob, bi)) + 5 for bi in b]
    if np.prod([k + 1 for k in kmaxes], dtype=float) > 2e7:
        return None

    # distribution of the scalar T = sum_i n_i w_i, built by successive outer
    # products over channels (exact, no sampling)
    probs = np.array([1.0])
    tvals = np.array([0.0])
    for bi, wi, kmax in zip(b, w, kmaxes):
        ks = np.arange(kmax + 1)
        pk = poisson.pmf(ks, bi)
        probs = np.outer(probs, pk).ravel()
        tvals = (tvals[:, None] + ks * wi).ravel()
        keep = probs > 1e-300
        probs, tvals = probs[keep], tvals[keep]
    q = const - 2.0 * tvals
    tol = 1e-9 * max(1.0, abs(q_obs))
    return float(np.sum(probs[q <= q_obs + tol]))


# ---------------------------------------------------------------------------
# signal strength
# ---------------------------------------------------------------------------


def mu_scan(k, s, b):
    """Best-fit mu and the two -2 dlogL = 1 crossings."""
    pos = s > 0
    # means must stay positive: mu > max_i(-b_i/s_i) over channels with s_i>0
    mu_floor = float(np.max(-b[pos] / s[pos])) if np.any(pos) else -np.inf
    lo_bound = mu_floor + 1e-9 * max(1.0, abs(mu_floor))

    f = lambda mu: q_of_mu(k, s, b, mu)
    hi_bound = 1.0 + 10.0 * max(1.0, np.sum(k) / max(np.sum(s), 1e-12))
    res = minimize_scalar(f, bounds=(lo_bound, hi_bound), method="bounded",
                          options={"xatol": 1e-10})
    mu_hat = float(res.x)
    q_min = float(res.fun)

    delta = lambda mu: f(mu) - q_min - 1.0

    def crossing(direction):
        step, edge = 0.05 * max(1.0, abs(mu_hat)), mu_hat
        for _ in range(4000):
            nxt = edge + direction * step
            if direction < 0 and nxt <= lo_bound:
                # -2dlogL may stay below 1 all the way to the physical edge
                return float("nan") if delta(lo_bound) < 0 else brentq(
                    delta, lo_bound, edge, xtol=1e-12)
            if delta(nxt) > 0:
                a, c = (nxt, edge) if direction < 0 else (edge, nxt)
                return float(brentq(delta, a, c, xtol=1e-12))
            edge = nxt
            step *= 1.05
        return float("nan")

    return mu_hat, q_min, crossing(-1), crossing(+1), lo_bound


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------


def analyse(data, ntoys, seed, outdir=None):
    n = np.asarray(data["observed"], dtype=float)
    b = np.asarray(data["background"], dtype=float)
    s = np.asarray(data["signal"], dtype=float)
    channels = list(data.get("channels", [f"ch{i}" for i in range(len(n))]))
    if np.any(b <= 0):
        raise ValueError("background expectation must be > 0 in every channel")

    logL_b = total_logL(n, b)
    logL_sb = total_logL(n, s + b)
    q_obs = -2.0 * (logL_sb - logL_b)

    n_pass, q_toys_b = run_toys(s, b, q_obs, ntoys, seed)
    p_toy = n_pass / ntoys
    p_err = float(np.sqrt(max(p_toy, 1.0 / ntoys) * (1 - p_toy) / ntoys))
    p_exact = exact_pvalue(s, b, q_obs)

    # if no toy is as extreme as the data the MC estimate saturates; fall back
    # on the exact lattice sum (same statistic, no sampling) for Z.
    p_for_z, p_source = p_toy, "toys"
    if n_pass == 0:
        if p_exact is not None and p_exact > 0:
            p_for_z, p_source = p_exact, "exact-enumeration (0 toys passed)"
        else:
            p_for_z, p_source = 1.0 / ntoys, f"upper limit 1/{ntoys} (0 toys passed)"
    Z = float(norm.isf(p_for_z))

    mu_hat, q_min, mu_lo, mu_hi, mu_floor = mu_scan(n, s, b)

    results = {
        "channels": channels,
        "observed": [int(x) for x in data["observed"]],
        "background": b.tolist(),
        "signal": s.tolist(),
        "logL_b": logL_b,
        "logL_sb": logL_sb,
        "test_statistic": q_obs,
        "p_value": p_toy,
        "significance": Z,
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi,
        "mu_err_up": mu_hi - mu_hat,
        "mu_err_down": mu_hat - mu_lo,
        "evidence_3sigma": bool(Z >= 3.0),
        "discovery_5sigma": bool(Z >= 5.0),
        "n_toys": int(ntoys),
        "n_toys_passing": int(n_pass),
        "p_value_uncertainty": p_err,
        "p_value_exact": p_exact,
        "p_value_used_for_Z": p_for_z,
        "p_value_source": p_source,
        "significance_from_toys_only": (float(norm.isf(p_toy)) if p_toy > 0
                                        else None),
        "q_min": q_min,
        "seed": int(seed),
    }

    if outdir is not None:
        import plots
        n_pass_sb, q_toys_sb = run_toys(s, b, q_obs, min(ntoys, 2_000_000),
                                        seed + 1, rng_mean=s + b)
        results["expected_p_value_under_sb"] = None  # not requested; placeholder
        del results["expected_p_value_under_sb"]
        plots.make_all(outdir, q_toys_b, q_toys_sb, q_obs, n, s, b,
                       mu_hat, q_min, mu_lo, mu_hi, mu_floor, results)

    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input_json")
    ap.add_argument("output_json")
    ap.add_argument("--ntoys", type=int,
                    default=int(os.environ.get("NTOYS", 10_000_000)))
    ap.add_argument("--seed", type=int, default=int(os.environ.get("SEED", 20260829)))
    ap.add_argument("--diagnostics", default=None,
                    help="directory for diagnostic plots (skipped if omitted)")
    args = ap.parse_args(argv)

    with open(args.input_json) as fh:
        data = json.load(fh)

    res = analyse(data, args.ntoys, args.seed, outdir=args.diagnostics)

    outdir = os.path.dirname(os.path.abspath(args.output_json))
    os.makedirs(outdir, exist_ok=True)
    with open(args.output_json, "w") as fh:
        json.dump(res, fh, indent=2)
        fh.write("\n")

    print(f"channels        : {', '.join(res['channels'])}")
    print(f"observed        : {res['observed']}")
    print(f"logL_b          : {res['logL_b']:.6f}")
    print(f"logL_sb         : {res['logL_sb']:.6f}")
    print(f"q_obs           : {res['test_statistic']:.6f}")
    print(f"p-value (toys)  : {res['p_value']:.3e} +- {res['p_value_uncertainty']:.1e}"
          f"   [{res['n_toys_passing']} / {res['n_toys']}]")
    if res["p_value_exact"] is not None:
        print(f"p-value (exact) : {res['p_value_exact']:.3e}")
    print(f"significance    : {res['significance']:.3f} sigma  ({res['p_value_source']})")
    print(f"3 sigma evidence: {res['evidence_3sigma']}")
    print(f"mu              : {res['mu_hat']:.3f} "
          f"+{res['mu_err_up']:.3f} -{res['mu_err_down']:.3f}")
    print(f"wrote {args.output_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
