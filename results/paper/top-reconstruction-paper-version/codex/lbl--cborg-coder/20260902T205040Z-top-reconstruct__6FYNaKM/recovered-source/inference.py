import pandas as pd
import numpy as np
import xgboost as xgb
import os
import json

def main():
    test_path = '/root/results/dataset_prepare/test.parquet'
    model_path = '/root/results/train/model_xgb.json'
    output_path = '/root/results/infer/inference_test_xgb.parquet'
    report_path = '/root/results/infer/inference_report_xgb.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df = pd.read_parquet(test_path)
    features = ['dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc', 'triplet_mass']
    
    bst = xgb.Booster()
    bst.load_model(model_path)
    
    dtest = xgb.DMatrix(df[features])
    probs = bst.predict(dtest)
    
    df['score_xgb'] = probs
    cols = ['event_id', 'i', 'j', 'k', 'is_truth', 'score_xgb']
    df[cols].to_parquet(output_path)
    
    from sklearn.metrics import roc_auc_score
    auc_test = roc_auc_score(df['is_truth'], df['score_xgb'])
    report = {'test_auc': float(auc_test)}
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"Inference complete. Test AUC: {auc_test:.4f}")

if __name__ == "__main__":
    main()
