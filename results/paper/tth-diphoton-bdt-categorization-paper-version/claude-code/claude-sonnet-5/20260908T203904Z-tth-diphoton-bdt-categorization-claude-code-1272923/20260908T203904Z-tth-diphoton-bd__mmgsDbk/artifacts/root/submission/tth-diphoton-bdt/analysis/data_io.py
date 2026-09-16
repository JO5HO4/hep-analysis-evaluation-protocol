"""ROOT input loading and object/event selection for tth-diphoton-bdt.

Reads the ATLAS open-data GamGam ROOT directory (MC/ and data/), builds
per-event flat rows implementing the object definitions and preselection
described in the task spec, and returns pandas DataFrames plus cutflow
bookkeeping. No ROOT inputs are copied anywhere; only derived tables are
written to the results directory.
"""
import math
import os

import awkward as ak
import numpy as np
import pandas as pd
import uproot

PHOTON_PT_MIN = 25.0
PHOTON_ETA_MAX = 2.37
PHOTON_CRACK_LO = 1.37
PHOTON_CRACK_HI = 1.52
LEPTON_PT_MIN = 10.0
JET_PT_MIN = 25.0
CENTRAL_JET_ETA_MAX = 2.5
BTAG_QUANTILE_MIN = 4
MASS_WINDOW_LO = 123.0
MASS_WINDOW_HI = 127.0
SIDEBAND_LOW = (105.0, 120.0)
SIDEBAND_HIGH = (130.0, 160.0)

# Nominal Higgs -> gamma gamma signal MC only. Sherpa yy / continuum MC
# is deliberately absent from this map -- any file not listed here is
# rejected by load_all() rather than silently processed.
MC_PROCESS_FILES = {
    "ggH": "ggH_preselection.root",
    "VBF": "VBF_preselection.root",
    "WH": "WH_preselection.root",
    "ZH": "ZH_preselection.root",
    "ggZH": "ggZH_preselection.root",
    "ttH": "ttH_preselection.root",
    "tH": "tH_preselection.root",
}
DATA_FILE = "data_preselection.root"

SIGNAL_PROCESSES = {"ttH", "tH"}
RESONANT_HIGGS_PROCESSES = {"ggH", "VBF", "WH", "ZH", "ggZH"}

MC_BRANCHES = [
    "eventNumber", "runNumber", "channelNumber", "mcWeight", "xsec", "filteff",
    "kfac", "sum_of_weights",
    "ScaleFactor_PILEUP", "ScaleFactor_PHOTON", "ScaleFactor_FTAG",
    "ScaleFactor_ELE", "ScaleFactor_MUON", "ScaleFactor_LepTRIGGER",
    "ScaleFactor_JVT",
    "photon_pt", "photon_eta", "photon_phi", "photon_e",
    "photon_isTightID", "photon_isTightIso",
    "lep_pt", "lep_eta", "lep_phi", "lep_e", "lep_type",
    "jet_pt", "jet_eta", "jet_phi", "jet_e", "jet_btag_quantile",
]
DATA_BRANCHES = [b for b in MC_BRANCHES if b not in (
    "mcWeight", "xsec", "filteff", "kfac", "sum_of_weights",
)] + ["eventNumber", "runNumber"]

SM_WEIGHT_SCALE_FACTOR_BRANCHES = [
    "ScaleFactor_PILEUP", "ScaleFactor_PHOTON", "ScaleFactor_FTAG",
    "ScaleFactor_ELE", "ScaleFactor_MUON", "ScaleFactor_LepTRIGGER",
    "ScaleFactor_JVT",
]


def _photon_kinematic_mask(pt, eta):
    abs_eta = np.abs(eta)
    in_crack = (abs_eta >= PHOTON_CRACK_LO) & (abs_eta <= PHOTON_CRACK_HI)
    return (pt > PHOTON_PT_MIN) & (abs_eta < PHOTON_ETA_MAX) & (~in_crack)


