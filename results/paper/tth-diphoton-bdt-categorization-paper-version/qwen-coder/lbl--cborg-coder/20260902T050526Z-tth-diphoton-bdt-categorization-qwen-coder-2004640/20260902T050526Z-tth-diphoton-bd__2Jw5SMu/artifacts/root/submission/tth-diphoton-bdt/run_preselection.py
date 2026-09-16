import os
import numpy as np
import pandas as pd
import uproot
import awkward as ak
import yaml
import json
from analysis.top_categorization import (
    build_jet_features, 
    invariant_mass, 
    stable_partition, 
    CATEGORY_ORDER, 
    BDT_FEATURES
)

def load_atlas_data(inputs_dir):
    """
    Load MC and Data from the specified directory.
    Expects layout: MC/ and data/
    """
    all_events = []
    
    # Load Data
    data_dir = os.path.join(inputs_dir, "data")
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(".root"):
                with uproot.open(os.path.join(data_dir, file)) as f:
                    tree = f["GamGam"]
                    df = tree.arrays(library="pd")
                    df["process"] = "data"
                    df["sample"] = file.replace(".root", "")
                    all_events.append(df)
                    
    # Load MC
    mc_dir = os.path.join(inputs_dir, "MC")
    if os.path.exists(mc_dir):
        for file in os.listdir(mc_dir):
            if file.endswith(".root"):
                # Filter for nominal Higgs MC
                # Skip Sherpa yy or others as requested
                if "yy" in file or "prompt" in file:
                    continue
                
                with uproot.open(os.path.join(mc_dir, file)) as f:
                    tree = f["GamGam"]
                    df = tree.arrays(library="pd")
                    df["process"] = "mc"
                    df["sample"] = file.replace(".root", "")
                    all_events.append(df)
                    
    return pd.concat(all_events, ignore_index=True) if all_events else pd.DataFrame()

def apply_preselection(df):
    """
    Apply required preselection cuts.
    """
    # Photon preselection (Simplified based on typical ATLAS GamGam:’pT’ and ‘eta’)
    # Requirement: Kinematic acceptance, no tight ID or isolation.
    # Assuming cols: photon_pt, photon_eta (arrays/lists)
    
    # For this implementation, we assume the ROOT files provide 
    # the leading and sub-leading photon properties.
    # Let's assume columns are gamma0_pt, gamma1_pt, gamma0_eta, gamma1_eta
    
    mask = (df['gamma0_pt'] > 20) & (df['gamma1_pt'] > 15)
    
    # Lepton preselection: pT > 10 GeV
    # Assume lists of leptons’ pT: electron_pt, muon_pt
    def count_leptons(row):
        e_count = sum(1 for p in row['electron_pt'] if p > 10)
        m_count = sum(1 for p in row['muon_pt'] if p > 10)
        return e_count + m_count
    
    df['n_leptons'] = df.apply(count_leptons, axis=1)
    
    # Jet preselection: pT > 25 GeV
    def filter_jets(row):
        pts = np.array(row['jet_pt'])
        etas = np.array(row['jet_eta'])
        btags = np.array(row['jet_btag_quantile'])
        
        valid = pts > 25
        pts = pts[valid]
        etas = etas[valid]
        btags = btags[valid]
        
        central = (np.abs(etas) <= 2.5)
        n_central = np.sum(central)
        n_btags = np.sum(btags >= 4)
        
        return pd.Series({
            'n_jets': len(pts),
            'n_central_jets': n_central,
            'n_btags': n_btags,
            'filtered_jets': list(zip(pts, etas, btags)) # for feature build
        })

    jet_data = df.apply(filter_jets, axis=1)
    df = pd.concat([df, jet_data], axis=1)
    
    # Hadronic Channel: 0 leptons, >= 3 jets, >= 1 b-jet
    df['is_hadronic'] = (df['n_leptons'] == 0) & (df['n_jets'] >= 3) & (df['n_btags'] >= 1)
    
    # Leptonic Bookkeeping: >= 1 lepton, >= 1 b-jet
    df['is_leptonic'] = (df['n_leptons'] >= 1) & (df['n_btags'] >= 1)
    
    return df[df['is_hadronic'] | df['is_leptonic']]

def main():
    inputs_dir = os.getenv("TB_HYY_INPUTS", "/root/data/GamGam")
    print(f"Loading data from {inputs_dir}...")
    df = load_atlas_data(inputs_dir)
    
    if df.empty:
        print("No data found. Exiting.")
        return

    print("Applying preselection...")
    df_selected = apply_preselection(df)
    
    # Save preselection
    df_selected.to_csv("/root/results/tth-diphoton-bdt/preselected_events.csv", index=False)
    print("Preselected events saved.")

if __name__ == "__main__":
    main()
