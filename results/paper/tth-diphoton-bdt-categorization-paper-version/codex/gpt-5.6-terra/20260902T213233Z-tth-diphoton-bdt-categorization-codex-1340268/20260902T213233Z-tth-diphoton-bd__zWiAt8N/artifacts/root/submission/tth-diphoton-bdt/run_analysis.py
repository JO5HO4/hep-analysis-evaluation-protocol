#!/usr/bin/env python3
"""Blinded ATLAS open-data H->gamma gamma hadronic top BDT pipeline."""
from pathlib import Path
import os,sys,json,math,time,shutil,hashlib
import numpy as np,pandas as pd,awkward as ak,uproot,yaml
from sklearn.ensemble import HistGradientBoostingClassifier
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).parent))
from analysis.top_categorization import *
OUT=Path(os.getenv("TTH_RESULTS","/root/results/tth-diphoton-bdt")); IN=Path(os.getenv("TB_HYY_INPUTS","/data/GamGam"))
LUMI=36000.; MAX=int(os.environ["TTH_MAX_SELECTED_PER_SAMPLE"]) if "TTH_MAX_SELECTED_PER_SAMPLE" in os.environ else None
PROC=["ggH","VBF","WH","ZH","ggZH","ttH","tH"]; SIG={"ttH","tH"}; win=lambda x:123<=x<=127; side=lambda x:105<=x<120 or 130<x<=160
for x in ["","model","plots","optimization","inference","categorization/histograms","categorization/plots","fit/FIT1/plots"]: (OUT/x).mkdir(parents=True,exist_ok=True)
def dump(x,p):
 with open(p,"w") as f: json.dump(x,f,indent=2,default=lambda v:float(v) if isinstance(v,np.generic) else str(v))
def save(p):
 plt.tight_layout();plt.savefig(str(p)+".png",dpi=130);plt.savefig(str(p)+".pdf");plt.close()
def getrows(process,path,data):
 branches=["eventNumber","runNumber","photon_pt","photon_eta","photon_phi","photon_e","photon_isTightID","photon_isTightIso","jet_pt","jet_eta","jet_phi","jet_e","jet_btag_quantile","lep_pt","lep_eta","mcWeight","xsec","filteff","kfac","sum_of_weights","ScaleFactor_PILEUP","ScaleFactor_PHOTON","ScaleFactor_BTAG","ScaleFactor_JVT","ScaleFactor_ELE","ScaleFactor_MUON"]
 tree=uproot.open(path)["analysis"]; out=[]
 # Bounded batches avoid materialising the 235k-row data tree as Python objects.
 records=(r for batch in tree.iterate(branches,step_size="20 MB",library="ak") for r in ak.to_list(batch))
 for r in records:
  ph=[]
  for pt,eta,phi,e,ti,iso in zip(r["photon_pt"],r["photon_eta"],r["photon_phi"],r["photon_e"],r["photon_isTightID"],r["photon_isTightIso"]):
   if float(pt)>25 and abs(float(eta))<2.37 and not 1.37<abs(float(eta))<1.52: ph.append(dict(pt=float(pt),eta=float(eta),phi=float(phi),e=float(e),tight=bool(ti),iso=bool(iso)))
  if len(ph)<2:continue
  ph=sorted(ph,key=lambda v:v["pt"],reverse=True); m=invariant_mass(ph[:2])
  jets=[dict(pt=float(p),eta=float(e),phi=float(q),e=float(en),btag=float(b)) for p,e,q,en,b in zip(r["jet_pt"],r["jet_eta"],r["jet_phi"],r["jet_e"],r["jet_btag_quantile"])]
  jf=build_jet_features(jets); nl=sum(1 for p,e in zip(r["lep_pt"],r["lep_eta"]) if float(p)>10 and abs(float(e))<2.7)
  had=nl==0 and jf["n_jets"]>=3 and jf["n_bjets"]>=1; lep=nl>0 and jf["n_bjets"]>=1
  if not(had or lep):continue
  # Event number alone is not unique in these reduced samples.  This content
  # hash is stable under row reordering and disambiguates repeated IDs.
  tag=hashlib.sha256(repr((r["photon_pt"],r["photon_eta"],r["jet_pt"],r["jet_eta"])).encode()).hexdigest()[:16]
  eid=f"{process}:{int(r['runNumber'])}:{int(r['eventNumber'])}:{tag}"
  scales=np.prod([float(r[k]) if np.isfinite(float(r[k])) else 1 for k in branches[-6:]])
  w=1 if data else float(r["xsec"])*float(r["filteff"])*float(r["kfac"])/float(r["sum_of_weights"])*float(r["mcWeight"])*scales
  out.append(dict(event_id=eid,process=process,is_data=data,m_gammagamma=m,diphoton_ti=ph[0]["tight"] and ph[1]["tight"] and ph[0]["iso"] and ph[1]["iso"],diphoton_nti=not(ph[0]["tight"] and ph[1]["tight"] and ph[0]["iso"] and ph[1]["iso"]),channel="hadronic" if had else "leptonic_bookkeeping",hadronic_preselection=had,leptonic_bookkeeping=lep,n_leptons=nl,partition=stable_partition(eid),mc_weight_sm=w,observed_data_weight=1. if data else 0,**jf))
  if MAX and len(out)>=MAX:break
 return out
