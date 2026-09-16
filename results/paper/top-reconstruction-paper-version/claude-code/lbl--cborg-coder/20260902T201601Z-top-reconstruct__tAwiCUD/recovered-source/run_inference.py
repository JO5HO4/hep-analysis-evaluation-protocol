import pandas as pd
import numpy as np
import xgboost as xgb
import json
import os

def run():
    test_df = pd.read_parquet("/root/results/dataset_prepare/test.parquet")
    bst = xgb.Booster()
    bst.load_model("/root/results/train/model_xgb.json")
    
    features = [
        "dr_min", "dr_mid", "dr_max", 
        "ratio_min", "ratio_mid", "ratio_max",
        "m123", "pt123", "pt_min", "pt_mid", "pt_max", "sum_pt"
    ]
    X_test = test_df[features].values
    dtest = xgb.DMatrix(X_test)
    
    scores = bst.predict(dtest)
    
    test_df['score_xgb'] = scores
    
    out_df = test_df[['event_id', 'i', 'j', 'k', 'is_truth', 'score_xgb']]
    
    os.makedirs("/root/results/infer", exist_ok=True)
    out_df.to_parquet("/root/results/infer/inference_test_xgb.parquet")
    
    def calculate_auc(y_true, y_scores):
        y_true = np.array(y_true)
        y_scores = np.array(y_scores)
        desc_score_indices = np.argsort(y_scores)[::-1]
        y_true = y_true[desc_score_indices]
        y_scores = y_scores[desc_score_indices]
        tps = np.cumsum(y_true)
        fps = np.cumsum(1 - y_true)
        if tps[-1] == 0 or fps[-1] == 0: return 0.5
        return np.trapz(tps/tps[-1], fps/fps[-1])
    
    auc_test = calculate_auc(test_df['is_truth'], scores)
    
    report = {
        "test_auc": float(auc_test),
        "n_triplets": len(test_df)
    }
    
    with open("/root/results/infer/inference_report_xgb.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Inference complete. Test AUC: {auc_test:.4f}")

if __name__ == "__main__":
    run()
