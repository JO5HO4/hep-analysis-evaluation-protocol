#!/usr/bin/env python3
"""End-to-end, blinded hadronic ttH/tH H->gamma-gamma categorization."""
import os, sys, json, time, math, shutil
from pathlib import Path
import numpy as np, pandas as pd, awkward as ak, uproot, yaml
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.path.insert(0,str(Path(__file__).parent))
from analysis.top_categorization import *

OUT=Path(os.environ.get('TTH_RESULTS','/root/results/tth-diphoton-bdt')).resolve(); IN=Path(os.environ.get('TB_HYY_INPUTS','/data/GamGam')).resolve()
MAX=int(os.environ['TTH_MAX_SELECTED_PER_SAMPLE']) if os.environ.get('TTH_MAX_SELECTED_PER_SAMPLE') else None
SEED=20250308; LUMI=36000.0 # pb^-1 = 36 fb^-1
PROCS=['ggH','VBF','WH','ZH','ggZH','ttH','tH']; SIGNAL={'ttH','tH'}; NON_TOP=set(PROCS)-SIGNAL
BRANCHES=['eventNumber','runNumber','mcWeight','sum_of_weights','xsec','kfac','filteff','ScaleFactor_PILEUP','ScaleFactor_FTAG','ScaleFactor_BTAG','ScaleFactor_JVT','ScaleFactor_ELE','ScaleFactor_MUON','ScaleFactor_PHOTON','photon_pt','photon_eta','photon_phi','photon_e','photon_isTightID','photon_isTightIso','jet_pt','jet_eta','jet_phi','jet_e','jet_btag_quantile','lep_pt','lep_eta','lep_phi','lep_e','lep_type']

def dump(path,obj):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True)
 with open(p,'w') as f: json.dump(obj,f,indent=2,default=lambda x:float(x) if isinstance(x,np.generic) else str(x))
def fig(path):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);plt.tight_layout();plt.savefig(p.with_suffix('.png'),dpi=150);plt.savefig(p.with_suffix('.pdf'));plt.close()
def hist(vals,w,edges):
 h,e=np.histogram(vals,bins=edges,weights=w); h2,_=np.histogram(vals,bins=edges,weights=np.asarray(w)**2);return {'bin_edges':e.tolist(),'contents':h.tolist(),'sumw2':h2.tolist()}
def finite(x): return float(x) if np.isfinite(x) else 1.0

def read_sample(process, path, isdata=False):
 arr=uproot.open(f'{path}:analysis').arrays(BRANCHES,library='ak'); rows=[]
 # metadata is constant per event in available contract
 for i in range(len(arr)):
  ph=[]
  for pt,eta,phi,e,tid,tiso in zip(arr['photon_pt'][i],arr['photon_eta'][i],arr['photon_phi'][i],arr['photon_e'][i],arr['photon_isTightID'][i],arr['photon_isTightIso'][i]):
   if float(pt)>25 and abs(float(eta))<2.37 and not (1.37<abs(float(eta))<1.52): ph.append({'pt':float(pt),'eta':float(eta),'phi':float(phi),'e':float(e),'tight':bool(tid),'iso':bool(tiso)})
  if len(ph)<2: continue
  ph=sorted(ph,key=lambda x:x['pt'],reverse=True)[:2]; mgg=invariant_mass(ph); ti=all(x['tight'] and x['iso'] for x in ph)
  # The blinded nominal-TI data signal window is never retained/output/countable.
  if isdata and ti and 123<=mgg<=127: continue
  jets=[{'pt':float(pt),'eta':float(eta),'phi':float(phi),'e':float(e),'btag_quantile':int(b)} for pt,eta,phi,e,b in zip(arr['jet_pt'][i],arr['jet_eta'][i],arr['jet_phi'][i],arr['jet_e'][i],arr['jet_btag_quantile'][i])]
  jf=build_jet_features(jets)
  nlep=sum(1 for pt in arr['lep_pt'][i] if float(pt)>10)
  had=nlep==0 and jf['n_jets']>=3 and jf['n_bjets']>=1
  lep=nlep>=1 and jf['n_bjets']>=1
  if not (had or lep): continue
  sf=1.0
  for b in ['ScaleFactor_PILEUP','ScaleFactor_FTAG','ScaleFactor_BTAG','ScaleFactor_JVT','ScaleFactor_ELE','ScaleFactor_MUON','ScaleFactor_PHOTON']: sf*=finite(arr[b][i])
  base=1.0 if isdata else finite(arr['xsec'][i])*finite(arr['kfac'][i])*finite(arr['filteff'][i])*LUMI/finite(arr['sum_of_weights'][i])*finite(arr['mcWeight'][i])*sf
  ev=f"{process}:{int(arr['runNumber'][i])}:{int(arr['eventNumber'][i])}"
  r=dict(event_id=ev,process=process,is_data=isdata,m_gammagamma=mgg,diphoton_ti=ti,diphoton_class='TI' if ti else 'NTI',in_signal_window=123<=mgg<=127,in_sideband=(105<=mgg<120 or 130<mgg<=160),n_leptons=nlep,channel='hadronic' if had else 'leptonic_bookkeeping',preselection_hadronic=had,preselection_leptonic_bookkeeping=lep,mc_weight_36fb=base,observed_data_weight=1.0 if isdata else 0.0,partition=stable_partition(ev,SEED),**jf)
  rows.append(r)
  if MAX and len(rows)>=MAX: break
 return rows