def _leading_two(mask, *fields):
    """Return leading-two-by-pt values (pt is fields[0]) for entries where
    mask is True, padded with NaN when fewer than two pass, as numpy arrays
    of shape (n_events, 2) per field, plus a bool array n_pass>=2."""
    pt = fields[0]
    pt_masked = ak.mask(pt, mask)
    order = ak.argsort(pt_masked, ascending=False)
    n_pass = ak.sum(mask, axis=1)
    out = []
    for f in fields:
        f_masked = ak.mask(f, mask)
        f_sorted = f_masked[order]
        f_pad = ak.pad_none(f_sorted, 2, axis=1)
        f_np = ak.to_numpy(ak.fill_none(f_pad[:, :2], np.nan))
        out.append(f_np)
    return np.asarray(ak.to_numpy(n_pass)), out


def _invariant_mass_pair(pt, eta, phi, e):
    px = pt[:, 0] * np.cos(phi[:, 0]) + pt[:, 1] * np.cos(phi[:, 1])
    py = pt[:, 0] * np.sin(phi[:, 0]) + pt[:, 1] * np.sin(phi[:, 1])
    pz = pt[:, 0] * np.sinh(eta[:, 0]) + pt[:, 1] * np.sinh(eta[:, 1])
    en = e[:, 0] + e[:, 1]
    m2 = en ** 2 - (px ** 2 + py ** 2 + pz ** 2)
    m = np.sqrt(np.clip(m2, 0.0, None))
    m[~np.isfinite(m2)] = np.nan
    return m


