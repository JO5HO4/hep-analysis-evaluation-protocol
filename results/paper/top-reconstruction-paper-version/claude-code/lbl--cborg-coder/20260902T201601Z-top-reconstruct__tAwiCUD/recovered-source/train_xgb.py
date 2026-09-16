import pandas as pd
import numpy as np
import xgboost as xgb
import json
import os

def calculate_auc(y_true, y_scores):
    y_true = np.array(y_true)
    y_scores = np.array(y_scores)
    desc_score_indices = np.argsort(y_scores)[::-1]
    y_true = y_true[desc_score_indices]
    y_scores = y_scores[desc_score_indices]
    tps = np.cumsum(y_true)
    fps = np.cumsum(1 - y_true)
    if tps[-1] == 0 or fps[-1] == 0:
        return 0.5
    return np.trapz(tps/tps[-1], fps/fps[-1])

def train():
    train_df = pd.read_parquet("/root/results/dataset_prepare/train.parquet")
    val_df = pd.read_parquet("/root/results/dataset_prepare/val.parquet")
    
    features = [
        "dr_min", "dr_mid", "dr_max", 
        "ratio_min", "ratio_mid", "ratio_max",
        "m123", "pt123", "pt_min", "pt_mid", "pt_max", "sum_pt"
    ]
    target = "is_truth"
    
    X_train = train_df[features].values
    y_train = train_df[target].values
    X_val = val_df[features].values
    y_val = val_df[target].values
    
    count_neg = np.sum(y_train == 0)
    count_pos = np.sum(y_train == 1)
    scale_pos_weight = count_neg / count_pos if count_pos > 0 else 1.0
    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    
    params = {
        "max_depth": 6,
        "eta": 0.05,
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "scale_pos_weight": scale_pos_weight,
        "seed": 42
    }
    
    bst = xgb.train(
        params,
        dtrain,
        num_boost_round=200,
        evals=[(dval, "val")],
        verbose_eval=False,
        early_stopping_rounds=20
    )
    
    preds_val = bst.predict(dval)
    auc_val = calculate_auc(y_val, preds_val)
    
    os.makedirs("/root/results/train", exist_ok=True)
    bst.save_model("/root/results/train/model_xgb.json")
    
    report = {
        "val_auc": float(auc_val),
        "scale_pos_weight": float(scale_pos_weight),
        "n_estimators": 200,
        "max_depth": 6,
        "features": features
    }
    
    with open("/root/results/train/training_report_xgb.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Training complete. Val AUC: {auc_val:.4f}")

if __name__ == "__main__":
    train()
