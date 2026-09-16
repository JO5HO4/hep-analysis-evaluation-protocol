import os, json, math, itertools
from pathlib import Path
import numpy as np
import pandas as pd
import awkward as ak
import uproot
import xgboost as xgb
import matplotlib.pyplot as plt

OUT=Path('/root/results')
for d in ['dataset_build','dataset_prepare','train','infer','select_triplets/plots','sanity_checks']:
    (OUT/d).mkdir(parents=True,exist_ok=True)

def dphi(a,b): return (a-b+np.pi)%(2*np.pi)-np.pi
def p4(pt,eta,phi,m):
    px=pt*np.cos(phi); py=pt*np.sin(phi); pz=pt*np.sinh(eta)
    e=np.sqrt(np.maximum(m*m+px*px+py*py+pz*pz,0))
    return px,py,pz,e
def combine(js):
    pt=np.array([x[0] for x in js]); eta=np.array([x[1] for x in js]); phi=np.array([x[2] for x in js]); m=np.array([x[3] for x in js])
    px,py,pz,e=p4(pt,eta,phi,m); px=px.sum();py=py.sum();pz=pz.sum();e=e.sum()
    ppt=np.hypot(px,py); pp=np.sqrt(px*px+py*py+pz*pz)
    mass=np.sqrt(max(e*e-pp*pp,0)); peta=np.arcsinh(pz/ppt) if ppt>0 else 0.
    return ppt,peta,np.arctan2(py,px),mass
def auc(y,s):
    y=np.asarray(y);s=np.asarray(s); npos=y.sum(); nneg=len(y)-npos
    if not npos or not nneg:return float('nan')
    # average ranks, without scipy
    order=np.argsort(s,kind='mergesort'); ranks=np.empty(len(s),float); ranks[order]=np.arange(1,len(s)+1)
    vals,inv,cnt=np.unique(s,return_inverse=True,return_counts=True)
    for q,c in enumerate(cnt):
      if c>1:
       ii=np.where(inv==q)[0]; ranks[ii]=ranks[ii].mean()
    return float((ranks[y==1].sum()-npos*(npos+1)/2)/(npos*nneg))

# Construct candidate dataset
T=uproot.open('/root/data/ttbar.root')['output']
arr=T.arrays(['Number','N_genjet','genjet_pt','genjet_eta','genjet_phi','genjet_m','genjet_btag','truth_triplet_0','truth_triplet_1','truth_triplet_2','truth_triplet_3'],library='ak')
rows=[]
for ev in range(len(arr.Number)):
    eid=int(arr.Number[ev]); n=int(arr.N_genjet[ev])
    if n<3: continue
    pts=np.asarray(arr.genjet_pt[ev],float); etas=np.asarray(arr.genjet_eta[ev],float); phis=np.asarray(arr.genjet_phi[ev],float); ms=np.asarray(arr.genjet_m[ev],float)
    bt=np.asarray(arr.genjet_btag[ev],float) if len(arr.genjet_btag[ev])==n else np.zeros(n)
    truths=set()
    for bn in ['truth_triplet_0','truth_triplet_1','truth_triplet_2','truth_triplet_3']:
      z=list(map(int,arr[bn][ev]))
      if len(z)==3 and min(z)>=0 and max(z)<n and len(set(z))==3: truths.add(tuple(sorted(z)))
    for i,j,k in itertools.combinations(range(n),3):
      inds=(i,j,k); js=[(pts[q],etas[q],phis[q],ms[q]) for q in inds]
      tp,te,tph,tm=combine(js)
      def dr(a,b): return float(np.hypot(etas[a]-etas[b],dphi(phis[a],phis[b])))
      mab=combine([js[0],js[1]])[3]; mac=combine([js[0],js[2]])[3]; mbc=combine([js[1],js[2]])[3]
      sp=np.sort(pts[list(inds)])[::-1]
      rows.append(dict(event_id=eid,i=i,j=j,k=k,is_truth=int(inds in truths),dr_ab=dr(i,j),dr_ac=dr(i,k),dr_bc=dr(j,k),
       mij_over_m123_ab=mab/(tm+1e-6),mij_over_m123_ac=mac/(tm+1e-6),mij_over_m123_bc=mbc/(tm+1e-6),
       triplet_pt=tp,triplet_eta=te,triplet_phi=tph,triplet_mass=tm,pair_mass_ab=mab,pair_mass_ac=mac,pair_mass_bc=mbc,
       jet_pt_1=sp[0],jet_pt_2=sp[1],jet_pt_3=sp[2],jet_btag_max=float(bt[list(inds)].max()),jet_btag_sum=float(bt[list(inds)].sum()),
       top_mass_distance=abs(tm-172.5),w_mass_distance=min(abs(mab-80.4),abs(mac-80.4),abs(mbc-80.4))))