def build_events(tree_arrays, process, is_data, max_rows=None):
    """Vectorized object selection + preselection for one input file.

    Returns (df, cutflow) where df has one row per event passing photon
    kinematic acceptance with >=2 qualifying photons, and cutflow is a
    dict of named-stage -> (raw_count, weighted_yield).
    """
    a = tree_arrays
    n_events_total = len(a["photon_pt"])

    photon_mask = _photon_kinematic_mask(a["photon_pt"], a["photon_eta"])
    n_photon_pass, (pt2, eta2, phi2, e2, tid2, tiso2) = _leading_two(
        photon_mask, a["photon_pt"], a["photon_eta"], a["photon_phi"], a["photon_e"],
        ak.values_astype(a["photon_isTightID"], np.float64),
        ak.values_astype(a["photon_isTightIso"], np.float64),
    )
    has_diphoton = n_photon_pass >= 2
    mgg = np.full(n_events_total, np.nan)
    valid = has_diphoton & np.all(np.isfinite(pt2), axis=1)
    mgg[valid] = _invariant_mass_pair(pt2[valid], eta2[valid], phi2[valid], e2[valid])

    both_tight = (tid2[:, 0] > 0.5) & (tiso2[:, 0] > 0.5) & (tid2[:, 1] > 0.5) & (tiso2[:, 1] > 0.5)
    diphoton_class = np.where(~has_diphoton, "none", np.where(both_tight, "TI", "NTI"))

    lep_mask = a["lep_pt"] > LEPTON_PT_MIN
    n_leptons = np.asarray(ak.to_numpy(ak.sum(lep_mask, axis=1)))

    jet_mask = a["jet_pt"] > JET_PT_MIN
    jet_central_mask = jet_mask & (np.abs(a["jet_eta"]) <= CENTRAL_JET_ETA_MAX)
    jet_forward_mask = jet_mask & (np.abs(a["jet_eta"]) > CENTRAL_JET_ETA_MAX)
    btag_mask = jet_mask & (a["jet_btag_quantile"] >= BTAG_QUANTILE_MIN)

    n_jets = np.asarray(ak.to_numpy(ak.sum(jet_mask, axis=1)))
    n_jets_central = np.asarray(ak.to_numpy(ak.sum(jet_central_mask, axis=1)))
    n_jets_forward = np.asarray(ak.to_numpy(ak.sum(jet_forward_mask, axis=1)))
    n_bjets = np.asarray(ak.to_numpy(ak.sum(btag_mask, axis=1)))

    jet_pt_masked = ak.mask(a["jet_pt"], jet_central_mask)
    jet_ht = np.asarray(ak.to_numpy(ak.fill_none(ak.sum(jet_pt_masked, axis=1), 0.0)))
    order = ak.argsort(jet_pt_masked, ascending=False)
    jet_pt_sorted = ak.fill_none(jet_pt_masked[order], np.nan)
    jet_eta_sorted = ak.fill_none(ak.mask(a["jet_eta"], jet_central_mask)[order], np.nan)
    jet_phi_sorted = ak.fill_none(ak.mask(a["jet_phi"], jet_central_mask)[order], np.nan)
    jet_e_sorted = ak.fill_none(ak.mask(a["jet_e"], jet_central_mask)[order], np.nan)
    jet2 = ak.pad_none(jet_pt_sorted, 2, axis=1)
    jet2_eta = ak.pad_none(jet_eta_sorted, 2, axis=1)
    jet2_phi = ak.pad_none(jet_phi_sorted, 2, axis=1)
    jet2_e = ak.pad_none(jet_e_sorted, 2, axis=1)
    lead_pt = ak.to_numpy(ak.fill_none(jet2[:, 0], np.nan))
    j0pt = ak.to_numpy(ak.fill_none(jet2[:, 0], np.nan))
    j1pt = ak.to_numpy(ak.fill_none(jet2[:, 1], np.nan))
    j0eta = ak.to_numpy(ak.fill_none(jet2_eta[:, 0], np.nan))
    j1eta = ak.to_numpy(ak.fill_none(jet2_eta[:, 1], np.nan))
    j0phi = ak.to_numpy(ak.fill_none(jet2_phi[:, 0], np.nan))
    j1phi = ak.to_numpy(ak.fill_none(jet2_phi[:, 1], np.nan))
    j0e = ak.to_numpy(ak.fill_none(jet2_e[:, 0], np.nan))
    j1e = ak.to_numpy(ak.fill_none(jet2_e[:, 1], np.nan))
    have2 = np.isfinite(j0pt) & np.isfinite(j1pt)
    dijet_mass = np.full(n_events_total, np.nan)
    dijet_mass[have2] = _invariant_mass_pair(
        np.stack([j0pt, j1pt], axis=1)[have2],
        np.stack([j0eta, j1eta], axis=1)[have2],
        np.stack([j0phi, j1phi], axis=1)[have2],
        np.stack([j0e, j1e], axis=1)[have2],
    )

    is_hadronic = (n_leptons == 0) & (n_jets >= 3) & (n_bjets >= 1)
    is_leptonic = (n_leptons >= 1) & (n_bjets >= 1)
    channel = np.where(is_hadronic, "hadronic", np.where(is_leptonic, "leptonic", "none"))

    if is_data:
        weight_sm = np.ones(n_events_total)
        mc_weight_per_fb = np.full(n_events_total, np.nan)
    else:
        sf_total = np.ones(n_events_total)
        for b in SM_WEIGHT_SCALE_FACTOR_BRANCHES:
            sf_total = sf_total * np.asarray(a[b])
        xsec_fb = np.asarray(a["xsec"]) * 1000.0
        gen_weight = np.asarray(a["mcWeight"])
        sum_weights = np.asarray(a["sum_of_weights"])
        mc_weight_per_fb = (
            xsec_fb * np.asarray(a["filteff"]) * np.asarray(a["kfac"])
            * (gen_weight / sum_weights) * sf_total
        )
        weight_sm = mc_weight_per_fb

    event_number = np.asarray(a["eventNumber"])
    run_number = np.asarray(a["runNumber"])
    event_id = np.array([f"{process}_{r}_{e}" for r, e in zip(run_number, event_number)])

    df = pd.DataFrame({
        "event_id": event_id,
        "eventNumber": event_number,
        "runNumber": run_number,
        "process": process,
        "is_data": is_data,
        "is_signal_class": process in SIGNAL_PROCESSES,
        "is_resonant_higgs_class": process in RESONANT_HIGGS_PROCESSES,
        "n_photon_pass_kinematic": n_photon_pass,
        "has_diphoton_candidate": has_diphoton,
        "m_gammagamma": mgg,
        "diphoton_class": diphoton_class,
        "photon_lead_tightID": tid2[:, 0] > 0.5,
        "photon_lead_tightIso": tiso2[:, 0] > 0.5,
        "photon_sublead_tightID": tid2[:, 1] > 0.5,
        "photon_sublead_tightIso": tiso2[:, 1] > 0.5,
        "n_leptons": n_leptons,
        "n_jets": n_jets,
        "n_jets_central": n_jets_central,
        "n_jets_forward": n_jets_forward,
        "n_bjets": n_bjets,
        "jet_ht": jet_ht,
        "leading_jet_pt": lead_pt,
        "dijet_mass_leading": dijet_mass,
        "channel": channel,
        "raw_weight": np.ones(n_events_total),
        "mc_weight_per_fb": mc_weight_per_fb,
        "event_weight": weight_sm,
    })

    cutflow = {
        "n_input_rows": n_events_total,
        "n_photon_kinematic_diphoton": int(np.sum(has_diphoton)),
        "n_lepton_pt10_ge1": int(np.sum(n_leptons >= 1)),
        "n_jet_pt25_ge3": int(np.sum(n_jets >= 3)),
        "n_bjet_ge1": int(np.sum(n_bjets >= 1)),
        "n_hadronic_channel": int(np.sum(is_hadronic)),
        "n_leptonic_channel_bookkeeping": int(np.sum(is_leptonic)),
    }

    df = df[df["has_diphoton_candidate"]].copy()
    df = df[df["channel"].isin(["hadronic", "leptonic"])].copy()

    if max_rows is not None and len(df) > max_rows:
        df = df.sort_values("event_id").head(max_rows).copy()

    return df, cutflow


