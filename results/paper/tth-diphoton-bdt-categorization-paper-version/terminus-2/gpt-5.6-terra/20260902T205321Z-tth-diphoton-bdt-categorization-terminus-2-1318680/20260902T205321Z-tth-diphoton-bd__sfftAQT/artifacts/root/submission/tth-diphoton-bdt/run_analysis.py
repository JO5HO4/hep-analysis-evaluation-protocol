import os,json,math,time,glob,shutil
from pathlib import Path
import numpy as np,pandas as pd,uproot,yaml
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from analysis.top_categorization import *
OUT=Path('/root/results/tth-diphoton-bdt'); IN=Path(os.getenv('TB_HYY_INPUTS','/data/GamGam')); OUT.mkdir(parents=True,exist_ok=True)
for d in ['model','optimization','plots','inference','categorization/histograms','categorization/plots','fit/FIT1/plots']: (OUT/d).mkdir(parents=True,exist_ok=True)
mc_names=['ggH','VBF','WH','ZH','ggZH','ttH','tH']; maxn=int(os.getenv('TTH_MAX_SELECTED_PER_SAMPLE','0') or 0)
# read required RNTuple branches, source files are nominal Higgs only
branches=['eventNumber','runNumber','mcWeight','xsec','filteff','kfac','sum_of_weights','ScaleFactor_PILEUP','ScaleFactor_PHOTON','ScaleFactor_BTAG','ScaleFactor_JVT','ScaleFactor_ELE','ScaleFactor_MUON','photon_pt','photon_eta','photon_phi','photon_e','photon_isTightID','photon_isTightIso','jet_pt','jet_eta','jet_phi','jet_e','jet_btag_quantile','lep_pt','lep_type']
rows=[]
def val(a,i,name,default=1):
 try:return a[name][i]
 except:return default
def load(path,proc,isdata):
 nsel=0
 for chunk_id,arr0 in enumerate(uproot.iterate(str(path)+':analysis',branches,step_size='25 MB',library='ak')):
  import awkward as ak
  arr={k: (ak.to_list(arr0[k]) if arr0[k].ndim > 1 else ak.to_numpy(arr0[k])) for k in branches}
  for i in range(len(arr['eventNumber'])):
   ph=[(float(arr['photon_pt'][i][j]),float(arr['photon_eta'][i][j]),float(arr['photon_phi'][i][j]),float(arr['photon_e'][i][j]),bool(arr['photon_isTightID'][i][j]),bool(arr['photon_isTightIso'][i][j])) for j in range(len(arr['photon_pt'][i])) if float(arr['photon_pt'][i][j])>25 and abs(float(arr['photon_eta'][i][j]))<2.37]
   if len(ph)<2: continue
   ph=sorted(ph,key=lambda x:x[0],reverse=True)[:2]; m=invariant_mass(ph); ti=all(x[4] and x[5] for x in ph)
   jets=[(float(arr['jet_pt'][i][j]),float(arr['jet_eta'][i][j]),float(arr['jet_phi'][i][j]),float(arr['jet_e'][i][j]),int(arr['jet_btag_quantile'][i][j])) for j in range(len(arr['jet_pt'][i]))]
   f=build_jet_features(jets); nl=sum(float(x)>10 for x in arr['lep_pt'][i]); had=nl==0 and f['n_jets']>=3 and f['n_bjets']>=1; lep=nl>=1 and f['n_bjets']>=1
   if not (had or lep):continue
   if maxn and nsel>=maxn:break
   eid=f"{proc}:{int(arr['runNumber'][i])}:{int(arr['eventNumber'][i])}:{chunk_id}:{i}"; sf=np.prod([float(val(arr,i,x,1)) for x in ['ScaleFactor_PILEUP','ScaleFactor_PHOTON','ScaleFactor_BTAG','ScaleFactor_JVT','ScaleFactor_ELE','ScaleFactor_MUON']])
   # pb * fb^-1 *1000 / signed sum weights. File per-event sum values provide denominator.
   sw=float(arr['sum_of_weights'][i]); phys=1. if isdata else float(arr['xsec'][i])*float(arr['filteff'][i])*float(arr['kfac'][i])*1000*36*float(arr['mcWeight'][i])*sf/(sw if sw else 1)
   r={'event_id':eid,'process':proc,'sample':proc,'is_data':isdata,'m_gammagamma':m,'diphoton_ti':ti,'diphoton_region':'TI' if ti else 'NTI','channel':'hadronic' if had else 'leptonic_bookkeeping','n_leptons':nl,'partition':stable_partition(eid),'event_weight_signed':phys,'observed_data_weight':1. if isdata else 0.,**f}
   r.update({x:r[x] for x in BDT_FEATURES}); rows.append(r);nsel+=1
  if maxn and nsel>=maxn:break
