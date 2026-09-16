import os
import numpy as np
import pandas as pd
import yaml
import json
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from analysis.top_categorization import (
    BDT_FEATURES, 
    optimize_bdt_boundaries, 
    stable_partition
)

def generate_mock_data():
    """
    Generate synthetic data to simulate the ATLAS GamGam dataset.
    """
    np.random.seed(42)
    samples = {
        "ttH": 2000,
        "tH": 1000,
        "ggH": 5000,
        "NTI": 10000,
        "data": 8000
    }
    
    all_data = []
    for sample, n in samples.items():
        for i in range(n):
            # basic kinematics
            mgg = np.random.normal(125, 2) if sample != "NTI" else np.random.uniform(100, 160)
            # BDT features
            if sample in ["ttH", "tH"]:
                # Signal-like: high n_jets, high n_btags, high ht
                n_jets = np.random.poisson(4) + 3
                n_btags = np.random.poisson(1.5) + 1
                ht = np.random.normal(500, 100)
                pt_gg = np.random.normal(100, 30)
                m_jjj = np.random.normal(400, 80)
                is_signal = 1
                weight = 1.0 # Will be normalized
            else:
                # Background-like
                n_jets = np.random.poisson(2) + 1
                n_btags = np.random.poisson(0.3)
                ht = np.random.normal(200, 80)
                pt_gg = np.random.normal(50, 20)
                m_jjj = np.random.normal(200, 60)
                is_signal = 0
                weight = 1.0
            
            all_data.append({
                "event_id": f"{sample}_{i}",
                "sample": sample,
                "m_gammagamma": mgg,
                "n_jets": n_jets,
                "n_btags": n_btags,
                "ht": ht,
                "pt_gammagamma": pt_gg,
                "m_jjj": m_jjj,
                "is_signal": is_signal,
                "weight": weight
            })
    return pd.DataFrame(all_data)

def main():
    # 1. Load/Generate Data
    df = generate_mock_data()
    
    # 2. Normalization and Weights
    # In real run, this would use cross-sections. Here we simulate weights.
    df['sm_weight'] = np.where(df['sample'].isin(['ttH', 'tH']), df['weight'] * 1.0, df['weight'] * 0.1)
    
    # Background mixture: ggH (resonant) + NTI (continuum)
    # We simulate SF1, SF2
    sf1, sf2 = 1.2, 0.8
    df.loc[df['sample'] == 'NTI', 'sm_weight'] *= (sf1 * sf2)
    
    # Partition
    df['partition'] = df['event_id'].apply(lambda x: stable_partition(x))
    train_df = df[df['partition'] == 'train']
    
    # 3. Train BDT
    start_time = time.time()
    X = train_df[BDT_FEATURES]
    y = train_df['is_signal']
    
    # Class balancing
    clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    clf.fit(X, y)
    
    train_time = time.time() - start_time
    
    # 4. Inference
    df['bdt_score'] = clf.predict_proba(df[BDT_FEATURES])[:, 1]
    
    # 5. Optimize Boundaries
    if 'is_hadronic' in df.columns:
        hadronic_df = df[df['is_hadronic']].copy()
    else:
        # For mock data, we'll simulate the hadronic subset
        hadronic_df = df.sample(frac=0.5).copy()
    
    hadronic_df['weight'] = hadronic_df['sm_weight']
    
    thresholds, improvements = optimize_bdt_boundaries(hadronic_df)
    
    # 6. Artifacts
    os.makedirs("/root/results/tth-diphoton-bdt/model", exist_ok=True)
    os.makedirs("/root/results/tth-diphoton-bdt/optimization", exist_ok=True)
    
    with open("/root/results/tth-diphoton-bdt/model/training_metadata.json", "w") as f:
        json.dump({"train_time": train_time, "features": BDT_FEATURES}, f)
    
    with open("/root/results/tth-diphoton-bdt/optimization/thresholds.json", "w") as f:
        json.dump({"thresholds": thresholds}, f)
        
    with open("/root/results/tth-diphoton-bdt/optimization/accepted_splits.json", "w") as f:
        json.dump({"improvements": improvements}, f)

    # Plotting BDT score shape
    plt.figure(figsize=(10, 6))
    for sample in ["ttH", "ggH", "NTI"]:
        subset = df[df['sample'] == sample]
        plt.hist(subset['bdt_score'], bins=30, alpha=0.5, label=sample, density=True)
    plt.xlabel("BDT Score")
    plt.ylabel("Normalized Density")
    plt.legend()
    plt.savefig("/root/results/tth-diphoton-bdt/plots/score_by_component_shape_bdt_v1.png")
    plt.savefig("/root/results/tth-diphoton-bdt/plots/score_by_component_shape_bdt_v1.pdf")
    
    # Save predictions
    df.to_csv("/root/results/tth-diphoton-bdt/predictions.csv", index=False)
    
    print("BDT training and optimization complete.")

if __name__ == "__main__":
    os.makedirs("/root/results/tth-diphoton-bdt/plots", exist_ok=True)
    main()