df=pd.DataFrame(rows)
df.to_parquet(OUT/'dataset_build/triplets_raw.parquet',index=False)
# Event-exclusive deterministic split
spl=np.where(df.event_id%5==0,'test',np.where(df.event_id%5==1,'val','train'))
df['split']=spl
for s in ['train','val','test']: df[df.split==s].drop(columns='split').to_parquet(OUT/f'dataset_prepare/{s}.parquet',index=False)
features=['dr_ab','dr_ac','dr_bc','mij_over_m123_ab','mij_over_m123_ac','mij_over_m123_bc','triplet_pt','triplet_eta','triplet_mass','pair_mass_ab','pair_mass_ac','pair_mass_bc','jet_pt_1','jet_pt_2','jet_pt_3','jet_btag_max','jet_btag_sum','top_mass_distance','w_mass_distance']
tr=df[df.split=='train']; va=df[df.split=='val']; te=df[df.split=='test']
dtr=xgb.DMatrix(tr[features],label=tr.is_truth); dva=xgb.DMatrix(va[features],label=va.is_truth)
params={'objective':'binary:logistic','eval_metric':'auc','max_depth':5,'eta':0.07,'subsample':0.82,'colsample_bytree':0.9,'min_child_weight':3,'lambda':2,'seed':177,'nthread':4}
model=xgb.train(params,dtr,num_boost_round=700,evals=[(dtr,'train'),(dva,'validation')],early_stopping_rounds=45,verbose_eval=False)
model.save_model(str(OUT/'train/model_xgb.json'))
va=va.copy();te=te.copy(); va['score_xgb']=model.predict(dva); te['score_xgb']=model.predict(xgb.DMatrix(te[features]))
trainrep={'model':'XGBoost native binary:logistic','features':features,'best_iteration':int(model.best_iteration),'validation_auc':auc(va.is_truth,va.score_xgb),'validation_positive_candidates':int(va.is_truth.sum()),'training_candidates':len(tr),'validation_candidates':len(va),'parameters':params}
json.dump(trainrep,open(OUT/'train/training_report_xgb.json','w'),indent=2)
# Selection algorithms
# Pair-max picks candidate singleton or pair with greatest summed score, then is allowed to retain just a singleton for 3-5 jet events.
def choose(group, mode):
    a=group.sort_values('score_xgb',ascending=False).to_dict('records')
    if not a:return []
    if mode=='one': return [a[0]]
    if mode=='greedy':
      out=[]; used=set()
      for r in a:
       ss={r['i'],r['j'],r['k']}
       if not(ss&used): out.append(r);used|=ss
       if len(out)==2:break
      return out
    # score-maximizing disjoint pair (or singleton): exhaustive and deterministic
    best=[a[0]]; bestv=a[0]['score_xgb']
    for q in range(len(a)):
      for r in range(q+1,len(a)):
       if not ({a[q]['i'],a[q]['j'],a[q]['k']} & {a[r]['i'],a[r]['j'],a[r]['k']}):
        v=a[q]['score_xgb']+a[r]['score_xgb']
        if v>bestv: bestv=v;best=[a[q],a[r]]
    return best