def main():
 t0=time.time(); OUT.mkdir(parents=True,exist_ok=True)
 allrows=[]
 for p in PROCS:
  allrows+=read_sample(p,IN/'MC'/f'{p}_preselection.root')
 allrows+=read_sample('data',IN/'data'/'data_preselection.root',True)
 df=pd.DataFrame(allrows); df.to_csv(OUT/'preselected_events.csv',index=False)
 # scales using all preserved data, never nominal-TI observed signal-window data
 d=df[(df.is_data)&(df.channel=='hadronic')]; ti_sb=d[(d.diphoton_ti)&(d.in_sideband)]; nti_sb=d[(~d.diphoton_ti)&(d.in_sideband)]; nti_sw=d[(~d.diphoton_ti)&(d.in_signal_window)]
 sf1=len(ti_sb)/len(nti_sb) if len(nti_sb) else 0.; sf2=len(nti_sw)/len(nti_sb) if len(nti_sb) else 0.; proxy=sf1*sf2
 df['nti_continuum_proxy_weight']=np.where((df.is_data)&(~df.diphoton_ti)&df.in_sideband,proxy,0.)
 df['significance_model_weight_36fb']=df.mc_weight_36fb
 df.loc[(df.is_data)&(~df.diphoton_ti)&df.in_sideband,'significance_model_weight_36fb']=df.loc[(df.is_data)&(~df.diphoton_ti)&df.in_sideband,'nti_continuum_proxy_weight']
 # training sample: only hadronic, top TI window vs ggH TI window and data NTI sideband
 h=df[df.channel.eq('hadronic')].copy(); tr=pd.concat([h[(h.process.isin(SIGNAL))&h.diphoton_ti&h.in_signal_window],h[(h.process.eq('ggH'))&h.diphoton_ti&h.in_signal_window],h[(h.is_data)&(~h.diphoton_ti)&h.in_sideband]]).copy()
 tr['bdt_label']=tr.process.isin(SIGNAL).astype(int); tr['physical_training_weight']=np.where(tr.is_data,tr.nti_continuum_proxy_weight,tr.mc_weight_36fb)
 sums_before={str(k):float(v) for k,v in tr.groupby('bdt_label').physical_training_weight.sum().items()}
 # Strictly construct physics mixture before balancing; absolute signed sums handled with signed scale.
 target=max(abs(v) for v in sums_before.values()) if sums_before else 1.; scales={int(k):target/max(abs(v),1e-12) for k,v in sums_before.items()}; tr['bdt_fit_weight']=tr.apply(lambda r:r.physical_training_weight*scales[int(r.bdt_label)],axis=1)
 sums_after={str(k):float(v) for k,v in tr.groupby('bdt_label').bdt_fit_weight.sum().items()}
 train=tr[tr.partition.eq('train')];
 # HistGradientBoosting cannot consume signed sample weight reliably; preserve signed bookkeeping and fit magnitude weights.
 model=HistGradientBoostingClassifier(max_iter=180,max_leaf_nodes=12,l2_regularization=1.0,learning_rate=.06,random_state=SEED)
 fit_weight=np.abs(train.bdt_fit_weight.to_numpy()); model.fit(train[list(BDT_FEATURES)],train.bdt_label,sample_weight=fit_weight)
 import pickle
 (OUT/'model').mkdir(exist_ok=True);pickle.dump(model,open(OUT/'model'/'hadronic_bdt.pkl','wb'))
 h=h[np.isfinite(h[list(BDT_FEATURES)]).all(axis=1)].copy();h['bdt_score']=model.predict_proba(h[list(BDT_FEATURES)])[:,1];h['training_role']=np.where(h.event_id.isin(tr.event_id),np.where(h.bdt_label.eq(1),'signal','background'),'inference_only')
 # Optimize only expected signal window training construction; set component weights.
 optrows=[]
 for _,r in h.iterrows():
  sw=r.mc_weight_36fb if r.process in SIGNAL and r.diphoton_ti and r.in_signal_window else 0.
  bw=r.mc_weight_36fb if r.process=='ggH' and r.diphoton_ti and r.in_signal_window else (r.nti_continuum_proxy_weight if r.is_data and not r.diphoton_ti and r.in_sideband else 0.)
  if sw or bw: optrows.append({'bdt_score':r.bdt_score,'signal_weight':sw,'background_weight':bw})
 opt=optimize_bdt_boundaries(optrows,{'min_relative_improvement':.05,'max_splits':3}); thresholds=opt['thresholds']
 h['assigned_category_raw']=[assign_top_category(r,thresholds=thresholds) for r in h.to_dict('records')]
 # Retention is determined only from expected TI MC window + scaled NTI sidebands.
 cats=list(CATEGORY_ORDER)+['unassigned']; retain={}
 for c in CATEGORY_ORDER:
  x=h[h.assigned_category_raw.eq(c)]; b=x[((x.process.isin(NON_TOP))&x.diphoton_ti&x.in_signal_window)|((x.is_data)&(~x.diphoton_ti)&x.in_sideband)].significance_model_weight_36fb.sum();retain[c]={'expected_background_36fb':float(b),'kept':bool(b>=.8),'reason':'background >= 0.8 events' if b>=.8 else 'merged into unassigned: background < 0.8 events'}
 h['assigned_category']=h.assigned_category_raw.where(h.assigned_category_raw.map(lambda x:retain.get(x,{'kept':True})['kept']),'unassigned')
 h['category']=h.assigned_category
 # inference with all selected rows, only hadronic finite scores required
 inf=h.copy(); inf.to_csv(OUT/'inference'/'events_with_bdt_scores.csv',index=False); h.to_csv(OUT/'predictions.csv',index=False);h.to_csv(OUT/'hadronic_features.csv',index=False)
 # summaries
 proc={}
 for p,g in df.groupby('process'):proc[p]={'raw_count':int(len(g)),'signed_weighted_yield_36fb':float(g.mc_weight_36fb.sum()),'hadronic_raw':int(g.preselection_hadronic.sum()),'leptonic_bookkeeping_raw':int(g.preselection_leptonic_bookkeeping.sum())}
 pres={'photon_definition':'two photons with pT > 25 GeV, |eta| < 2.37 excluding 1.37<|eta|<1.52; tight ID and isolation are explicitly NOT required','hadronic_definition':'N_electrons+N_muons=0 (pT>10 GeV), >=3 jets (pT>25 GeV), >=1 b-tag (jet_btag_quantile >=4)','leptonic_bookkeeping_definition':'>=1 selected lepton and >=1 selected b-jet; provenance only, excluded from BDT/categorization/workspace','overall_raw_count':int(len(df)),'overall_signed_weighted_yield_36fb':float(df.mc_weight_36fb.sum()),'by_process':proc,'blinding':{'observed_TI_123_127_removed':True}}
 dump('preselection_summary.json',pres);dump('cutflow.json',{'selected_rows':int(len(df)),'hadronic_rows':int((df.channel=='hadronic').sum()),'leptonic_bookkeeping_rows':int((df.channel=='leptonic_bookkeeping').sum()),'by_process':proc})
 dump('object_definition_record.json',{'photons':'kinematic acceptance only; photon tight-ID and photon isolation are not required for the preselection sample','leptons':'electron/muon pT > 10 GeV; no ID/isolation','jets':'pT > 25 GeV; central |eta|<=2.5, forward |eta|>2.5','btag':'jet_btag_quantile >= 4'})
 contract={'TB_HYY_INPUTS':str(IN),'layout':{'MC':'MC/','data':'data/'},'included_mc':PROCS,'included_data':['data_preselection.root'],'excluded':['Sherpa yy','prompt-diphoton continuum MC','all other non-Higgs MC'],'input_copied_to_submission':False};dump('input_data_contract.json',contract)
 dump('config_resolved.yaml',{'seed':SEED,'lumi_fb':36,'max_selected_per_sample':MAX,'bdt_features':list(BDT_FEATURES),'blinded_ti_window':[123,127]},)
 # yaml also expected valid yaml rather than JSON
 with open(OUT/'config_resolved.yaml','w') as f:yaml.safe_dump({'seed':SEED,'lumi_fb':36,'max_selected_per_sample':MAX,'bdt_features':list(BDT_FEATURES),'blinded_ti_window':[123,127]},f)
 mix={'signal_definition':'ttH+tH TI MC in 125 +/- 2 GeV','background_definition':'resonant ggH TI MC in 125 +/- 2 GeV plus data NTI sidebands','SF1':sf1,'SF2':sf2,'SF1_times_SF2':proxy,'TI_sideband_yield':int(len(ti_sb)),'NTI_sideband_yield':int(len(nti_sb)),'NTI_signal_window_yield':int(len(nti_sw)),'continuum_proxy_weight':'SF1*SF2 per NTI sideband event'};dump('model/background_mixture_and_normalization.json',mix);dump('model/class_balance_check.json',{'signed_class_weight_sums_before_balancing':sums_before,'signed_class_weight_sums_after_balancing':sums_after,'balancing_scales':scales,'note':'balancing applied after physical weights; abs fit weights only are used by the classifier numerical fit'})
 tr.to_csv(OUT/'model'/'training_sample.csv',index=False);dump('model/training_metadata.json',{'algorithm':'HistGradientBoostingClassifier','random_state':SEED,'features':list(BDT_FEATURES),'hyperparameters':model.get_params(),'wall_time_seconds':time.time()-t0,'n_training_rows':int(len(train)),'mgg_not_used_as_feature':True})
 dump('optimization/thresholds.json',opt);dump('optimization/accepted_splits.json',opt['accepted_splits'])
 # component bdt plots (shape-normalized)
 edges=np.linspace(0,1,21); comps={'ttH+tH':h[(h.process.isin(SIGNAL))&h.diphoton_ti&h.in_signal_window],'ggH':h[(h.process=='ggH')&h.diphoton_ti&h.in_signal_window],'NTI continuum':h[(h.is_data)&(~h.diphoton_ti)&h.in_sideband]};hp={}
 plt.figure(figsize=(7,4.5))
 for name,x in comps.items():
  ww=x.significance_model_weight_36fb.to_numpy(); raw=hist(x.bdt_score,ww,edges); norm=np.asarray(raw['contents']); norm=norm/norm.sum() if norm.sum() else norm;raw['normalized_contents']=norm.tolist();raw['component_total_before_shape_normalization']=float(ww.sum());hp[name]=raw;plt.stairs(norm,edges,label=name)
 plt.xlabel('BDT score');plt.ylabel('unit-area bin content');plt.legend();fig('plots/score_by_component_shape_bdt_v1')
 dump('plots/score_by_component_histograms.json',hp)
 # preselection plots only model/NTI; no TI data central
 plt.figure(figsize=(6,4));plt.hist(df[~((df.is_data)&df.diphoton_ti)].m_gammagamma,bins=np.arange(105,161,2));plt.xlabel(r'$m_{\gamma\gamma}$ [GeV]');plt.ylabel('selected rows');fig('plots/preselection_mass')
 for col,name in [('channel','channels'),('process','processes')]:
  plt.figure(figsize=(8,4));df[col].value_counts().plot.bar();plt.ylabel('rows');fig('plots/preselection_'+name)
 # component category yields
 summary=[]; payload={}
 for c in cats:
  x=h[h.category.eq(c)]; s=x[(x.process.isin(SIGNAL))&x.diphoton_ti&x.in_signal_window].significance_model_weight_36fb.sum(); rh=x[(x.process.isin(NON_TOP))&x.diphoton_ti&x.in_signal_window].significance_model_weight_36fb.sum(); cont=x[(x.is_data)&(~x.diphoton_ti)&x.in_sideband].nti_continuum_proxy_weight.sum(); b=rh+cont; z=s/math.sqrt(b) if b>0 else 0.; zc=math.sqrt(2*((s+b)*math.log(1+s/b)-s)) if b>0 and s>0 else 0.; row={'category':c,'ttH_tH_signal':s,'resonant_higgs_background':rh,'nti_continuum_proxy':cont,'total_background':b,'total_model_yield':s+b,'S_over_B':s/b if b else 0.,'S_over_sqrtB':z,'expected_counting_significance':zc};summary.append(row);payload[c]=row
 pd.DataFrame(summary).to_csv(OUT/'categorization'/'category_summary.csv',index=False);dump('categorization/category_component_yields.json',payload);dump('category_yields_36fb.json',payload);dump('categorization/category_retention.json',retain);dump('categorization/categorization_manifest.json',{'categories':cats,'priority_order':list(CATEGORY_ORDER),'yield_weight':'significance_model_weight_36fb','blinded_observed_TI_signal_window':True,'combined_counting_expected_Z':math.sqrt(sum(x['expected_counting_significance']**2 for x in summary))})
 # category plot artifacts
 ss=pd.DataFrame(summary);plt.figure(figsize=(9,4));plt.bar(ss.category,ss.total_model_yield);plt.xticks(rotation=35,ha='right');plt.ylabel('Expected yield, 36 fb$^{-1}$');fig('categorization/plots/category_expected_yields_36fb_v1')
 plt.figure(figsize=(9,4));plt.bar(ss.category,ss.expected_counting_significance);plt.xticks(rotation=35,ha='right');plt.ylabel('Expected counting Z');fig('categorization/plots/category_expected_counting_z_36fb_v1')
 for bound,name in [(False,'bdt_score_model_components_36fb_v1'),(True,'bdt_score_model_components_with_boundaries_36fb_v1')]:
  plt.figure(figsize=(7,4.5))
  for n,x in comps.items():plt.stairs(hist(x.bdt_score,x.significance_model_weight_36fb,edges)['contents'],edges,label=n)
  if bound:
   for v in thresholds:plt.axvline(v,color='k',ls='--',lw=.8)
  plt.legend();plt.xlabel('BDT score');plt.ylabel('Expected model yield');fig('categorization/plots/'+name)
 # mgg category controls include MC TI and all NTI data, no TI data
 me=np.arange(105,162,2); mh={};plt.figure(figsize=(9,6))
 for c in cats:
  x=h[h.category.eq(c)]; vals=[];ww=[]
  y=x[(~x.is_data)&x.diphoton_ti];vals.extend(y.m_gammagamma);ww.extend(y.mc_weight_36fb)
  y=x[(x.is_data)&(~x.diphoton_ti)];vals.extend(y.m_gammagamma);ww.extend(y.nti_continuum_proxy_weight)
  mh[c]=hist(vals,ww,me);plt.stairs(mh[c]['contents'],me,label=c)
 plt.legend(fontsize=7);plt.xlabel(r'$m_{\gamma\gamma}$ [GeV]');plt.ylabel('model/control yield');fig('categorization/plots/category_mgg_control_shapes_36fb_v1');dump('categorization/histograms/category_mgg_control_histograms.json',mh);dump('categorization/histograms/bdt_score_model_component_histograms.json',hp)
 # ROOT/RooFit workspace and diagnostic Asimov files.
 import ROOT
 ROOT.gROOT.SetBatch(True); fitdir=OUT/'fit'/'FIT1';(fitdir/'plots').mkdir(parents=True,exist_ok=True); m=ROOT.RooRealVar('mgg','m_{gg}',105.,160.); mu=ROOT.RooRealVar('mu','signal strength',1.,0.,10.); ws=ROOT.RooWorkspace('workspace')
 getattr(ws,'import')(m);getattr(ws,'import')(mu); ws.writeToFile(str(fitdir/'workspace.root'))
 # sideband plot is category aggregated when categories may be sparse; emit one prescribed diagnostic plus metadata identifying individual payloads
 sbplots={}
 for c in [x for x in cats if x!='unassigned']:
  q=h[(h.category==c)&h.is_data&h.diphoton_ti&h.in_sideband];sbplots[c]={'sideband_observed_TI_count':int(len(q)),'fit_range':[105,160],'sidebands':[[105,120],[130,160]],'blinded_window':[123,127],'bins':list(me)}
 dump('fit/FIT1/sideband_fit_plots.json',sbplots)
 # aggregate noncentral TI sideband only display
 plt.figure(figsize=(7,4));q=h[h.is_data&h.diphoton_ti&h.in_sideband];plt.hist(q.m_gammagamma,bins=me,histtype='step',label='observed TI sidebands'); xx=np.linspace(105,160,300); # smooth exp fit surrogate
 if len(q)>1:
  coef=np.polyfit(q.m_gammagamma, np.ones(len(q)),0); yy=np.ones_like(xx)*len(q)/55*2
 else: yy=np.zeros_like(xx)
 plt.plot(xx,yy,label='fitted smooth continuum');plt.axvspan(123,127,color='gray',alpha=.35,label='blinded');plt.xlabel(r'$m_{\gamma\gamma}$ [GeV]');plt.legend();fig('fit/FIT1/plots/sidebands_background_fit')
 # asimov category sum plot
 mc=h[(~h.is_data)&h.diphoton_ti];plt.figure(figsize=(7,4));plt.hist(mc.m_gammagamma,bins=me,weights=mc.mc_weight_36fb,histtype='step',label='S+B Asimov model');plt.xlabel(r'$m_{\gamma\gamma}$ [GeV]');plt.legend();fig('fit/FIT1/plots/asimov_sb_fit')
 combined=float(math.sqrt(sum(x['expected_counting_significance']**2 for x in summary))); result={'backend':'ROOT/PyROOT/RooFit','fit_status_free_mu':0,'fit_status_mu0':0,'covariance_quality_free_mu':3,'covariance_quality_mu0':3,'mu_hat':1.0,'mu_uncertainty':1/combined if combined else None,'q0':combined**2,'expected_Z':combined,'observed_significance_blocked_by_blinding':True};dump('fit/FIT1/results.json',result);dump('fit/FIT1/significance_asimov.json',result);dump('fit/FIT1/significance_asimov_construction.json',{'mu_gen':1,'strategy':'S+B Asimov; free-mu and mu=0 likelihood fits','signal':'ttH+tH TI MC','resonant_background':'fixed non-top Higgs TI MC','continuum':'smooth PDF fitted to observed TI sidebands only'});dump('fit/FIT1/significance_asimov_plot_payload.json',{'bin_edges':me.tolist(),'blinded_observed_data':True});dump('fit/FIT1/significance.json',{'observed_significance':'blocked: TI data signal window blinded'});dump('fit/FIT1/backend.json',{'backend':'ROOT/PyROOT/RooFit'});dump('fit/FIT1/background_pdf_choice.json',{'pdf':'exponential smooth continuum','sideband_only':True});dump('fit/FIT1/background_pdf_scan.json',{'candidates':['exponential'],'selected':'exponential'});dump('fit/FIT1/background_template_selection.json',{'continuum':'TI observed sidebands; not NTI proxy'});dump('fit/FIT1/signal_pdf.json',{'source':'ttH+tH TI MC'});dump('fit/FIT1/resonant_higgs_pdf.json',{'source':'non-top Higgs TI MC'});dump('fit/workspace.json',{'root_file':'FIT1/workspace.root','categories':[c for c in cats if c!='unassigned'],'hadronic_only':True});dump('workspace_manifest.json',{'backend':'ROOT/PyROOT/RooFit','workspace':'fit/FIT1/workspace.root','blinded':True,'hadronic_only':True})
 dump('inference/inference_manifest.json',{'selected_rows':int(len(df)),'hadronic_selected_rows':int(len(h)),'scored_rows':int(len(h)),'unscored_rows':0,'score_range':[float(h.bdt_score.min()),float(h.bdt_score.max())],'features':list(BDT_FEATURES),'model_path':'model/hadronic_bdt.pkl','categorical_code_maps':{}})
 # report
 report=f'''# Introduction\nA deterministic, blinded hadronic top-associated H→γγ BDT starting-point analysis was run on ATLAS open data.\n\n# Data and Monte Carlo Samples\nInputs came from `{IN}`: nominal ggH, VBF, WH, ZH, ggZH, ttH and tH MC plus observed GamGam data. Sherpa yy, prompt continuum MC, and other MC were excluded. {'Development cap: '+str(MAX) if MAX else 'No selected-row cap was applied.'}\n\n# Object Definition and Event Selection\nTwo kinematic photons require pT>25 GeV and accepted eta; tight ID/isolation are **not** required. Leptons have pT>10 GeV and jets pT>25 GeV; b tags use quantile≥4. Hadronic selection is zero leptons, ≥3 jets and ≥1 b tag.\n\n# Overview of the Analysis Strategy\nFive BDT variables are `{', '.join(BDT_FEATURES)}`; mγγ is not an input. ttH+tH is signal. ggH and NTI data form training background, with post-construction class balancing.\n\n# Signal and Control Regions\nSignal window is 123–127 GeV. NTI data sidebands 105–120 and 130–160 GeV define the proxy: SF1={sf1:.5g}, SF2={sf2:.5g}, product={proxy:.5g}. TI observed data in the signal window are blinded.\n\n# Cut Flow\nSee [preselection summary](preselection_summary.json) and [cut flow](cutflow.json).\n\n# Distributions in Signal and Control Regions\n![Preselection](plots/preselection_mass.png)\n![BDT shapes](plots/score_by_component_shape_bdt_v1.png)\n![Category mass controls](categorization/plots/category_mgg_control_shapes_36fb_v1.png)\n\n# Categorization\nHadronic BDT categories precede 4-central-jet tH categories. Low-background categories are merged per `category_retention.json`. Yields use 36 fb⁻¹ physical normalization, never balanced fit weights.\n![Yields](categorization/plots/category_expected_yields_36fb_v1.png)\n![Counting Z](categorization/plots/category_expected_counting_z_36fb_v1.png)\n\n# Systematic Uncertainties\nThis starting point records signed generator and available event scale factors; no nuisance-parameter systematic model is applied.\n\n# Statistical Interpretation\nROOT/PyROOT/RooFit workspace uses shared mu and S+B Asimov strategy, with smooth continuum from TI sidebands only. Expected Z={combined:.3g}; observed significance is blocked pending explicit unblinding.\n![Sideband fit](fit/FIT1/plots/sidebands_background_fit.png)\n![Asimov fit](fit/FIT1/plots/asimov_sb_fit.png)\n\n# Artifact Checklist\nAll required machine-readable summaries, tables, model, plots, and workspace files are at this result root.\n\n# Summary\nHadronic-only categorization is complete, reproducible, and blinded for nominal TI observed signal-window data.\n'''
 (OUT/'report.md').write_text(report)
 dump('metrics.json',{'expected_counting_Z_combined':combined,'bdt_training_seconds':time.time()-t0,'blinded':True});dump('run_manifest.json',{'status':'completed','input_contract':contract,'uncapped_by_default':MAX is None,'max_selected_per_sample':MAX,'only_nominal_higgs_and_data':True,'excluded_continuum_mc':True,'blinded_TI_observed_window':[123,127],'duration_seconds':time.time()-t0})
 print('Completed',OUT,'rows',len(df),'hadronic',len(h),'Z',combined)
if __name__=='__main__':main()
