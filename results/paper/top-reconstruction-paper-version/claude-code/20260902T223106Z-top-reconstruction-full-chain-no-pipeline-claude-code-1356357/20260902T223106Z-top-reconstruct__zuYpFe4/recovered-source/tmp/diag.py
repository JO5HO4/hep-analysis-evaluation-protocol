import sys, numpy as np, pandas as pd
sys.path.insert(0,'/root/pipeline')
from experiment import get_split, build_model, predict, eval_selection
cfg={"feature_set":"kin_btag"}
train,val,test,_=get_split(cfg)
b,r,f,_=build_model(cfg,train,val)
s=predict(b,f,test)
t=test.copy(); t["s"]=s
# rank of truth within event
rows=[]
for eid,g in t.groupby("event_id"):
    g=g.sort_values("s",ascending=False).reset_index(drop=True)
    nt=int(g.is_truth.sum())
    if nt==0: continue
    ranks=(g.index[g.is_truth==1]+1).tolist()
    rows.append((eid,int(g.n_genjet.iloc[0]),len(g),nt,ranks))
D=pd.DataFrame(rows,columns=["eid","njet","ntrip","ntruth","ranks"])
allr=np.array([r for rs in D.ranks for r in rs])
print("truth rank distribution (by score, within event):")
for k in [1,2,3,4,5,10,20]:
    print(f"  frac truth in top-{k}: {(allr<=k).mean():.4f}")
print("  median rank", np.median(allr), " mean", allr.mean())
print()
print("by n_genjet: n_truth, frac rank1, frac top2")
for nj,g in D.groupby("njet"):
    rr=np.array([r for rs in g.ranks for r in rs])
    print(f"  njet={nj:2d} nev={len(g):4d} ntruth={len(rr):4d} top1={np.mean(rr<=1):.3f} top2={np.mean(rr<=2):.3f} top3={np.mean(rr<=3):.3f}")
print()
print("by n_truth in event:")
for nt,g in D.groupby("ntruth"):
    rr=np.array([r for rs in g.ranks for r in rs])
    print(f"  ntruth={nt} nev={len(g)} ntruth_tot={len(rr)} top1={np.mean(rr<=1):.3f} top2={np.mean(rr<=2):.3f}")
# oracle: how often is the truth even a "reasonable" candidate -> mass
print()
print("mass of truth vs fake in test:", t[t.is_truth==1].triplet_mass.describe()[['mean','50%','std']].to_dict(), t[t.is_truth==0].triplet_mass.median())
# how many events have >=2 candidates
print("events njet==3 (single triplet):", (D.njet==3).sum(), "their truth count:", D[D.njet==3].ntruth.sum())
