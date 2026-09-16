#!/usr/bin/env python3
from __future__ import annotations
import os,sys,json,time,math,glob,hashlib,warnings
from pathlib import Path
import numpy as np, pandas as pd, awkward as ak, uproot, yaml
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import joblib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analysis.top_categorization import BDT_FEATURES,CATEGORY_ORDER,stable_partition,optimize_bdt_boundaries
warnings.filterwarnings('ignore'); np.random.seed(1729)
BASE=Path(__file__).resolve().parents[1]; OUT=Path('/root/results/tth-diphoton-bdt'); IN=Path(os.environ.get('TB_HYY_INPUTS','/data/GamGam'))
SAMPLES=['VBF','WH','ZH','ggH','ggZH','tH','ttH','data']; LUMI=36000.0; MAX=os.getenv('TTH_MAX_SELECTED_PER_SAMPLE'); MAX=int(MAX) if MAX else None
for d in ['model','optimization','plots','inference','categorization/plots','categorization/histograms','fit/FIT1/plots']:(OUT/d).mkdir(parents=True,exist_ok=True)
def dump(p,x):
 p=OUT/p; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,indent=2,allow_nan=False,default=lambda z: z.item() if hasattr(z,'item') else str(z)))
def savefig(path):
 plt.tight_layout(); plt.savefig(OUT/(path+'.png'),dpi=140); plt.savefig(OUT/(path+'.pdf')); plt.close()
def az(s,b):
 s=max(0.,s); b=max(1e-12,b); return math.sqrt(max(0.,2*((s+b)*math.log1p(s/b)-s)))
def hist_payload(x,w,edges):
 h=np.histogram(x,bins=edges,weights=w)[0]; h2=np.histogram(x,bins=edges,weights=np.asarray(w)**2)[0]
 return {'bin_edges':list(map(float,edges)),'bin_contents':list(map(float,h)),'sumw2':list(map(float,h2)),'total_before_shape_normalization':float(np.sum(w))}

def read_sample(sample):
 f=IN/('data/data_preselection.root' if sample=='data' else f'MC/{sample}_preselection.root'); t=uproot.open(f)['analysis']
 br=['eventNumber','runNumber','channelNumber','num_events','sum_of_weights','xsec','kfac','filteff','mcWeight','ScaleFactor_PILEUP','ScaleFactor_PHOTON','ScaleFactor_BTAG','ScaleFactor_JVT','photon_pt','photon_eta','photon_phi','photon_e','photon_isTightID','photon_isTightIso','lep_pt','lep_type','jet_pt','jet_eta','jet_phi','jet_e','jet_btag_quantile']
 a=t.arrays(br,library='ak'); pk=(a.photon_pt>25)&(abs(a.photon_eta)<2.37)&~((abs(a.photon_eta)>1.37)&(abs(a.photon_eta)<1.52)); idx=ak.local_index(a.photon_pt)[pk]; cand=ak.num(idx)>=2
 jets=a.jet_pt>25; nlep=ak.sum(a.lep_pt>10,axis=1); nj=ak.sum(jets,axis=1); nb=ak.sum(jets&(a.jet_btag_quantile>=4),axis=1); had=cand&(nlep==0)&(nj>=3)&(nb>=1)
 sel=np.where(np.asarray(had))[0]; raw=int(len(sel));
 if MAX: sel=sel[:MAX]
 def arr(name): return np.asarray(a[name][sel])
 ii=idx[sel,0]; jj=idx[sel,1]; row=ak.local_index(a.photon_pt[sel],axis=0)
 def jag(name,ind): return np.asarray(a[name][sel][row,ind])
 pt1,pt2=jag('photon_pt',ii),jag('photon_pt',jj); eta1,eta2=jag('photon_eta',ii),jag('photon_eta',jj); phi1,phi2=jag('photon_phi',ii),jag('photon_phi',jj); e1,e2=jag('photon_e',ii),jag('photon_e',jj)
 m=np.sqrt(np.maximum(0,(e1+e2)**2-(pt1*np.cos(phi1)+pt2*np.cos(phi2))**2-(pt1*np.sin(phi1)+pt2*np.sin(phi2))**2-(pt1*np.sinh(eta1)+pt2*np.sinh(eta2))**2))
 ti=jag('photon_isTightID',ii).astype(bool)&jag('photon_isTightIso',ii).astype(bool)&jag('photon_isTightID',jj).astype(bool)&jag('photon_isTightIso',jj).astype(bool)
 jpt=a.jet_pt[sel][jets[sel]]; jeta=a.jet_eta[sel][jets[sel]]; jphi=a.jet_phi[sel][jets[sel]]; jb=a.jet_btag_quantile[sel][jets[sel]]
 ncentral=np.asarray(ak.sum(abs(jeta)<=2.5,axis=1)); ht=np.asarray(ak.sum(jpt,axis=1)); lead=np.asarray(ak.max(jpt,axis=1))
 # all photon-jet delta R combinations
 dr1=np.sqrt((jeta-eta1[:,None])**2+np.minimum(abs(jphi-phi1[:,None]),2*np.pi-abs(jphi-phi1[:,None]))**2); dr2=np.sqrt((jeta-eta2[:,None])**2+np.minimum(abs(jphi-phi2[:,None]),2*np.pi-abs(jphi-phi2[:,None]))**2); mindr=np.asarray(ak.min(ak.concatenate([dr1,dr2],axis=1),axis=1))
 eid=[f'{int(r)}:{int(e)}:{sample}' for r,e in zip(arr('runNumber'),arr('eventNumber'))]
 if sample=='data': phys=np.zeros(len(sel)); obs=np.ones(len(sel))
 else:
  sf=arr('ScaleFactor_PILEUP')*arr('ScaleFactor_PHOTON')*arr('ScaleFactor_BTAG')*arr('ScaleFactor_JVT'); sf=np.where(np.isfinite(sf),sf,1)
  phys=LUMI*arr('xsec')*arr('kfac')*arr('filteff')*arr('mcWeight')*sf/arr('sum_of_weights'); obs=np.zeros(len(sel))
 df=pd.DataFrame({'event_id':eid,'run_number':arr('runNumber'),'event_number':arr('eventNumber'),'sample':sample,'process':sample,'is_data':sample=='data','is_signal':sample in ['ttH','tH'],'m_gammagamma':m,'diphoton_ti':ti,'diphoton_nti':~ti,'photon1_pt':pt1,'photon2_pt':pt2,'n_leptons':np.asarray(nlep[sel]),'n_jets':np.asarray(nj[sel]),'n_central_jets':ncentral,'n_forward_jets':np.asarray(nj[sel])-ncentral,'n_bjets':np.asarray(nb[sel]),'ht_jets':ht,'leading_jet_pt':lead,'min_dr_gam_jet':mindr,'passes_hadronic_preselection':True,'preselection_channel':'hadronic','sm_mc_weight_36fb':phys,'event_weight':phys,'observed_data_weight':obs})
 df['partition']=[stable_partition(x) for x in eid]; return df,raw,str(f)