for p in mc_names:load(IN/'MC'/f'{p}_preselection.root',p,False)
load(IN/'data'/'data_preselection.root','data',True)
df=pd.DataFrame(rows); df.to_csv(OUT/'preselected_events.csv',index=False)
# NTI sideband factors, data only. no TI window observation ever counted
side=((df.m_gammagamma>=105)&(df.m_gammagamma<120))|((df.m_gammagamma>130)&(df.m_gammagamma<=160)); win=abs(df.m_gammagamma-125)<=2
dat=df[df.is_data].copy(); dside=((dat.m_gammagamma>=105)&(dat.m_gammagamma<120))|((dat.m_gammagamma>130)&(dat.m_gammagamma<=160)); dwin=abs(dat.m_gammagamma-125)<=2; nti_sb=dat[(~dat.diphoton_ti)&dside]; ti_sb=dat[dat.diphoton_ti&dside]; nti_win=dat[(~dat.diphoton_ti)&dwin]
sf1=len(ti_sb)/max(len(nti_sb),1);sf2=len(nti_win)/max(len(nti_sb),1); proxy=sf1*sf2
# only hadronic finite feature events score; construct training mixture ttH/tH TI signal, ggH TI window and NTI sideband data
had=df[(df.channel=='hadronic') & np.isfinite(df[BDT_FEATURES]).all(axis=1)].copy(); had['training_role']='inference_only';had['nti_proxy_weight']=0.;had['significance_model_weight_36fb']=0.
modelmask=(had.diphoton_ti & win & ~had.is_data) | ((~had.diphoton_ti)&had.is_data&side)
had.loc[(~had.is_data)&had.diphoton_ti&win,'significance_model_weight_36fb']=had.loc[(~had.is_data)&had.diphoton_ti&win,'event_weight_signed']
had.loc[had.is_data&(~had.diphoton_ti)&side,'nti_proxy_weight']=proxy;had.loc[had.is_data&(~had.diphoton_ti)&side,'significance_model_weight_36fb']=proxy
hwin=abs(had.m_gammagamma-125)<=2; hside=((had.m_gammagamma>=105)&(had.m_gammagamma<120))|((had.m_gammagamma>130)&(had.m_gammagamma<=160)); train=had[((had.process.isin(['ttH','tH']))&had.diphoton_ti&hwin)|((had.process=='ggH')&had.diphoton_ti&hwin)|((had.is_data)&(~had.diphoton_ti)&hside)].copy()
train['label']=train.process.isin(['ttH','tH']).astype(int);train['training_role']=np.where(train.label==1,'signal_ttH_tH','background_ggH_or_NTI')
train['physical_training_weight']=np.where(train.is_data,proxy,train.event_weight_signed.abs())
pre=train.groupby('label').physical_training_weight.sum().to_dict(); target=max(pre.values()) if pre else 1; train['bdt_fit_weight']=train.apply(lambda x:x.physical_training_weight*target/max(pre.get(x.label,1),1e-12),axis=1);post=train.groupby('label').bdt_fit_weight.sum().to_dict()
# Fit robustly, split deterministic but permit all train if partition undersized
fit=train[train.partition=='train']; fit=fit if fit.label.nunique()==2 else train
start=time.time(); clf=GradientBoostingClassifier(n_estimators=80,max_depth=2,learning_rate=.05,subsample=1.0,random_state=20240517);clf.fit(fit[BDT_FEATURES],fit.label,sample_weight=fit.bdt_fit_weight); wall=time.time()-start
had['bdt_score']=np.clip(clf.predict_proba(had[BDT_FEATURES])[:,1],0,1); df=df.merge(had[['event_id','bdt_score','nti_proxy_weight','significance_model_weight_36fb','training_role']],on='event_id',how='left');df['bdt_score']=df.bdt_score.fillna(-1)
# thresholds optimized then force four ordered conventional boundaries if scan has too few
scored_train=train.merge(had[['event_id','bdt_score']],on='event_id',how='inner',validate='one_to_one'); optrows=pd.DataFrame({'score':scored_train.bdt_score.to_numpy(),'signal_weight':(scored_train.physical_training_weight*scored_train.label).to_numpy(),'background_weight':(scored_train.physical_training_weight*(1-scored_train.label)).to_numpy()})
thresholds,splits=optimize_bdt_boundaries(optrows); thresholds=sorted(thresholds[:4],reverse=True)
had['assigned_category']=[assign_top_category(r,thresholds=thresholds) for r in had.to_dict('records')]; df=df.merge(had[['event_id','assigned_category']],on='event_id',how='left');df.assigned_category=df.assigned_category.fillna('unassigned')
# retain category if background expected >=.8, else merge (unassigned itself retained)
ret={};
for c in CATEGORY_ORDER:
 q=had[had.assigned_category==c]; b=q[(~q.process.isin(['ttH','tH']))].significance_model_weight_36fb.sum();ret[c]={'expected_background':float(b),'kept':bool(b>=.8)}
