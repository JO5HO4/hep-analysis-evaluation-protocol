#!/usr/bin/env python3
"""Diagnostic plots for the 4-lepton counting analysis."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# validated categorical slots 1/2 + status:critical, light surface
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#dcdbd6"
C_BONLY = "#2a78d6"   # slot 1 - background-only toys
C_SB = "#eb6834"      # slot 2 - signal+background toys
C_OBS = "#e34948"     # observed value marker


def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
        ax.spines[side].set_linewidth(1.0)
    ax.tick_params(colors=INK2, labelsize=9, length=3, width=0.8)


def plot_teststat(path, q_b, q_sb, q_obs, res):
    lo = min(q_b.min(), q_sb.min(), q_obs) - 1.0
    hi = max(q_b.max(), q_sb.max(), q_obs) + 1.0
    bins = np.linspace(lo, hi, 160)

    fig, ax = plt.subplots(figsize=(9.0, 5.2), facecolor=SURFACE)
    _style(ax)

    for q, colour, label in ((q_b, C_BONLY, "background-only toys"),
                             (q_sb, C_SB, "signal+background toys")):
        h, _ = np.histogram(q, bins=bins)
        ax.step(bins[:-1], h / len(q) / np.diff(bins), where="post",
                color=colour, linewidth=2.0, label=label)

    ax.axvline(q_obs, color=C_OBS, linewidth=2.0, linestyle="-")
    ax.set_yscale("log")
    ymin = 1.0 / len(q_b) / (bins[1] - bins[0]) * 0.4
    ax.set_ylim(ymin, None)

    ytop = ax.get_ylim()[1]
    ax.annotate(f"observed  q = {q_obs:.2f}", xy=(q_obs, ytop * 0.35),
                xytext=(8, 0), textcoords="offset points",
                color=C_OBS, fontsize=10, fontweight="bold", va="center")
    ax.annotate("more signal-like  ←", xy=(0.02, 0.02),
                xycoords="axes fraction", color=INK2, fontsize=9)

    # direct labels on the two curves, at their modes
    for q, colour, label in ((q_b, C_BONLY, "background-only"),
                             (q_sb, C_SB, "signal+background")):
        h, _ = np.histogram(q, bins=bins)
        i = int(np.argmax(h))
        ax.annotate(label, xy=(bins[i], h[i] / len(q) / (bins[1] - bins[0])),
                    xytext=(0, 12), textcoords="offset points",
                    color=colour, fontsize=10, fontweight="bold", ha="center")

    p = res["p_value"]
    ptxt = (f"p = {p:.2e}" if p > 0 else "p = 0 (no toy passed)")
    ax.set_title("Likelihood-ratio test statistic from pseudo-experiments",
                 color=INK, fontsize=13, fontweight="bold", loc="left", pad=14)
    ax.text(0.0, 1.015,
            f"{res['n_toys']:,} toys per hypothesis   ·   "
            f"{res['n_toys_passing']:,} background toys at least as signal-like   ·   "
            f"{ptxt}   ·   Z = {res['significance']:.2f}σ",
            transform=ax.transAxes, color=INK2, fontsize=9.5, va="bottom")
    ax.set_xlabel("q = −2 (logL$_{s+b}$ − logL$_{b}$)", color=INK2, fontsize=10)
    ax.set_ylabel("probability density", color=INK2, fontsize=10)
    leg = ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    for t in leg.get_texts():
        t.set_color(INK2)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def plot_mu_scan(path, k, s, b, mu_hat, q_min, mu_lo, mu_hi, mu_floor, res):
    import analysis

    # frame the scan on the region that matters: out to roughly +-3 sigma
    span = max(mu_hi - mu_hat, mu_hat - mu_lo, 0.5)
    x_lo = max(mu_floor, mu_hat - 3.4 * span)
    x_hi = mu_hat + 3.4 * span
    if x_hi < 1.15:                       # always keep the SM point in view
        x_hi = 1.15
    xs = np.linspace(x_lo, x_hi, 900)
    ys = np.array([analysis.q_of_mu(k, s, b, m) for m in xs]) - q_min
    y_top = 10.0                          # 0 .. ~3 sigma

    fig, ax = plt.subplots(figsize=(9.0, 5.2), facecolor=SURFACE)
    _style(ax)

    ax.set_xlim(xs[0], xs[-1])
    ax.set_ylim(0, y_top)

    ax.plot(xs, ys, color=C_BONLY, linewidth=2.0, zorder=3)
    ax.axhline(1.0, color=INK2, linewidth=1.0, linestyle="--", zorder=2)
    ax.text(xs[-1], 1.12, "−2ΔlogL = 1  (±1σ)", color=INK2, fontsize=9,
            va="bottom", ha="right")

    ax.vlines([mu_lo, mu_hi], 0, 1, color=C_OBS, linewidth=1.5,
              linestyle=":", zorder=3)
    ax.plot([mu_hat], [0.0], "o", color=C_OBS, markersize=9,
            markeredgecolor=SURFACE, markeredgewidth=2.0, zorder=4)
    ax.annotate(f"$\\hat{{\\mu}}$ = {mu_hat:.2f}"
                f"$^{{+{mu_hi - mu_hat:.2f}}}_{{-{mu_hat - mu_lo:.2f}}}$",
                xy=(mu_hat, 0.0), xytext=(10, 16), textcoords="offset points",
                color=C_OBS, fontsize=12, fontweight="bold")
    if xs[0] <= 1.0 <= xs[-1]:
        ax.axvline(1.0, color=INK2, linewidth=1.0, alpha=0.55, zorder=1)
        ax.annotate("SM ($\\mu$=1)", xy=(1.0, y_top * 0.93),
                    xytext=(5, 0), textcoords="offset points",
                    color=INK2, fontsize=9.5)

    ax.set_title("Profile of the signal strength", color=INK, fontsize=13,
                 fontweight="bold", loc="left", pad=14)
    ax.text(0.0, 1.015,
            f"±1σ interval [{mu_lo:.3f}, {mu_hi:.3f}]   ·   "
            f"q($\\mu$) = −2[logL($\\mu$) − logL(0)]",
            transform=ax.transAxes, color=INK2, fontsize=9.5, va="bottom")
    ax.set_xlabel("signal strength  $\\mu$", color=INK2, fontsize=10)
    ax.set_ylabel("−2ΔlogL($\\mu$)", color=INK2, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def make_all(outdir, q_b, q_sb, q_obs, k, s, b, mu_hat, q_min, mu_lo, mu_hi,
             mu_floor, res):
    os.makedirs(outdir, exist_ok=True)
    plot_teststat(os.path.join(outdir, "test_statistic_distributions.png"),
                  q_b, q_sb, q_obs, res)
    plot_mu_scan(os.path.join(outdir, "mu_scan.png"),
                 k, s, b, mu_hat, q_min, mu_lo, mu_hi, mu_floor, res)
