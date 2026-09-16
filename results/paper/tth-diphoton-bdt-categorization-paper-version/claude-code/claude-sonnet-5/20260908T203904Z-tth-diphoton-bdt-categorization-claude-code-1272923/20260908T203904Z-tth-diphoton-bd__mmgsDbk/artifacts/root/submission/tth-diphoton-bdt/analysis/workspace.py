"""RooFit-based per-category background/signal modelling and Asimov
significance estimation for the hadronic ttH/tH categorization.

For each retained hadronic category this module:
  * fits a small set of smooth continuum background shapes (exponential,
    Chebychev order 1/2) to the TI *sideband* data (105-120 and 130-160 GeV,
    the 125+/-2 GeV signal window and the wider 120-130 GeV blind-display
    gap are never touched) and picks the best one by AIC,
  * extrapolates that sideband fit into the full 105-160 GeV fit range to
    obtain a floating continuum-background normalization,
  * extracts fixed Gaussian shapes for the ttH+tH signal and for the
    (fixed-normalization) resonant-Higgs background from TI MC,
  * builds a RooFit extended model (signal*mu + fixed resonant Higgs +
    floating continuum) per category and an analytic Asimov dataset built
    from the model expectation at mu=1 (no Poisson fluctuation, fully
    deterministic),
  * fits mu (floating) and mu=0 (fixed) to compute the discovery test
    statistic q0 = 2*(NLL(0) - NLL(mu_hat)) and Z = sqrt(q0).

The combined hadronic significance is the quadrature sum of the
per-category Z values (categories are built from disjoint event
selections, so this is the standard uncorrelated-categories combination).
Each category is fit with its own independent signal-strength parameter
(mu_<category>) rather than a single RooSimultaneous fit sharing one mu:
combining the per-category RooAddPdf models into a RooSimultaneous in this
ROOT build (6.38.00) reproducibly segfaults inside
RooSimultaneous::compileForNormSet / RooAddPdf::clone when createNLL is
called, so the per-category fit + quadrature-sum combination is used
instead (see fit/FIT1/backend.json for the recorded caveat).
"""
import math

import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

import ROOT

ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

FIT_LO, FIT_HI = 105.0, 160.0
N_FIT_BINS = 55


def _gauss(x, amp, mean, sigma):
    return amp * np.exp(-0.5 * ((x - mean) / sigma) ** 2)