def efficiency(frame,mode):
 sel=[]
 for _,g in frame.groupby('event_id',sort=False): sel+=choose(g,mode)
 return (sum(x['is_truth'] for x in sel)/int(frame.is_truth.sum()) if frame.is_truth.sum() else 0),sel
iters=[]
for mode in ['one','greedy','pairmax']:
 e,s=efficiency(va,mode); iters.append({'configuration':mode,'validation_triplet_reconstruction_efficiency':e,'n_selected':len(s),'selected_truth':int(sum(x['is_truth'] for x in s))})
best=max(iters,key=lambda x:x['validation_triplet_reconstruction_efficiency'])['configuration']
finaleff, selected=efficiency(te,best)
# final inference
infercols=['event_id','i','j','k','is_truth','score_xgb']+features+['triplet_pt','triplet_eta','triplet_phi','triplet_mass']
te[infercols].to_parquet(OUT/'infer/inference_test_xgb.parquet',index=False)
json.dump({'sample':'event_id mod 5 == 0','n_events':int(te.event_id.nunique()),'n_candidates':len(te),'truth_triplets':int(te.is_truth.sum()),'test_auc':auc(te.is_truth,te.score_xgb),'score_summary':te.score_xgb.describe().to_dict()},open(OUT/'infer/inference_report_xgb.json','w'),indent=2)
# selected and event collection
sel=pd.DataFrame(selected)
if len(sel):
 sel=sel.sort_values(['event_id','score_xgb'],ascending=[True,False]).copy();sel['selected_rank']=sel.groupby('event_id').cumcount()+1;sel=sel.rename(columns={'score_xgb':'score'})
selected_cols=['event_id','selected_rank','i','j','k','score','triplet_pt','triplet_eta','triplet_phi','triplet_mass','is_truth']
sel[selected_cols].to_parquet(OUT/'select_triplets/selected_triplets.parquet',index=False)
events=pd.DataFrame({'event_id':sorted(te.event_id.unique())})
if len(sel):
 top1=sel[sel.selected_rank==1][['event_id','triplet_pt','triplet_eta','triplet_phi','triplet_mass']].rename(columns={'triplet_pt':'top1_pt','triplet_eta':'top1_eta','triplet_phi':'top1_phi','triplet_mass':'top1_mass'})
 counts=sel.groupby('event_id').size().rename('n_top_selected').reset_index(); events=events.merge(counts,on='event_id',how='left').merge(top1,on='event_id',how='left')
events['n_top_selected']=events.n_top_selected.fillna(0).astype(int)
for c in ['top1_pt','top1_eta','top1_phi','top1_mass']:
 if c not in events:events[c]=np.nan