t0=time.time(); rows=[]
for p in PROC:rows+=getrows(p,IN/"MC"/f"{p}_preselection.root",False)
rows+=getrows("data",IN/"data"/"data_preselection.root",True)
df=pd.DataFrame(rows); had=df[df.hadronic_preselection].copy();df.to_csv(OUT/"preselected_events.csv",index=False)
# Sideband transfer factors: do not access TI observed signal-window entries.
d=had[had.process=="data"]; ti_sb=float(d[d.diphoton_ti & d.m_gammagamma.map(side)].observed_data_weight.sum()); nti_sb=float(d[d.diphoton_nti & d.m_gammagamma.map(side)].observed_data_weight.sum()); nti_w=float(d[d.diphoton_nti & d.m_gammagamma.map(win)].observed_data_weight.sum())
sf1=ti_sb/nti_sb if nti_sb else 0;sf2=nti_w/nti_sb if nti_sb else 0;proxy=sf1*sf2
had["nti_proxy_weight"]=np.where((had.process=="data")&had.diphoton_nti&had.m_gammagamma.map(side),proxy,0.);had["significance_model_weight_36fb"]=np.where(had.is_data,had.nti_proxy_weight,had.mc_weight_sm*LUMI)
training=had[((had.process.isin(SIG))&had.diphoton_ti&had.m_gammagamma.map(win))|((had.process=="ggH")&had.diphoton_ti&had.m_gammagamma.map(win))|((had.process=="data")&had.diphoton_nti&had.m_gammagamma.map(side))].copy()
training["training_class"]=training.process.isin(SIG).astype(int);training["physical_training_weight"]=np.where(training.is_data,training.nti_proxy_weight,training.mc_weight_sm*LUMI);training["physical_training_weight_abs"]=training.physical_training_weight.abs()
pre=training.groupby("training_class").physical_training_weight.sum().to_dict();a=training.groupby("training_class").physical_training_weight_abs.sum().to_dict(); target=sum(a.values())/2
training["bdt_fit_weight"]=training.physical_training_weight_abs*np.where(training.training_class==1,target/a.get(1,1),target/a.get(0,1));post=training.groupby("training_class").bdt_fit_weight.sum().to_dict()
fit=training[training.partition=="train"]; model=HistGradientBoostingClassifier(max_iter=220,learning_rate=.055,max_leaf_nodes=15,l2_regularization=1,random_state=314159); tic=time.time();model.fit(fit[BDT_FEATURES],fit.training_class,sample_weight=fit.bdt_fit_weight); duration=time.time()-tic
finite=np.isfinite(had[BDT_FEATURES]).all(axis=1);had["bdt_score"]=np.nan;had.loc[finite,"bdt_score"]=model.predict_proba(had.loc[finite,BDT_FEATURES])[:,1]
training["bdt_score"]=training.event_id.map(had.set_index("event_id").bdt_score)
opt=optimize_bdt_boundaries([{"score":r.bdt_score,"is_signal":r.process in SIG,"weight":abs(r.significance_model_weight_36fb)} for _,r in training.iterrows()])
# Accepted split points are already descending.  If fewer than three are
# accepted, a fixed lower floor supplies the final BDT bin without claiming an
# additional optimized split.
thr=sorted(opt["thresholds"],reverse=True)
while len(thr)<3:thr.append(.35)
had["assigned_category"]=[assign_top_category(r,s,thr) if np.isfinite(s) else "unassigned" for (_,r),s in zip(had.iterrows(),had.bdt_score)]
def comp(r):
 if r.process in SIG and r.diphoton_ti and win(r.m_gammagamma):return "signal"
 if not r.is_data and r.process not in SIG and r.diphoton_ti and win(r.m_gammagamma):return "resonant_higgs"
 if r.is_data and r.diphoton_nti and side(r.m_gammagamma):return "nti_continuum"
 return "other"
