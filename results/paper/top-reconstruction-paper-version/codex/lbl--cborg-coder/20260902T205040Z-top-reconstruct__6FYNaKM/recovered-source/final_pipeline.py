import uproot
import pandas as pd
import numpy as np
from itertools import combinations
import os
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def main():
    # --- 1. Build Dataset ---
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
    genjet_pt, genjet_eta, genjet_phi, genjet_m = data['genjet_pt'], data['genjet_eta'], data['genjet_phi'], data['genjet_m']
    truth_cols = ['truth_triplet_0', 'truth_triplet_1', 'truth_triplet_2', 'truth_triplet_3']
    for i in range(len(numbers)):
        eid, nj = numbers[i], n_genjets[i]
        if nj < 3: continue
        pt, eta, phi, m = np.asarray(genjet_pt[i]), np.asarray(genjet_eta[i]), np.asarray(genjet_phi[i]), np.asarray(genjet_m[i])
        px, py, pz = pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta)
        e = np.sqrt(pt**2 + pz**2 + m**2)
        truth_triplets = []
        for col in truth_cols:
            t = data[col][i]
            if t is not None and len(t) == 3 and all(idx >= 0 for idx in t): truth_triplets.append(set(t))
        for combo in combinations(range(nj), 3):
            idx_i, idx_j, idx_k = combo
            is_truth = 1 if set(combo) in truth_triplets else 0
            deta_ij, dphi_ij = eta[idx_i]-eta[idx_j], np.abs(phi[idx_i]-phi[idx_j])
            dr_ab = np.sqrt(deta_ij**2 + np.minimum(dphi_ij, 2*np.pi-dphi_ij)**2)
            deta_ik, dphi_ik = eta[idx_i]-eta[idx_k], np.abs(phi[idx_i]-phi[idx_k])
            dr_ac = np.sqrt(deta_ik**2 + np.minimum(dphi_ik, 2*np.pi-dphi_ik)**2)
            deta_jk, dphi_jk = eta[idx_j]-eta[idx_k], np.abs(phi[idx_j]-phi[idx_k])
            dr_bc = np.sqrt(deta_jk**2 + np.minimum(dphi_jk, 2*np.pi-dphi_jk)**2)
            e_abc, px_abc, py_abc, pz_abc = e[idx_i]+e[idx_j]+e[idx_k], px[idx_i]+px[idx_j]+px[idx_k], py[idx_i]+py[idx_j]+py[idx_k], pz[idx_i]+pz[idx_j]+pz[idx_k]
            m_abc = np.sqrt(max(0, e_abc**2 - px_abc**2 - py_abc**2 - pz_abc**2))
            def get_m(ia, ib): return np.sqrt(max(0, (e[ia]+e[ib])**2 - (px[ia]+px[ib])**2 - (py[ia]+py[ib])**2 - (pz[ia]+pz[ib])**2))
            m_ab, m_ac, m_bc = get_m(idx_i, idx_j), get_m(idx_i, idx_k), get_m(idx_j, idx_k)
            all_triplets.append({'event_id': eid, 'i': idx_i, 'j': idx_j, 'k': idx_k, 'is_truth': is_truth,
                                'dr_ab': dr_ab, 'dr_ac': dr_ac, 'dr_bc': dr_bc,
                                'mij_over_m123_ab': m_ab/m_abc if m_abc > 0 else 0,
                                'mij_over_m123_ac': m_ac/m_abc if m_abc > 0 else 0,
                                'mij_over_m123_bc': m_bc/m_abc if m_abc > 0 else 0,
                                'triplet_mass': m_abc, 'triplet_pt': np.sqrt(px_abc**2 + py_abc**2),
                                'triplet_eta': np.arcsinh(pz_abc/np.sqrt(px_abc**2+py_abc**2)) if (px_abc**2+py_abc**2)>0 else 0,
                                'triplet_phi': np.arctan2(py_abc, px_abc)})
    df = pd.DataFrame(all_triplets)
    df.to_parquet(output_path)

    # --- 2. Prepare Data ---
    unique_events = df['event_id'].unique()
    train_events, test_events = train_test_split(unique_events, test_size=0.2, random_state=42)
    train_events, val_events = train_test_split(train_events, test_size=0.2, random_state=42)
    train_df = df[df['event_id'].isin(train_events)]
    val_df = df[df['event_id'].isin(val_events)]
    test_df = df[df['event_id'].isin(test_events)]
    os.makedirs('/root/results/dataset_prepare', exist_ok=True)
    train_df.to_parquet('/root/results/dataset_prepare/train.parquet')
    val_df.to_parquet('/root/results/dataset_prepare/val.parquet')
    test_df.to_parquet('/root/results/dataset_prepare/test.parquet')

    # --- 3. Train Model ---
    features = ['dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc', 'triplet_mass', 'triplet_pt']
    X_train, y_train = train_df[features], train_df['is_truth']
    X_val, y_val = val_df[features], val_df['is_truth']
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, scale_pos_weight=scale_pos_weight, random_state=42)
    model.fit(X_train, y_train)
    y_prob_val = model.predict_proba(X_val)[:, 1]
    auc_val = roc_auc_score(y_val, y_prob_val)
    os.makedirs('/root/results/train', exist_ok=True)
    model.get_booster().save_model('/root/results/train/model_xgb.json')
    with open('/root/results/train/training_report_xgb.json', 'w') as f:
        json.dump({'validation_auc': float(auc_val), 'features': features}, f, indent=4)

    # --- 4. Inference ---
    dtest = xgb.DMatrix(test_df[features])
    test_probs = model.get_booster().predict(dtest)
    test_df = test_df.copy()
    test_df['score_xgb'] = test_probs
    os.makedirs('/root/results/infer', exist_ok=True)
    test_df[['event_id', 'i', 'j', 'k', 'is_truth', 'score_xgb']].to_parquet('/root/results/infer/inference_test_xgb.parquet')
    with open('/root/results/infer/inference_report_xgb.json', 'w') as f:
        json.dump({'test_auc': float(roc_auc_score(test_df['is_truth'], test_df['score_xgb']))}, f, indent=4)

    # --- 5. Selection ---
    selected_triplets, event_summary = [], []
    total_truth = test_df['is_truth'].sum()
    recovered_truth = 0
    for eid, group in test_df.groupby('event_id'):
        group = group.sort_values('score_xgb', ascending=False)
        selected_in_event, used_jets = [], set()
        for _, row in group.iterrows():
            if len(selected_in_event) >= 2: break
            jets = {int(row['i']), int(row['j']), int(row['k'])}
            if jets.isdisjoint(used_jets):
                selected_in_event.append(row)
                used_jets.update(jets)
                if row['is_truth'] == 1: recovered_truth += 1
        for rank, row in enumerate(selected_in_event):
            selected_triplets.append({
                'event_id': eid, 'selected_rank': rank + 1, 'i': int(row['i']), 'j': int(row['j']), 'k': int(row['k']),
                'score': row['score_xgb'], 'triplet_pt': row['triplet_pt'], 'triplet_eta': row['triplet_eta'],
                'triplet_phi': row['triplet_phi'], 'triplet_mass': row['triplet_mass']
            })
        n_sel = len(selected_in_event)
        top1 = selected_in_event[0] if n_sel >= 1 else None
        event_summary.append({
            'event_id': eid, 'n_top_selected': n_sel,
            'top1_pt': top1['triplet_pt'] if top1 is not None else 0.0,
            'top1_eta': top1['triplet_eta'] if top1 is not None else 0.0,
            'top1_phi': top1['triplet_phi'] if top1 is not None else 0.0,
            'top1_mass': top1['triplet_mass'] if top1 is not None else 0.0,
        })
    os.makedirs('/root/results/select_triplets', exist_ok=True)
    pd.DataFrame(selected_triplets).to_parquet('/root/results/select_triplets/selected_triplets.parquet')
    pd.DataFrame(event_summary).to_parquet('/root/results/select_triplets/event_selection.parquet')
    efficiency = recovered_truth / total_truth if total_truth > 0 else 0
    with open('/root/results/select_triplets/selection_report.json', 'w') as f:
        json.dump({'triplet_reconstruction_efficiency': float(efficiency), 'total_truth_triplets': int(total_truth), 'recovered_truth_triplets': int(recovered_truth), 'selection_strategy': 'greedy_score_disjoint_jets', 'max_candidates_per_event': 2}, f, indent=4)
    print(f"Final Efficiency: {efficiency:.4f}")

if __name__ == "__main__":
    main()
