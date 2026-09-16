"""ROOT/PyROOT/RooFit combined hadronic workspace and Asimov expected significance.

Strategy (identical in spirit to ``tb-hyy``):

* one shared signal-strength parameter ``mu`` multiplying the ``ttH+tH``
  component in every hadronic category;
* per category the expected mass spectrum is
  ``mu*(ttH+tH) + fixed resonant-Higgs background + floating smooth continuum``;
* the smooth continuum is determined **from observed TI data sidebands only**
  (105-120 and 130-160 GeV), then extrapolated with the fitted PDF over the
  full 105-160 GeV fit range;
* signal-plus-background Asimov pseudo-data is generated with ``mu_gen = 1``;
* a free-``mu`` fit and a ``mu = 0`` fit give
  ``q0 = 2*(NLL(0) - NLL(mu_hat))`` and the expected discovery significance
  ``Z = sqrt(q0)``.

Observed TI data in 125 +/- 2 GeV is never read: the observed significance is
blocked unless an explicit unblinding step is added.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

from .top_categorization import CATEGORY_ORDER


def _import_root():
    import ROOT

    ROOT.gROOT.SetBatch(True)
    ROOT.gRandom.SetSeed(20240917)
    ROOT.RooRandom.randomGenerator().SetSeed(20240917)
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    return ROOT


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def _weighted_gauss_moments(
    values: np.ndarray, weights: np.ndarray, lo: float, hi: float
) -> tuple[float, float, float]:
    mask = (values >= lo) & (values <= hi) & np.isfinite(values) & np.isfinite(weights)
    v, w = values[mask], weights[mask]
    if w.sum() <= 0 or len(v) < 2:
        return 125.0, 2.0, float(w.sum() if len(w) else 0.0)
    mean = float(np.average(v, weights=w))
    var = float(np.average((v - mean) ** 2, weights=w))
    sigma = math.sqrt(max(var, 1e-4))
    return mean, sigma, float(w.sum())


def _fit_gauss_to_hist(
    ROOT, mgg, values: np.ndarray, weights: np.ndarray, name: str, nbins: int, lo: float, hi: float
) -> dict[str, Any]:
    """Fit a Gaussian to a weighted m_yy histogram; robust to negative weights."""
    seed_mean, seed_sigma, sumw = _weighted_gauss_moments(values, weights, 118.0, 132.0)
    contents, edges = np.histogram(values, bins=nbins, range=(lo, hi), weights=weights)
    contents = np.clip(contents, 0.0, None)

    th1 = ROOT.TH1D(f"h_{name}", f"h_{name}", nbins, lo, hi)
    for i, c in enumerate(contents):
        th1.SetBinContent(i + 1, float(c))
        th1.SetBinError(i + 1, math.sqrt(max(float(c), 1e-12)))
    dh = ROOT.RooDataHist(f"dh_{name}", f"dh_{name}", ROOT.RooArgList(mgg), th1)

    mean = ROOT.RooRealVar(f"mean_{name}", "mean", seed_mean, 118.0, 132.0)
    sigma = ROOT.RooRealVar(f"sigma_{name}", "sigma", max(seed_sigma, 0.7), 0.5, 8.0)
    pdf = ROOT.RooGaussian(f"pdf_{name}", "gauss", mgg, mean, sigma)
    res = pdf.fitTo(
        dh,
        ROOT.RooFit.Save(True),
        ROOT.RooFit.PrintLevel(-1),
        ROOT.RooFit.SumW2Error(True),
        ROOT.RooFit.Minimizer("Minuit2", "migrad"),
    )
    status = int(res.status()) if res else -1
    cov = int(res.covQual()) if res else -1
    info = {
        "pdf": "RooGaussian",
        "mean": float(mean.getVal()),
        "mean_error": float(mean.getError()),
        "sigma": float(sigma.getVal()),
        "sigma_error": float(sigma.getError()),
        "fit_status": status,
        "cov_quality": cov,
        "seed_mean": seed_mean,
        "seed_sigma": seed_sigma,
        "raw_entries": int(np.isfinite(values).sum()),
        "sum_weights_in_118_132": sumw,
    }
    # freeze the shape
    mean.setConstant(True)
    sigma.setConstant(True)
    return {"pdf": pdf, "params": [mean, sigma], "info": info, "datahist": dh, "th1": th1}


BKG_PDF_CANDIDATES = {
    "exponential": {"n_params": 1, "formula": "exp(a0 * m)"},
    "power_law": {"n_params": 1, "formula": "(m/100)^a0"},
    "expo_poly1": {"n_params": 2, "formula": "exp(a0*m + a1*m*m)"},
    "bernstein2": {"n_params": 2, "formula": "Bernstein order 2"},
}


def _make_bkg_pdf(ROOT, mgg, kind: str, tag: str):
    keep: list[Any] = []
    if kind == "exponential":
        a0 = ROOT.RooRealVar(f"bkg_a0_{tag}", "a0", -0.02, -0.5, 0.2)
        pdf = ROOT.RooExponential(f"bkg_{tag}", "bkg", mgg, a0)
        keep = [a0]
    elif kind == "power_law":
        a0 = ROOT.RooRealVar(f"bkg_p0_{tag}", "p0", -3.0, -20.0, 5.0)
        pdf = ROOT.RooGenericPdf(
            f"bkg_{tag}", "bkg", "pow(@0/100.0, @1)", ROOT.RooArgList(mgg, a0)
        )
        keep = [a0]
    elif kind == "expo_poly1":
        a0 = ROOT.RooRealVar(f"bkg_e0_{tag}", "e0", -0.02, -0.5, 0.2)
        a1 = ROOT.RooRealVar(f"bkg_e1_{tag}", "e1", 0.0, -1e-3, 1e-3)
        pdf = ROOT.RooGenericPdf(
            f"bkg_{tag}", "bkg", "exp(@0*@1 + @0*@0*@2)", ROOT.RooArgList(mgg, a0, a1)
        )
        keep = [a0, a1]
    elif kind == "bernstein2":
        c0 = ROOT.RooRealVar(f"bkg_b0_{tag}", "b0", 0.5, 0.0, 10.0)
        c1 = ROOT.RooRealVar(f"bkg_b1_{tag}", "b1", 0.3, 0.0, 10.0)
        c2 = ROOT.RooRealVar(f"bkg_b2_{tag}", "b2", 0.2, 0.0, 10.0)
        pdf = ROOT.RooBernstein(
            f"bkg_{tag}", "bkg", mgg, ROOT.RooArgList(c0, c1, c2)
        )
        keep = [c0, c1, c2]
    else:  # pragma: no cover
        raise ValueError(f"unknown background pdf {kind}")
    return pdf, keep


def _sideband_dataset(ROOT, mgg, values: np.ndarray, tag: str):
    ds = ROOT.RooDataSet(f"ti_sb_{tag}", "TI sideband data", ROOT.RooArgSet(mgg))
    for v in values:
        mgg.setVal(float(v))
        ds.add(ROOT.RooArgSet(mgg))
    return ds


# --------------------------------------------------------------------------
# main entry point
# --------------------------------------------------------------------------


def build_workspace_and_significance(
    df: pd.DataFrame,
    retention: Mapping[str, Any],
    sf: Mapping[str, Any],
    cfg: Mapping[str, Any],
    outdir: Path,
) -> dict[str, Any]:
    """Build the combined hadronic RooFit workspace and the Asimov expected Z."""
    ROOT = _import_root()

    fit_cfg = cfg["fit"]
    lo, hi = [float(x) for x in fit_cfg["mgg_range_gev"]]
    nbins = int(fit_cfg["n_bins"])
    sb_lo = [float(x) for x in cfg["selection"]["sideband_low_gev"]]
    sb_hi = [float(x) for x in cfg["selection"]["sideband_high_gev"]]

    categories = [c for c in CATEGORY_ORDER if c in retention["kept_categories"]]

    mgg = ROOT.RooRealVar("m_yy", "m_{#gamma#gamma}", lo, hi, "GeV")
    mgg.setBins(nbins)
    mgg.setRange("FULL", lo, hi)
    mgg.setRange("SBLO", sb_lo[0], sb_lo[1])
    mgg.setRange("SBHI", sb_hi[0], sb_hi[1])

    mu = ROOT.RooRealVar("mu", "signal strength", 1.0, -5.0, 20.0)
    normset = ROOT.RooArgSet(mgg)  # persistent: getVal() must not take an r-value

    keep: list[Any] = [mgg, mu]
    cat_index = ROOT.RooCategory("cat", "analysis category")
    pdf_map: dict[str, Any] = {}
    asimov_map: dict[str, Any] = {}
    per_cat: list[dict[str, Any]] = []
    scan_record: dict[str, Any] = {}
    signal_pdf_record: dict[str, Any] = {}
    resonant_pdf_record: dict[str, Any] = {}
    plot_payload: dict[str, Any] = {}
    sideband_plot_record: dict[str, Any] = {}

    # ---------------- inclusive fallback shapes (limited MC statistics) -----
    had = df[df["passes_hadronic_preselection"] & df["category_is_kept"]]
    mc_ti = had[had["is_mc"] & had["photon_ti"]]
    incl_sig = mc_ti[mc_ti["process_role"] == "signal_top"]
    incl_res = mc_ti[mc_ti["process_role"] == "resonant_higgs"]
    incl_sig_fit = _fit_gauss_to_hist(
        ROOT, mgg, incl_sig["m_gammagamma"].to_numpy(float),
        incl_sig["weight_mc_36fb"].to_numpy(float), "sig_inclusive", nbins, lo, hi,
    )
    incl_res_fit = _fit_gauss_to_hist(
        ROOT, mgg, incl_res["m_gammagamma"].to_numpy(float),
        incl_res["weight_mc_36fb"].to_numpy(float), "res_inclusive", nbins, lo, hi,
    )
    keep += [incl_sig_fit, incl_res_fit]
    min_raw = int(fit_cfg["min_raw_entries_for_per_category_shape"])

    for cat in categories:
        tag = cat.replace("+", "").replace("-", "_")
        sub = had[had["category"] == cat]
        sig_rows = sub[sub["is_mc"] & sub["photon_ti"] & (sub["process_role"] == "signal_top")]
        res_rows = sub[sub["is_mc"] & sub["photon_ti"] & (sub["process_role"] == "resonant_higgs")]
        ti_data = sub[sub["is_data"] & sub["photon_ti"]]
        ti_sb = ti_data[ti_data["in_sideband"]]
        sb_values = ti_sb["m_gammagamma"].to_numpy(float)

        n_sig = float(sig_rows["weight_mc_36fb"].sum())
        n_res = float(res_rows["weight_mc_36fb"].sum())

        # ---- signal / resonant shapes ----
        if len(sig_rows) >= min_raw:
            sfit = _fit_gauss_to_hist(
                ROOT, mgg, sig_rows["m_gammagamma"].to_numpy(float),
                sig_rows["weight_mc_36fb"].to_numpy(float), f"sig_{tag}", nbins, lo, hi,
            )
            sig_source = "per-category fit"
        else:
            sfit = incl_sig_fit
            sig_source = "inclusive hadronic fit (insufficient per-category MC statistics)"
        if len(res_rows) >= min_raw:
            rfit = _fit_gauss_to_hist(
                ROOT, mgg, res_rows["m_gammagamma"].to_numpy(float),
                res_rows["weight_mc_36fb"].to_numpy(float), f"res_{tag}", nbins, lo, hi,
            )
            res_source = "per-category fit"
        else:
            rfit = incl_res_fit
            res_source = "inclusive hadronic fit (insufficient per-category MC statistics)"
        keep += [sfit, rfit]
        signal_pdf_record[cat] = {
            **sfit["info"], "source": sig_source,
            "template": "ttH + tH TI MC", "n_raw_mc_rows": int(len(sig_rows)),
            "expected_yield_36fb_full_range": n_sig,
        }
        resonant_pdf_record[cat] = {
            **rfit["info"], "source": res_source,
            "template": "non-top Higgs TI MC (ggH, VBF, WH, ZH, ggZH)",
            "n_raw_mc_rows": int(len(res_rows)),
            "expected_yield_36fb_full_range": n_res,
        }

        # ---- continuum background from observed TI data sidebands only ----
        ds = _sideband_dataset(ROOT, mgg, sb_values, tag)
        keep.append(ds)
        scan_entries: list[dict[str, Any]] = []
        best = None
        for kind in fit_cfg["background_pdf_candidates"]:
            pdf, pars = _make_bkg_pdf(ROOT, mgg, kind, f"{kind}_{tag}")
            keep += [pdf, pars]
            try:
                res = pdf.fitTo(
                    ds, ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1),
                    ROOT.RooFit.Range("SBLO,SBHI"),
                    ROOT.RooFit.Minimizer("Minuit2", "migrad"),
                )
                nll = float(res.minNll()) if res else float("inf")
                status = int(res.status()) if res else -1
                covq = int(res.covQual()) if res else -1
            except Exception as exc:  # pragma: no cover - defensive
                nll, status, covq = float("inf"), -99, -99
                res = None
                scan_entries.append({"pdf": kind, "error": str(exc)})
                continue
            k = BKG_PDF_CANDIDATES[kind]["n_params"]
            aic = 2 * k + 2 * nll if math.isfinite(nll) else float("inf")
            entry = {
                "pdf": kind, "formula": BKG_PDF_CANDIDATES[kind]["formula"],
                "n_params": k, "min_nll": nll if math.isfinite(nll) else None,
                "aic": aic if math.isfinite(aic) else None,
                "fit_status": status, "cov_quality": covq,
                "parameters": {p.GetName(): [float(p.getVal()), float(p.getError())] for p in pars},
            }
            scan_entries.append(entry)
            if math.isfinite(aic) and status == 0 and (best is None or aic < best[0]):
                best = (aic, kind, pdf, pars, entry)
        if best is None:  # fall back to the most robust single-parameter shape
            pdf, pars = _make_bkg_pdf(ROOT, mgg, "exponential", f"fallback_{tag}")
            pdf.fitTo(ds, ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1),
                      ROOT.RooFit.Range("SBLO,SBHI"))
            keep += [pdf, pars]
            best = (float("nan"), "exponential", pdf, pars, {"pdf": "exponential",
                                                             "note": "fallback"})
        aic, kind, bkg_pdf, bkg_pars, best_entry = best
        for p in bkg_pars:
            p.setConstant(False)
        scan_record[cat] = {
            "candidates": scan_entries, "selected": kind, "criterion": "minimum AIC = 2k + 2*NLL",
            "n_ti_sideband_events": int(len(sb_values)),
        }

        # ---- sideband-normalisation extrapolation to the full range ----
        integral_sb = bkg_pdf.createIntegral(
            normset, ROOT.RooFit.NormSet(normset), ROOT.RooFit.Range("SBLO")
        ).getVal() + bkg_pdf.createIntegral(
            normset, ROOT.RooFit.NormSet(normset), ROOT.RooFit.Range("SBHI")
        ).getVal()
        n_sb = float(len(sb_values))
        n_bkg_full = n_sb / integral_sb if integral_sb > 0 else n_sb
        n_bkg = ROOT.RooRealVar(f"nbkg_{tag}", "continuum yield", n_bkg_full,
                                0.0, max(20.0 * max(n_bkg_full, 1.0), 100.0))
        nsig_var = ROOT.RooRealVar(f"nsig_{tag}", "signal yield", n_sig)
        nsig_var.setConstant(True)
        nres_var = ROOT.RooRealVar(f"nres_{tag}", "resonant yield", n_res)
        nres_var.setConstant(True)
        mu_nsig = ROOT.RooProduct(f"mu_nsig_{tag}", "mu*nsig", ROOT.RooArgList(mu, nsig_var))
        model = ROOT.RooAddPdf(
            f"model_{tag}", "model",
            ROOT.RooArgList(sfit["pdf"], rfit["pdf"], bkg_pdf),
            ROOT.RooArgList(mu_nsig, nres_var, n_bkg),
        )
        keep += [n_bkg, nsig_var, nres_var, mu_nsig, model]

        # ---- S+B Asimov with mu_gen = 1 ----
        mu.setVal(float(fit_cfg["mu_gen"]))
        asimov = model.generateBinned(normset, ROOT.RooFit.ExpectedData(True))
        asimov.SetName(f"asimov_{tag}")
        keep.append(asimov)

        cat_index.defineType(cat)
        pdf_map[cat] = model
        asimov_map[cat] = asimov

        # ---- payloads for the plots ----
        edges = np.linspace(lo, hi, nbins + 1)
        centers = 0.5 * (edges[1:] + edges[:-1])
        curve = []
        for c in centers:
            mgg.setVal(float(c))
            curve.append(float(bkg_pdf.getVal(normset)))
        curve_arr = np.array(curve) * n_bkg_full * (hi - lo) / nbins
        sb_counts, _ = np.histogram(sb_values, bins=edges)
        sideband_plot_record[cat] = {
            "binning": {"n_bins": nbins, "low": lo, "high": hi, "edges": edges.tolist()},
            "observed_ti_sideband_counts": sb_counts.tolist(),
            "fitted_continuum_curve": curve_arr.tolist(),
            "n_ti_sideband_events": int(n_sb),
            "fitted_full_range_yield": n_bkg_full,
            "sideband_fraction_of_pdf": float(integral_sb),
            "pdf": kind,
            "blinded_range_gev": list(cfg["blinding"]["blinded_range_gev"]),
        }

        asimov_counts = np.array([asimov.weight(i) for i in range(asimov.numEntries())])
        per_cat.append({
            "category": cat, "n_sig_36fb": n_sig, "n_resonant_36fb": n_res,
            "n_ti_sideband_observed": int(n_sb),
            "n_continuum_full_range_extrapolated": n_bkg_full,
            "background_pdf": kind, "signal_shape_source": sig_source,
            "resonant_shape_source": res_source,
            "asimov_total": float(asimov_counts.sum()),
        })
        plot_payload[cat] = {
            "edges": edges.tolist(),
            "asimov_counts": asimov_counts.tolist(),
        }

    if not categories:
        raise RuntimeError("no retained hadronic categories: cannot build the workspace")

    # ---------------- combined likelihood ----------------
    sim = ROOT.RooSimultaneous("sim_model", "combined hadronic model", cat_index)
    for cat in categories:
        sim.addPdf(pdf_map[cat], cat)
    keep.append(sim)

    nll_list = ROOT.RooArgList()
    nlls = []
    for cat in categories:
        nll = pdf_map[cat].createNLL(asimov_map[cat], ROOT.RooFit.Extended(True))
        nlls.append(nll)
        nll_list.add(nll)
    total_nll = ROOT.RooAddition("nll_total", "combined NLL", nll_list)
    keep += [nlls, total_nll]

    def minimize(label: str) -> dict[str, Any]:
        minim = ROOT.RooMinimizer(total_nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(1)
        minim.setEps(1e-3)
        status = int(minim.minimize("Minuit2", "migrad"))
        hesse_status = int(minim.hesse())
        result = minim.save(f"fit_{label}", f"fit_{label}")
        return {
            "label": label, "migrad_status": status, "hesse_status": hesse_status,
            "fit_status": int(result.status()), "cov_quality": int(result.covQual()),
            "min_nll": float(result.minNll()), "edm": float(result.edm()),
            "_result": result,
        }

    mu.setVal(1.0)
    mu.setConstant(False)
    free_fit = minimize("free_mu")
    mu_hat = float(mu.getVal())
    mu_err = float(mu.getError())

    mu.setVal(0.0)
    mu.setConstant(True)
    cond_fit = minimize("mu0")
    mu.setConstant(False)
    mu.setVal(mu_hat)

    q0 = 2.0 * (cond_fit["min_nll"] - free_fit["min_nll"])
    if mu_hat < 0:
        q0 = 0.0
    q0 = max(q0, 0.0)
    z_exp = math.sqrt(q0)

    # ---------------- workspace persistence ----------------
    ws = ROOT.RooWorkspace("tth_hyy_hadronic", "combined hadronic H->yy workspace")
    getattr(ws, "import")(sim, ROOT.RooFit.RecycleConflictNodes())
    combined_ok = True
    try:
        imports = [ROOT.RooFit.Import(cat, asimov_map[cat]) for cat in categories]
        combined = ROOT.RooDataHist(
            "asimov_combined", "combined S+B Asimov (mu_gen=1)",
            ROOT.RooArgList(mgg), ROOT.RooFit.Index(cat_index), *imports,
        )
        getattr(ws, "import")(combined)
        keep.append(combined)
    except Exception:  # pragma: no cover - defensive
        combined_ok = False
    for cat in categories:
        try:
            getattr(ws, "import")(asimov_map[cat])
        except Exception:  # pragma: no cover
            pass
    ws_path = outdir / "workspace.root"
    ws.writeToFile(str(ws_path))

    hs3_path = None
    try:
        tool = ROOT.RooJSONFactoryWSTool(ws)
        hs3_path = outdir.parent / "workspace.json"
        tool.exportJSON(str(hs3_path))
        hs3_ok = True
    except Exception as exc:  # pragma: no cover
        hs3_ok = False
        hs3_error = str(exc)
    else:
        hs3_error = None

    return {
        "categories": categories,
        "per_category": per_cat,
        "mu_hat": mu_hat,
        "mu_uncertainty": mu_err,
        "free_fit": {k: v for k, v in free_fit.items() if k != "_result"},
        "conditional_fit": {k: v for k, v in cond_fit.items() if k != "_result"},
        "q0": q0,
        "expected_Z": z_exp,
        "mu_gen": float(fit_cfg["mu_gen"]),
        "workspace_path": str(ws_path),
        "combined_asimov_dataset": combined_ok,
        "hs3_export_ok": hs3_ok,
        "hs3_export_error": hs3_error,
        "hs3_path": str(hs3_path) if hs3_ok and hs3_path else None,
        "background_pdf_scan": scan_record,
        "signal_pdf": signal_pdf_record,
        "resonant_pdf": resonant_pdf_record,
        "sideband_plots": sideband_plot_record,
        "asimov_plot_payload": plot_payload,
        "binning": {"n_bins": nbins, "low": lo, "high": hi},
        "mgg_range": [lo, hi],
        "sidebands": [sb_lo, sb_hi],
    }