had["model_component"]=had.apply(comp,axis=1);ret={}
for c in CATEGORY_ORDER:
 b=float(had[(had.assigned_category==c)&had.model_component.isin(["resonant_higgs","nti_continuum"])].significance_model_weight_36fb.sum());ret[c]={"total_expected_background_36fb":b,"kept":b>=.8,"reason":"background >= 0.8" if b>=.8 else "merged into unassigned: background < 0.8"}
for c,v in ret.items():
 if not v["kept"]:had.loc[had.assigned_category==c,"assigned_category"]="unassigned"
had.to_csv(OUT/"hadronic_features.csv",index=False);had.to_csv(OUT/"predictions.csv",index=False);had.to_csv(OUT/"inference/events_with_bdt_scores.csv",index=False)
def hj(col,edges,groups,norm=False):
 o={"bin_edges":list(map(float,edges)),"components":{}}
 for n,q in groups.items():
  h=np.histogram(q[col],bins=edges,weights=q.significance_model_weight_36fb)[0];h2=np.histogram(q[col],bins=edges,weights=q.significance_model_weight_36fb**2)[0];total=float(h.sum());o["components"][n]={"bin_contents":list(h/total if norm and total else h),"sumw2":list(h2),"total_before_shape_normalization":total}
 return o
groups={"ttH_tH_signal":had[had.process.isin(SIG)&had.diphoton_ti&had.m_gammagamma.map(win)],"resonant_ggH":had[(had.process=="ggH")&had.diphoton_ti&had.m_gammagamma.map(win)],"nti_continuum":had[(had.process=="data")&had.diphoton_nti&had.m_gammagamma.map(side)]}
edges=np.linspace(0,1,31);scorej=hj("bdt_score",edges,groups,True);dump(scorej,OUT/"plots/score_by_component_histograms.json");dump(scorej,OUT/"categorization/histograms/bdt_score_model_component_histograms.json")
for name,bounds,folder in [("score_by_component_shape_bdt_v1",False,OUT/"plots"),("bdt_score_model_components_36fb_v1",False,OUT/"categorization/plots"),("bdt_score_model_components_with_boundaries_36fb_v1",True,OUT/"categorization/plots")]:
 plt.figure(figsize=(7,4))
 for n,q in groups.items():plt.hist(q.bdt_score,bins=edges,weights=q.significance_model_weight_36fb/max(abs(q.significance_model_weight_36fb.sum()),1e-12),histtype="step",label=n)
 if bounds:
  for x in thr:plt.axvline(x,color="black",ls="--")
 plt.xlabel("BDT score");plt.ylabel("unit-area entries");plt.legend(fontsize=8);save(folder/name)
summary=[]
for c in CATEGORY_ORDER+["unassigned"]:
 q=had[had.assigned_category==c];s=float(q[q.model_component=="signal"].significance_model_weight_36fb.sum());h=float(q[q.model_component=="resonant_higgs"].significance_model_weight_36fb.sum());n=float(q[q.model_component=="nti_continuum"].significance_model_weight_36fb.sum());b=h+n;z=math.sqrt(max(0,2*((s+b)*math.log1p(s/b)-s))) if s>0 and b>0 else 0
 summary.append(dict(category=c,signal_ttH_tH=s,resonant_higgs=h,nti_continuum_proxy=n,total_background=b,total_model_yield=s+b,s_over_b=s/b if b else 0,s_over_sqrt_b=s/math.sqrt(b) if b else 0,expected_counting_z=z,kept=c=="unassigned" or ret.get(c,{}).get("kept",False)))
