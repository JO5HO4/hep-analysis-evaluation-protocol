import pandas as pd
import xgboost as xgb
import json
from sklearn.metrics import roc_auc_score

test_df = pd.read_parquet('/root/results/dataset_prepare/test.parquet')
features = ['dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc']

model = xgb.XGBClassifier()
model.load_model('/root/results/train/model_xgb.json')

probs = model.predict_proba(test_df[features])[:, 1]
test_df['score_xgb'] = probs

# Result parquet
out_df = test_df[['event_id', 'i', 'j', 'k', 'is_truth', 'score_xgb']]
out_df.to_parquet('/root/results/infer/inference_test_xgb.parquet')

# Report
val_auc = roc_auc_score(test_df['is_truth'], probs)
report = {'test_auc': float(val_auc)}
with open('/root/results/infer/inference_report_xgb.json', 'w') as f:
    json.dump(report, f, indent=4)

print(f'Inference complete. Test AUC: {val_auc:.4f}')