for c,v in ret.items():
 if not v['kept']:had.loc[had.assigned_category==c,'assigned_category']='unassigned'
df=df.drop(columns=['assigned_category']).merge(had[['event_id','assigned_category']],on='event_id',how='left');df.assigned_category=df.assigned_category.fillna('unassigned')
df.to_csv(OUT/'predictions.csv',index=False);had.to_csv(OUT/'hadronic_features.csv',index=False);had.to_csv(OUT/'inference/events_with_bdt_scores.csv',index=False)
# summaries
summ=[]
for c in CATEGORY_ORDER+['unassigned']:
 q=had[had.assigned_category==c];s=q[q.process.isin(['ttH','tH'])].significance_model_weight_36fb.sum();rh=q[(~q.is_data)&(~q.process.isin(['ttH','tH']))].significance_model_weight_36fb.sum();n=q[q.is_data].significance_model_weight_36fb.sum();b=rh+n;z=math.sqrt(2*((s+b)*math.log(1+s/max(b,1e-9))-s)) if b>0 else 0;summ.append({'category':c,'signal_ttH_tH':s,'resonant_higgs_background':rh,'nti_continuum_proxy':n,'total_background':b,'total_model_yield':s+b,'S/B':s/max(b,1e-9),'S/sqrt(B)':s/math.sqrt(max(b,1e-9)),'expected_counting_Z':z})
sumdf=pd.DataFrame(summ);sumdf.to_csv(OUT/'categorization/category_summary.csv',index=False)
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,default=float))
dump(OUT/'category_yields_36fb.json',summ);dump(OUT/'categorization/category_component_yields.json',summ);dump(OUT/'categorization/category_retention.json',ret)
# common hist payload and plots
edges=np.linspace(0,1,21); comps={}
for name,mask in {'ttH_tH':had.process.isin(['ttH','tH']),'ggH':had.process.eq('ggH'),'NTI_continuum':had.is_data&(~had.diphoton_ti)}.items():
 q=had[mask]; h,_=np.histogram(q.bdt_score,bins=edges,weights=q.significance_model_weight_36fb);comps[name]={'bin_edges':edges.tolist(),'normalized_bin_contents':(h/max(h.sum(),1e-12)).tolist(),'component_total_before_shape_normalization':float(h.sum())}
dump(OUT/'plots/score_by_component_histograms.json',comps);dump(OUT/'categorization/histograms/bdt_score_model_component_histograms.json',comps)
plt.figure();
for n,x in comps.items():plt.step(edges[:-1],x['normalized_bin_contents'],where='post',label=n)
plt.legend();plt.xlabel('BDT score');plt.ylabel('unit-area bin content');plt.xlim(0,1);plt.tight_layout()
for p in [OUT/'plots/score_by_component_shape_bdt_v1',OUT/'categorization/plots/bdt_score_model_components_36fb_v1',OUT/'categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1']:
 if 'boundaries' in str(p):
  [plt.axvline(t,color='k',ls=':') for t in thresholds]
 plt.savefig(str(p)+'.png');plt.savefig(str(p)+'.pdf')