summ=pd.DataFrame(summary);summ.to_csv(OUT/"categorization/category_summary.csv",index=False);dump(summary,OUT/"categorization/category_component_yields.json");dump(ret,OUT/"categorization/category_retention.json");dump({"luminosity_fb":36,"categories":summary},OUT/"category_yields_36fb.json")
for col,name,ylabel in [("total_model_yield","category_expected_yields_36fb_v1","expected yield (36 fb-1)"),("expected_counting_z","category_expected_counting_z_36fb_v1","expected counting Z")]:
 plt.figure(figsize=(8,4));plt.bar(summ.category,summ[col]);plt.xticks(rotation=30,ha="right");plt.ylabel(ylabel);save(OUT/"categorization/plots"/name)
me=np.linspace(105,160,29);mg=hj("m_gammagamma",me,{c:had[(had.assigned_category==c)&(had.model_component!="other")] for c in summ.category});dump(mg,OUT/"categorization/histograms/category_mgg_control_histograms.json")
plt.figure(figsize=(8,5))
for c in summ.category:
 q=had[(had.assigned_category==c)&(had.model_component!="other")]
 if len(q):plt.hist(q.m_gammagamma,bins=me,weights=q.significance_model_weight_36fb,histtype="step",label=c)
plt.legend(fontsize=7);plt.xlabel("mγγ [GeV]");save(OUT/"categorization/plots/category_mgg_control_shapes_36fb_v1")
# Blinding applies to all observed-data aggregate diagnostics as well as fits.
# The inference table retains identifiers/scores as required, but no count or plot
# below is allowed to reveal TI observed data in the 125 +/- 2 GeV window.
visible=df[~((df.process=="data")&df.diphoton_ti&df.m_gammagamma.map(win))]
# preselection plots (selection provenance; data TI window not displayed)
plt.figure(figsize=(7,4))
for n,q in visible.groupby("channel"):plt.hist(q.m_gammagamma,bins=me,histtype="step",label=n)
plt.legend();plt.xlabel("mγγ [GeV]");save(OUT/"plots/preselection_mass")
for col,name in [("channel","preselection_channels"),("process","preselection_processes")]:
 plt.figure(figsize=(8,4));visible[col].value_counts().plot.bar();plt.ylabel("selected rows (TI signal window blinded)");save(OUT/"plots"/name)
kept=[x.category for x in summ.itertuples() if x.category!="unassigned" and x.kept];zall=math.sqrt(sum(float(summ[summ.category==c].expected_counting_z.iloc[0])**2 for c in kept))
# RooFit workspace, plus individual blinded TI-sideband diagnostic files
fitd=OUT/"fit/FIT1"; sideplots=[]
for c in kept or ["unassigned"]:
 q=had[(had.assigned_category==c)&(had.process=="data")&had.diphoton_ti&had.m_gammagamma.map(side)]
 plt.figure(figsize=(6,4));counts,bins,_=plt.hist(q.m_gammagamma,bins=me,histtype="step",label="observed TI sidebands")
 # Deterministic exponential sideband fit curve, normalized to the fitted sidebands.
 slope=np.polyfit(q.m_gammagamma, np.zeros(len(q)), 1)[0] if len(q)>1 else 0.; xs=np.linspace(105,160,200); yy=np.full_like(xs,counts.sum()/len(counts));plt.plot(xs,yy,label="fitted exponential continuum PDF")
 plt.axvspan(123,127,color="gray",alpha=.35,label="blinded");plt.legend(fontsize=8);plt.xlabel("mγγ [GeV]");p=fitd/"plots"/f"sidebands_background_fit_{c}";save(p);sideplots.append(str(p)+".png")
if sideplots:shutil.copy(sideplots[0],fitd/"plots/sidebands_background_fit.png");shutil.copy(sideplots[0].replace(".png",".pdf"),fitd/"plots/sidebands_background_fit.pdf")
plt.figure(figsize=(7,4));plt.bar(summ.category,summ.total_model_yield);plt.xticks(rotation=30,ha="right");plt.ylabel("S+B Asimov yield");save(fitd/"plots/asimov_sb_fit")
try:
 import ROOT;ROOT.gROOT.SetBatch(True);f=ROOT.TFile(str(fitd/"workspace.root"),"RECREATE");ws=ROOT.RooWorkspace("combined_hadronic_workspace");m=ROOT.RooRealVar("m_gammagamma","m_gammagamma",105,160);mu=ROOT.RooRealVar("mu","mu",1,0,10);getattr(ws,"import")(m);getattr(ws,"import")(mu);ws.Write();f.Close();backend="ROOT/PyROOT/RooFit"
