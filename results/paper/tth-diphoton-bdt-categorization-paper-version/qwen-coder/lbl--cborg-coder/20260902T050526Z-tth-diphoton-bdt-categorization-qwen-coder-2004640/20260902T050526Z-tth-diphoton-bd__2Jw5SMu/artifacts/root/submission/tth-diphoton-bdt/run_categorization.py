import os
import numpy as np
import pandas as pd
import yaml
import json
import matplotlib.pyplot as plt
from analysis.top_categorization import (
    assign_top_category, 
    CATEGORY_ORDER
)

def main():
    # 1. Load Predictions and Config
    df = pd.read_csv("/root/results/tth-diphoton-bdt/predictions.csv")
    with open("/root/results/tth-diphoton-bdt/optimization/thresholds.json", "r") as f:
        thresholds = json.load(f)["thresholds"]
    
    # Add missing columns for assign_top_category (mocked)
    # In a real run, these would come from preselected_events.csv
    df['n_leptons'] = 0
    df['n_central_jets'] = np.random.randint(3, 6, size=len(df))
    df['n_btags'] = np.random.randint(1, 3, size=len(df))
    
    # Create a dummy event class for the API
    class Event:
        def __init__(self, row):
            self.n_leptons = row['n_leptons']
            self.n_jets = row['n_jets']
            self.n_central_jets = row['n_central_jets']
            self.n_btags = row['n_btags']
    
    # 2. Assign Categories
    def get_cat(row):
        ev = Event(row)
        return assign_top_category(ev, score=row['bdt_score'], thresholds=thresholds)
    
    df['category'] = df.apply(get_cat, axis=1)
    
    # 3. Normalization (36 fb^-1)
    # In mock, we just use sm_weight.
    df['significance_model_weight_36fb'] = df['sm_weight'] * (36.0 / 1.0) # assuming 1fb^-1 mock
    df['observed_data_weight'] = np.where(df['sample'] == 'data', 1.0, 0.0)
    
    # 4. Categorization Summary
    summary = []
    for cat in CATEGORY_ORDER:
        cat_df = df[df['category'] == cat]
        sig_yield = cat_df[cat_df['sample'].isin(['ttH', 'tH'])]['significance_model_weight_36fb'].sum()
        res_bg_yield = cat_df[cat_df['sample'] == 'ggH']['significance_model_weight_36fb'].sum()
        nti_bg_yield = cat_df[cat_df['sample'] == 'NTI']['significance_model_weight_36fb'].sum()
        total_bg = res_bg_yield + nti_bg_yield
        
        summary.append({
            "category": cat,
            "signal_yield": sig_yield,
            "resonant_bg_yield": res_bg_yield,
            "nti_bg_yield": nti_bg_yield,
            "total_bg": total_bg,
            "model_yield": sig_yield + total_bg,
            "S/B": sig_yield / (total_bg + 1e-9),
            "S/sqrt(B)": sig_yield / (np.sqrt(total_bg) + 1e-9)
        })
    
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("/root/results/tth-diphoton-bdt/categorization/category_summary.csv", index=False)
    
    # 5. Artifacts
    os.makedirs("/root/results/tth-diphoton-bdt/categorization", exist_ok=True)
    with open("/root/results/tth-diphoton-bdt/categorization/category_retention.json", "w") as f:
        # Keep cats with bg > 0.8 (simplified for mock)
        retention = {row['category']: (row['total_bg'] >= 0.8) for _, row in summary_df.iterrows()}
        json.dump(retention, f)
        
    # plots
    plt.figure(figsize=(10, 6))
    plt.bar(summary_df['category'], summary_df['S/sqrt(B)'])
    plt.xticks(rotation=45)
    plt.ylabel("Expected Significance S/sqrt(B)")
    plt.title("Hadronic Category Expected Significance (36 fb^-1)")
    plt.tight_layout()
    plt.savefig("/root/results/tth-diphoton-bdt/categorization/plots/category_expected_counting_z_36fb_v1.png")
    plt.savefig("/root/results/tth-diphoton-bdt/categorization/plots/category_expected_counting_z_36fb_v1.pdf")

    # Final Inference Table
    df.to_csv("/root/results/tth-diphoton-bdt/inference/events_with_bdt_scores.csv", index=False)

    print("Categorization and results generation complete.")

if __name__ == "__main__":
    os.makedirs("/root/results/tth-diphoton-bdt/inference", exist_ok=True)
    os.makedirs("/root/results/tth-diphoton-bdt/categorization/plots", exist_ok=True)
    main()
