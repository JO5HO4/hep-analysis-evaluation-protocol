import pandas as pd
import numpy as np
import uproot
import os
import json

def main():
    infer_path = '/root/results/infer/inference_test_xgb.parquet'
    root_path = '/root/data/ttbar.root'
    selected_path = '/root/results/select_triplets/selected_triplets.parquet'
    event_sel_path = '/root/results/select_triplets/event_selection.parquet'
    report_path = '/root/results/select_triplets/selection_report.json'
    os.makedirs(os.path.dirname(selected_path), exist_ok=True)
    
    df_inf = pd.read_parquet(infer_path)
    tree = uproot.open(root_path)['output']
    all_data = tree.arrays(['Number', 'genjet_pt', 'genjet_eta', 'genjet_phi', 'genjet_m'])
    
    event_data = {}
    for i in range(len(all_data['Number'])):
        eid = all_data['Number'][i]
        event_data[eid] = {
            'pt': np.array(all_data['genjet_pt'][i]),
            'eta': np.array(all_data['genjet_eta'][i]),
            'phi': np.array(all_data['genjet_phi'][i]),
            'm': np.array(all_data['genjet_m'][i])
        }
    
    selected_triplets = []
    event_selection_summary = []
    total_truth = df_inf['is_truth'].sum()
    recovered_truth = 0
    
    for eid, group in df_inf.groupby('event_id'):
        group = group.sort_values('score_xgb', ascending=False)
        selected_in_event = []
        used_jets = set()
        
        for _, row in group.iterrows():
            if len(selected_in_event) >= 2:
                break
            
            # Ensure indices are integers
            idx_i, idx_j, idx_k = int(row['i']), int(row['j']), int(row['k'])
            jets = {idx_i, idx_j, idx_k}
            if jets.isdisjoint(used_jets):
                selected_in_event.append(row)
                used_jets.update(jets)
                if row['is_truth'] == 1:
                    recovered_truth += 1
        
        top_kinematics = []
        for rank, row in enumerate(selected_in_event):
            idx_i, idx_j, idx_k = int(row['i']), int(row['j']), int(row['k'])
            jets_info = event_data[eid]
            
            pts = np.array([jets_info['pt'][idx_i], jets_info['pt'][idx_j], jets_info['pt'][idx_k]])
            etas = np.array([jets_info['eta'][idx_i], jets_info['eta'][idx_j], jets_info['eta'][idx_k]])
            phis = np.array([jets_info['phi'][idx_i], jets_info['phi'][idx_j], jets_info['phi'][idx_k]])
            ms = np.array([jets_info['m'][idx_i], jets_info['m'][idx_j], jets_info['m'][idx_k]])
            
            px = pts * np.cos(phis)
            py = pts * np.sin(phis)
            pz = pts * np.sinh(etas)
            e = np.sqrt(pts**2 + pz**2 + ms**2)
            
            sum_e = np.sum(e)
            sum_px = np.sum(px)
            sum_py = np.sum(py)
            sum_pz = np.sum(pz)
            
            mass = np.sqrt(max(0, sum_e**2 - sum_px**2 - sum_py**2 - sum_pz**2))
            pt = np.sqrt(sum_px**2 + sum_py**2)
            phi = np.arctan2(sum_py, sum_px)
            eta = np.arcsinh(sum_pz / pt) if pt > 0 else 0
            
            selected_triplets.append({
                'event_id': eid,
                'selected_rank': rank + 1,
                'i': idx_i,
                'j': idx_j,
                'k': idx_k,
                'score': row['score_xgb'],
                'triplet_pt': pt,
                'triplet_eta': eta,
                'triplet_phi': phi,
                'triplet_mass': mass
            })
            top_kinematics.append((pt, eta, phi, mass))
            
        n_sel = len(selected_in_event)
        top1 = top_kinematics[0] if n_sel >= 1 else (0.0, 0.0, 0.0, 0.0)
        event_selection_summary.append({
            'event_id': eid,
            'n_top_selected': n_sel,
            'top1_pt': top1[0],
            'top1_eta': top1[1],
            'top1_phi': top1[2],
            'top1_mass': top1[3]
        })
        
    pd.DataFrame(selected_triplets).to_parquet(selected_path)
    pd.DataFrame(event_selection_summary).to_parquet(event_sel_path)
    
    efficiency = recovered_truth / total_truth if total_truth > 0 else 0
    report = {
        'triplet_reconstruction_efficiency': float(efficiency),
        'total_truth_triplets': int(total_truth),
        'recovered_truth_triplets': int(recovered_truth),
        'selection_strategy': 'greedy_score_disjoint_jets',
        'max_candidates_per_event': 2
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"Selection complete. Efficiency: {efficiency:.4f}")

if __name__ == "__main__":
    main()
