#!/usr/bin/env python3
"""Poisson counting analysis for independent signal channels."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln, ndtri, xlogy


N_TOYS = 2_000_000
RANDOM_SEED = 20260829


def load_counts(path: Path) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    required = ("channels", "observed", "background", "signal")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")

    channels = data["channels"]
    observed = np.asarray(data["observed"], dtype=float)
    background = np.asarray(data["background"], dtype=float)
    signal = np.asarray(data["signal"], dtype=float)

    if not isinstance(channels, list) or not channels:
        raise ValueError("channels must be a non-empty list")
    if any(array.ndim != 1 for array in (observed, background, signal)):
        raise ValueError("observed, background, and signal must be one-dimensional")
    if not (len(channels) == observed.size == background.size == signal.size):
        raise ValueError("channels, observed, background, and signal must have equal lengths")
    if not all(np.all(np.isfinite(a)) for a in (observed, background, signal)):
        raise ValueError("all numerical inputs must be finite")
    if np.any(observed < 0) or np.any(observed != np.floor(observed)):
        raise ValueError("observed counts must be non-negative integers")
    if np.any(background <= 0):
        raise ValueError("background expectations must be strictly positive")
    if np.any(signal < 0) or not np.any(signal > 0):
        raise ValueError("signal expectations must be non-negative, with at least one positive")

    return [str(c) for c in channels], observed, background, signal


def log_likelihood(counts: np.ndarray, means: np.ndarray) -> float:
    """Total independent-Poisson log likelihood, including factorial terms."""
    return float(np.sum(-means + xlogy(counts, means) - gammaln(counts + 1.0)))


def fixed_test_statistic(counts: np.ndarray, background: np.ndarray,
                         signal: np.ndarray) -> np.ndarray:
    """Return -2 log[L(s+b)/L(b)] for one dataset or rows of datasets."""
    # Factorial terms cancel. This form is fast and stable for toy batches.
    weights = np.log1p(signal / background)
    return 2.0 * (np.sum(signal) - np.asarray(counts) @ weights)


def generate_background_toys(background: np.ndarray, signal: np.ndarray,
                             q_observed: float, n_toys: int,
                             seed: int) -> tuple[float, int, np.ndarray]:
    rng = np.random.default_rng(seed)
    q_toys = np.empty(n_toys, dtype=float)
    # Limit the temporary count array for inputs with many channels.
    chunk_size = max(1, min(200_000, 5_000_000 // background.size))
    tail_count = 0
    offset = 0
    while offset < n_toys:
        stop = min(offset + chunk_size, n_toys)
        counts = rng.poisson(background, size=(stop - offset, background.size))
        values = fixed_test_statistic(counts, background, signal)
        q_toys[offset:stop] = values
        tail_count += int(np.count_nonzero(values <= q_observed))
        offset = stop
    return tail_count / n_toys, tail_count, q_toys


def fit_signal_strength(observed: np.ndarray, background: np.ndarray,
                        signal: np.ndarray) -> tuple[float, float, float, callable]:
    """Fit physical mu >= 0 and obtain likelihood-ratio 1-sigma crossings."""
    def logl(mu: float) -> float:
        return log_likelihood(observed, mu * signal + background)

    def score(mu: float) -> float:
        means = mu * signal + background
        return float(np.sum(signal * (observed / means - 1.0)))

    if score(0.0) <= 0.0:
        mu_hat = 0.0
    else:
        upper = max(1.0, float(np.sum(observed) / np.sum(signal)))
        while score(upper) > 0.0:
            upper *= 2.0
            if upper > 1.0e9:
                raise RuntimeError("could not bracket the signal-strength maximum")
        mu_hat = float(brentq(score, 0.0, upper, xtol=1e-13, rtol=1e-14))

    logl_hat = logl(mu_hat)

    def delta(mu: float) -> float:
        return 2.0 * (logl_hat - logl(mu))

    # At a physical boundary there may be no lower crossing; report the boundary.
    if mu_hat == 0.0 or delta(0.0) < 1.0:
        mu_lo = 0.0
    else:
        mu_lo = float(brentq(lambda mu: delta(mu) - 1.0, 0.0, mu_hat,
                             xtol=1e-12, rtol=1e-13))

    upper = max(1.0, 2.0 * mu_hat)
    while delta(upper) < 1.0:
        upper *= 2.0
        if upper > 1.0e9:
            raise RuntimeError("could not bracket the upper 1-sigma crossing")
    mu_hi = float(brentq(lambda mu: delta(mu) - 1.0, mu_hat, upper,
                         xtol=1e-12, rtol=1e-13))
    return mu_hat, mu_lo, mu_hi, delta


def make_diagnostics(diagnostics: Path, q_toys: np.ndarray, q_observed: float,
                     mu_hat: float, mu_lo: float, mu_hi: float,
                     delta: callable) -> None:
    diagnostics.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(q_toys, bins=140, histtype="stepfilled", color="#4C78A8",
            alpha=0.75, label="Background-only toys")
    ax.axvline(q_observed, color="#D62728", linewidth=2,
               label=f"Observed q = {q_observed:.3f}")
    ax.set_xlabel(r"$q=-2\log[L(s+b)/L(b)]$")
    ax.set_ylabel("Pseudo-experiments per bin")
    ax.set_yscale("log")
    ax.set_title("Background-only test-statistic distribution")
    ax.legend()
    fig.tight_layout()
    fig.savefig(diagnostics / "test_statistic_distribution.png", dpi=160)
    plt.close(fig)

    plot_max = max(mu_hi * 1.35, mu_hat + 0.5, 1.0)
    mus = np.linspace(0.0, plot_max, 700)
    deltas = np.array([delta(float(mu)) for mu in mus])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(mus, deltas, color="#4C78A8", linewidth=2)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1,
               label=r"$-2\Delta\log L=1$")
    ax.axvline(mu_hat, color="#D62728", linewidth=1.5,
               label=rf"$\hat{{\mu}}={mu_hat:.3f}$")
    ax.scatter([mu_lo, mu_hi], [1.0, 1.0], color="#F58518", zorder=3,
               label="68% likelihood crossings")
    ax.set_xlim(0.0, plot_max)
    ax.set_ylim(0.0, max(2.5, min(12.0, float(np.max(deltas)) * 1.05)))
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_ylabel(r"$-2\Delta\log L(\mu)$")
    ax.set_title("Signal-strength likelihood profile")
    ax.legend()
    fig.tight_layout()
    fig.savefig(diagnostics / "mu_likelihood_scan.png", dpi=160)
    plt.close(fig)


def analyze(input_path: Path, output_path: Path, diagnostics: Path) -> dict:
    channels, observed, background, signal = load_counts(input_path)
    logl_b = log_likelihood(observed, background)
    logl_sb = log_likelihood(observed, background + signal)
    q_observed = -2.0 * (logl_sb - logl_b)

    p_value, tail_count, q_toys = generate_background_toys(
        background, signal, q_observed, N_TOYS, RANDOM_SEED
    )
    # JSON has no representation for the infinite Z at an empirical endpoint.
    significance = (float(ndtri(1.0 - p_value))
                    if 0.0 < p_value < 1.0 else None)
    p_value_mc_se = math.sqrt(p_value * (1.0 - p_value) / N_TOYS)

    mu_hat, mu_lo, mu_hi, delta = fit_signal_strength(observed, background, signal)
    make_diagnostics(diagnostics, q_toys, q_observed, mu_hat, mu_lo, mu_hi, delta)

    result = {
        "logL_b": logl_b,
        "logL_sb": logl_sb,
        "test_statistic": q_observed,
        "p_value": p_value,
        "significance": significance,
        "p_value_mc_se": p_value_mc_se,
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi,
        "n_toys": N_TOYS,
        "tail_toys": tail_count,
        "random_seed": RANDOM_SEED,
        "tail_definition": "q_toy <= q_observed",
        "channels": channels,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write("\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()
    diagnostics = Path(__file__).resolve().parent / "diagnostics"
    result = analyze(args.input_json, args.output_json, diagnostics)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