start=time.time(); frames=[]; raw={}; files=[]
for s in SAMPLES:
 d,n,f=read_sample(s); frames.append(d);raw[s]=n;files.append(f);print(s,len(d),'of',n,flush=True)
df=pd.concat(frames,ignore_index=True); side=((df.m_gammagamma>=105)&(df.m_gammagamma<120))|((df.m_gammagamma>130)&(df.m_gammagamma<=160)); win=abs(df.m_gammagamma-125)<=2
data=df.is_data; nti=df.diphoton_nti; ti=df.diphoton_ti
TI_sb=float((data&ti&side).sum()); NTI_sb=float((data&nti&side).sum()); NTI_win=float((data&nti&win).sum()); SF1=TI_sb/NTI_sb; SF2=NTI_win/NTI_sb; SF=SF1*SF2
df['nti_continuum_proxy_weight']=np.where(data&nti&side,SF,0.0); df['significance_model_weight_36fb']=df.sm_mc_weight_36fb+df.nti_continuum_proxy_weight
# Training: top TI window, ggH TI window, and data NTI sidebands. Signed physical weights remain explicit; nonnegative magnitudes are needed by sklearn.
role=np.full(len(df),'not_training',object); role[(~data)&df.is_signal&ti&win]='signal_top_higgs'; role[(df['sample']=='ggH')&ti&win]='background_resonant_ggH'; role[data&nti&side]='background_nti_sideband'
df['training_role']=role; tr=df[(df.partition=='train')&(df.training_role!='not_training')].copy(); tr['target']=(tr.training_role=='signal_top_higgs').astype(int)
base=np.where(tr.target==1,np.abs(tr.sm_mc_weight_36fb),np.where(tr.training_role=='background_resonant_ggH',np.abs(tr.sm_mc_weight_36fb),tr.nti_continuum_proxy_weight)); tr['mixture_weight']=base
pre={str(k):float(base[tr.target.values==k].sum()) for k in [0,1]}; factors={k:(0.5/pre[str(k)] if pre[str(k)]>0 else 0) for k in [0,1]}; tr['bdt_fit_weight']=[base[i]*factors[int(y)] for i,y in enumerate(tr.target)]; post={str(k):float(tr.loc[tr.target==k,'bdt_fit_weight'].sum()) for k in [0,1]}
t0=time.time(); model=HistGradientBoostingClassifier(max_iter=180,learning_rate=.055,max_leaf_nodes=15,l2_regularization=1.0,random_state=1729).fit(tr[BDT_FEATURES],tr.target,sample_weight=tr.bdt_fit_weight); train_seconds=time.time()-t0; joblib.dump(model,OUT/'model/bdt_model.joblib')
df['bdt_score']=model.predict_proba(df[BDT_FEATURES])[:,1]; tr['bdt_score']=model.predict_proba(tr[BDT_FEATURES])[:,1]
# Optimize on validation physical model rows only, never nominal TI data window.
optrows=df[(df.partition=='validation')&(((~data)&ti&win)|(data&nti&side))].copy(); opt=optimize_bdt_boundaries(optrows,{'max_categories':4,'min_background':0.8}); bounds=sorted(opt['boundaries'],reverse=True)
# Four reported BDT labels; only optimized regions are kept. Missing labels are empty/not kept. Lowest accepted edge defines failure region for tH cuts.
thresholds=bounds[:]; cats=[]
for _,r in df.iterrows():
 s=r.bdt_score; c='unassigned'
 for i,t in enumerate(thresholds[:4]):
  if s>=t: c=CATEGORY_ORDER[i]; break
 if c=='unassigned' and r.n_central_jets==4: c='tH_had_4j1b' if r.n_bjets==1 else ('tH_had_4j2b' if r.n_bjets>=2 else c)
 cats.append(c)
