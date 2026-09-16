import pandas as pd
import numpy as np
import xgboost as xgb
import json
import os
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
def main():
    train_df = pd.read_parquet("/root/results/dataset_prepare/train.parquet")
    val_df = pd.read_parquet("/root/results/dataset_prepare/val.parquet")

    features = ["dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc"]
    target = "is_truth"

    X_train = train_df[features]
    y_train = train_df[target]
    X_val = val_df[features]
    y_val = val_df[target]

    # Class balancing: the number of truth triplets is much smaller.
    # Calculate scale_pos_weight
    num_pos = y_train.sum()
    num_neg = len(y_train) - num_pos
    scale_pos_weight = num_neg / num_pos if num_pos > 0 else 1.0

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        objective="binary:logistic",
        random_state=42,
        tree_method="hist"
    )

    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

    # Predict probabilities
    probs = model.predict_proba(X_val)[:, 1]
    val_auc = roc_auc_score(y_val, probs)

    # Save model
    os.makedirs("/root/results/train", exist_ok=True)
    model.save_model("/root/results/train/model_xgb.json")

    # Save report
    report = {
        "validation_auc": float(val_auc),
        "train_size": len(train_df),
        "val_size": len(val_df),
        "scale_pos_weight": float(scale_pos_weight)
    }
    with open("/root/results/train/training_report_xgb.json", "w") as f:
        json.dump(report, f, indent=4)

    print(f"Model trained. Val AUC: {val_auc:.4f}")
if __name__ == "__main__":
    main()
