"""All PNG/PDF plots produced by the pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

COMPONENT_STYLE = {
    "signal_ttH_tH": {"label": "ttH + tH signal", "color": "#d62728"},
    "resonant_higgs_bkg": {"label": "resonant Higgs bkg", "color": "#1f77b4"},
    "nti_continuum_bkg": {"label": "NTI continuum bkg", "color": "#2ca02c"},
}


def _save(fig: plt.Figure, stem: Path) -> list[str]:
    stem.parent.mkdir(parents=True, exist_ok=True)
    out = []
    for ext in ("png", "pdf"):
        path = stem.with_suffix(f".{ext}")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        out.append(str(path))
    plt.close(fig)
    return out


# --------------------------------------------------------------------------
# Preselection plots
# --------------------------------------------------------------------------


def plot_preselection(df: pd.DataFrame, cfg: Mapping[str, Any], outdir: Path) -> list[str]:
    written: list[str] = []
    sel = cfg["selection"]
    blind_lo, blind_hi = cfg["blinding"]["blinded_range_gev"]
    edges = np.linspace(*sel["mgg_fit_range_gev"], 56)

    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    had = df[df["passes_hadronic_preselection"]]
    mc = had[had["is_mc"] & had["photon_ti"]]
    for role, color, label in [
        ("signal_top", "#d62728", "ttH + tH TI MC (36 fb$^{-1}$)"),
        ("resonant_higgs", "#1f77b4", "non-top Higgs TI MC (36 fb$^{-1}$)"),
    ]:
        sub = mc[mc["process_role"] == role]
        ax.hist(
            sub["m_gammagamma"],
            bins=edges,
            weights=sub["weight_mc_36fb"],
            histtype="step",
            lw=1.8,
            color=color,
            label=label,
        )
    nti = had[had["is_data"] & had["photon_nti"]]
    counts, _ = np.histogram(nti["m_gammagamma"], bins=edges)
    scale = 1.0
    ax.step(
        edges[:-1],
        counts * scale / max(counts.max(), 1) * max(
            np.histogram(
                mc["m_gammagamma"], bins=edges, weights=mc["weight_mc_36fb"]
            )[0].max(),
            1e-9,
        ),
        where="post",
        color="#2ca02c",
        lw=1.4,
        ls="--",
        label="NTI data control shape (arb. norm., unblinded)",
    )
    ti = had[had["is_data"] & had["photon_ti"]]
    ti_sb = ti[(ti["m_gammagamma"] < blind_lo) | (ti["m_gammagamma"] > blind_hi)]
    c, _ = np.histogram(ti_sb["m_gammagamma"], bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    nz = c > 0
    ax.errorbar(
        centers[nz],
        c[nz],
        yerr=np.sqrt(c[nz]),
        fmt="ko",
        ms=3.5,
        label="observed TI data (sidebands only)",
    )
    ax.axvspan(blind_lo, blind_hi, color="0.85", alpha=0.6, zorder=0)
    ax.text(
        0.5 * (blind_lo + blind_hi),
        ax.get_ylim()[1] * 0.92,
        "blinded\n(TI data)",
        ha="center",
        fontsize=8,
        color="0.3",
    )
    ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
    ax.set_ylabel("events / bin")
    ax.set_title("Hadronic preselection: diphoton mass")
    ax.legend(fontsize=8)
    written += _save(fig, outdir / "preselection_mass")

    # channels
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    counts = df.groupby(["preselection_channel", "process"]).size().unstack(fill_value=0)
    counts.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
    ax.set_yscale("log")
    ax.set_ylabel("selected rows")
    ax.set_xlabel("preselection channel")
    ax.set_title("Preselected rows by channel and process")
    ax.legend(fontsize=7, ncol=2)
    written += _save(fig, outdir / "preselection_channels")

    # processes
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    proc = df.groupby("process").size().sort_values(ascending=False)
    axes[0].bar(proc.index, proc.to_numpy(), color="#4c72b0")
    axes[0].set_yscale("log")
    axes[0].set_ylabel("selected rows (raw)")
    axes[0].set_title("Raw selected rows by process")
    axes[0].tick_params(axis="x", rotation=45)
    mcw = (
        df[df["is_mc"]].groupby("process")["weight_mc_36fb"].sum().sort_values(ascending=False)
    )
    axes[1].bar(mcw.index, mcw.to_numpy(), color="#dd8452")
    axes[1].set_ylabel("weighted yield @ 36 fb$^{-1}$")
    axes[1].set_title("Weighted MC yield by process (all selected)")
    axes[1].tick_params(axis="x", rotation=45)
    fig.tight_layout()
    written += _save(fig, outdir / "preselection_processes")
    return written


# --------------------------------------------------------------------------
# BDT score shape comparison
# --------------------------------------------------------------------------


def plot_score_shapes(payload: Mapping[str, Any], stem: Path) -> list[str]:
    edges = np.array(payload["binning"]["edges"], dtype=float)
    centers = 0.5 * (edges[1:] + edges[:-1])
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    for name, style in COMPONENT_STYLE.items():
        comp = payload["components"].get(name)
        if comp is None:
            continue
        values = np.array(comp["normalized_contents"], dtype=float)
        ax.step(
            np.append(edges[:-1], edges[-1]),
            np.append(values, values[-1] if len(values) else 0.0),
            where="post",
            lw=1.9,
            color=style["color"],
            label=f"{style['label']} (raw {comp['raw_total']}, "
            f"tot {comp['total_before_shape_normalization']:.3g})",
        )
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("BDT score")
    ax.set_ylabel("fraction of events / bin (unit area)")
    ax.set_title("Hadronic BDT score: shape comparison (equal area)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    return _save(fig, stem)


# --------------------------------------------------------------------------
# Categorization plots
# --------------------------------------------------------------------------


def plot_category_yields(summary: pd.DataFrame, stem: Path) -> list[str]:
    keep = summary[summary["category"] != "unassigned"]
    x = np.arange(len(keep))
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.bar(x, keep["nti_continuum_bkg_yield"], label="NTI continuum bkg", color="#2ca02c")
    ax.bar(
        x,
        keep["resonant_higgs_bkg_yield"],
        bottom=keep["nti_continuum_bkg_yield"],
        label="resonant Higgs bkg",
        color="#1f77b4",
    )
    ax.bar(
        x,
        keep["signal_ttH_tH_yield"],
        bottom=keep["total_background_yield"],
        label="ttH + tH signal",
        color="#d62728",
    )
    for xi, (s, b) in enumerate(
        zip(keep["signal_ttH_tH_yield"], keep["total_background_yield"])
    ):
        ax.text(xi, s + b, f"S={s:.2f}\nB={b:.2f}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(keep["category"], rotation=20, ha="right")
    ax.set_ylabel("expected events in 125 $\\pm$ 2 GeV @ 36 fb$^{-1}$")
    ax.set_title("Expected category yields (observed TI signal window blinded)")
    ax.legend(fontsize=8)
    ax.margins(y=0.18)
    return _save(fig, stem)


def plot_category_significance(
    summary: pd.DataFrame, combined: float, stem: Path
) -> list[str]:
    keep = summary[summary["category"] != "unassigned"]
    x = np.arange(len(keep))
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.bar(x, keep["expected_counting_significance"], color="#9467bd")
    for xi, z in enumerate(keep["expected_counting_significance"]):
        ax.text(xi, z, f"{z:.3f}", ha="center", va="bottom", fontsize=8)
    ax.axhline(combined, color="k", ls="--", lw=1.2, label=f"combined Z = {combined:.3f}")
    ax.set_xticks(x)
    ax.set_xticklabels(keep["category"], rotation=20, ha="right")
    ax.set_ylabel("expected counting significance Z")
    ax.set_title("Expected counting significance per category @ 36 fb$^{-1}$")
    ax.legend(fontsize=8)
    ax.margins(y=0.18)
    return _save(fig, stem)


def plot_bdt_model_components(
    payload: Mapping[str, Any], stem: Path, boundaries: Sequence[float] | None = None
) -> list[str]:
    edges = np.array(payload["binning"]["edges"], dtype=float)
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    for name, style in COMPONENT_STYLE.items():
        comp = payload["components"].get(name)
        if comp is None:
            continue
        values = np.array(comp["contents"], dtype=float)
        errs = np.sqrt(np.array(comp["sumw2"], dtype=float))
        centers = 0.5 * (edges[1:] + edges[:-1])
        ax.step(
            np.append(edges[:-1], edges[-1]),
            np.append(values, values[-1] if len(values) else 0.0),
            where="post",
            lw=1.8,
            color=style["color"],
            label=f"{style['label']} ({values.sum():.2f} ev)",
        )
        ax.errorbar(centers, values, yerr=errs, fmt="none", ecolor=style["color"], alpha=0.5)
    ax.set_yscale("symlog", linthresh=1e-3)
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("BDT score")
    ax.set_ylabel("expected events @ 36 fb$^{-1}$")
    title = "BDT score: expected model components"
    if boundaries:
        for i, b in enumerate(sorted(boundaries, reverse=True)):
            ax.axvline(b, color="k", ls=":", lw=1.4)
            ax.text(
                b,
                ax.get_ylim()[1],
                f" b{i + 1}={b:.2f}",
                rotation=90,
                va="top",
                ha="left",
                fontsize=7,
            )
        title += " with category boundaries"
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    return _save(fig, stem)


def plot_category_mgg_shapes(payload: Mapping[str, Any], stem: Path) -> list[str]:
    cats = list(payload["categories"].keys())
    if not cats:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "no retained categories", ha="center")
        return _save(fig, stem)
    edges = np.array(payload["binning"]["edges"], dtype=float)
    centers = 0.5 * (edges[1:] + edges[:-1])
    ncol = min(3, len(cats))
    nrow = int(np.ceil(len(cats) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.6 * ncol, 3.6 * nrow), squeeze=False)
    blind = payload["blinding"]["observed_ti_blinded_range_gev"]
    for idx, cat in enumerate(cats):
        ax = axes[idx // ncol][idx % ncol]
        data = payload["categories"][cat]
        for key, color, label in [
            ("nti_continuum_control_shape_scaled_by_SF1", "#2ca02c", "NTI cont. (x SF1)"),
            ("resonant_higgs_ti_mc_36fb", "#1f77b4", "resonant Higgs"),
            ("signal_ttH_tH_ti_mc_36fb", "#d62728", "ttH + tH"),
        ]:
            values = np.array(data[key]["contents"], dtype=float)
            ax.step(
                np.append(edges[:-1], edges[-1]),
                np.append(values, values[-1]),
                where="post",
                lw=1.5,
                color=color,
                label=label,
            )
        obs = np.array(data["observed_ti_data_sidebands_only"]["contents"], dtype=float)
        nz = obs > 0
        ax.errorbar(
            centers[nz], obs[nz], yerr=np.sqrt(obs[nz]), fmt="ko", ms=3, label="obs TI (SB)"
        )
        ax.axvspan(blind[0], blind[1], color="0.85", alpha=0.7, zorder=0)
        ax.set_title(cat, fontsize=9)
        ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
        ax.set_ylabel("events / bin")
        ax.tick_params(labelsize=8)
        if idx == 0:
            ax.legend(fontsize=7)
    for j in range(len(cats), nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")
    fig.suptitle(
        "Per-category $m_{\\gamma\\gamma}$ control shapes "
        "(grey band = blinded observed TI window; NTI unblinded)",
        fontsize=10,
    )
    fig.tight_layout()
    return _save(fig, stem)


# --------------------------------------------------------------------------
# Workspace / fit diagnostics
# --------------------------------------------------------------------------


def plot_sideband_fits(payload: Mapping[str, Any], plotdir: Path) -> dict[str, Any]:
    """Per-category TI-sideband background-fit plots plus a combined summary."""
    plotdir.mkdir(parents=True, exist_ok=True)
    cats = list(payload.keys())
    per_category_files: dict[str, list[str]] = {}

    def draw(ax, cat: str) -> None:
        rec = payload[cat]
        edges = np.array(rec["binning"]["edges"], dtype=float)
        centers = 0.5 * (edges[1:] + edges[:-1])
        counts = np.array(rec["observed_ti_sideband_counts"], dtype=float)
        curve = np.array(rec["fitted_continuum_curve"], dtype=float)
        blo, bhi = rec["blinded_range_gev"]
        in_sb = (centers < blo) | (centers > bhi)
        ax.errorbar(
            centers[in_sb],
            counts[in_sb],
            yerr=np.sqrt(np.clip(counts[in_sb], 0, None)),
            fmt="ko",
            ms=3.5,
            label=f"observed TI sideband data ({int(rec['n_ti_sideband_events'])})",
        )
        ax.plot(
            centers,
            curve,
            color="#d62728",
            lw=1.8,
            label=f"fitted continuum PDF ({rec['pdf']})",
        )
        ax.axvspan(blo, bhi, color="0.85", alpha=0.75, zorder=0)
        ax.text(
            0.5 * (blo + bhi),
            ax.get_ylim()[1] * 0.9,
            "blinded",
            ha="center",
            fontsize=7,
            color="0.3",
        )
        ax.set_xlim(edges[0], edges[-1])
        ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
        ax.set_ylabel(f"events / {edges[1] - edges[0]:.2f} GeV")
        ax.set_title(
            f"{cat}: TI sideband fit, N(105-160) = {rec['fitted_full_range_yield']:.1f}",
            fontsize=9,
        )
        ax.legend(fontsize=7)

    for cat in cats:
        fig, ax = plt.subplots(figsize=(6.6, 4.4))
        draw(ax, cat)
        per_category_files[cat] = _save(fig, plotdir / f"sidebands_background_fit_{cat}")

    ncol = min(3, max(len(cats), 1))
    nrow = int(np.ceil(max(len(cats), 1) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(5.2 * ncol, 3.9 * nrow), squeeze=False)
    for idx, cat in enumerate(cats):
        draw(axes[idx // ncol][idx % ncol], cat)
    for j in range(len(cats), nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")
    fig.suptitle(
        "Observed TI data sideband continuum fits (per workspace category)", fontsize=11
    )
    fig.tight_layout()
    combined = _save(fig, plotdir / "sidebands_background_fit")
    return {"per_category": per_category_files, "combined_summary": combined}


def plot_asimov_fit(
    result: Mapping[str, Any], plotdir: Path
) -> tuple[list[str], dict[str, Any]]:
    """Full-range Asimov S+B spectrum, summed over the workspace categories."""
    payload = result["asimov_plot_payload"]
    cats = list(payload.keys())
    if not cats:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "no categories", ha="center")
        return _save(fig, plotdir / "asimov_sb_fit"), {}

    edges = np.array(payload[cats[0]]["edges"], dtype=float)
    centers = 0.5 * (edges[1:] + edges[:-1])
    total = np.zeros(len(centers))
    for cat in cats:
        total += np.array(payload[cat]["asimov_counts"], dtype=float)

    # Analytic components summed over categories, using the fitted shapes.
    sig = np.zeros(len(centers))
    res = np.zeros(len(centers))
    bkg = np.zeros(len(centers))
    width = edges[1] - edges[0]
    for cat in cats:
        sp = result["signal_pdf"][cat]
        rp = result["resonant_pdf"][cat]
        sb = result["sideband_plots"][cat]
        nsig = sp["expected_yield_36fb_full_range"] * result["mu_hat"]
        nres = rp["expected_yield_36fb_full_range"]
        gauss = lambda x, m, s: np.exp(-0.5 * ((x - m) / s) ** 2) / (
            s * np.sqrt(2 * np.pi)
        )
        sig += nsig * gauss(centers, sp["mean"], sp["sigma"]) * width
        res += nres * gauss(centers, rp["mean"], rp["sigma"]) * width
        bkg += np.array(sb["fitted_continuum_curve"], dtype=float)

    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(7.8, 6.2), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    ax.errorbar(
        centers,
        total,
        yerr=np.sqrt(np.clip(total, 0, None)),
        fmt="ko",
        ms=3.5,
        label=f"S+B Asimov data ($\\mu_{{gen}}$ = {result['mu_gen']:.0f})",
    )
    ax.plot(centers, bkg + res + sig, color="#d62728", lw=2.0, label="fitted S+B model")
    ax.plot(centers, bkg + res, color="#1f77b4", lw=1.5, ls="--", label="B (continuum + resonant)")
    ax.plot(centers, bkg, color="#2ca02c", lw=1.2, ls=":", label="continuum only")
    ax.set_ylabel(f"events / {width:.2f} GeV")
    ax.set_title(
        "Combined hadronic Asimov S+B fit  "
        f"($\\hat{{\\mu}}$ = {result['mu_hat']:.3f} $\\pm$ {result['mu_uncertainty']:.3f}, "
        f"$Z_{{exp}}$ = {result['expected_Z']:.3f})"
    )
    ax.legend(fontsize=8)
    model = bkg + res + sig
    axr.plot(centers, total - (bkg + res), color="#d62728", lw=1.6, label="Asimov - B")
    axr.plot(centers, sig, color="k", lw=1.2, ls="--", label="fitted signal")
    axr.axhline(0.0, color="0.5", lw=0.8)
    axr.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]")
    axr.set_ylabel("S")
    axr.legend(fontsize=7)
    fig.tight_layout()
    files = _save(fig, plotdir / "asimov_sb_fit")

    return files, {
        "binning": {
            "edges": edges.tolist(),
            "n_bins": len(centers),
            "low": float(edges[0]),
            "high": float(edges[-1]),
        },
        "summed_over_categories": cats,
        "asimov_total_counts": total.tolist(),
        "fitted_signal": sig.tolist(),
        "fitted_resonant": res.tolist(),
        "fitted_continuum": bkg.tolist(),
        "fitted_total_model": model.tolist(),
        "mu_hat": result["mu_hat"],
        "mu_gen": result["mu_gen"],
        "per_category_asimov": {c: payload[c]["asimov_counts"] for c in cats},
    }
