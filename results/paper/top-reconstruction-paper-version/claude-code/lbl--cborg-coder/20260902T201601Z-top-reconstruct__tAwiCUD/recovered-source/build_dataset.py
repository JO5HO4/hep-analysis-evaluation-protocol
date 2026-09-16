import uproot
import numpy as np
import pandas as pd
from itertools import combinations
import os

def delta_r(eta1, phi1, eta2, phi2):
    dphi = np.abs(phi1 - phi2)
    dphi = np.where(dphi > np.pi, 2 * np.pi - dphi, dphi)
    return np.sqrt((eta1 - eta2)**2 + dphi**2)

def get_4vector(pt, eta, phi, m):
    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)
    e = np.sqrt(px**2 + py**2 + pz**2 + m**2)
    return np.array([e, px, py, pz])

def build_triplets():
    file = uproot.open("/root/data/ttbar.root")
    tree = file["output"]
    
    data = tree.arrays([
        "Number", 
        "genjet_pt", "genjet_eta", "genjet_phi", "genjet_m", 
        "truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"
    ], library="np")

    all_triplets = []

    for i in range(len(data["Number"])):
        event_id = data["Number"][i]
        pt = data["genjet_pt"][i]
        eta = data["genjet_eta"][i]
        phi = data["genjet_phi"][i]
        m = data["genjet_m"][i]
        
        truth_sets = []
        for tt_key in ["truth_triplet_0", "truth_triplet_1", "truth_triplet_2", "truth_triplet_3"]:
            tt_val = data[tt_key][i]
            if tt_val is not None:
                valid_indices = [idx for idx in tt_val if idx >= 0]
                if len(valid_indices) == 3:
                    truth_sets.append(set(valid_indices))

        n_jets = len(pt)
        if n_jets < 3:
            continue

        fours = []
        for j in range(n_jets):
            fours.append(get_4vector(pt[j], eta[j], phi[j], m[j]))

        for idxs in combinations(range(n_jets), 3):
            i_idx, j_idx, k_idx = idxs
            is_truth = 0
            for ts in truth_sets:
                if set(idxs) == ts:
                    is_truth = 1
                    break
            
            p1, p2, p3 = fours[i_idx], fours[j_idx], fours[k_idx]
            
            p12 = p1 + p2
            m_ab = np.sqrt(max(0, p12[0]**2 - (p12[1]**2 + p12[2]**2 + p12[3]**2)))
            p13 = p1 + p3
            m_ac = np.sqrt(max(0, p13[0]**2 - (p13[1]**2 + p13[2]**2 + p13[3]**2)))
            p23 = p2 + p3
            m_bc = np.sqrt(max(0, p23[0]**2 - (p23[1]**2 + p23[2]**2 + p23[3]**2)))
            p123 = p1 + p2 + p3
            m123 = np.sqrt(max(0, p123[0]**2 - (p123[1]**2 + p123[2]**2 + p123[3]**2)))
            
            pt123 = np.sqrt(p123[1]**2 + p123[2]**2)
            
            dr_ab = delta_r(eta[i_idx], phi[i_idx], eta[j_idx], phi[j_idx])
            dr_ac = delta_r(eta[i_idx], phi[i_idx], eta[k_idx], phi[k_idx])
            dr_bc = delta_r(eta[j_idx], phi[j_idx], eta[k_idx], phi[k_idx])
            
            # Sort features for permutation invariance
            dr_vals = sorted([dr_ab, dr_ac, dr_bc])
            m_ratios = sorted([m_ab/m123 if m123>0 else 0, m_ac/m123 if m123>0 else 0, m_bc/m123 if m123>0 else 0])
            pt_vals = sorted([pt[i_idx], pt[j_idx], pt[k_idx]])
            
            all_triplets.append({
                "event_id": event_id,
                "i": i_idx, "j": j_idx, "k": k_idx,
                "is_truth": is_truth,
                "dr_ab": dr_ab, "dr_ac": dr_ac, "dr_bc": dr_bc,
                "mij_over_m123_ab": m_ab/m123 if m123>0 else 0,
                "mij_over_m123_ac": m_ac/m123 if m123>0 else 0,
                "mij_over_m123_bc": m_bc/m123 if m123>0 else 0,
                "m123": m123,
                "pt123": pt123,
                "dr_min": dr_vals[0], "dr_mid": dr_vals[1], "dr_max": dr_vals[2],
                "ratio_min": m_ratios[0], "ratio_mid": m_ratios[1], "ratio_max": m_ratios[2],
                "pt_min": pt_vals[0], "pt_mid": pt_vals[1], "pt_max": pt_vals[2],
                "sum_pt": sum(pt_vals)
            })

    df = pd.DataFrame(all_triplets)
    os.makedirs("/root/results/dataset_build", exist_ok=True)
    df.to_parquet("/root/results/dataset_build/triplets_raw.parquet")
    print(f"Saved {len(df)} triplets to /root/results/dataset_build/triplets_raw.parquet")

if __name__ == "__main__":
    build_triplets()
