import pandas as pd
from sklearn.model_selection import train_test_split
import os
def main():
    df = pd.read_parquet("/root/results/dataset_build/triplets_raw.parquet")

    # We split by event_id to avoid data leakage
    event_ids = df["event_id"].unique()
    train_events, test_events = train_test_split(event_ids, test_size=0.2, random_state=42)
    train_val_events, val_events = train_test_split(train_events, test_size=0.1, random_state=42)

    train_df = df[df["event_id"].isin(train_val_events)]
    val_df = df[df["event_id"].isin(val_events)]
    test_df = df[df["event_id"].isin(test_events)]

    os.makedirs("/root/results/dataset_prepare", exist_ok=True)
    train_df.to_parquet("/root/results/dataset_prepare/train.parquet")
    val_df.to_parquet("/root/results/dataset_prepare/val.parquet")
    test_df.to_parquet("/root/results/dataset_prepare/test.parquet")

    print(f"Train: {len(train_df)} triplets, Val: {len(val_df)} triplets, Test: {len(test_df)} triplets")
if __name__ == "__main__":
    main()
