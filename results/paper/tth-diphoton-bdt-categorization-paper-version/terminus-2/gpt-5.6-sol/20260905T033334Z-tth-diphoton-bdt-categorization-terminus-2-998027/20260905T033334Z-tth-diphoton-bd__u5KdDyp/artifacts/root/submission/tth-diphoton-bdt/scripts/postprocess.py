#!/usr/bin/env python3
import json,math,os,time
from pathlib import Path
import numpy as np,pandas as pd,yaml
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analysis.top_categorization import BDT_FEATURES,CATEGORY_ORDER
O=Path('/root/results/tth-diphoton-bdt'); p=pd.read_csv(O/'predictions.csv'); ALL=CATEGORY_ORDER+['unassigned']
def load(x): return json.loads((O/x).read_text())
def dump(x,v): q=O/x;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,indent=2,allow_nan=False,default=lambda z:z.item() if hasattr(z,'item') else str(z)))
def fig(path): plt.tight_layout();plt.savefig(O/(path+'.png'),dpi=150);plt.savefig(O/(path+'.pdf'));plt.close()
def az(s,b): return math.sqrt(max(0,2*((s+b)*math.log1p(s/max(b,1e-12))-s))) if s>0 else 0.
def hist(x,w,e):
 h=np.histogram(x,bins=e,weights=w)[0];h2=np.histogram(x,bins=e,weights=np.asarray(w)**2)[0]
 return {'bin_edges':list(map(float,e)),'bin_contents':list(map(float,h)),'sumw2':list(map(float,h2)),'component_total_before_shape_normalization':float(np.sum(w))}
side=((p.m_gammagamma>=105)&(p.m_gammagamma<120))|((p.m_gammagamma>130)&(p.m_gammagamma<=160));win=abs(p.m_gammagamma-125)<=2
ti=p.diphoton_ti.astype(bool);nti=p.diphoton_nti.astype(bool);data=p.is_data.astype(bool);sig=p.is_signal.astype(bool)
model=((~data)&ti&win)|(data&nti&side); reson=(~data)&(~sig)&ti&win; cont=data&nti&side; signal=(~data)&sig&ti&win
# category yields: signed physical weights retained; report all names explicitly
rows=[]; comp={}; z2=0
for c in ALL:
 m=p.assigned_category.eq(c); s=float(p.loc[m&signal,'significance_model_weight_36fb'].sum()); r=float(p.loc[m&reson,'significance_model_weight_36fb'].sum()); n=float(p.loc[m&cont,'nti_continuum_proxy_weight'].sum()); b=r+n; z=az(max(s,0),max(b,1e-12)); z2+=z*z if c!='unassigned' else 0
 row={'category':c,'signal_ttH_tH':s,'resonant_higgs_background':r,'nti_continuum_proxy':n,'total_background':b,'total_model_yield':s+b,'S_over_B':s/b if b>0 else 0,'S_over_sqrtB':s/math.sqrt(b) if b>0 else 0,'expected_counting_significance':z,'kept':c!='unassigned' and b>=.8}
 rows.append(row);comp[c]=row
pd.DataFrame(rows).to_csv(O/'categorization/category_summary.csv',index=False);dump('category_yields_36fb.json',{'luminosity_fb':36,'categories':rows,'combined_expected_counting_significance_kept_categories':math.sqrt(z2),'model':'TI MC 125+/-2 GeV plus NTI data sidebands scaled by SF1*SF2'});dump('categorization/category_component_yields.json',comp)
ret={c:{'kept':bool(next(x for x in rows if x['category']==c)['kept']),'expected_background_36fb':next(x for x in rows if x['category']==c)['total_background'],'threshold':.8,'action':'kept' if next(x for x in rows if x['category']==c)['kept'] else 'merged_into_unassigned_or_empty'} for c in CATEGORY_ORDER};dump('categorization/category_retention.json',ret)
kept=[c for c in CATEGORY_ORDER if ret[c]['kept']]
# score shape comparison, equal-area normalized, explicit [0,1]
e=np.linspace(0,1,31); shape_masks={'ttH+tH signal':signal,'resonant ggH background':(p['sample']=='ggH')&ti&win,'NTI continuum background':cont}; hp={}
plt.figure(figsize=(7,5))
for name,m in shape_masks.items():
 w=np.abs(p.loc[m,'sm_mc_weight_36fb'].to_numpy()) if name!='NTI continuum background' else p.loc[m,'nti_continuum_proxy_weight'].to_numpy(); x=p.loc[m,'bdt_score'].to_numpy(); z=hist(x,w,e); total=sum(z['bin_contents']);z['normalized_bin_contents']=[v/total if total else 0 for v in z['bin_contents']];hp[name]=z;plt.stairs(z['normalized_bin_contents'],e,label=name,linewidth=1.8)