df['assigned_category']=cats
# Retain category only with expected TI-window resonant + scaled NTI background >=0.8.
bkgmask=((~data)&(~df.is_signal)&ti&win)|(data&nti&side); retention={}
for c in CATEGORY_ORDER:
 b=float(df.loc[(df.assigned_category==c)&bkgmask,'significance_model_weight_36fb'].sum()); keep=b>=.8; retention[c]={'expected_background_36fb':b,'minimum':.8,'kept':keep}
 if not keep: df.loc[df.assigned_category==c,'assigned_category']='unassigned'
# outputs tables
cols=['event_id','run_number','event_number','sample','process','is_data','is_signal','event_weight','sm_mc_weight_36fb','observed_data_weight','nti_continuum_proxy_weight','significance_model_weight_36fb','m_gammagamma','diphoton_ti','diphoton_nti','passes_hadronic_preselection','preselection_channel','partition']+BDT_FEATURES+['n_central_jets','n_forward_jets','n_leptons','photon1_pt','photon2_pt','bdt_score','training_role','assigned_category']
df[cols].to_csv(OUT/'preselected_events.csv',index=False); df[cols].to_csv(OUT/'predictions.csv',index=False); df[cols].to_csv(OUT/'hadronic_features.csv',index=False); df[cols].to_csv(OUT/'inference/events_with_bdt_scores.csv',index=False); tr.to_csv(OUT/'model/training_sample.csv',index=False)
# summaries
proc={s:{'raw_selected':raw[s],'written_selected':int((df['sample']==s).sum()),'signed_weighted_yield_36fb':float(df.loc[df['sample']==s,'sm_mc_weight_36fb'].sum())} for s in SAMPLES}
dump('preselection_summary.json',{'photon_definition':'two photons pT>25 GeV, |eta|<2.37 excluding 1.37<|eta|<1.52; no tight-ID or isolation requirement','hadronic_definition':'zero pT>10 GeV leptons, >=3 pT>25 GeV jets, >=1 b jet (quantile>=4)','leptonic_bookkeeping':'not retained','counts':proc,'overall_raw':sum(raw.values()),'overall_written':len(df)})
dump('cutflow.json',{'input_tree_rows':{s:int(uproot.open(files[i])['analysis'].num_entries) for i,s in enumerate(SAMPLES)},'hadronic_selected':proc})
dump('object_definition_record.json',{'units':'GeV','photons':{'pt_min':25,'eta_max':2.37,'crack_excluded':[1.37,1.52],'tight_id_required':False,'isolation_required':False},'leptons':{'pt_min':10,'id_required':False,'isolation_required':False},'jets':{'pt_min':25,'central':'|eta|<=2.5','forward':'|eta|>2.5','btag':'jet_btag_quantile>=4'}})
dump('input_data_contract.json',{'input_root':str(IN),'source':'TB_HYY_INPUTS' if os.getenv('TB_HYY_INPUTS') else 'default','files':files,'included':'nominal Higgs MC and observed GamGam data only','excluded':['Sherpa yy','prompt diphoton MC','all non-Higgs MC'],'root_inputs_copied':False})
dump('model/background_mixture_and_normalization.json',{'SF1':SF1,'SF2':SF2,'SF1_times_SF2':SF,'TI_sideband_yield':TI_sb,'NTI_sideband_yield':NTI_sb,'NTI_window_yield':NTI_win,'signal':'ttH+tH TI MC, 125+/-2 GeV','background':'ggH TI MC 125+/-2 GeV plus data NTI sidebands','nominal_TI_data_window_used':False})
dump('model/class_balance_check.json',{'before':pre,'after':post,'factors':factors,'note':'balancing after physical signal and mixture weights; yields never use bdt_fit_weight'})
dump('model/training_metadata.json',{'features':BDT_FEATURES,'mass_is_input':False,'classifier':'sklearn HistGradientBoostingClassifier','hyperparameters':model.get_params(),'seed':1729,'training_seconds':train_seconds,'partitions':'stable SHA256 60/20/20','training_rows':len(tr)})
dump('optimization/thresholds.json',{'thresholds_descending':thresholds,'blinded':True}); dump('optimization/accepted_splits.json',opt)