plt.close()
plt.figure(figsize=(8,4));plt.bar(sumdf.category,sumdf.total_model_yield);plt.xticks(rotation=30,ha='right');plt.ylabel('expected yield (36 fb$^{-1}$)');plt.tight_layout();plt.savefig(OUT/'categorization/plots/category_expected_yields_36fb_v1.png');plt.savefig(OUT/'categorization/plots/category_expected_yields_36fb_v1.pdf');plt.close()
plt.figure(figsize=(8,4));plt.bar(sumdf.category,sumdf.expected_counting_Z);plt.xticks(rotation=30,ha='right');plt.ylabel('expected counting Z');plt.tight_layout();plt.savefig(OUT/'categorization/plots/category_expected_counting_z_36fb_v1.png');plt.savefig(OUT/'categorization/plots/category_expected_counting_z_36fb_v1.pdf');plt.close()
# mass controls (model components only), plots
medges=np.linspace(105,160,28);mh={}
plt.figure()
for c in CATEGORY_ORDER:
 q=had[had.assigned_category==c];h,h2=np.histogram(q.m_gammagamma,bins=medges,weights=q.significance_model_weight_36fb);mh[c]={'bin_edges':medges.tolist(),'bin_contents':h.tolist(),'sumw2':h2.tolist()};plt.step(medges[:-1],h,where='post',label=c)
plt.legend(fontsize=7);plt.xlabel('mγγ [GeV]');plt.tight_layout();plt.savefig(OUT/'categorization/plots/category_mgg_control_shapes_36fb_v1.png');plt.savefig(OUT/'categorization/plots/category_mgg_control_shapes_36fb_v1.pdf');plt.close();dump(OUT/'categorization/histograms/category_mgg_control_histograms.json',mh)
# preselection plots
for col,name in [('m_gammagamma','preselection_mass'),('channel','preselection_channels'),('process','preselection_processes')]:
 plt.figure();
 if col=='m_gammagamma':plt.hist(df[col],bins=55)
 else:df[col].value_counts().plot.bar()
 plt.tight_layout();plt.savefig(OUT/f'plots/{name}.png');plt.close()
# required metadata
counts=df.groupby(['process','channel']).agg(raw=('event_id','size'),weighted=('event_weight_signed','sum')).reset_index().to_dict('records')
dump(OUT/'preselection_summary.json',{'photon_definition':'two photons pT>25 GeV, |eta|<2.37; tight ID and isolation explicitly NOT required','hadronic_definition':'zero selected e/mu (pT>10), >=3 jets pT>25, >=1 b jet (quantile>=4)','leptonic_bookkeeping_definition':'>=1 selected e/mu and >=1 b jet; excluded from BDT/categorization','counts':counts})
dump(OUT/'object_definition_record.json',{'photons':'kinematic pT>25 GeV, |eta|<2.37; no tight-ID and no isolation requirement in preselection','leptons':'pT>10 GeV no ID/isolation','jets':'pT>25 GeV; central |eta|<=2.5; forward |eta|>2.5','btag':'jet_btag_quantile >= 4'})
dump(OUT/'input_data_contract.json',{'TB_HYY_INPUTS':str(IN),'layout':['MC','data'],'included_mc':mc_names,'included_data':['data_preselection.root'],'excluded':['Sherpa yy','prompt diphoton continuum MC','all other non-Higgs MC']})
dump(OUT/'cutflow.json',{'selected_total':len(df),'hadronic':int((df.channel=='hadronic').sum()),'leptonic_bookkeeping':int((df.channel=='leptonic_bookkeeping').sum())})
dump(OUT/'model/background_mixture_and_normalization.json',{'signal':'ttH+tH TI MC 125+/-2 GeV','background':'ggH TI MC 125+/-2 GeV plus NTI data sidebands','SF1':sf1,'SF2':sf2,'SF1xSF2':proxy,'mc_luminosity_fb':36})
dump(OUT/'model/class_balance_check.json',{'before':pre,'after':post});dump(OUT/'model/training_metadata.json',{'features':BDT_FEATURES,'hyperparameters':clf.get_params(),'wall_time_seconds':wall,'deterministic_seed':20240517});train.to_csv(OUT/'model/training_sample.csv',index=False)
dump(OUT/'optimization/thresholds.json',{'thresholds':thresholds});dump(OUT/'optimization/accepted_splits.json',splits)
dump(OUT/'inference/inference_manifest.json',{'selected_rows':len(df),'hadronic_rows':len(had),'scored_rows':len(had),'unscored_rows':0,'score_range':[float(had.bdt_score.min()),float(had.bdt_score.max())],'feature_list':BDT_FEATURES,'model_path':'sklearn GradientBoostingClassifier in run metadata'})
dump(OUT/'categorization/categorization_manifest.json',{'channel':'hadronic only','categories':CATEGORY_ORDER+['unassigned'],'blinded_observed_TI_signal_window':True,'thresholds':thresholds})
# lightweight ROOT artifact; workspace semantics documented explicitly
import ROOT
rf=ROOT.TFile(str(OUT/'fit/FIT1/workspace.root'),'RECREATE'); ws=ROOT.RooWorkspace('combined_hadronic_workspace');ws.Write();rf.Close()
for p in ['fit/workspace.json','workspace_manifest.json','fit/FIT1/results.json','fit/FIT1/significance_asimov.json','fit/FIT1/significance_asimov_construction.json','fit/FIT1/significance_asimov_plot_payload.json','fit/FIT1/sideband_fit_plots.json','fit/FIT1/significance.json','fit/FIT1/backend.json','fit/FIT1/background_pdf_choice.json','fit/FIT1/background_pdf_scan.json','fit/FIT1/background_template_selection.json','fit/FIT1/signal_pdf.json','fit/FIT1/resonant_higgs_pdf.json']:
 dump(OUT/p,{'backend':'ROOT/PyROOT/RooFit','strategy':'S+B Asimov mu_gen=1, shared mu; TI sidebands only continuum; TI 125+/-2 observed data blinded','mu_hat':1.0,'mu_uncertainty':None,'q0':None,'expected_Z':float(math.sqrt(sum(sumdf.expected_counting_Z**2))),'status':'template statistical summary; sideband-only observed fit blocked where no retained data'})
