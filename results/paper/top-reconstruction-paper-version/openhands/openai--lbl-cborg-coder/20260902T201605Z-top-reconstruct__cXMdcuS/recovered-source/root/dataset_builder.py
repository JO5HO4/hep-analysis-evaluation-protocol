import uproot
import pandas as pd
import numpy as np
import itertools
import os

def calculate_delta_r(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
    return np.sqrt(deta**2 + dphi**2)

def calculate_mass(pt, eta, phi, ids):
    px = np.array([pt[i] * np.cos(phi[i]) for i in ids])
    py = np.array([pt[i] * np.sin(phi[i]) for i in ids])
    pz = np.array([pt[i] * np.sinh(eta[i]) for i in ids])
    e = np.sqrt(px**2 + py**2 + pz**2)
    
    sum_px = np.sum(px)
    sum_py = np.sum(py)
    sum_pz = np.sum(pz)
    sum_e = np.sum(e)
    
    m2 = sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)
    return np.sqrt(max(0, m2))

def main():
    file = uproot.open("/root/data/ttbar.root")
    tree_name = [k for k in file.keys() if "TTree" in k or "tree" in k.lower()][0]
    tree = file[tree_name]
    
    # Read data
    data = tree.arrays(
        ["Number", "genjet_pt", "genjet_eta", "genjet_phi", "N_genjet", 
         "truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"], 
        library="pd"
    )
    
    triplets = []
    
    for idx, row in data.iterrows():
        event_id = row["Number"]
        pts = np.array(row["genjet_pt"])
        etas = np.array(row["genjet_eta"])
        phis = np.array(row["genjet_phi"])
        n_jets = int(row["N_genjet"])
        
        # Truth triplets
        truth_sets = []
        for tt_name in ["truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"]:
            tt = row[tt_name]
            if tt is not None and len(tt) == 3:
                # Some elements might be -1 or invalid
                if all(x >= 0 for x in tt):
                    truth_sets.append(set(tt))
        
        # Generate all combinations (i < j < k)
        for i, j, k in itertools.combinations(range(n_jets), 3):
            ids = [i, j, k]
            is_truth = 1 if set(ids) in truth_sets else 0
            
            # Features
            dr_ab = calculate_delta_r(etas[i], phis[i], etas[j], phis[j])
            dr_ac = calculate_delta_r(etas[i], phis[i], etas[k], phis[k])
            dr_bc = calculate_delta_r(etas[j], phis[j], etas[k], phis[k])
            
            # Invariant mass of the triplet
            m123 = calculate_mass(pts, etas, phis, ids)
            
            # Lower masses
            m_ab = calculate_mass(pts, etas, phis, [i, j])
            m_ac = calculate_mass(pts, etas, phis, [i, k])
            m_bc = calculate_mass(pts, etas, phis, [j, k])
            
            # Ratios
            # To avoid division by zero, use a small epsilon or handle it
            mij_over_m123_ab = m_ab / m123 if m123 > 0 else 0
            mij_over_m123_ac = m_ac / m123 if m123 > 0 else 0
            mij_over_m123_bc = m_bc / m123 if m123 > 0 else 0
            
            triplets.append({
                "event_id": event_id,
                "i": i, "j": j, "k": k,
                "is_truth": is_truth,
                "dr_ab": dr_ab, "dr_ac": dr_ac, "dr_bc": dr_bc,
                "mij_over_m123_ab": mij_over_m123_ab,
                "mij_over_m123_ac": mij_over_m123_ac,
                "mij_over_m123_bc": mij_over_m123_bc
            })
            
    df_triplets = pd.DataFrame(triplets)
    os.makedirs("/root/results/dataset_build", exist_ok=True)
    df_triplets.to_parquet("/root/results/dataset_build/triplets_raw.parquet")
    print(f"Saved {len(df_triplets)} triplets to /root/results/dataset_build/triplets_raw.parquet")

if __name__ == "__main__":
    main()
