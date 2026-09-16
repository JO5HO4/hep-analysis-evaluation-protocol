import pandas as pd
import numpy as np
import uproot
import os
import json
import matplotlib.pyplot as plt

def get_kinematics(event_id, i, j, k, tree_data):
    # tree_data should be accessed via index or cached
    # For efficiency, let's pre-load the necessary columns for the test events
    pass

def select():
    # Load inference results
    infer_df = pd.read_parquet("/root/results/infer/inference_test_xgb.parquet")
    
    # Load original jet data for kinematics
    file = uproot.open("/root/data/ttbar.root")
    tree = file["output"]
    
    # We only need jets for the events present in the test set
    test_event_ids = infer_df['event_id'].unique()
    
    # Since we might have many events, reading them all and indexing is faster
    # but let's be mindful of memory. 10k events is small.
    all_data = tree.arrays([
        "Number", "genjet_pt", "genjet_eta", "genjet_phi", "genjet_m"
    ], library="np")
    
    # Create a map for fast lookup: event_id -> index in all_data
    event_map = {num: idx for idx, num in enumerate(all_data["Number"])}
    
    selected_all = []
    event_selection_summary = []
    
    # Group by event
    for event_id, group in infer_df.groupby('event_id'):
        # Sort by score descending
        sorted_triplets = group.sort_values('score_xgb', ascending=False)
        
        picked_indices = [] # List of (i, j, k)
        used_jets = set()
        
        for _, row in sorted_triplets.iterrows():
            if len(picked_indices) >= 2:
                break
                
            triplet_jets = {int(row['i']), int(row['j']), int(row['k'])}
            if triplet_jets.isdisjoint(used_jets):
                picked_indices.append((int(row['i']), int(row['j']), int(row['k']), row['score_xgb']))
                used_jets.update(triplet_jets)
        
        # Calculate kinematics for picked
        event_idx = event_map[event_id]
        pts = all_data["genjet_pt"][event_idx]
        etas = all_data["genjet_eta"][event_idx]
        phis = all_data["genjet_phi"][event_idx]
        ms = all_data["genjet_m"][event_idx]
        
        top_kin = []
        for rank, (i, j, k, score) in enumerate(picked_indices):
            # 4-vectors
            def get_4v(idx):
                px = pts[idx] * np.cos(phis[idx])
                py = pts[idx] * np.sin(phis[idx])
                pz = pts[idx] * np.sinh(etas[idx])
                e = np.sqrt(px**2 + py**2 + pz**2 + ms[idx]**2)
                return np.array([e, px, py, pz])
            
            p_tot = get_4v(i) + get_4v(j) + get_4v(k)
            mass = np.sqrt(max(0, p_tot[0]**2 - (p_tot[1]**2 + p_tot[2]**2 + p_tot[3]**2)))
            pt = np.sqrt(p_tot[1]**2 + p_tot[2]**2)
            phi = np.arctan2(p_tot[2], p_tot[1])
            eta = np.arcsinh(p_tot[3] / pt) if pt > 0 else 0
            
            selected_all.append({
                "event_id": event_id,
                "selected_rank": rank + 1,
                "i": i, "j": j, "k": k,
                "score": score,
                "triplet_pt": pt, "triplet_eta": eta, "triplet_phi": phi, "triplet_mass": mass
            })
            top_kin.append((pt, eta, phi, mass))
            
        # Event summary
        n_sel = len(top_kin)
        summary = {"event_id": event_id, "n_top_selected": n_sel}
        if n_sel >= 1:
            summary["top1_pt"], summary["top1_eta"], summary["top1_phi"], summary["top1_mass"] = top_kin[0]
        else:
            summary["top1_pt"] = summary["top1_eta"] = summary["top1_phi"] = summary["top1_mass"] = np.nan
        event_selection_summary.append(summary)

    # Save results
    selected_df = pd.DataFrame(selected_all)
    summary_df = pd.DataFrame(event_selection_summary)
    
    os.makedirs("/root/results/select_triplets", exist_ok=True)
    selected_df.to_parquet("/root/results/select_triplets/selected_triplets.parquet")
    summary_df.to_parquet("/root/results/select_triplets/event_selection.parquet")
    
    # Efficiency calculation
    # Truth matched triplets in test set
    truth_triplets = infer_df[infer_df['is_truth'] == 1]
    total_truth_count = len(truth_triplets)
    
    # How many of those were selected?
    # Need to join selected_df with truth_triplets on event_id and i,j,k
    # Sort i,j,k to ensure matching
    def sort_ijk(row):
        return tuple(sorted([row['i'], row['j'], row['k']]))
    
    selected_df['ijk'] = selected_df.apply(sort_ijk, axis=1)
    truth_triplets['ijk'] = truth_triplets.apply(sort_ijk, axis=1)
    
    merged = truth_triplets.merge(selected_df[['event_id', 'ijk']], on=['event_id', 'ijk'], how='inner')
    recovered_count = len(merged)
    
    efficiency = recovered_count / total_truth_count if total_truth_count > 0 else 0
    
    report = {
        "triplet_reconstruction_efficiency": float(efficiency),
        "total_truth_triplets": int(total_truth_count),
        "recovered_truth_triplets": int(recovered_count),
        "selection_strategy": "greedy_disjoint_top2",
        "score_threshold": "none"
    }
    
    with open("/root/results/select_triplets/selection_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Efficiency: {efficiency:.4f}")
    
    # Plotting
    os.makedirs("/root/results/select_triplets/plots", exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.hist(selected_df['triplet_mass'], bins=50, range=(100, 250), histtype='step', lw=2)
    plt.xlabel("Triplet Mass [GeV]")
    plt.ylabel("Count")
    plt.title("Selected Top Candidates Mass")
    plt.grid(True, alpha=0.3)
    plt.savefig("/root/results/select_triplets/plots/mass_dist.png")
    plt.close()

if __name__ == "__main__":
    select()