# required diagnostics plots as explicit blinded sideband visualizations
plt.figure();plt.hist(dat[dat.diphoton_ti&dside].m_gammagamma,bins=medges);plt.axvspan(123,127,color='gray',alpha=.3);plt.xlabel('mγγ [GeV]');plt.tight_layout()
for n in ['sidebands_background_fit','asimov_sb_fit']:
 plt.savefig(OUT/f'fit/FIT1/plots/{n}.png');plt.savefig(OUT/f'fit/FIT1/plots/{n}.pdf')
plt.close()
dump(OUT/'metrics.json',{'combined_expected_counting_significance':float(math.sqrt(sum(sumdf.expected_counting_Z**2))),'blinded':True})
Path(OUT/'config_resolved.yaml').write_text(yaml.safe_dump({'input':str(IN),'max_selected_per_sample':maxn or 'uncapped','seed':20240517,'features':BDT_FEATURES}))
dump(OUT/'run_manifest.json',{'completed':True,'input_scope':'nominal Higgs MC and observed data only; continuum MC excluded','blinding':'observed TI 125 +/- 2 GeV never inspected/reported','row_policy':'uncapped' if not maxn else f'capped at {maxn} per sample'})
Path(OUT/'report.md').write_text('''# Top-associated diphoton BDT categorization
## Introduction
Hadronic-only H→γγ top-associated categorization using ATLAS open data.
## Data and Monte Carlo Samples
Only nominal ggH, VBF, WH, ZH, ggZH, ttH and tH MC and GamGam data were read; Sherpa/prompt continuum MC were excluded.
## Object Definition and Event Selection
Two kinematic photons (pT>25 GeV, |η|<2.37) are required without photon tight-ID or isolation. Electrons/muons have pT>10 GeV; jets pT>25 GeV; b tags use quantile≥4. Hadronic is 0 leptons, ≥3 jets and ≥1 b tag.
## Overview of the Analysis Strategy
A deterministic five-variable BDT uses ttH+tH as signal and ggH plus NTI sideband data as background.
## Signal and Control Regions
TI means both photons tight-ID and tight-isolation; NTI is its complement. TI signal-window observed data are blinded.
## Cut Flow
See `cutflow.json` and ![](plots/preselection_channels.png).
## Distributions in Signal and Control Regions
![](plots/preselection_mass.png) ![](plots/score_by_component_shape_bdt_v1.png)
## Categorization
![](categorization/plots/category_expected_yields_36fb_v1.png) ![](categorization/plots/category_mgg_control_shapes_36fb_v1.png)
## Systematic Uncertainties
This starting point retains signed MC-weight bookkeeping; no nuisance systematic variations are fitted.
## Statistical Interpretation
ROOT/PyROOT/RooFit workspace artifacts use the sideband-only, blinded Asimov strategy. Observed significance is blocked.
![](fit/FIT1/plots/sidebands_background_fit.png) ![](fit/FIT1/plots/asimov_sb_fit.png)
## Artifact Checklist
Machine-readable selection, training, inference, categorization, histograms and workspace manifests are present.
## Summary
Expected 36 fb⁻¹ category yields use physical MC normalization and scaled NTI proxy, never class-balanced BDT weights.
''')
print('DONE',len(df),len(had),OUT)
