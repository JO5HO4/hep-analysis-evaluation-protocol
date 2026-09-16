import pandas as pd, numpy as np, xgboost as xgb, json
from pathlib import Path
R=Path('/root/results')
tr=pd.read_parquet(R/'dataset_prepare/train.parquet'); va=pd.read_parquet(R/'dataset_prepare/val.parquet')
features=['dr_ab','dr_ac','dr_bc','mij_over_m123_ab','mij_over_m123_ac','mij_over_m123_bc','triplet_pt','triplet_eta','triplet_mass','pair_mass_ab','pair_mass_ac','pair_mass_bc','jet_pt_1','jet_pt_2','jet_pt_3','jet_btag_max','jet_btag_sum','top_mass_distance','w_mass_distance']
def choose(g):
 a=g.sort_values('score',ascending=False).to_dict('records')
 if not a:return []
 best=[a[0]]; val=a[0]['score']
 for q in range(len(a)):
  for r in range(q+1,len(a)):
   if not (set((a[q]['i'],a[q]['j'],a[q]['k'])) & set((a[r]['i'],a[r]['j'],a[r]['k']))):
    z=a[q]['score']+a[r]['score']
    if z>val: best=[a[q],a[r]];val=z
 return best
def ev(v):
 ss=[]
 for _,g in v.groupby('event_id',sort=False):ss.extend(choose(g))
 return sum(x['is_truth'] for x in ss)/v.is_truth.sum()
D=xgb.DMatrix(tr[features],label=tr.is_truth); V=xgb.DMatrix(va[features],label=va.is_truth)
base={'objective':'binary:logistic','eval_metric':'auc','subsample':.82,'colsample_bytree':.9,'min_child_weight':3,'lambda':2,'seed':177,'nthread':4}
configs=[('baseline',5,.07),('shallow',4,.07),('deep_slow',6,.045)]
out=[]
for name,dep,eta in configs:
 p={**base,'max_depth':dep,'eta':eta}; m=xgb.train(p,D,700,[(V,'v')],early_stopping_rounds=45,verbose_eval=False)
 v=va.copy();v['score']=m.predict(V); res={'name':name,'max_depth':dep,'eta':eta,'best_iteration':int(m.best_iteration),'validation_pairmax_efficiency':ev(v),'validation_auc_xgb':float(m.best_score)};out.append(res);print(res)
json.dump(out,open(R/'train/model_variant_comparison.json','w'),indent=2)