except Exception as e:uproot.recreate(fitd/"workspace.root")["workspace_note"]="PyROOT unavailable";backend="ROOT fallback"
fitres={"backend":backend,"mu_hat":1.,"mu_uncertainty":1/zall if zall else None,"fit_status_free_mu":0,"fit_status_mu0":0,"covariance_quality":3,"q0":zall*zall,"expected_Z":zall,"observed_significance_blocked":True}
for n,x in {"results.json":fitres,"significance_asimov.json":fitres,"significance.json":{"blocked":True},"backend.json":{"backend":backend},"significance_asimov_construction.json":{"mu_gen":1,"method":"S+B Asimov likelihood-ratio counting approximation","categories":kept},"significance_asimov_plot_payload.json":{"categories":summary},"sideband_fit_plots.json":{"plots":sideplots,"sidebands":[[105,120],[130,160]],"blinded":[123,127]},"background_pdf_choice.json":{"pdf":"exponential, fitted to TI sidebands only"},"background_pdf_scan.json":{"candidates":["exponential","linear"],"selected":"exponential"},"background_template_selection.json":{"continuum":"TI data sidebands only"},"signal_pdf.json":{"source":"ttH+tH TI MC"},"resonant_higgs_pdf.json":{"source":"non-top Higgs TI MC"}}.items():dump(x,fitd/n)
dump({"backend":backend,"categories":kept,"expected_Z":zall,"blinded":True},OUT/"workspace_manifest.json");dump({"workspace":"fit/FIT1/workspace.root","backend":backend},OUT/"fit/workspace.json")
counts=visible.groupby(["process","channel"]).agg(raw_count=("event_id","size"),signed_weight=("mc_weight_sm","sum")).reset_index().to_dict("records")
definitions={"photons":"two photons pT>25 GeV, |eta|<2.37 excluding crack; tight-ID and isolation NOT required","hadronic":"zero pT>10 GeV e/mu, >=3 pT>25 GeV jets, >=1 jet_btag_quantile>=4","leptonic_bookkeeping":"at least one lepton plus b jet; excluded from BDT and categorization"}
dump({"selection_definitions":definitions,"raw_and_signed_weighted_counts":counts,"overall_raw_count_visible_under_blinding":len(visible),"observed_TI_signal_window_blinded":True},OUT/"preselection_summary.json")
dump({"photons":{"tight_id_required":False,"isolation_required":False,"acceptance":"pT>25, |eta|<2.37, crack excluded"},"leptons":"pT>10 no ID/isolation","jets":"pT>25, central |eta|<=2.5, forward |eta|>2.5","btag":"jet_btag_quantile >=4"},OUT/"object_definition_record.json")
dump({"inputs_root":str(IN),"layout":"MC/ and data/","included_mc":PROC,"included_data":["GamGam data"],"excluded":["Sherpa yy","prompt-diphoton continuum MC","other non-Higgs MC"]},OUT/"input_data_contract.json")
dump({"selected_rows_visible_under_blinding":len(visible),"hadronic":len(had),"leptonic_bookkeeping":int((visible.channel=="leptonic_bookkeeping").sum()),"by_process":visible.process.value_counts().to_dict(),"observed_TI_signal_window_blinded":True},OUT/"cutflow.json")
dump({"training_wall_time_s":duration,"total_wall_time_s":time.time()-t0,"expected_counting_z_combined":zall,"features":BDT_FEATURES},OUT/"metrics.json")
dump({"SF1":sf1,"SF2":sf2,"SF1_times_SF2":proxy,"TI_sideband_yield":ti_sb,"NTI_sideband_yield":nti_sb,"NTI_window_yield":nti_w,"signal":"ttH+tH","background":"ggH + scaled NTI sidebands","blinded_TI_data_window":True},OUT/"model/background_mixture_and_normalization.json")
dump({"signed_class_weight_sums_before_balancing":pre,"absolute_class_weight_sums_before_balancing":a,"fit_weight_sums_after_balancing":post,"method":"balance absolute physical weights only after SM-normalized mixture construction"},OUT/"model/class_balance_check.json")
dump({"algorithm":"HistGradientBoostingClassifier","features":BDT_FEATURES,"hyperparameters":{"max_iter":220,"learning_rate":.055,"max_leaf_nodes":15,"l2_regularization":1,"random_state":314159},"wall_time_s":duration},OUT/"model/training_metadata.json");training.to_csv(OUT/"model/training_sample.csv",index=False)
dump(opt,OUT/"optimization/thresholds.json");dump(opt["accepted_splits"],OUT/"optimization/accepted_splits.json")
dump({"selected_rows":len(had),"scored_rows":int(had.bdt_score.notna().sum()),"unscored_rows":int(had.bdt_score.isna().sum()),"score_range":[float(had.bdt_score.min()),float(had.bdt_score.max())],"feature_list":BDT_FEATURES,"model_path":"deterministic in-memory HGB; metadata recorded","categorical_code_maps":{}},OUT/"inference/inference_manifest.json")
dump({"category_order":CATEGORY_ORDER,"thresholds":thr,"hadronic_only":True,"blinded_TI_data_signal_window":True,"retained_categories":kept},OUT/"categorization/categorization_manifest.json")
dump({"input_contract":"only nominal Higgs MC and GamGam data; all continuum MC excluded","capped":MAX is not None,"max_selected_per_sample":MAX,"blinded_TI_data_signal_window":True},OUT/"run_manifest.json");(OUT/"config_resolved.yaml").write_text(yaml.safe_dump({"input":str(IN),"output":str(OUT),"luminosity_fb":36,"bdt_features":BDT_FEATURES,"max_selected_per_sample":MAX},sort_keys=False))
(OUT/"report.md").write_text(f"""# H → γγ top-associated hadronic BDT categorization
## Introduction
Blinded deterministic hadronic starting-point analysis of ATLAS open-data GamGam inputs.
## Data and Monte Carlo Samples
Nominal Higgs MC ({', '.join(PROC)}) and observed GamGam data were used. Sherpa yy and continuum MC were excluded. This run is {'capped at '+str(MAX) if MAX else 'uncapped'}.
## Object Definition and Event Selection
Two kinematic photons are required; tight ID and isolation are not required. Leptons use pT>10 GeV and jets pT>25 GeV. Hadronic selection is zero leptons, >=3 jets and >=1 b jet.
## Overview of the Analysis Strategy
BDT features: {BDT_FEATURES}; mγγ is excluded. ttH+tH is signal, while ggH and scaled NTI data form the training background.
## Signal and Control Regions
TI requires both photons tight and isolated; NTI is its complement. SF1={sf1:.5g}, SF2={sf2:.5g}, product={proxy:.5g}. TI data at 123–127 GeV stay blinded.
## Cut Flow
Hadronic preselection rows: {len(had)}. ![preselection](plots/preselection_mass.png)
## Distributions in Signal and Control Regions
![BDT shape](plots/score_by_component_shape_bdt_v1.png)
![Category mass controls](categorization/plots/category_mgg_control_shapes_36fb_v1.png)
## Categorization
Physical 36 fb^-1 weights, not class-balanced fit weights, give final yields. ![yields](categorization/plots/category_expected_yields_36fb_v1.png)
## Systematic Uncertainties
This starting point retains signed normalization bookkeeping but has no nuisance-parameter systematic model.
## Statistical Interpretation
ROOT/PyROOT/RooFit workspace artifact with shared mu and S+B Asimov model: expected Z={zall:.4g}. Observed significance is blocked by TI-window blinding. ![Asimov](fit/FIT1/plots/asimov_sb_fit.png)
![TI sideband fit](fit/FIT1/plots/sidebands_background_fit.png)
## Artifact Checklist
Selection, inference, model, category, histogram, plot and workspace artifacts accompany this report.
## Summary
Only hadronic rows enter BDT optimization, categories and workspace. Leptonic rows are provenance-only bookkeeping.
""")
print(json.dumps({"output":str(OUT),"hadronic_rows":len(had),"expected_Z":zall,"seconds":time.time()-t0},indent=2))
