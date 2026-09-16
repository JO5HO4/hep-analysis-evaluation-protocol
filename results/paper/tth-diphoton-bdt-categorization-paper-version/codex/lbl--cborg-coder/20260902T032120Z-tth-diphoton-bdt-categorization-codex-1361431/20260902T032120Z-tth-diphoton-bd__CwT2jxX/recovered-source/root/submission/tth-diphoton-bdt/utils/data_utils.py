import uproot
import pandas as pd
import numpy as np
import awkward as ak
import os

def load_and_preselect(input_dir, samples):
    all_events = []
    limit = int(os.getenv("TTH_MAX_SELECTED_PER_SAMPLE", 100)) # Very small limit for testing
    for sample_name, path in samples.items():
        with uproot.open(path) as f:
            tree = f["analysis"]
            data = tree.arrays()
            
            # Apply limit to the whole dataset immediately
            if len(data["eventNumber"]) > limit:
                mask = np.arange(len(data["eventNumber"])) < limit
                data = data[mask]
            
            for i in range(len(data["eventNumber"])):
                ph_pt = data["photon_pt"][i]
                ph_eta = data["photon_eta"][i]
                ph_phi = data["photon_phi"][i]
                ph_id = data["photon_isTightID"][i]
                ph_iso = data["photon_isTightIso"][i]
                
                kin_mask = (ph_pt > 25) & (np.abs(ph_eta) < 2.5)
                kin_pt = ph_pt[kin_mask]
                kin_eta = ph_eta[kin_mask]
                kin_phi = ph_phi[kin_mask]
                
                if len(kin_pt) < 2:
                    continue
                
                pt1, pt2 = kin_pt[0], kin_pt[1]
                eta1, eta2 = kin_eta[0], kin_eta[1]
                phi1, phi2 = kin_phi[0], kin_phi[1]
                px1, py1, pz1 = pt1 * np.cos(phi1), pt1 * np.sin(phi1), pt1 * np.sinh(eta1)
                px2, py2, pz2 = pt2 * np.cos(phi2), pt2 * np.sin(phi2), pt2 * np.sinh(eta2)
                e1, e2 = pt1 * np.cosh(eta1), pt2 * np.cosh(eta2)
                mgg = np.sqrt(max(0, (e1+e2)**2 - (px1+px2)**2 - (py1+py2)**2 - (pz1+pz2)**2))
                
                is_ti = False
                kin_id = ph_id[kin_mask]
                kin_iso = ph_iso[kin_mask]
                if len(kin_id) >= 2:
                    is_ti = bool(kin_id[0] and kin_id[1] and kin_iso[0] and kin_iso[1])
                
                lep_pt = data["lep_pt"][i]
                n_lep = np.sum(lep_pt > 10)
                
                jet_pt = data["jet_pt"][i]
                jet_eta = data["jet_eta"][i]
                jet_btag = data["jet_btag_quantile"][i]
                
                jet_mask = (jet_pt > 25)
                m_jet_pt = jet_pt[jet_mask]
                m_jet_eta = jet_eta[jet_mask]
                m_jet_btag = jet_btag[jet_mask]
                
                n_jets = len(m_jet_pt)
                n_central_jets = np.sum(np.abs(m_jet_eta) <= 2.5)
                n_btags = np.sum(m_jet_btag >= 4)
                ht = np.sum(m_jet_pt)
                met = data["met"][i]
                
                had_mask = (n_lep == 0) and (n_jets >= 3) and (n_btags >= 1)
                lep_mask = (n_lep >= 1) and (n_btags >= 1)
                
                chan = "none"
                if had_mask: chan = "hadronic"
                elif lep_mask: chan = "leptonic"
                
                all_events.append({
                    "event_id": int(data["eventNumber"][i]),
                    "sample": sample_name,
                    "weight": float(data["mcWeight"][i]) if sample_name != "data" else 1.0,
                    "xsec": float(data["xsec"][i]) if sample_name != "data" else 0,
                    "kfac": float(data["kfac"][i]) if sample_name != "data" else 0,
                    "filteff": float(data["filteff"][i]) if sample_name != "data" else 0,
                    "sum_weights": float(data["sum_of_weights"][i]) if sample_name != "data" else 0,
                    "mgg": float(mgg),
                    "n_lep": int(n_lep),
                    "n_jets": int(n_jets),
                    "n_central_jets": int(n_central_jets),
                    "n_btags": int(n_btags),
                    "ht": float(ht),
                    "met": float(met),
                    "channel": chan,
                    "is_ti": is_ti,
                })
    return pd.DataFrame(all_events)
