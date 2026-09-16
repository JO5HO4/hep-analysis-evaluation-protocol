import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import os
import json

def main():
    train_path = '/root/results/dataset_prepare/train.parquet'
    val_path = '/root/results/dataset_prepare/val.parquet'
    model_output = '/root/results/train/model_xgb.json'
    report_output = '/root/results/train/training_report_xgb.json'
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    
    train_df = pd.read_parquet(train_path)
    val_df = pd.read_parquet(val_path)
    
    features = ['dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc', 'triplet_mass', 'triplet_pt']
    target = 'is_truth'
    
    X_train = train_df[features]
    y_train = train_df[target]
    X_val = val_df[features]
    y_val = val_df[target]
    
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric='auc'
    )
    
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    
    y_prob = model.predict_proba(X_val)[:, 1]
    auc_val = roc_auc_score(y_val, y_prob)
    precision, recall, _ = precision_recall_curve(y_val, y_prob)
    pr_auc = auc(recall, precision)
    
    model.get_booster().save_model(model_output)
    
    report = {
        'validation_auc': float(auc_val),
        'validation_pr_auc': float(pr_auc),
        'scale_pos_weight': float(scale_pos_weight),
        'features': features
    }
    with open(report_output, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Model trained. Val AUC: {auc_val:.4f}, PR AUC: {pr_auc:.4f}")

if __name__ == "__main__":
    main()
