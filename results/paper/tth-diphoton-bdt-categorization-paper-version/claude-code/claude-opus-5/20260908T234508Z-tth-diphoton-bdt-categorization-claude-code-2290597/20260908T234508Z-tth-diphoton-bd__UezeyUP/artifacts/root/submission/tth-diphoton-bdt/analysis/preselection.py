"""Vectorised object selection, event preselection and cut flow.

The definitions implemented here are the vectorised twin of the scalar
reference implementations in :mod:`analysis.top_categorization`; a per-run
cross-check (:func:`crosscheck_scalar_vs_vectorised`) verifies that the two
agree event-by-event on a deterministic random subset.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import awkward as ak
import numpy as np
import pandas as pd
import uproot

from .top_categorization import (
    BDT_FEATURES,
    MASS_WINDOWS,
    OBJECT_SELECTION,
    build_jet_features,
    build_lepton_features,
    diphoton_features,
    photon_kinematic_acceptance,
    stable_partition,
)

BRANCHES = [
    "photon_pt",
    "photon_eta",
    "photon_phi",
    "photon_e",
    "photon_isTightID",
    "photon_isTightIso",
    "jet_pt",
    "jet_eta",
    "jet_phi",
    "jet_e",
    "jet_btag_quantile",
    "lep_pt",
    "lep_eta",
    "lep_phi",
    "lep_e",
    "lep_type",
    "met",
    "met_phi",
    "eventNumber",
    "runNumber",
    "channelNumber",
    "passes_hadronic_preselection",
    "passes_leptonic_preselection",
    "preselection_channel_id",
]

MC_BRANCHES = [
    "mcWeight",
    "xsec",
    "kfac",
    "filteff",
    "sum_of_weights",
    "num_events",
    "ScaleFactor_PILEUP",
    "ScaleFactor_PHOTON",
    "ScaleFactor_BTAG",
    "ScaleFactor_JVT",
]

CUTFLOW_STAGES = [
    "input_rows",
    "photons_in_kinematic_acceptance>=2",
    "mgg_in_105_160",
    "relative_pt_cuts",
    "hadronic_or_leptonic_channel",
    "hadronic_channel",
    "leptonic_bookkeeping_only",
]


def object_definition_record(cfg: Mapping[str, Any]) -> dict[str, Any]:
    """The machine-readable object-definition record."""
    obj = cfg["objects"]
    return {
        "photons": {
            "collection": "photon_*",
            "pt_min_gev": obj["photons"]["pt_min_gev"],
            "pt_operator": ">",
            "abs_eta_max": obj["photons"]["abs_eta_max"],
            "crack_veto_abs_eta": obj["photons"]["crack_veto"],
            "require_tight_id": False,
            "require_isolation": False,
            "photon_tight_id_required": False,
            "photon_isolation_required": False,
            "explicit_statement": (
                "Photon tight ID (photon_isTightID) is NOT required and photon "
                "isolation (photon_isTightIso) is NOT required for this "
                "preselection sample. Both flags are read and stored, but only "
                "to define the TI / NTI diphoton control categories used for "
                "the data-driven continuum estimate; neither is applied as an "
                "event selection cut at preselection."
            ),
            "higgs_candidate": (
                "two leading-pT photons passing kinematic acceptance; "
                "relative-pT cuts lead pT/m_yy > "
                f"{obj['photons']['lead_pt_over_mgg_min']} and sublead pT/m_yy > "
                f"{obj['photons']['sublead_pt_over_mgg_min']}"
            ),
            "ti_definition": (
                "TI diphoton: BOTH photons pass tight ID AND tight isolation."
            ),
            "nti_definition": (
                "NTI diphoton: at least one of the two photons FAILS tight ID "
                "or FAILS tight isolation."
            ),
            "m_gammagamma": "retained for bookkeeping and later validation; never a BDT input",
        },
        "electrons_muons": {
            "collection": "lep_*",
            "pt_min_gev": obj["leptons"]["pt_min_gev"],
            "pt_operator": ">",
            "flavours": {"electron": "lep_type == 11", "muon": "lep_type == 13"},
            "require_id": False,
            "require_isolation": False,
            "explicit_statement": (
                "No lepton ID and no lepton isolation requirement is applied "
                "for this preselection sample."
            ),
        },
        "jets": {
            "collection": "jet_*",
            "pt_min_gev": obj["jets"]["pt_min_gev"],
            "pt_operator": ">",
            "central_definition": f"|eta| <= {obj['jets']['central_abs_eta_max']}",
            "forward_definition": f"|eta| > {obj['jets']['central_abs_eta_max']}",
            "btag_definition": (
                f"{obj['jets']['btag_variable']} >= {obj['jets']['btag_min_quantile']}"
            ),
            "btag_definition_note": (
                "Documented b-tag working point: the per-jet b-tagging "
                "quantile stored in the open-data ntuple, jet_btag_quantile >= 4."
            ),
            "forward_jet_availability": (
                "The current ATLAS open-data GamGam ntuples contain no "
                "reconstructed jets with |eta| > 2.5, so n_jets_forward is "
                "identically 0 in this run. Leptonic top-associated categories "
                "that rely on forward jets are therefore out of scope."
            ),
        },
        "missing_transverse_momentum": {"branch": "met", "units": "GeV"},
        "channels": {
            "hadronic": (
                f"n_leptons == {cfg['selection']['hadronic']['n_leptons']} AND "
                f"n_jets >= {cfg['selection']['hadronic']['min_n_jets']} AND "
                f"n_bjets >= {cfg['selection']['hadronic']['min_n_bjets']}"
            ),
            "leptonic_bookkeeping": (
                f"n_leptons >= {cfg['selection']['leptonic_bookkeeping']['min_n_leptons']} AND "
                f"n_bjets >= {cfg['selection']['leptonic_bookkeeping']['min_n_bjets']} "
                "(provenance only; excluded from BDT training, boundary "
                "optimisation, categorization metrics and the workspace)"
            ),
        },
        "units": {"momenta": "GeV", "energies": "GeV", "cross_sections": "pb"},
    }


def _mgg_region(mgg: np.ndarray, cfg: Mapping[str, Any]) -> np.ndarray:
    sel = cfg["selection"]
    out = np.full(mgg.shape, "outside", dtype=object)
    lo = sel["sideband_low_gev"]
    hi = sel["sideband_high_gev"]
    win = sel["signal_window_gev"]
    out[(mgg >= lo[0]) & (mgg < lo[1])] = "sideband_low"
    out[(mgg >= hi[0]) & (mgg < hi[1])] = "sideband_high"
    out[(mgg >= lo[1]) & (mgg < hi[0])] = "transition"
    out[(mgg >= win[0]) & (mgg <= win[1])] = "signal_window"
    return out


def process_sample(
    sample: Mapping[str, Any],
    cfg: Mapping[str, Any],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Read one sample and return its selected rows plus its cut flow."""
    obj = cfg["objects"]
    sel = cfg["selection"]
    is_mc = sample["kind"] == "mc"
    branches = list(BRANCHES) + (MC_BRANCHES if is_mc else [])

    tree = uproot.open(sample["path"])[sample["tree"]]
    arrays = tree.arrays(branches)
    n_input = len(arrays)

    cutflow: dict[str, Any] = {
        "sample": sample["sample"],
        "role": sample["role"],
        "stages": [],
    }

    def stage(name: str, mask: np.ndarray | None, weights: np.ndarray | None) -> None:
        n = int(n_input if mask is None else np.count_nonzero(mask))
        entry: dict[str, Any] = {"stage": name, "raw_events": n}
        if weights is not None:
            w = weights if mask is None else weights[mask]
            entry["weighted_events_36fb"] = float(np.sum(w))
            entry["sum_positive_weights"] = float(np.sum(w[w > 0]))
            entry["sum_negative_weights"] = float(np.sum(w[w < 0]))
            entry["n_negative_weight_events"] = int(np.count_nonzero(w < 0))
        cutflow["stages"].append(entry)

    # ---------------- photons ----------------
    ppt = arrays["photon_pt"]
    peta = arrays["photon_eta"]
    pphi = arrays["photon_phi"]
    pe = arrays["photon_e"]
    abs_peta = abs(peta)
    crack = obj["photons"]["crack_veto"]
    acc = (
        (ppt > obj["photons"]["pt_min_gev"])
        & (abs_peta < obj["photons"]["abs_eta_max"])
        & ~((abs_peta > crack[0]) & (abs_peta < crack[1]))
    )
    n_acc = ak.to_numpy(ak.sum(acc, axis=1))

    # ---------------- MC normalisation weights ----------------
    lumi_pb = float(cfg["normalization"]["luminosity_fb"]) * 1000.0
    if is_mc:
        mc_weight = ak.to_numpy(arrays["mcWeight"]).astype(np.float64)
        xsec = ak.to_numpy(arrays["xsec"]).astype(np.float64)
        kfac = ak.to_numpy(arrays["kfac"]).astype(np.float64)
        filteff = ak.to_numpy(arrays["filteff"]).astype(np.float64)
        sumw = ak.to_numpy(arrays["sum_of_weights"]).astype(np.float64)
        sf_total = np.ones(n_input, dtype=np.float64)
        for name in cfg["normalization"]["scale_factors"]:
            sf_total *= ak.to_numpy(arrays[name]).astype(np.float64)
        # Luminosity-independent SM-normalised MC weight, in units of 1/pb.
        w_per_pb = xsec * kfac * filteff / np.where(sumw != 0, sumw, np.nan) * mc_weight * sf_total
        w_36fb = lumi_pb * w_per_pb
    else:
        mc_weight = np.ones(n_input)
        xsec = kfac = filteff = sumw = np.zeros(n_input)
        sf_total = np.ones(n_input)
        w_per_pb = np.zeros(n_input)
        w_36fb = np.zeros(n_input)

    stage("input_rows", None, w_36fb if is_mc else None)

    mask2 = n_acc >= 2
    stage("photons_in_kinematic_acceptance>=2", mask2, w_36fb if is_mc else None)

    order = ak.argsort(ak.where(acc, ppt, -1.0), axis=1, ascending=False)
    ppt_s, peta_s, pphi_s, pe_s = ppt[order], peta[order], pphi[order], pe[order]
    tid_s = arrays["photon_isTightID"][order]
    tiso_s = arrays["photon_isTightIso"][order]

    keep = mask2
    idx_keep = np.nonzero(keep)[0]
    if idx_keep.size == 0:
        empty = pd.DataFrame(columns=_columns())
        for name in CUTFLOW_STAGES[2:]:
            stage(name, np.zeros(n_input, dtype=bool), w_36fb if is_mc else None)
        return empty, cutflow

    def lead_sub(arr):  # noqa: ANN001
        sub = arr[keep]
        return ak.to_numpy(sub[:, 0]).astype(np.float64), ak.to_numpy(sub[:, 1]).astype(np.float64)

    pt1, pt2 = lead_sub(ppt_s)
    eta1, eta2 = lead_sub(peta_s)
    phi1, phi2 = lead_sub(pphi_s)
    e1, e2 = lead_sub(pe_s)

    px = pt1 * np.cos(phi1) + pt2 * np.cos(phi2)
    py = pt1 * np.sin(phi1) + pt2 * np.sin(phi2)
    pz = pt1 * np.sinh(eta1) + pt2 * np.sinh(eta2)
    energy = e1 + e2
    m2 = energy**2 - (px**2 + py**2 + pz**2)
    mgg = np.sqrt(np.clip(m2, 0.0, None))
    pt_gg = np.hypot(px, py)
    dphi = (phi1 - phi2 + np.pi) % (2 * np.pi) - np.pi
    dr_gg = np.hypot(eta1 - eta2, dphi)

    fit_lo, fit_hi = sel["mgg_fit_range_gev"]
    in_range = (mgg >= fit_lo) & (mgg <= fit_hi)
    full = np.zeros(n_input, dtype=bool)
    full[idx_keep[in_range]] = True
    stage("mgg_in_105_160", full, w_36fb if is_mc else None)

    safe_mgg = np.where(mgg > 0, mgg, np.nan)
    rel = (
        (pt1 / safe_mgg > obj["photons"]["lead_pt_over_mgg_min"])
        & (pt2 / safe_mgg > obj["photons"]["sublead_pt_over_mgg_min"])
    )
    base = in_range & rel
    full = np.zeros(n_input, dtype=bool)
    full[idx_keep[base]] = True
    stage("relative_pt_cuts", full, w_36fb if is_mc else None)

    ti = ak.to_numpy(
        tid_s[keep][:, 0] & tid_s[keep][:, 1] & tiso_s[keep][:, 0] & tiso_s[keep][:, 1]
    ).astype(bool)

    # ---------------- jets ----------------
    jpt = arrays["jet_pt"][keep]
    jeta = arrays["jet_eta"][keep]
    jbtag = arrays["jet_btag_quantile"][keep]
    jsel = jpt > obj["jets"]["pt_min_gev"]
    is_central = abs(jeta) <= obj["jets"]["central_abs_eta_max"]
    is_btag = jbtag >= obj["jets"]["btag_min_quantile"]
    n_jets = ak.to_numpy(ak.sum(jsel, axis=1)).astype(np.int64)
    n_jets_central = ak.to_numpy(ak.sum(jsel & is_central, axis=1)).astype(np.int64)
    n_jets_forward = ak.to_numpy(ak.sum(jsel & ~is_central, axis=1)).astype(np.int64)
    n_bjets = ak.to_numpy(ak.sum(jsel & is_btag, axis=1)).astype(np.int64)
    n_bjets_central = ak.to_numpy(ak.sum(jsel & is_btag & is_central, axis=1)).astype(np.int64)
    ht_jets = ak.to_numpy(ak.sum(ak.where(jsel, jpt, 0.0), axis=1)).astype(np.float64)
    jpt_sorted = ak.sort(ak.where(jsel, jpt, -1.0), axis=1, ascending=False)
    jpt_pad = ak.fill_none(ak.pad_none(jpt_sorted, 2, axis=1, clip=True), -1.0)
    lead_jet_pt = np.clip(ak.to_numpy(jpt_pad[:, 0]).astype(np.float64), 0.0, None)
    sublead_jet_pt = np.clip(ak.to_numpy(jpt_pad[:, 1]).astype(np.float64), 0.0, None)

    # ---------------- leptons ----------------
    lpt = arrays["lep_pt"][keep]
    ltype = arrays["lep_type"][keep]
    lsel = lpt > obj["leptons"]["pt_min_gev"]
    n_el = ak.to_numpy(ak.sum(lsel & (ltype == 11), axis=1)).astype(np.int64)
    n_mu = ak.to_numpy(ak.sum(lsel & (ltype == 13), axis=1)).astype(np.int64)
    n_leptons = n_el + n_mu

    had = (
        (n_leptons == sel["hadronic"]["n_leptons"])
        & (n_jets >= sel["hadronic"]["min_n_jets"])
        & (n_bjets >= sel["hadronic"]["min_n_bjets"])
    )
    lep = (
        (n_leptons >= sel["leptonic_bookkeeping"]["min_n_leptons"])
        & (n_bjets >= sel["leptonic_bookkeeping"]["min_n_bjets"])
    )
    selected = base & (had | lep)

    full = np.zeros(n_input, dtype=bool)
    full[idx_keep[selected]] = True
    stage("hadronic_or_leptonic_channel", full, w_36fb if is_mc else None)
    full_h = np.zeros(n_input, dtype=bool)
    full_h[idx_keep[base & had]] = True
    stage("hadronic_channel", full_h, w_36fb if is_mc else None)
    full_l = np.zeros(n_input, dtype=bool)
    full_l[idx_keep[base & lep & ~had]] = True
    stage("leptonic_bookkeeping_only", full_l, w_36fb if is_mc else None)

    # ---------------- build the dataframe ----------------
    keep_idx = np.nonzero(selected)[0]
    row_index = idx_keep[keep_idx]

    event_number = ak.to_numpy(arrays["eventNumber"])[row_index].astype(np.int64)
    run_number = ak.to_numpy(arrays["runNumber"])[row_index].astype(np.int64)
    channel_number = ak.to_numpy(arrays["channelNumber"])[row_index].astype(np.int64)

    name = sample["sample"]
    event_id = np.array(
        [
            f"{name}|{c}|{r}|{e}"
            for c, r, e in zip(channel_number, run_number, event_number)
        ],
        dtype=object,
    )

    channel = np.where(had[keep_idx], "hadronic", "leptonic_bookkeeping").astype(object)

    df = pd.DataFrame(
        {
            "event_id": event_id,
            "sample": name,
            "process": name,
            "process_role": sample["role"],
            "is_mc": is_mc,
            "is_data": not is_mc,
            "channel_number": channel_number,
            "run_number": run_number,
            "event_number": event_number,
            "m_gammagamma": mgg[keep_idx],
            "pt_gg": pt_gg[keep_idx],
            "delta_r_gg": dr_gg[keep_idx],
            "lead_photon_pt": pt1[keep_idx],
            "sublead_photon_pt": pt2[keep_idx],
            "lead_photon_eta": eta1[keep_idx],
            "sublead_photon_eta": eta2[keep_idx],
            "photon_ti": ti[keep_idx],
            "photon_nti": ~ti[keep_idx],
            "n_electrons": n_el[keep_idx],
            "n_muons": n_mu[keep_idx],
            "n_leptons": n_leptons[keep_idx],
            "n_jets": n_jets[keep_idx],
            "n_jets_central": n_jets_central[keep_idx],
            "n_jets_forward": n_jets_forward[keep_idx],
            "n_bjets": n_bjets[keep_idx],
            "n_bjets_central": n_bjets_central[keep_idx],
            "ht_jets": ht_jets[keep_idx],
            "lead_jet_pt": lead_jet_pt[keep_idx],
            "sublead_jet_pt": sublead_jet_pt[keep_idx],
            "met": ak.to_numpy(arrays["met"])[row_index].astype(np.float64),
            "passes_hadronic_preselection": had[keep_idx],
            "passes_leptonic_preselection": lep[keep_idx],
            "preselection_channel": channel,
            "upstream_passes_hadronic": ak.to_numpy(
                arrays["passes_hadronic_preselection"]
            )[row_index],
            "upstream_passes_leptonic": ak.to_numpy(
                arrays["passes_leptonic_preselection"]
            )[row_index],
            "mc_generator_weight": mc_weight[row_index],
            "mc_xsec_pb": xsec[row_index],
            "mc_kfactor": kfac[row_index],
            "mc_filter_efficiency": filteff[row_index],
            "mc_sum_of_weights": sumw[row_index],
            "mc_scale_factor_product": sf_total[row_index],
            "weight_sm_per_pb": w_per_pb[row_index],
            "weight_mc_36fb": w_36fb[row_index],
            "observed_data_weight": np.where(is_mc, 0.0, 1.0),
        }
    )
    df["mgg_region"] = _mgg_region(df["m_gammagamma"].to_numpy(), cfg)
    df["in_signal_window"] = df["mgg_region"] == "signal_window"
    df["in_sideband"] = df["mgg_region"].isin(["sideband_low", "sideband_high"])
    df["partition"] = [
        stable_partition(
            eid,
            seed=cfg["partition"]["seed"],
            fractions=cfg["partition"]["fractions"],
        )
        for eid in df["event_id"]
    ]

    cap = cfg["run"].get("max_selected_per_sample")
    cutflow["row_cap_applied"] = False
    cutflow["rows_before_cap"] = int(len(df))
    if cap is not None and len(df) > cap:
        df = df.sort_values("event_id", kind="mergesort").head(int(cap)).reset_index(drop=True)
        cutflow["row_cap_applied"] = True
        cutflow["row_cap"] = int(cap)
    cutflow["rows_written"] = int(len(df))
    cutflow["selected_hadronic"] = int(df["passes_hadronic_preselection"].sum())
    cutflow["selected_leptonic_bookkeeping"] = int(
        (df["passes_leptonic_preselection"] & ~df["passes_hadronic_preselection"]).sum()
    )
    return df.reset_index(drop=True), cutflow