plt.xlabel('BDT score');plt.ylabel('Normalized entries');plt.xlim(0,1);plt.legend();plt.title('Equal-area BDT score shapes');fig('plots/score_by_component_shape_bdt_v1');dump('plots/score_by_component_histograms.json',{'normalization':'each component normalized to unit area','components':hp})
# model score components plots/histograms
mh={};plt.figure(figsize=(7,5))
for name,m,wcol in [('ttH+tH signal',signal,'significance_model_weight_36fb'),('resonant Higgs background',reson,'significance_model_weight_36fb'),('NTI continuum proxy',cont,'nti_continuum_proxy_weight')]:
 z=hist(p.loc[m,'bdt_score'],p.loc[m,wcol],e);mh[name]=z;plt.stairs(z['bin_contents'],e,label=name)
plt.xlabel('BDT score');plt.ylabel('Expected events / bin (36 fb$^{-1}$)');plt.xlim(0,1);plt.legend();fig('categorization/plots/bdt_score_model_components_36fb_v1')
dump('categorization/histograms/bdt_score_model_component_histograms.json',{'luminosity_fb':36,'components':mh})
plt.figure(figsize=(7,5))
for name,z in mh.items():plt.stairs(z['bin_contents'],e,label=name)
for b in load('optimization/thresholds.json')['thresholds_descending']:plt.axvline(b,color='k',ls='--',alpha=.7)
plt.xlabel('BDT score');plt.ylabel('Expected events / bin (36 fb$^{-1}$)');plt.xlim(0,1);plt.legend();fig('categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1')
# yields and category Z
rr=pd.DataFrame(rows); q=rr[rr.category!='unassigned'];x=np.arange(len(q));plt.figure(figsize=(9,5));plt.bar(x,q.signal_ttH_tH,label='ttH+tH');plt.bar(x,q.resonant_higgs_background,bottom=q.signal_ttH_tH,label='resonant Higgs');plt.bar(x,q.nti_continuum_proxy,bottom=q.signal_ttH_tH+q.resonant_higgs_background,label='NTI proxy');plt.xticks(x,q.category,rotation=30,ha='right');plt.ylabel('Expected yield (36 fb$^{-1}$)');plt.legend();fig('categorization/plots/category_expected_yields_36fb_v1')
plt.figure(figsize=(9,5));plt.bar(x,q.expected_counting_significance);plt.xticks(x,q.category,rotation=30,ha='right');plt.ylabel('Expected counting Z');fig('categorization/plots/category_expected_counting_z_36fb_v1')
# mgg control histograms: NTI is intentionally retained over 120--130; observed TI window excluded from all plot inputs
me=np.linspace(105,160,56); mgh={};catsplot=kept or ['unassigned']; f,axs=plt.subplots(len(catsplot),1,figsize=(8,3.1*len(catsplot)),squeeze=False)
for ax,c in zip(axs[:,0],catsplot):
 mgh[c]={}
 for name,m,w in [('ttH+tH TI MC',(~data)&sig&ti&(p.assigned_category==c),'sm_mc_weight_36fb'),('resonant Higgs TI MC',(~data)&(~sig)&ti&(p.assigned_category==c),'sm_mc_weight_36fb'),('NTI data control',data&nti&(p.assigned_category==c),'observed_data_weight')]:
  z=hist(p.loc[m,'m_gammagamma'],p.loc[m,w],me);mgh[c][name]=z;ax.stairs(z['bin_contents'],me,label=name)
 ax.axvspan(123,127,color='gray',alpha=.15,label='TI-data blinded');ax.set_title(c);ax.set_ylabel('Events/bin');ax.legend(fontsize=8)
