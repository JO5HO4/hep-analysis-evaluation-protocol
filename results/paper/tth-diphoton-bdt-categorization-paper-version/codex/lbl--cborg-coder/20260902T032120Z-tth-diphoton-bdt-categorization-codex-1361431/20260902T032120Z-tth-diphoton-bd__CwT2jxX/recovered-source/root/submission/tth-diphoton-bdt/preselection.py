import uproot
import pandas as pd
import numpy as np
import os
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def process_sample(file_path, sample_name, config):
    with uproot.open(file_path) as f:
        tree = f["analysis"]
        # We only need necessary branches
        branches = [
            "eventNumber", "mcWeight", "xsec", "kfac", "filteff", "sum_of_weights",
            "photon_pt", "photon_eta", "photon_phi", "photon_isTightID", "photon_isTightIso",
            "lep_pt", "lep_eta", "lep_phi", "lep_type",
            "jet_pt", "jet_eta", "jet_phi", "jet_btag_quantile",
            "met", "met_phi"
        ]
        data = tree.arrays(branches, library="pd")
        
    # The data returned by uproot.arrays(library="pd") for jagged arrays are lists in cells
    df = pd.DataFrame()
    df["event_id"] = data["eventNumber"]
    df["weight"] = data["mcWeight"]
    df["xsec"] = data["xsec"]
    df["kfac"] = data["kfac"]
    df["filteff"] = data["filteff"]
    df["sum_weights"] = data["sum_of_weights"]
    df["met"] = data["met"]
    df["sample"] = sample_name
    
    # Process photons
    # Build Higgs candidate from 2 photons passing kinematic acceptance
    # The prompt doesn't specify kinematic acceptance, but usually it's pt > 25 and |eta| < 2.5
    # Let's assume pt > 25 and |eta| < 2.5 as a baseline for "kinematic acceptance"
    def get_higgs_candidate(ph_pt, ph_eta, ph_phi):
        # Find photons passing kinematic acceptance
        mask = (np.array(ph_pt) > 25) & (np.abs(np.array(ph_eta)) < 2.5)
        pts = np.array(ph_pt)[mask]
        etas = np.array(ph_eta)[mask]
        phis = np.array(ph_phi)[mask]
        
        if len(pts) < 2:
            return None
        
        # Use the two leading photons
        # (Actually, the laest analysis typically uses the two highest pT photons)
        # We need to handle the jagged nature. 
        # In a real analysis, we'd use the best pair. Here we'll take the first two.
        
        # For simplicity, we use the first two photons that pass the mask.
        # (Wait, the input arrays are already filtered for the event)
        # Since ph_pt is a list for each event:
        
        # I'll rewrite this as a loop over events or use awkward array.
        return True # Placeholder

    # Instead of the helper, let's use awkward arrays for efficiency
    # I will rewrite this using awkward array.
    return df

# I'll use awkward array directly in the main pipeline.
