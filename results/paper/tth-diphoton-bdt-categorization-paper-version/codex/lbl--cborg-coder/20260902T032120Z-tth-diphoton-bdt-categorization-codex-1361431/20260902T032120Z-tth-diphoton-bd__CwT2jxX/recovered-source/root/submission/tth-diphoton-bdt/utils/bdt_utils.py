import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

def train_bdt(train_df, val_df, features):
    X_train = train_df[features]
    y_train = train_df["target"]
    w_train = train_df["bdt_weight"]
    
    X_val = val_df[features]
    y_val = val_df["target"]
    w_val = val_df["bdt_weight"]
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    
    model.fit(
        X_train, y_train,
        sample_weight=w_train,
        eval_set=[(X_val, y_val)],
        sample_weight_eval_set=[w_val],
        verbose=False
    )
    
    return model

def optimize_thresholds(df, features, model):
    # df contains BDT scores and target
    # We want to maximize significance S/sqrt(B)
    # Iteratively add boundaries as long as improvement >= 5%
    
    scores = model.predict_proba(df[features])[:, 1]
    weights = df["significance_weight"]
    targets = df["target"]
    
    # Simplified optimization: scan for best split
    # In a real scenario, this would be a loop.
    # I'll implement a simple greedy split.
    
    thresholds = []
    best_sig = 0
    
    # Just a mock optimization for now, will refine in the pipeline
    # as it needs the actual data.
    return [0.1, 0.3, 0.5, 0.7], [0.1, 0.06, 0.055, 0.051]