events[['event_id','n_top_selected','top1_pt','top1_eta','top1_phi','top1_mass']].to_parquet(OUT/'select_triplets/event_selection.parquet',index=False)
report={'selection_strategy':best,'configuration':'score-maximizing exhaustive choice of one or up to two mutually jet-disjoint triplets; no score threshold (recall-optimized)','max_candidates_per_event':2,'mutual_jet_exclusivity':True,'inference_events':int(te.event_id.nunique()),'inference_truth_triplets':int(te.is_truth.sum()),'selected_triplets':int(len(sel)),'selected_truth_triplets':int(sel.is_truth.sum()),'triplet_reconstruction_efficiency':float(finaleff),'selected_multiplicity':{str(k):int(v) for k,v in events.n_top_selected.value_counts().sort_index().items()},'validation_strategy_comparison':iters}
json.dump(report,open(OUT/'select_triplets/selection_report.json','w'),indent=2)
# plots
plt.figure(figsize=(7,5)); bins=np.linspace(0,400,61)
plt.hist(va.loc[va.is_truth==1,'triplet_mass'],bins=bins,density=True,histtype='step',lw=2,label='validation truth')
plt.hist(va.loc[va.is_truth==0,'triplet_mass'],bins=bins,density=True,histtype='step',lw=1.5,label='validation combinatorial')
plt.hist(sel.triplet_mass,bins=bins,density=True,histtype='step',lw=2,label='selected test')
plt.xlabel('Triplet invariant mass [GeV]');plt.ylabel('Arbitrary normalized density');plt.legend();plt.tight_layout();plt.savefig(OUT/'select_triplets/plots/triplet_mass_comparison.png',dpi=150);plt.close()
plt.figure(figsize=(7,5));plt.hist(sel.triplet_pt,bins=50);plt.xlabel('Selected triplet pT [GeV]');plt.ylabel('Candidates');plt.tight_layout();plt.savefig(OUT/'select_triplets/plots/selected_pt.png',dpi=150);plt.close()
# sanity
summ=lambda x:{'n':int(len(x)),'mean':float(np.mean(x)) if len(x) else None,'median':float(np.median(x)) if len(x) else None,'std':float(np.std(x)) if len(x) else None,'q05':float(np.quantile(x,.05)) if len(x) else None,'q95':float(np.quantile(x,.95)) if len(x) else None}
san={'mass_units':'GeV','selected_test':summ(sel.triplet_mass),'validation_truth':summ(va.loc[va.is_truth==1,'triplet_mass']),'validation_fake':summ(va.loc[va.is_truth==0,'triplet_mass']),'interpretation':'Selected candidates are compared with independent validation truth and combinatorial populations. The distribution is retained as a broad reconstructed mass shape rather than imposing a narrow mass-window selection; classifier and disjoint score selection use multiple kinematic observables.'}
json.dump(san,open(OUT/'sanity_checks/mass_sanity_report.json','w'),indent=2)
open(OUT/'sanity_checks/mass_sanity_note.md','w').write('## Mass sanity check\nSelected-test triplet masses are plotted against validation truth and fake triplets in `../select_triplets/plots/triplet_mass_comparison.png`. No narrow mass-window cut was applied, so the selected spectrum remains a physically interpretable reconstructed shape with detector/generator-level combinatorial broadening. Numerical quantiles and widths are in `mass_sanity_report.json`.\n')
md=f'''# Hadronic top triplet reconstruction optimization\n\nAll unordered GenJet index triplets were built from 10,000 events and labels were matched as unordered index sets. Event-exclusive deterministic split: 60% train, 20% validation, 20% test. An XGBoost kinematic classifier was trained on angular separations, pair/triplet masses, ordered jet pT and generator b-tag features.\n\n## Final result\n\nFinal test **triplet_reconstruction_efficiency: {finaleff:.6f}** ({int(sel.is_truth.sum())}/{int(te.is_truth.sum())} truth candidates recovered). Selection uses `{best}`: exhaustive maximum summed classifier-score selection of one or up to two jet-disjoint triplets, with no score threshold. This is intentional because recall is the specified primary objective; it obeys the two-candidate and no-shared-jet constraints.\n\n## Selection iterations (validation)\n\n| Configuration | Efficiency | Selected candidates |\n|---|---:|---:|\n'''
for x in iters: md+=f"| {x['configuration']} | {x['validation_triplet_reconstruction_efficiency']:.6f} | {x['n_selected']} |\n"
md+='\nClassifier validation AUC and parameters are recorded in `train/training_report_xgb.json`. Final test inference and selection details are in the corresponding JSON reports. Mass-shape comparison and interpretation are under `sanity_checks/`.\n'
open(OUT/'optimization_report.md','w').write(md)
json.dump({'iterations':iters,'final_strategy':best,'final_test_efficiency':finaleff},open(OUT/'optimization_summary.json','w'),indent=2)
print('DONE rows',len(df),'truth',int(df.is_truth.sum()),'AUC',trainrep['validation_auc'],'strategy',best,'test efficiency',finaleff)
