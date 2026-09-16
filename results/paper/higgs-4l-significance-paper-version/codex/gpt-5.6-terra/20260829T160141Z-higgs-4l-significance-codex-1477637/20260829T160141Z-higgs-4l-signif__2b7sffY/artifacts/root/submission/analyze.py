#!/usr/bin/env python3
"""Likelihood and toy-MC analysis for independent Poisson counting channels."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import gammaln, ndtri


DEFAULT_TOYS = 2_000_000
DEFAULT_SEED = 20260829


def poisson_log_likelihood(counts: np.ndarray, means: np.ndarray) -> float:
    """Return sum(log Poisson(count_i | mean_i)) for positive means."""
    return float(np.sum(-means + counts * np.log(means) - gammaln(counts + 1.0)))


def log_likelihood_mu(mu: float, counts: np.ndarray, background: np.ndarray,
                      signal: np.ndarray) -> float:
    """Poisson log likelihood at physical signal strength mu >= 0."""
    means = background + mu * signal
    return poisson_log_likelihood(counts, means)


def parse_input(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    with path.open(encoding="utf-8") as infile:
        payload: dict[str, Any] = json.load(infile)
    required = ("channels", "observed", "background", "signal")
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError("Input is missing required field(s): " + ", ".join(missing))

    channels = list(payload["channels"])
    counts = np.asarray(payload["observed"], dtype=float)
    background = np.asarray(payload["background"], dtype=float)
    signal = np.asarray(payload["signal"], dtype=float)
    n = len(channels)
    if n == 0 or any(values.size != n for values in (counts, background, signal)):
        raise ValueError("channels, observed, background, and signal must be nonempty and equal length")
    if not (np.all(np.isfinite(counts)) and np.all(np.isfinite(background)) and np.all(np.isfinite(signal))):
        raise ValueError("All numeric input values must be finite")
    if np.any(counts < 0) or np.any(counts != np.floor(counts)):
        raise ValueError("observed counts must be nonnegative integers")
    # A positive background is needed for the finite likelihood-ratio statistic used here.
    if np.any(background <= 0):
        raise ValueError("background expectations must be strictly positive")
    if np.any(signal < 0) or not np.any(signal > 0):
        raise ValueError("signal expectations must be nonnegative, with at least one positive entry")
    return counts, background, signal, channels


def determine_mu_interval(counts: np.ndarray, background: np.ndarray,
                          signal: np.ndarray) -> tuple[float, float, float, float]:
    """Find constrained MLE and the two Delta(-2logL)=1 endpoints."""
    # The likelihood is concave, so a broad bounded minimization of -logL is reliable.
    total_signal = float(np.sum(signal))
    upper_guess = max(10.0, (float(np.sum(counts)) + 10.0 * math.sqrt(float(np.sum(counts)) + 1.0)) / total_signal)
    objective = lambda mu: -log_likelihood_mu(mu, counts, background, signal)
    fit = minimize_scalar(objective, bounds=(0.0, upper_guess), method="bounded", options={"xatol": 1e-12})
    # Expand only in the unlikely event that the provisional upper bound held the optimum.
    while fit.x > 0.999 * upper_guess:
        upper_guess *= 2.0
        fit = minimize_scalar(objective, bounds=(0.0, upper_guess), method="bounded", options={"xatol": 1e-12})
    mu_hat = float(fit.x)
    logl_hat = -float(fit.fun)
    delta = lambda mu: -2.0 * (log_likelihood_mu(mu, counts, background, signal) - logl_hat)

    # In the supplied-like use case mu_hat > 0, yielding two crossings.  At a boundary
    # MLE, the lower physical edge is reported as zero if it lies inside 1 sigma.
    if delta(0.0) <= 1.0:
        mu_lo = 0.0
    else:
        mu_lo = float(brentq(lambda mu: delta(mu) - 1.0, 0.0, mu_hat, xtol=1e-12))

    hi_bracket = max(1.0, 2.0 * mu_hat + 1.0)
    while delta(hi_bracket) < 1.0:
        hi_bracket *= 2.0
    mu_hi = float(brentq(lambda mu: delta(mu) - 1.0, mu_hat, hi_bracket, xtol=1e-12))
    return mu_hat, mu_lo, mu_hi, logl_hat


def generate_toys(background: np.ndarray, log_ratio: np.ndarray, q_constant: float,
                  q_observed: float, n_toys: int, seed: int) -> tuple[np.ndarray, int]:
    """Generate b-only toys and return all q values plus tail count.

    q = 2 sum(signal) - 2 sum(k_i log((b_i+s_i)/b_i)); lower q is more signal-like.
    """
    rng = np.random.default_rng(seed)
    toy_q = np.empty(n_toys, dtype=float)
    tail_count = 0
    batch_size = min(200_000, n_toys)
    offset = 0
    while offset < n_toys:
        current = min(batch_size, n_toys - offset)
        toy_counts = rng.poisson(background, size=(current, background.size))
        values = q_constant - 2.0 * (toy_counts @ log_ratio)
        toy_q[offset:offset + current] = values
        tail_count += int(np.count_nonzero(values <= q_observed + 1e-12))
        offset += current
    return toy_q, tail_count


def make_plots(diagnostics: Path, toy_q: np.ndarray, q_observed: float,
               counts: np.ndarray, background: np.ndarray, signal: np.ndarray,
               mu_hat: float, logl_hat: float, mu_hi: float) -> None:
    diagnostics.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bins = min(120, max(30, int(np.sqrt(toy_q.size))))
    ax.hist(toy_q, bins=bins, density=True, color="#5b8db8", alpha=0.8, label="Background-only toys")
    ax.axvline(q_observed, color="#c43c39", linewidth=2, label=f"Observed q = {q_observed:.3f}")
    ax.set_xlabel(r"$q=-2\ln(L_{s+b}/L_b)$")
    ax.set_ylabel("Probability density")
    ax.set_title("Likelihood-ratio statistic under background only")
    ax.legend()
    fig.tight_layout()
    fig.savefig(diagnostics / "test_statistic_toys.png", dpi=160)
    plt.close(fig)

    scan_hi = max(mu_hi * 1.25, mu_hat * 2.0 + 1.0)
    mu_grid = np.linspace(0.0, scan_hi, 800)
    curve = np.array([-2.0 * (log_likelihood_mu(mu, counts, background, signal) - logl_hat) for mu in mu_grid])
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(mu_grid, curve, color="#365f91", linewidth=2)
    ax.axhline(1.0, color="#777777", linestyle="--", label=r"$-2\Delta\log L=1$")
    ax.axvline(mu_hat, color="#c43c39", linestyle="--", label=fr"$\hat{{\mu}}={mu_hat:.3f}$")
    ax.set_xlim(0.0, scan_hi)
    ax.set_ylim(bottom=0.0)
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_ylabel(r"$-2\Delta\log L(\mu)$")
    ax.set_title("Profile likelihood scan")
    ax.legend()
    fig.tight_layout()
    fig.savefig(diagnostics / "mu_profile_scan.png", dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--toys", type=int, default=DEFAULT_TOYS, help="number of b-only toys (default: 2,000,000)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="random seed for reproducible toys")
    parser.add_argument("--diagnostics-dir", type=Path, default=None, help="directory for the two PNG diagnostic plots")
    args = parser.parse_args()
    if args.toys < 1_000_000:
        parser.error("--toys must be at least 1,000,000")

    counts, background, signal, channels = parse_input(args.input_json)
    sb = background + signal
    logl_b = poisson_log_likelihood(counts, background)
    logl_sb = poisson_log_likelihood(counts, sb)
    q_observed = -2.0 * (logl_sb - logl_b)

    log_ratio = np.log(sb / background)
    q_constant = 2.0 * float(np.sum(signal))
    toy_q, tail_count = generate_toys(background, log_ratio, q_constant, q_observed, args.toys, args.seed)
    p_value = tail_count / args.toys
    p_value_mc_se = math.sqrt(p_value * (1.0 - p_value) / args.toys)
    significance = float(ndtri(1.0 - p_value)) if p_value > 0.0 else float("inf")

    mu_hat, mu_lo, mu_hi, logl_hat = determine_mu_interval(counts, background, signal)
    diagnostics_dir = args.diagnostics_dir
    if diagnostics_dir is None:
        diagnostics_dir = Path(__file__).resolve().parent / "diagnostics"
    make_plots(diagnostics_dir, toy_q, q_observed, counts, background, signal, mu_hat, logl_hat, mu_hi)

    results = {
        "logL_b": logl_b,
        "logL_sb": logl_sb,
        "test_statistic": q_observed,
        "p_value": p_value,
        "p_value_mc_se": p_value_mc_se,
        "significance": significance,
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi,
        "n_toys": args.toys,
        "toy_tail_count": tail_count,
        "random_seed": args.seed,
        "channels": channels,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_json.open("w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=2, allow_nan=False)
        outfile.write("\n")


if __name__ == "__main__":
    main()