def _columns() -> list[str]:
    return [
        "event_id",
        "sample",
        "process",
        "process_role",
        "is_mc",
        "is_data",
        "channel_number",
        "run_number",
        "event_number",
        "m_gammagamma",
        "pt_gg",
        "delta_r_gg",
        "lead_photon_pt",
        "sublead_photon_pt",
        "lead_photon_eta",
        "sublead_photon_eta",
        "photon_ti",
        "photon_nti",
        "n_electrons",
        "n_muons",
        "n_leptons",
        "n_jets",
        "n_jets_central",
        "n_jets_forward",
        "n_bjets",
        "n_bjets_central",
        "ht_jets",
        "lead_jet_pt",
        "sublead_jet_pt",
        "met",
        "passes_hadronic_preselection",
        "passes_leptonic_preselection",
        "preselection_channel",
        "upstream_passes_hadronic",
        "upstream_passes_leptonic",
        "mc_generator_weight",
        "mc_xsec_pb",
        "mc_kfactor",
        "mc_filter_efficiency",
        "mc_sum_of_weights",
        "mc_scale_factor_product",
        "weight_sm_per_pb",
        "weight_mc_36fb",
        "observed_data_weight",
        "mgg_region",
        "in_signal_window",
        "in_sideband",
        "partition",
    ]


