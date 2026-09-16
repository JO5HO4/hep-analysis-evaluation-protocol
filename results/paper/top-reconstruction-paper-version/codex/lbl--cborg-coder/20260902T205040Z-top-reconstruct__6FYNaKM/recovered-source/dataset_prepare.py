import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def main():
    input_path = '/root/results/dataset_build/triplets_raw.parquet'
    output_dir = '/root/results/dataset_prepare'
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_parquet(input_path)
    
    # Split by event
    unique_events = df['event_id'].unique()
    train_events, test_events = train_test_split(unique_events, test_size=0.2, random_state=42)
    train_events, val_events = train_test_split(train_events, test_size=0.2, random_state=42)
    
    train_df = df[df['event_id'].isin(train_events)]
    val_df = df[df['event_id'].isin(val_events)]
    test_df = df[df['event_id'].isin(test_events)]
    
    train_df.to_parquet(f'{output_dir}/train.parquet')
    val_df.to_parquet(f'{output_dir}/val.parquet')
    test_df.to_parquet(f'{output_dir}/test.parquet')
    
    print(f"Split events: Train {len(train_events)}, Val {len(val_events)}, Test {len(test_events)}")
    print(f"Split triplets: Train {len(train_df)}, Val {len(val_df)}, Test {len(test_df)}")

if __name__ == "__main__":
    main()
