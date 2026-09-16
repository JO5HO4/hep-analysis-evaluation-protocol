import uproot
import pandas as pd
import numpy as np
from itertools import combinations

def delta_r(eta1, phi1, eta2, phi2):
    dphi = phi1 - phi2
    dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
    return np.sqrt((eta1 - eta2)**2 + dphi**2)

def get_mass(pts, etas, phis):
    px = pts * np.cos(phis)
    py = pts * np.sin(phis)
    pz = pts * np.sinh(etas)
    e = pts * np.cosh(etas)
    sum_px, sum_py, sum_pz, sum_e = np.sum(px), np.sum(py), np.sum(pz), np.sum(e)
    m2 = sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)
    return np.sqrt(max(0, m2))

def get_pair_mass(pt1, eta1, phi1, pt2, eta2, phi2):
    px1, py1 = pt1*np.cos(phi1), pt1*np.sin(phi1)
    pz1, e1 = pt1*np.sinh(eta1), pt1*np.cosh(eta1)
    px2, py2 = pt2*np.cos(phi2), pt2*np.sin(phi2)
    pz2, e2 = pt2*np.sinh(eta2), pt2*np.cosh(eta2)
    m2 = (e1+e2)**2 - ((px1+px2)**2 + (py1+py2)**2 + (pz1+pz2)**2)
    return np.sqrt(max(0, m2))

file = uproot.open('/root/data/ttbar.root')
tree = file['output']
branches = ['Number', 'N_genjet', 'genjet_pt', 'genjet_eta', 'genjet_phi']
for i in range(4): branches.append(f'truth_triplet_{i}')

data = tree.arrays(branches)
all_triplets = []

for i in range(len(data['Number'])):
    ev_id = data['Number'][i]
    n_jets = data['N_genjet'][i]
    pts = np.array(data['genjet_pt'][i])
    etas = np.array(data['genjet_eta'][i])
    phis = np.array(data['genjet_phi'][i])
    truth_sets = []
    for t_idx in range(4):
        triplet = data[f'truth_triplet_{t_idx}'][i]
        if triplet[0] != -1: truth_sets.append(set(triplet))
    
    for idxs in combinations(range(n_jets), 3):
        i_idx, j_idx, k_idx = idxs
        is_truth = 1 if set(idxs) in truth_sets else 0
        dr_ab = delta_r(etas[i_idx], phis[i_idx], etas[j_idx], phis[j_idx])
        dr_ac = delta_r(etas[i_idx], phis[i_idx], etas[k_idx], phis[k_idx])
        dr_bc = delta_r(etas[j_idx], phis[j_idx], etas[k_idx], phis[k_idx])
        m123 = get_mass(pts[list(idxs)], etas[list(idxs)], phis[list(idxs)])
        m_ab = get_pair_mass(pts[i_idx], etas[i_idx], phis[i_idx], pts[j_idx], etas[j_idx], phis[j_idx])
        m_ac = get_pair_mass(pts[i_idx], etas[i_idx], phis[i_idx], pts[k_idx], etas[k_idx], phis[k_idx])
        m_bc = get_pair_mass(pts[j_idx], etas[j_idx], phis[j_idx], pts[k_idx], etas[k_idx], phis[k_idx])
        mij_over_m123_ab = m_ab / m123 if m123 > 0 else 0
        mij_over_m123_ac = m_ac / m123 if m123 > 0 else 0
        mij_over_m123_bc = m_bc / m123 if m123 > 0 else 0
        all_triplets.append([ev_id, i_idx, j_idx, k_idx, is_truth, dr_ab, dr_ac, dr_bc, mij_over_m123_ab, mij_over_m123_ac, mij_over_m123_bc])

df = pd.DataFrame(all_triplets, columns=['event_id', 'i', 'j', 'k', 'is_truth', 'dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc'])
df.to_parquet('/root/results/dataset_build/triplets_raw.parquet')
print('Successfully wrote triplets_raw.parquet')
