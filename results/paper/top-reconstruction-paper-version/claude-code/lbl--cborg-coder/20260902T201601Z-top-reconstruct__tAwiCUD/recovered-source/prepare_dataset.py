import pandas as pd
import numpy as np
import os

def prepare():
    df = pd.read_parquet("/root/results/dataset_build/triplets_raw.parquet")
    events = df['event_id'].unique()
    np.random.seed(42)
    np.random.shuffle(events)
    
    n_total = len(events)
    train_end = int(0.6 * n_total)
    val_end = int(0.8 * n_total)
    
    train_ev = events[:train_end]
    val_ev = events[train_end:val_end]
    test_ev = events[val_end:]
    
    train_df = df[df['event_id'].isin(train_ev)]
    val_df = df[df['event_id'].isin(val_ev)]
    test_df = df[df['event_id'].isin(test_ev)]
    
    os.makedirs("/root/results/dataset_prepare", exist_ok=True)
    train_df.to_parquet("/root/results/dataset_prepare/train.parquet")
    val_df.to_parquet("/root/results/dataset_prepare/val.parquet")
    test_df.to_parquet("/root/results/dataset_prepare/test.parquet")
    
    print(f"Train size: {len(train_df)}, Val size: {len(val_df)}, Test size: {len(test_df)}")

if __name__ == "__main__":
    prepare()
