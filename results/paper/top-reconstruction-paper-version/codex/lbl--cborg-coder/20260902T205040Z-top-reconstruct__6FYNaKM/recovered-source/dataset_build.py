import uproot
import pandas as pd
import numpy as np
from itertools import combinations
import os

def main():
    file_path = '/root/data/ttbar.root'
    output_path = '/root/results/dataset_build/triplets_raw.parquet'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    tree = uproot.open(file_path)['output']
    branches = ['Number', 'N_genjet', 'genjet_pt', 'genjet_eta', 'genjet_phi', 'genjet_m', 
                'truth_triplet_0', 'truth_triplet_1', 'truth_triplet_2', 'truth_triplet_3']
    data = tree.arrays(branches)
    
    all_triplets = []
    
    numbers = np.asarray(data['Number'])
    n_genjets = np.asarray(data['N_genjet'])
    
    # We will index these awkward arrays inside the loop
    genjet_pt = data['genjet_pt']
    genjet_eta = data['genjet_eta']
    genjet_phi = data['genjet_phi']
    genjet_m = data['genjet_m']
    
    truth_cols = ['truth_triplet_0', 'truth_triplet_1', 'truth_triplet_2', 'truth_triplet_3']
    
    for i in range(len(numbers)):
        eid = numbers[i]
        nj = n_genjets[i]
        if nj < 3: continue
        
        pt = np.asarray(genjet_pt[i])
        eta = np.asarray(genjet_eta[i])
        phi = np.asarray(genjet_phi[i])
        m = np.asarray(genjet_m[i])
        
        px = pt * np.cos(phi)
        py = pt * np.sin(phi)
        pz = pt * np.sinh(eta)
        e = np.sqrt(pt**2 + pz**2 + m**2)
        
        truth_triplets = []
        for col in truth_cols:
            triplet = data[col][i]
            if triplet is not None and len(triplet) == 3 and all(idx >= 0 for idx in triplet):
                truth_triplets.append(set(triplet))
        
        for combo in combinations(range(nj), 3):
            idx_i, idx_j, idx_k = combo
            is_truth = 1 if set(combo) in truth_triplets else 0
            
            deta_ij = eta[idx_i] - eta[idx_j]
            dphi_ij = np.abs(phi[idx_i] - phi[idx_j])
            dphi_ij = np.minimum(dphi_ij, 2 * np.pi - dphi_ij)
            dr_ab = np.sqrt(deta_ij**2 + dphi_ij**2)
            
            deta_ik = eta[idx_i] - eta[idx_k]
            dphi_ik = np.abs(phi[idx_i] - phi[idx_k])
            dphi_ik = np.minimum(dphi_ik, 2 * np.pi - dphi_ik)
            dr_ac = np.sqrt(deta_ik**2 + dphi_ik**2)
            
            deta_jk = eta[idx_j] - eta[idx_k]
            dphi_jk = np.abs(phi[idx_j] - phi[idx_k])
            dphi_jk = np.minimum(dphi_jk, 2 * np.pi - dphi_jk)
            dr_bc = np.sqrt(deta_jk**2 + dphi_jk**2)
            
            # Mass
            e_abc = e[idx_i] + e[idx_j] + e[idx_k]
            px_abc = px[idx_i] + px[idx_j] + px[idx_k]
            py_abc = py[idx_i] + py[idx_j] + py[idx_k]
            pz_abc = pz[idx_i] + pz[idx_j] + pz[idx_k]
            m_abc = np.sqrt(max(0, e_abc**2 - px_abc**2 - py_abc**2 - pz_abc**2))
            
            def get_m(ia, ib):
                ea = e[ia] + e[ib]
                pxa = px[ia] + px[ib]
                pya = py[ia] + py[ib]
                pza = pz[ia] + pz[ib]
                return np.sqrt(max(0, ea**2 - pxa**2 - pya**2 - pza**2))
                
            m_ab = get_m(idx_i, idx_j)
            m_ac = get_m(idx_i, idx_k)
            m_bc = get_m(idx_j, idx_k)
            
            all_triplets.append({
                'event_id': eid, 'i': idx_i, 'j': idx_j, 'k': idx_k, 'is_truth': is_truth,
                'dr_ab': dr_ab, 'dr_ac': dr_ac, 'dr_bc': dr_bc,
                'mij_over_m123_ab': m_ab/m_abc if m_abc > 0 else 0,
                'mij_over_m123_ac': m_ac/m_abc if m_abc > 0 else 0,
                'mij_over_m123_bc': m_bc/m_abc if m_abc > 0 else 0,
                'triplet_mass': m_abc
            })
            
    df = pd.DataFrame(all_triplets)
    df.to_parquet(output_path)
    print(f"Saved {len(df)} triplets to {output_path}")

if __name__ == "__main__":
    main()