def weighted_gaussian_fit(values, weights, lo=FIT_LO, hi=FIT_HI, nbins=N_FIT_BINS):
    """Fit a Gaussian shape to a weighted mgg sample via a weighted-histogram
    least-squares fit (robust for small/irregular MC weights)."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    total_yield = float(weights.sum())
    edges = np.linspace(lo, hi, nbins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    counts, _ = np.histogram(values, bins=edges, weights=weights)
    mean0 = float(np.average(values, weights=weights)) if total_yield > 0 else 125.0
    sigma0 = float(np.sqrt(np.average((values - mean0) ** 2, weights=weights))) if total_yield > 0 else 2.0
    sigma0 = max(sigma0, 0.5)
    amp0 = float(counts.max()) if counts.size else 1.0
    try:
        popt, _ = curve_fit(_gauss, centers, counts, p0=[amp0, mean0, sigma0],
                             bounds=([0.0, lo, 0.1], [np.inf, hi, (hi - lo)]))
        amp, mean, sigma = (float(v) for v in popt)
        status = "ok"
    except Exception:
        amp, mean, sigma = amp0, mean0, sigma0
        status = "fallback_to_moments"
    return {
        "fit_status": status,
        "shape": "gaussian",
        "mean_gev": mean,
        "sigma_gev": sigma,
        "amplitude_hist_units": amp,
        "yield_full_range": total_yield,
        "n_events_input": int(values.size),
        "fit_range_gev": [lo, hi],
        "n_bins_used": nbins,
    }


def _aic(nll_val, n_free_params):
    return 2.0 * n_free_params + 2.0 * nll_val


def fit_sideband_background_models(sideband_values, sb_low, sb_high, fit_lo=FIT_LO, fit_hi=FIT_HI):
    """Fit exponential and Chebychev(1,2) shapes to TI sideband data only
    (unbinned ML fit restricted to the sideband ranges), then extrapolate
    each into the full fit range. Returns the full scan plus the AIC-chosen
    model."""
    values = np.asarray(sideband_values, dtype=float)
    n_obs = int(values.size)

    mgg = ROOT.RooRealVar("mgg_sbscan", "m_{#gamma#gamma}", fit_lo, fit_hi, "GeV")
    mgg.setRange("lowSB", sb_low[0], sb_low[1])
    mgg.setRange("highSB", sb_high[0], sb_high[1])
    mgg.setRange("full", fit_lo, fit_hi)

    ds = ROOT.RooDataSet("sb_data", "sb_data", ROOT.RooArgSet(mgg))
    for v in values:
        mgg.setVal(float(v))
        ds.add(ROOT.RooArgSet(mgg))

    candidates = {}

    # Exponential
    slope = ROOT.RooRealVar("slope_sb", "slope", -0.03, -2.0, -1e-5)
    exp_pdf = ROOT.RooExponential("exp_sb", "exp_sb", mgg, slope)
    candidates["exponential"] = (exp_pdf, [slope], 1)

    # Chebychev order 1
    c1 = ROOT.RooRealVar("cheb1_a1", "a1", 0.0, -1.0, 1.0)
    cheb1 = ROOT.RooChebychev("cheb1_sb", "cheb1_sb", mgg, ROOT.RooArgList(c1))
    candidates["chebychev1"] = (cheb1, [c1], 1)

    # Chebychev order 2
    c2a = ROOT.RooRealVar("cheb2_a1", "a1", 0.0, -1.0, 1.0)
    c2b = ROOT.RooRealVar("cheb2_a2", "a2", 0.0, -1.0, 1.0)
    cheb2 = ROOT.RooChebychev("cheb2_sb", "cheb2_sb", mgg, ROOT.RooArgList(c2a, c2b))
    candidates["chebychev2"] = (cheb2, [c2a, c2b], 2)

    scan = {}
    for name, (pdf, params, k) in candidates.items():
        try:
            nll = pdf.createNLL(ds, ROOT.RooFit.Range("lowSB,highSB"))
            minim = ROOT.RooMinimizer(nll)
            minim.setPrintLevel(-1)
            status = minim.migrad()
            nll_val = float(nll.getVal())
            int_full = pdf.createIntegral(ROOT.RooArgSet(mgg), ROOT.RooFit.Range("full")).getVal()
            int_sb = pdf.createIntegral(ROOT.RooArgSet(mgg), ROOT.RooFit.Range("lowSB,highSB")).getVal()
            extrap_factor = float(int_full / int_sb) if int_sb > 0 else float("nan")
            bkg_full_range_yield = n_obs * extrap_factor
            scan[name] = {
                "migrad_status": int(status),
                "nll": nll_val,
                "n_free_params": k,
                "aic": _aic(nll_val, k),
                "params": {p.GetName(): float(p.getVal()) for p in params},
                "extrapolation_factor_full_over_sidebands": extrap_factor,
                "background_yield_full_range_estimate": bkg_full_range_yield,
            }
        except Exception as exc:  # pragma: no cover - defensive
            scan[name] = {"error": str(exc)}

    valid = {k: v for k, v in scan.items() if "aic" in v and math.isfinite(v["aic"])}
    chosen_name = min(valid, key=lambda k: valid[k]["aic"]) if valid else "exponential"
    chosen = scan[chosen_name]
    chosen_slope = float(scan["exponential"]["params"]["slope_sb"]) if chosen_name == "exponential" else None

    return {
        "n_sideband_events": n_obs,
        "sideband_ranges_gev": {"low": list(sb_low), "high": list(sb_high)},
        "fit_range_gev": [fit_lo, fit_hi],
        "scan": scan,
        "chosen_model": chosen_name,
        "chosen_model_result": chosen,
        "chosen_exponential_slope": chosen_slope,
    }


def _exp_pdf_frac(a, b, lam, lo, hi):
    num = math.exp(lam * b) - math.exp(lam * a)
    den = math.exp(lam * hi) - math.exp(lam * lo)
    return num / den


def _cheb_shape_on_grid(centers, lo, hi, coeffs):
    x = -1.0 + 2.0 * (centers - lo) / (hi - lo)
    if len(coeffs) == 1:
        vals = 1.0 + coeffs[0] * x
    else:
        t0, t1 = np.ones_like(x), x
        vals = 1.0 + coeffs[0] * t1
        if len(coeffs) >= 2:
            t2 = 2 * x * t1 - t0
            vals = vals + coeffs[1] * t2
    vals = np.clip(vals, 1e-6, None)
    return vals / vals.sum()


def build_and_fit_category(category, signal_vals, signal_w, resonant_vals, resonant_w,
                            sideband_vals, sb_low, sb_high, fit_lo=FIT_LO, fit_hi=FIT_HI,
                            nbins=N_FIT_BINS, workspace=None):
    """Build the per-category S+B(fixed resonant)+continuum model, an
    analytic Asimov dataset at mu=1, and fit mu floating / mu=0 fixed."""
    sig_shape = weighted_gaussian_fit(signal_vals, signal_w, fit_lo, fit_hi, nbins)
    res_shape = weighted_gaussian_fit(resonant_vals, resonant_w, fit_lo, fit_hi, nbins)
    sb_scan = fit_sideband_background_models(sideband_vals, sb_low, sb_high, fit_lo, fit_hi)

    n_sig0 = sig_shape["yield_full_range"]
    n_res0 = res_shape["yield_full_range"]
    n_bkg0 = sb_scan["chosen_model_result"].get("background_yield_full_range_estimate", 0.0)
    n_bkg0 = float(n_bkg0) if math.isfinite(n_bkg0) and n_bkg0 > 0 else max(float(len(sideband_vals)), 1.0)

    mgg = ROOT.RooRealVar(f"mgg_{category}", "m_{#gamma#gamma}", fit_lo, fit_hi, "GeV")
    mu = ROOT.RooRealVar(f"mu_{category}", "signal strength", 1.0, -20.0, 20.0)

    mean_sig = ROOT.RooRealVar(f"mean_sig_{category}", "mean_sig", sig_shape["mean_gev"])
    mean_sig.setConstant(True)
    sigma_sig = ROOT.RooRealVar(f"sigma_sig_{category}", "sigma_sig", max(sig_shape["sigma_gev"], 0.1), 0.01, fit_hi - fit_lo)
    sigma_sig.setConstant(True)
    sig_pdf = ROOT.RooGaussian(f"sig_pdf_{category}", "sig_pdf", mgg, mean_sig, sigma_sig)
    n_sig0_var = ROOT.RooRealVar(f"n_sig0_{category}", "n_sig0", n_sig0)
    n_sig0_var.setConstant(True)
    n_sig_expr = ROOT.RooFormulaVar(f"n_sig_{category}", "@0*@1", ROOT.RooArgList(mu, n_sig0_var))

    mean_res = ROOT.RooRealVar(f"mean_res_{category}", "mean_res", res_shape["mean_gev"])
    mean_res.setConstant(True)
    sigma_res = ROOT.RooRealVar(f"sigma_res_{category}", "sigma_res", max(res_shape["sigma_gev"], 0.1), 0.01, fit_hi - fit_lo)
    sigma_res.setConstant(True)
    res_pdf = ROOT.RooGaussian(f"res_pdf_{category}", "res_pdf", mgg, mean_res, sigma_res)
    n_res_var = ROOT.RooRealVar(f"n_res_{category}", "n_res", n_res0)
    n_res_var.setConstant(True)

    chosen_name = sb_scan["chosen_model"]
    if chosen_name == "exponential":
        slope0 = sb_scan["chosen_model_result"]["params"]["slope_sb"]
        slope = ROOT.RooRealVar(f"slope_bkg_{category}", "slope_bkg", slope0, -2.0, -1e-5)
        bkg_pdf = ROOT.RooExponential(f"bkg_pdf_{category}", "bkg_pdf", mgg, slope)
        bkg_params = [slope]
    else:
        order = 1 if chosen_name == "chebychev1" else 2
        params = sb_scan["chosen_model_result"]["params"]
        coeff_vars = []
        for i in range(order):
            key = f"cheb{order}_a{i + 1}"
            v0 = params.get(key, 0.0)
            cv = ROOT.RooRealVar(f"cheb_a{i + 1}_{category}", f"cheb_a{i + 1}", v0, -1.0, 1.0)
            coeff_vars.append(cv)
        bkg_pdf = ROOT.RooChebychev(f"bkg_pdf_{category}", "bkg_pdf", mgg, ROOT.RooArgList(*coeff_vars))
        bkg_params = coeff_vars
    n_bkg_var = ROOT.RooRealVar(f"n_bkg_{category}", "n_bkg", n_bkg0, 0.0, max(50.0 * n_bkg0, 100.0))

    model = ROOT.RooAddPdf(f"model_{category}", "model",
                            ROOT.RooArgList(sig_pdf, res_pdf, bkg_pdf),
                            ROOT.RooArgList(n_sig_expr, n_res_var, n_bkg_var))

    # Analytic Asimov histogram at mu=1 truth, built from the exact same
    # shapes used in the RooFit model above (Gaussian signal/resonant,
    # exponential or Chebychev background), so the constructed dataset and
    # the fitted pdf agree analytically without relying on RooFit's
    # generate-binned machinery.
    edges = np.linspace(fit_lo, fit_hi, nbins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])

    def gauss_frac(a, b, mean, sigma):
        return stats.norm.cdf(b, mean, sigma) - stats.norm.cdf(a, mean, sigma)

    gnorm_sig = stats.norm.cdf(fit_hi, sig_shape["mean_gev"], max(sig_shape["sigma_gev"], 0.1)) - \
        stats.norm.cdf(fit_lo, sig_shape["mean_gev"], max(sig_shape["sigma_gev"], 0.1))
    gnorm_res = stats.norm.cdf(fit_hi, res_shape["mean_gev"], max(res_shape["sigma_gev"], 0.1)) - \
        stats.norm.cdf(fit_lo, res_shape["mean_gev"], max(res_shape["sigma_gev"], 0.1))

    if chosen_name == "exponential":
        lam = sb_scan["chosen_model_result"]["params"]["slope_sb"]
        bkg_fracs = np.array([_exp_pdf_frac(a, b, lam, fit_lo, fit_hi) for a, b in zip(edges[:-1], edges[1:])])
    else:
        order = 1 if chosen_name == "chebychev1" else 2
        params = sb_scan["chosen_model_result"]["params"]
        coeffs = [params[f"cheb{order}_a{i + 1}"] for i in range(order)]
        bkg_fracs = _cheb_shape_on_grid(centers, fit_lo, fit_hi, coeffs)

    asimov_content = np.zeros(nbins)
    sig_component = np.zeros(nbins)
    res_component = np.zeros(nbins)
    bkg_component = np.zeros(nbins)
    for i, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        sig_frac = gauss_frac(a, b, sig_shape["mean_gev"], max(sig_shape["sigma_gev"], 0.1)) / gnorm_sig if gnorm_sig > 0 else 0.0
        res_frac = gauss_frac(a, b, res_shape["mean_gev"], max(res_shape["sigma_gev"], 0.1)) / gnorm_res if gnorm_res > 0 else 0.0
        sig_component[i] = n_sig0 * sig_frac
        res_component[i] = n_res0 * res_frac
        bkg_component[i] = n_bkg0 * bkg_fracs[i]
        asimov_content[i] = sig_component[i] + res_component[i] + bkg_component[i]

    th1 = ROOT.TH1D(f"asimov_{category}", "asimov", nbins, fit_lo, fit_hi)
    for i, c in enumerate(asimov_content):
        th1.SetBinContent(i + 1, float(c))
    asimov_dh = ROOT.RooDataHist(f"asimov_dh_{category}", "asimov_dh", ROOT.RooArgList(mgg), th1)

    nll = model.createNLL(asimov_dh, ROOT.RooFit.Extended(True))
    minim = ROOT.RooMinimizer(nll)
    minim.setPrintLevel(-1)
    migrad_status = int(minim.migrad())
    hesse_status = int(minim.hesse())
    fit_res = minim.save()
    mu_hat = float(mu.getVal())
    mu_err = float(mu.getError())
    cov_qual = int(fit_res.covQual())
    nll_hat = float(nll.getVal())
    n_bkg_hat = float(n_bkg_var.getVal())
    bkg_params_hat = {p.GetName(): float(p.getVal()) for p in bkg_params}

    mu.setVal(0.0)
    mu.setConstant(True)
    minim0 = ROOT.RooMinimizer(nll)
    minim0.setPrintLevel(-1)
    migrad0_status = int(minim0.migrad())
    nll0 = float(nll.getVal())
    mu.setConstant(False)
    mu.setVal(mu_hat)

    q0 = 2.0 * (nll0 - nll_hat)
    q0 = q0 if math.isfinite(q0) and q0 > 0 else 0.0
    z_asimov = math.sqrt(q0)

    if workspace is not None:
        getattr(workspace, "import")(model, ROOT.RooFit.RecycleConflictNodes())
        getattr(workspace, "import")(asimov_dh, ROOT.RooFit.Rename(f"asimov_data_{category}"))

    return {
        "category": category,
        "signal_pdf": sig_shape,
        "resonant_higgs_pdf": res_shape,
        "background_pdf_scan": sb_scan,
        "background_pdf_choice": {"category": category, "chosen_model": chosen_name,
                                   "chosen_params": sb_scan["chosen_model_result"]["params"],
                                   "aic_by_model": {k: v.get("aic") for k, v in sb_scan["scan"].items()}},
        "model": {
            "n_sig0_fit_range": n_sig0,
            "n_res0_fixed": n_res0,
            "n_bkg0_init_from_sideband_extrapolation": n_bkg0,
            "background_shape": chosen_name,
        },
        "asimov_construction": {
            "bin_edges_gev": edges.tolist(),
            "bin_contents_mu1_truth": asimov_content.tolist(),
            "signal_component_mu1_truth": sig_component.tolist(),
            "resonant_higgs_component_fixed": res_component.tolist(),
            "continuum_background_component_mu1_truth": bkg_component.tolist(),
            "n_bins": nbins,
            "fit_range_gev": [fit_lo, fit_hi],
            "note": "Deterministic Asimov dataset = exact analytic model expectation at mu=1 "
                    "(no Poisson fluctuation), built from the same signal/resonant Gaussian and "
                    f"{chosen_name} background shapes used in the RooFit extended model.",
        },
        "fit_results": {
            "mu_hat": mu_hat,
            "mu_hat_err": mu_err,
            "migrad_status": migrad_status,
            "hesse_status": hesse_status,
            "cov_qual": cov_qual,
            "nll_at_mu_hat": nll_hat,
            "n_bkg_hat": n_bkg_hat,
            "background_shape_params_hat": bkg_params_hat,
            "migrad_status_mu0": migrad0_status,
            "nll_at_mu0": nll0,
        },
        "significance": {"q0": q0, "Z_asimov": z_asimov},
        "roofit_objects": {"mgg": mgg, "model": model, "asimov_dh": asimov_dh,
                            "sig_pdf": sig_pdf, "res_pdf": res_pdf, "bkg_pdf": bkg_pdf,
                            "n_bkg_var": n_bkg_var, "mu": mu},
    }