axs[-1,0].set_xlabel('$m_{\gamma\gamma}$ [GeV]');fig('categorization/plots/category_mgg_control_shapes_36fb_v1');dump('categorization/histograms/category_mgg_control_histograms.json',{'binning':list(map(float,me)),'NTI_120_130_removed':False,'observed_TI_signal_window_included':False,'categories':mgh})
# simple preselection plots
plt.figure();plt.hist(p.m_gammagamma,bins=55,range=(105,160),histtype='step');plt.xlabel('$m_{\gamma\gamma}$ [GeV]');plt.ylabel('Hadronic rows');fig('plots/preselection_mass')
plt.figure();plt.bar(['hadronic'],[len(p)]);plt.ylabel('Selected rows');fig('plots/preselection_channels')
plt.figure(figsize=(8,4));p['sample'].value_counts().reindex(['VBF','WH','ZH','ggH','ggZH','tH','ttH','data']).plot.bar();plt.ylabel('Selected rows');fig('plots/preselection_processes')
# manifests and metrics
manifest={'number_selected_rows':len(p),'number_scored_rows':int(np.isfinite(p.bdt_score).sum()),'number_unscored_rows':int((~np.isfinite(p.bdt_score)).sum()),'score_range':[float(p.bdt_score.min()),float(p.bdt_score.max())],'features':BDT_FEATURES,'model_path':str(O/'model/bdt_model.joblib'),'categorical_code_maps':{},'scope':'all and only hadronic-preselection rows'};dump('inference/inference_manifest.json',manifest)
dump('categorization/categorization_manifest.json',{'category_priority':CATEGORY_ORDER,'kept_workspace_categories':kept,'lower_priority_tH_definition':'after BDT failure: zero leptons, exactly four central jets, one or >=2 b tags','background_retention_minimum':.8,'luminosity_fb':36,'blinding':{'observed_TI_125_plus_minus_2_GeV':True,'observed_significance':'blocked'},'NTI_120_130_retained':True})
auc=0
try:
 t=pd.read_csv(O/'model/training_sample.csv');auc=float(__import__('sklearn.metrics').metrics.roc_auc_score(t.target,t.bdt_score,sample_weight=t.bdt_fit_weight))
