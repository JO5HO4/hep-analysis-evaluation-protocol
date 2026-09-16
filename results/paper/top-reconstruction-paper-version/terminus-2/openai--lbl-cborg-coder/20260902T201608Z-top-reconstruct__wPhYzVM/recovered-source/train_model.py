import pandas as pd
import xgboost as xgb
import json
from sklearn.metrics import roc_auc_score

train_df = pd.read_parquet('/root/results/dataset_prepare/train.parquet')
val_df = pd.read_parquet('/root/results/dataset_prepare/val.parquet')

features = ['dr_ab', 'dr_ac', 'dr_bc', 'mij_over_m123_ab', 'mij_over_m123_ac', 'mij_over_m123_bc']
target = 'is_truth'

X_train = train_df[features]
y_train = train_df[target]
X_val = val_df[features]
y_val = val_df[target]

num_neg = (y_train == 0).sum()
num_pos = (y_train == 1).sum()
scale_weight = num_neg / num_pos

model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    scale_pos_weight=scale_weight,
    objective='binary:logistic',
    random_state=42
)

model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

probs = model.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, probs)

# Use the booster to save the model as JSON
model.get_booster().save_model('/root/results/train/model_xgb.json')

report = {
    'val_auc': float(val_auc),
    'train_triplets': len(train_df),
    'val_triplets': len(val_df),
    'scale_pos_weight': float(scale_weight)
}
with open('/root/results/train/training_report_xgb.json', 'w') as f:
    json.dump(report, f, indent=4)

print(f'Training complete. Val AUC: {val_auc:.4f}')