def crosscheck_scalar_vs_vectorised(
    sample: Mapping[str, Any],
    cfg: Mapping[str, Any],
    df: pd.DataFrame,
    n_check: int = 150,
) -> dict[str, Any]:
    """Re-derive a deterministic subset of rows with the scalar reference API."""
    if df.empty:
        return {"sample": sample["sample"], "n_checked": 0, "status": "empty"}

    rng = np.random.default_rng(int(cfg["run"]["seed"]))
    take = min(n_check, len(df))
    picks = np.sort(rng.choice(len(df), size=take, replace=False))
    wanted = set(
        zip(
            df["channel_number"].to_numpy()[picks],
            df["run_number"].to_numpy()[picks],
            df["event_number"].to_numpy()[picks],
        )
    )

    tree = uproot.open(sample["path"])[sample["tree"]]
    arrays = tree.arrays(
        [
            "photon_pt",
            "photon_eta",
            "photon_phi",
            "photon_e",
            "jet_pt",
            "jet_eta",
            "jet_btag_quantile",
            "lep_pt",
            "lep_type",
            "eventNumber",
            "runNumber",
            "channelNumber",
        ]
    )
    key = list(
        zip(
            ak.to_numpy(arrays["channelNumber"]).astype(np.int64),
            ak.to_numpy(arrays["runNumber"]).astype(np.int64),
            ak.to_numpy(arrays["eventNumber"]).astype(np.int64),
        )
    )
    lookup = {k: i for i, k in enumerate(key) if k in wanted}

    indexed = df.set_index(["channel_number", "run_number", "event_number"])
    n_checked = 0
    mismatches: list[dict[str, Any]] = []
    for k, row_i in lookup.items():
        try:
            ref = indexed.loc[k]
        except KeyError:
            continue
        if isinstance(ref, pd.DataFrame):
            ref = ref.iloc[0]
        photons = [
            {"pt": float(p), "eta": float(e), "phi": float(f), "e": float(en)}
            for p, e, f, en in zip(
                ak.to_list(arrays["photon_pt"][row_i]),
                ak.to_list(arrays["photon_eta"][row_i]),
                ak.to_list(arrays["photon_phi"][row_i]),
                ak.to_list(arrays["photon_e"][row_i]),
            )
        ]
        accepted = [p for p in photons if photon_kinematic_acceptance(p)]
        accepted.sort(key=lambda p: p["pt"], reverse=True)
        if len(accepted) < 2:
            continue
        dif = diphoton_features(accepted)
        jets = [
            {"pt": float(p), "eta": float(e), "btag_quantile": int(b)}
            for p, e, b in zip(
                ak.to_list(arrays["jet_pt"][row_i]),
                ak.to_list(arrays["jet_eta"][row_i]),
                ak.to_list(arrays["jet_btag_quantile"][row_i]),
            )
        ]
        jf = build_jet_features(jets)
        leps = [
            {"pt": float(p), "type": int(t)}
            for p, t in zip(
                ak.to_list(arrays["lep_pt"][row_i]), ak.to_list(arrays["lep_type"][row_i])
            )
        ]
        lf = build_lepton_features(leps)

        n_checked += 1
        for field, value in [
            ("m_gammagamma", dif["m_gammagamma"]),
            ("pt_gg", dif["pt_gg"]),
            ("n_jets", jf["n_jets"]),
            ("n_jets_central", jf["n_jets_central"]),
            ("n_bjets", jf["n_bjets"]),
            ("ht_jets", jf["ht_jets"]),
            ("n_leptons", lf["n_leptons"]),
        ]:
            got = float(ref[field])
            if not np.isclose(got, float(value), rtol=1e-5, atol=1e-4):
                mismatches.append(
                    {"event": list(k), "field": field, "vectorised": got, "scalar": float(value)}
                )

    return {
        "sample": sample["sample"],
        "n_checked": n_checked,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
        "status": "ok" if not mismatches else "MISMATCH",
    }


