import pandas as pd
import numpy as np
import xgboost as xgb
import json
import os
def main():
    test_df = pd.read_parquet("/root/results/dataset_prepare/test.parquet")
    features = ["dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc"]

    # Load model
    model = xgb.XGBClassifier()
    model.load_model("/root/results/train/model_xgb.json")

    X_test = test_df[features]
    probs = model.predict_proba(X_test)[:, 1]

    # Result dataframe
    res_df = test_df[["event_id", "i", "j", "k", "is_truth"]].copy()
    res_df["score_xgb"] = probs

    os.makedirs("/root/results/infer", exist_ok=True)
    res_df.to_parquet("/root/results/infer/inference_test_xgb.parquet")

    # Summary report
    # Calculate some basic stats
    num_truth = res_df["is_truth"].sum()
    # a simple metric: fraction of truth triplets with score > 0.5
    high_score_truth = res_df[(res_df["is_truth"] == 1) & (res_df["score_xgb"] > 0.5)].shape[0]

    report = {
        "test_size": len(res_df),
        "num_truth": int(num_truth),
        "truth_recall_at_05": float(high_score_truth / num_truth) if num_truth > 0 else 0
    }
    with open("/root/results/infer/inference_report_xgb.json", "w") as f:
        json.dump(report, f, indent=4)

    print("Inference completed and results saved.")
if __name__ == "__main__":
    main()
