import pandas as pd
import numpy as np

df = pd.read_parquet('/root/results/dataset_build/triplets_raw.parquet')

# We must split by event_id to prevent leakage
events = df['event_id'].unique()
np.random.seed(42)
np.random.shuffle(events)

# 60% train, 20% val, 20% test
n = len(events)
train_evs = events[:int(0.6 * n)]
val_evs = events[int(0.6 * n):int(0.8 * n)]
test_evs = events[int(0.8 * n):]

train_df = df[df['event_id'].isin(train_evs)]
val_df = df[df['event_id'].isin(val_evs)]
test_df = df[df['event_id'].isin(test_evs)]

train_df.to_parquet('/root/results/dataset_prepare/train.parquet')
val_df.to_parquet('/root/results/dataset_prepare/val.parquet')
test_df.to_parquet('/root/results/dataset_prepare/test.parquet')

print(f'Train events: {len(train_evs)}, triplets: {len(train_df)}')
print(f'Val events: {len(val_evs)}, triplets: {len(val_df)}')
print(f'Test events: {len(test_evs)}, triplets: {len(test_df)}')
