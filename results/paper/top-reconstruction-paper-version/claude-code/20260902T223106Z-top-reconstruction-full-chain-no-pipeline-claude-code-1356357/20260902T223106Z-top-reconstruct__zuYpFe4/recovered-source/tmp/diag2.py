import sys, numpy as np, pandas as pd
sys.path.insert(0,'/root/pipeline')
from experiment import get_raw
df=get_raw()
tr=df[df.is_truth==1]
print("truth triplets by n_genjet (all 10k events):")
tot=len(tr)
cum=0
for nj,g in tr.groupby("n_genjet"):
    cum+=len(g)
    print(f"  njet={nj:2d}: {len(g):5d} truths ({len(g)/tot*100:5.1f}%)  cum={cum/tot*100:5.1f}%  n_triplets={int(df[df.n_genjet==nj].n_triplets_event.iloc[0])} maxdisjoint={'2' if nj>=6 else '1'}")
print("\nTruths in events that can only fit ONE candidate (njet<6):", (tr.n_genjet<6).sum(), f"= {(tr.n_genjet<6).mean()*100:.1f}%")
print("Truths in events that can fit TWO (njet>=6):", (tr.n_genjet>=6).sum())