def load_one_file(path, process, is_data, max_rows=None):
    branches = DATA_BRANCHES if is_data else MC_BRANCHES
    with uproot.open(path) as f:
        tree = f["analysis"]
        arrays = tree.arrays(branches, library="ak")
    df, cutflow = build_events(arrays, process, is_data, max_rows=max_rows)
    return df, cutflow


def load_all(inputs_dir, max_rows_per_sample=None):
    """Load all nominal Higgs MC processes and observed data.

    Returns (df_all, cutflow_by_process, input_manifest).
    """
    mc_dir = os.path.join(inputs_dir, "MC")
    data_dir = os.path.join(inputs_dir, "data")

    available_mc = set(os.listdir(mc_dir)) if os.path.isdir(mc_dir) else set()
    rejected = sorted(available_mc - set(MC_PROCESS_FILES.values()))

    frames = []
    cutflows = {}
    manifest_files = []
    for process, fname in sorted(MC_PROCESS_FILES.items()):
        path = os.path.join(mc_dir, fname)
        if not os.path.exists(path):
            continue
        df, cutflow = load_one_file(path, process, is_data=False, max_rows=max_rows_per_sample)
        frames.append(df)
        cutflows[process] = cutflow
        manifest_files.append({"process": process, "file": fname, "role": "nominal_higgs_signal_mc"})

    data_path = os.path.join(data_dir, DATA_FILE)
    if os.path.exists(data_path):
        df, cutflow = load_one_file(data_path, "data", is_data=True, max_rows=max_rows_per_sample)
        frames.append(df)
        cutflows["data"] = cutflow
        manifest_files.append({"process": "data", "file": DATA_FILE, "role": "observed_data"})

    df_all = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    manifest = {
        "inputs_dir": inputs_dir,
        "mc_dir": mc_dir,
        "data_dir": data_dir,
        "processed_files": manifest_files,
        "rejected_mc_files_not_nominal_higgs": rejected,
        "allowed_mc_processes": sorted(MC_PROCESS_FILES.keys()),
        "signal_processes": sorted(SIGNAL_PROCESSES),
        "resonant_higgs_processes": sorted(RESONANT_HIGGS_PROCESSES),
    }
    return df_all, cutflows, manifest