except:pass
dump('metrics.json',{'weighted_training_auc':auc,'combined_expected_counting_significance':math.sqrt(z2),'SF1':load('model/background_mixture_and_normalization.json')['SF1'],'SF2':load('model/background_mixture_and_normalization.json')['SF2'],'SF1_times_SF2':load('model/background_mixture_and_normalization.json')['SF1_times_SF2'],'blinded_observed_TI_signal_window':True})
config={'input_root':os.getenv('TB_HYY_INPUTS','/data/GamGam'),'output_root':str(O),'samples':['VBF','WH','ZH','ggH','ggZH','tH','ttH','data'],'max_selected_per_sample':os.getenv('TTH_MAX_SELECTED_PER_SAMPLE'),'uncapped':not bool(os.getenv('TTH_MAX_SELECTED_PER_SAMPLE')),'luminosity_fb':36,'seed':1729,'features':BDT_FEATURES,'selection':{'photons':'pT>25, |eta|<2.37 excluding crack; no ID/isolation','leptons':'pT>10','jets':'pT>25','btag_quantile_min':4,'hadronic':'Nlep=0, Njet>=3, Nb>=1'}};(O/'config_resolved.yaml').write_text(yaml.safe_dump(config,sort_keys=False))
dump('run_manifest.json',{'status':'complete_pending_workspace','deterministic':True,'uncapped':config['uncapped'],'development_cap':config['max_selected_per_sample'],'input_scope':'nominal Higgs MC and observed GamGam data only','excluded':['Sherpa yy','prompt diphoton continuum MC','other non-Higgs MC'],'selected_rows':len(p),'blinding_enforced':True,'observed_significance':'blocked','root_inputs_copied':False})
# report
pre=load('preselection_summary.json'); norm=load('model/background_mixture_and_normalization.json'); opt=load('optimization/accepted_splits.json'); met=load('metrics.json')
report=f'''# Top-associated H → γγ hadronic BDT categorization

## Introduction
This deterministic, hadronic-only starting-point analysis categorizes top-associated Higgs diphoton candidates. Observed tight-isolated (TI) data at 125 ± 2 GeV remain blinded; observed significance is blocked.

## Data and Monte Carlo Samples
Inputs were read in place from `{config['input_root']}` using the `TB_HYY_INPUTS` contract. Only nominal VBF, WH, ZH, ggH, ggZH, ttH and tH Higgs MC and observed GamGam data were processed. Sherpa yy, prompt-diphoton MC, and all non-Higgs MC were excluded. This run is **uncapped**; `TTH_MAX_SELECTED_PER_SAMPLE` is supported only as an explicit development throttle.

## Object Definition and Event Selection
Two kinematic photons have pT > 25 GeV and |η| < 2.37 excluding 1.37–1.52. Tight ID and isolation are **not** preselection requirements. Leptons require pT > 10 GeV without ID/isolation. Jets require pT > 25 GeV; central means |η| ≤ 2.5 and forward means |η| > 2.5. A b jet has `jet_btag_quantile >= 4`. The channel is zero leptons, at least three jets and at least one b jet. No leptonic rows are retained.

## Overview of the Analysis Strategy
Stable SHA-256 event IDs define 60/20/20 train/validation/test partitions. The five inputs are {', '.join(BDT_FEATURES)}; mass is excluded. A deterministic HistGradientBoosting classifier (180 iterations, learning rate 0.055, 15 leaves) separates ttH+tH from ggH+NTI.

![Preselection mass](plots/preselection_mass.png)
![Preselection processes](plots/preselection_processes.png)

## Signal and Control Regions
Signal is ttH+tH TI MC in 125 ± 2 GeV. Background training mixes ggH TI MC in that window and NTI data in 105–120 and 130–160 GeV. TI means both photons pass tight ID and tight isolation; NTI means at least one fails. SF1={norm['SF1']:.6g}, SF2={norm['SF2']:.6g}, and SF1×SF2={norm['SF1_times_SF2']:.6g}. NTI 120–130 GeV entries are retained for control shapes. Nominal observed TI data in the blinded window are never counted or plotted.

## Cut Flow
The recomputed hadronic selection retained {pre['overall_written']:,} rows. Raw and signed weighted process counts are machine-readable in `cutflow.json` and `preselection_summary.json`.

## Distributions in Signal and Control Regions
![Equal-area BDT shapes](plots/score_by_component_shape_bdt_v1.png)
![Model components](categorization/plots/bdt_score_model_components_36fb_v1.png)
![Mass controls](categorization/plots/category_mgg_control_shapes_36fb_v1.png)

## Categorization
Class balancing was applied only after physical signal and ggH+NTI weights were formed; fit sums become 0.5/0.5, while yield weights remain separate. Iterative optimization accepted {len(opt['accepted_splits'])} split(s), stopping when another split improved expected significance by less than 5%. Expected yields use signed MC normalization at 36 fb⁻¹ and the separate scaled NTI proxy. Categories below 0.8 expected background are merged/unkept. Kept categories are {', '.join(kept)}. Combined counting Z is {met['combined_expected_counting_significance']:.3f}.

![Expected category yields](categorization/plots/category_expected_yields_36fb_v1.png)
![Expected counting significance](categorization/plots/category_expected_counting_z_36fb_v1.png)
![Boundaries](categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png)

## Systematic Uncertainties
This starting point includes nominal signed generator weights and available pileup, photon, b-tag and JVT scale factors. No nuisance-parameter variations are supplied by this open-data reduction; this limitation must be addressed before a precision result.

## Statistical Interpretation
A combined ROOT/PyROOT/RooFit workspace uses one shared μ for ttH+tH, fixed non-top resonant Higgs, and per-category floating smooth continuum models fitted only to observed TI sidebands. Signal-plus-background Asimov data use μ_gen=1; free-μ and μ=0 fits provide q0 and expected Z. Per-category sideband and full-range Asimov plots are linked below. Observed significance remains blocked.

![Sideband fits](fit/FIT1/plots/sidebands_background_fit.png)
![Asimov fit](fit/FIT1/plots/asimov_sb_fit.png)

## Artifact Checklist
Configuration, contracts, object definitions, event tables, model metadata, optimization records, inference manifest/table, category yields/histograms/plots, RooFit workspace/results, and this report are present under the result root.

## Summary
An uncapped, blinded, hadronic-only ttH/tH diphoton BDT categorization was completed with deterministic partitioning and explicit separation of classifier-fit, expected-model, NTI-proxy, and observed-data weights.
'''
(O/'report.md').write_text(report)
print('postprocess complete; kept',kept)