def preselection_summary(
    df: pd.DataFrame, cfg: Mapping[str, Any], object_record: Mapping[str, Any]
) -> dict[str, Any]:
    """Raw and weighted preselection counts, overall and by process."""

    def block(sub: pd.DataFrame) -> dict[str, Any]:
        w = sub["weight_mc_36fb"].to_numpy()
        return {
            "raw_events": int(len(sub)),
            "weighted_events_36fb": float(w.sum()),
            "sum_positive_weights_36fb": float(w[w > 0].sum()),
            "sum_negative_weights_36fb": float(w[w < 0].sum()),
            "n_negative_weight_events": int((w < 0).sum()),
            "n_positive_weight_events": int((w > 0).sum()),
            "observed_data_rows": int(sub["observed_data_weight"].sum()),
            "raw_ti": int(sub["photon_ti"].sum()),
            "raw_nti": int(sub["photon_nti"].sum()),
        }

    had = df[df["passes_hadronic_preselection"]]
    lep_only = df[df["passes_leptonic_preselection"] & ~df["passes_hadronic_preselection"]]

    by_process: dict[str, Any] = {}
    for name, sub in df.groupby("process", sort=True):
        by_process[str(name)] = {
            "role": str(sub["process_role"].iloc[0]),
            "all_selected": block(sub),
            "hadronic": block(sub[sub["passes_hadronic_preselection"]]),
            "leptonic_bookkeeping_only": block(
                sub[sub["passes_leptonic_preselection"] & ~sub["passes_hadronic_preselection"]]
            ),
        }

    return {
        "definitions": {
            "photon_selection": object_record["photons"],
            "hadronic_event_selection": {
                "statement": object_record["channels"]["hadronic"],
                "n_leptons": cfg["selection"]["hadronic"]["n_leptons"],
                "min_n_jets": cfg["selection"]["hadronic"]["min_n_jets"],
                "min_n_bjets": cfg["selection"]["hadronic"]["min_n_bjets"],
                "required_channel": True,
            },
            "leptonic_bookkeeping_selection": {
                "retained": True,
                "statement": object_record["channels"]["leptonic_bookkeeping"],
                "min_n_leptons": cfg["selection"]["leptonic_bookkeeping"]["min_n_leptons"],
                "min_n_bjets": cfg["selection"]["leptonic_bookkeeping"]["min_n_bjets"],
                "role": "bookkeeping / provenance only",
                "excluded_from": [
                    "hadronic BDT training",
                    "BDT boundary optimisation",
                    "categorization metrics and category yields",
                    "RooFit statistical workspace",
                ],
                "reason": (
                    "The current open-data ROOT inputs contain no reconstructed "
                    "forward jets, so leptonic top-associated categories are out "
                    "of scope for this analysis."
                ),
            },
            "lepton_selection": object_record["electrons_muons"],
            "jet_selection": object_record["jets"],
            "mass_windows_gev": MASS_WINDOWS,
        },
        "row_policy": {
            "max_selected_per_sample": cfg["run"]["max_selected_per_sample"],
            "source": cfg["run"]["max_selected_per_sample_source"],
            "uncapped": cfg["run"]["max_selected_per_sample"] is None,
        },
        "partition": {
            "identifier": "event_id = sample|channelNumber|runNumber|eventNumber",
            "method": "BLAKE2b(seed:event_id) -> uniform [0,1) -> bucket",
            "order_independent": True,
            "seed": cfg["partition"]["seed"],
            "fractions": cfg["partition"]["fractions"],
            "counts": {k: int(v) for k, v in df["partition"].value_counts().items()},
            "hadronic_counts": {
                k: int(v) for k, v in had["partition"].value_counts().items()
            },
        },
        "overall": block(df),
        "hadronic": block(had),
        "leptonic_bookkeeping_only": block(lep_only),
        "by_process": by_process,
        "by_channel": {
            "hadronic": int(len(had)),
            "leptonic_bookkeeping_only": int(len(lep_only)),
        },
        "bdt_features": list(BDT_FEATURES),
        "m_gammagamma_retained_for_bookkeeping": True,
    }
