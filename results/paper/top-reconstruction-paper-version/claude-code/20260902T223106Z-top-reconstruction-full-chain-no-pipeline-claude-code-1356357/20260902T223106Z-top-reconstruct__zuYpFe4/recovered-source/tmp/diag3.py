import sys, numpy as np, pandas as pd
sys.path.insert(0,'/root/pipeline')
from cv import cv_config
r,oof=cv_config({"name":"diag","feature_set":"kin_btag_compl","params":{"nthread":32}},verbose=True)
df=pd.read_parquet('/root/results/dataset_build/triplets_raw.parquet'); df["s"]=oof
np.save('/tmp/oof_kbc.npy',oof)
tr=df[df.is_truth==1].copy()
rank=df.groupby("event_id")["s"].rank(ascending=False,method="first")
df["rank"]=rank; tr=df[df.is_truth==1]
got=tr["rank"]<=1
print("\nMISSED (rank>1) vs FOUND (rank1) truth triplets:")
for name,sub in (("found",tr[got]),("missed",tr[~got])):
    print(f" {name}: n={len(sub)} mass med={sub.triplet_mass.median():.1f} mean={sub.triplet_mass.mean():.1f} "
          f"mW_nonb med={sub.mW_nonb.median():.1f} n_btag med={sub.n_btag.median():.1f} "
          f"drmax med={sub.dr_max.median():.2f} minjetpt med={sub.jet_pt_c.median():.1f}")
print("\ntruth mass quantiles:", np.round(np.quantile(tr.triplet_mass,[.05,.25,.5,.75,.95]),1))
print("frac truth with mass in [140,210]:", ((tr.triplet_mass>140)&(tr.triplet_mass<210)).mean())
print("frac FOUND with mass in [140,210]:", ((tr[got].triplet_mass>140)&(tr[got].triplet_mass<210)).mean())
print("frac MISSED with mass in [140,210]:", ((tr[~got].triplet_mass>140)&(tr[~got].triplet_mass<210)).mean())
# how often does a fake beat the truth while being "more top-like"?
print("\nnjet<6 only:")
sub=tr[tr.n_genjet<6]
print(" top1 acc:", (sub['rank']<=1).mean(), " n=",len(sub))
sub2=tr[tr.n_genjet>=6]
print("njet>=6 top1:", (sub2['rank']<=1).mean(), "top2:",(sub2['rank']<=2).mean()," n=",len(sub2))
