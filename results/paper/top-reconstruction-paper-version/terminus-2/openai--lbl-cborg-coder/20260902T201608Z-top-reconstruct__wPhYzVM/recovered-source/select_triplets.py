import pandas as pd
import numpy as np
import json
import uproot

# 1. Load data
infer_df = pd.read_parquet('/root/results/infer/inference_test_xgb.parquet')
# We need the actual jet kinematics for the selection part
file = uproot.open('/root/data/ttbar.root')
tree = file['output']

# Load all events needed for the test set
test_ev_ids = infer_df['event_id'].unique()
# Optimization: only load necessary branches for these events
# For simplicity, we'll iterate through test events since it's only ~1700

selected_list = []
event_selection_list = []

# Pre-calculate reconstruction efficiency
total_truth_triplets = infer_df[infer_df['is_truth'] == 1].shape[0]
recovered_truth_triplets = 0

# For efficiency, we'll use a dictionary for kinematics lookup if needed
# but it's better to use the tree.arrays filter

# To make this efficient, we retrieve all jet data for the test events
# Use a set for fast lookup of test events
test_ev_set = set(test_ev_ids)

# Since the original file isn't indexable by 'Number' easily, we'll read all and filter
# but since it's small (5MB), we just read it
all_data = tree.arrays(['Number', 'genjet_pt', 'genjet_eta', 'genjet_phi'])
kinematics = {}
for i in range(len(all_data['Number'])):
    ev = all_data['Number'][i]
    if ev in test_ev_set:
        kinematics[ev] = {
            'pt': np.array(all_data['genjet_pt'][i]),
            'eta': np.array(all_data['genjet_eta'][i]),
            'phi': np.array(all_data['genjet_phi'][i])
        }

def get_triplet_kinematics(ev, i, j, k):
    kin = kinematics[ev]
    pts = kin['pt'][[i, j, k]]
    etas = kin['eta'][[i, j, k]]
    phis = kin['phi'][[i, j, k]]
    
    px = pts * np.cos(phis)
    py = pts * np.sin(phis)
    pz = pts * np.sinh(etas)
    e = pts * np.cosh(etas)
    
    sum_px, sum_py, sum_pz, sum_e = np.sum(px), np.sum(py), np.sum(pz), np.sum(e)
    mass = np.sqrt(max(0, sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)))
    pt = np.sqrt(sum_px**2 + sum_py**2)
    phi = np.arctan2(sum_py, sum_px)
    eta = np.arctanh(sum_pz / sum_e) if abs(sum_pz/sum_e) < 1 else (1 if sum_pz > 0 else -1)
    return pt, eta, phi, mass

for ev in test_ev_ids:
    ev_triplets = infer_df[infer_df['event_id'] == ev].sort_values('score_xgb', ascending=False)
    
    selected_in_ev = []
    used_jets = set()
    
    for _, row in ev_triplets.iterrows():
        if len(selected_in_ev) >= 2: break
        
        jets = {int(row['i']), int(row['j']), int(row['k'])}
        if jets.isdisjoint(used_jets):
            selected_in_ev.append(row)
            used_jets.update(jets)
            if row['is_truth'] == 1: recovered_truth_triplets += 1

    # Record selection for results
    for rank, row in enumerate(selected_in_ev, 1):
        pt, eta, phi, mass = get_triplet_kinematics(ev, int(row['i']), int(row['j']), int(row['k']))
        selected_list.append([
            ev, rank, int(row['i']), int(row['j']), int(row['k']), 
            row['score_xgb'], pt, eta, phi, mass
        ])
    
    # Record event selection
    if len(selected_in_ev) > 0:
        row = selected_in_ev[0]
        pt, eta, phi, mass = get_triplet_kinematics(ev, int(row['i']), int(row['j']), int(row['k']))
        event_selection_list.append([ev, len(selected_in_ev), pt, eta, phi, mass])
    else:
        event_selection_list.append([ev, 0, 0, 0, 0, 0])

# Save results
selected_df = pd.DataFrame(selected_list, columns=['event_id', 'selected_rank', 'i', 'j', 'k', 'score', 'triplet_pt', 'triplet_eta', 'triplet_phi', 'triplet_mass'])
selected_df.to_parquet('/root/results/select_triplets/selected_triplets.parquet')

event_df = pd.DataFrame(event_selection_list, columns=['event_id', 'n_top_selected', 'top1_pt', 'top1_eta', 'top1_phi', 'top1_mass'])
event_df.to_parquet('/root/results/select_triplets/event_selection.parquet')

efficiency = recovered_truth_triplets / total_truth_triplets if total_truth_triplets > 0 else 0
report = {
    'triplet_reconstruction_efficiency': float(efficiency),
    'total_truth_triplets': int(total_truth_triplets),
    'recovered_truth_triplets': int(recovered_truth_triplets),
    'selection_strategy': 'greedy_disjoint_top2'
}
with open('/root/results/select_triplets/selection_report.json', 'w') as f:
    json.dump(report, f, indent=4)

print(f'Selection complete. Efficiency: {efficiency:.4f}')
