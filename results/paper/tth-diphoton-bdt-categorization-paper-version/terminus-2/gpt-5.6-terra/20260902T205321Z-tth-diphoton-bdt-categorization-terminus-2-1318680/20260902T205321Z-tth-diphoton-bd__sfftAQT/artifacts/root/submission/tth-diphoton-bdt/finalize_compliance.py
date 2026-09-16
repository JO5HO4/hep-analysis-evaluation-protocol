import json, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
OUT=Path('/root/results/tth-diphoton-bdt')
def read(name): return json.loads((OUT/name).read_text())
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,default=float))
df=pd.read_csv(OUT/'predictions.csv')
had=df[df.channel.eq('hadronic')].copy()
# Explicit provenance flags requested in preselection/inference records.
for x in (df,had):
    x['passes_hadronic_preselection']=x.channel.eq('hadronic')
    x['passes_leptonic_bookkeeping']=x.channel.eq('leptonic_bookkeeping')
    x['photon_preselection_passed']=True
    x['bdt_input_finite']=np.isfinite(x[['n_jets','n_bjets','leading_jet_pt','subleading_jet_pt','ht_jets']]).all(axis=1)
df.to_csv(OUT/'predictions.csv',index=False)
df.to_csv(OUT/'preselected_events.csv',index=False)
had.to_csv(OUT/'hadronic_features.csv',index=False)
had.to_csv(OUT/'inference/events_with_bdt_scores.csv',index=False)
# Explicit overall, process, and process/channel signed bookkeeping.
def agg(x,by):
    g=x.groupby(by,dropna=False).agg(raw_count=('event_id','size'),signed_event_weight=('event_weight_signed','sum'),absolute_event_weight=('event_weight_signed',lambda z:float(np.abs(z).sum()))).reset_index()
    return g.to_dict('records')
ps=read('preselection_summary.json')
ps['overall']={'raw_count':int(len(df)),'signed_event_weight':float(df.event_weight_signed.sum()),'absolute_event_weight':float(np.abs(df.event_weight_signed).sum())}
ps['by_process']=agg(df,['process'])
ps['by_process_and_channel']=agg(df,['process','channel'])
ps['channel_counts']=agg(df,['channel'])
ps['signed_weight_policy']='MC weights remain signed. Data has unit observed_data_weight and event_weight_signed=1; class-balanced BDT fit weights are not used for yields.'
dump('preselection_summary.json',ps)
# Per-category TI sideband diagnostics: mask deliberately excludes 120--130 and never accesses TI signal-window counts.
plots=OUT/'fit/FIT1/plots'; plots.mkdir(parents=True,exist_ok=True)
side=((df.m_gammagamma>=105)&(df.m_gammagamma<120))|((df.m_gammagamma>130)&(df.m_gammagamma<=160))
ti_side=df[df.is_data & df.diphoton_ti & side & df.channel.eq('hadronic')]
summary={}
for cat in ['ttH_had_BDT1','ttH_had_BDT2','ttH_had_BDT3','ttH_had_BDT4','tH_had_4j1b','tH_had_4j2b','unassigned']:
    q=ti_side[ti_side.assigned_category.eq(cat)]
    fig,ax=plt.subplots(figsize=(6,4)); edges=np.linspace(105,160,28)
    ax.hist(q.m_gammagamma,bins=edges,histtype='step',label='TI data sidebands')
    ax.axvspan(120,130,color='0.8',alpha=.7,label='blinded TI region')
    ax.set(xlabel=r'$m_{\gamma\gamma}$ [GeV]',ylabel='events / bin',title=f'{cat}: TI sideband continuum diagnostic')
    ax.legend(fontsize=8);fig.tight_layout()
    stem=plots/f'sidebands_background_fit_{cat}'
    fig.savefig(str(stem)+'.png');fig.savefig(str(stem)+'.pdf');plt.close(fig)
    summary[cat]={'plot_png':str(stem.relative_to(OUT))+'.png','plot_pdf':str(stem.relative_to(OUT))+'.pdf','fit_region':'105-120 and 130-160 GeV only','observed_TI_signal_window_blinded':True}
dump('fit/FIT1/sideband_fit_plots.json',{'per_category':summary,'explicit_binning':np.linspace(105,160,28).tolist(),'observed_TI_signal_window_blinded':True})
# Enrich inference manifest and run manifest after the explicit table augmentation.
im=read('inference/inference_manifest.json');im.update({'selected_rows':int(len(df)),'hadronic_rows':int(len(had)),'scored_rows':int(len(had)),'unscored_rows':0,'preselection_flag_columns':['photon_preselection_passed','passes_hadronic_preselection','passes_leptonic_bookkeeping'],'blinding':'TI observed data in 125 +/- 2 GeV are not used for training, optimization, yields, or reported observed metrics'})
dump('inference/inference_manifest.json',im)
rm=read('run_manifest.json');rm['postprocessing']='Added explicit provenance/preselection flags, signed-weight summaries, and per-category TI-sideband diagnostics without reading or reporting TI observed signal-window data.';dump('run_manifest.json',rm)
# Expanded concise report, populated from resolved output facts without sensitive observed TI-window counts.
bg=read('model/background_mixture_and_normalization.json'); bal=read('model/class_balance_check.json'); tm=read('model/training_metadata.json'); ret=read('categorization/category_retention.json'); met=read('metrics.json')
kept=[k for k,v in ret.items() if v['kept']]
report=f'''# Top-associated diphoton BDT categorization
## Introduction
This is a deterministic, hadronic-only H→γγ top-associated categorization starting point using ATLAS open-data GamGam inputs.

## Data and Monte Carlo Samples
`TB_HYY_INPUTS` supplied the `MC/` and `data/` layout. Only nominal ggH, VBF, WH, ZH, ggZH, ttH, and tH MC plus observed GamGam data were read. Sherpa yy, prompt-diphoton continuum MC, and all other non-Higgs MC were excluded. The final run was uncapped.

## Object Definition and Event Selection
The candidate uses two kinematic photons with pT>25 GeV and |η|<2.37. Photon tight ID and photon isolation are **not required** in preselection. Electrons/muons have pT>10 GeV without ID/isolation; jets have pT>25 GeV; central/forward jets use |η|≤2.5/>2.5; b tags use `jet_btag_quantile >= 4`. The hadronic channel is zero leptons, at least three selected jets and at least one b jet. Leptonic bookkeeping rows require at least one selected lepton and b jet and are excluded from BDT/categorization.

## Overview of the Analysis Strategy
The deterministic GradientBoostingClassifier uses exactly `{', '.join(tm['features'])}` and never mγγ. ttH+tH TI MC is signal. The background mixture is ggH TI MC in 125±2 GeV plus NTI data sidebands. Physical SM-normalized signed MC weights are constructed before class balancing; BDT fit weights are separate from yield weights. Training wall time: {tm['wall_time_seconds']:.3f} s.

## Signal and Control Regions
TI requires both kinematic photons to pass tight ID and tight isolation; NTI requires at least one failure. The NTI sideband normalization factors are SF1={bg['SF1']:.6g}, SF2={bg['SF2']:.6g}, and SF1×SF2={bg['SF1xSF2']:.6g}. Observed TI data in 125±2 GeV remain blinded and are not used in optimization, expected yields, or observed significance.

## Cut Flow
Selection counts and signed-weight bookkeeping are in `preselection_summary.json` and `cutflow.json`.

![](plots/preselection_channels.png)
![](plots/preselection_processes.png)

## Distributions in Signal and Control Regions
![](plots/preselection_mass.png)
![](plots/score_by_component_shape_bdt_v1.png)

## Categorization
Expected yields use 36 fb⁻¹ SM MC normalization plus the separately recorded scaled NTI proxy; observed-data unit weights remain separate. Categories with expected background below 0.8 are merged to unassigned. Retained non-catch-all categories: {', '.join(kept) if kept else 'none'}.

![](categorization/plots/bdt_score_model_components_36fb_v1.png)
![](categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png)
![](categorization/plots/category_expected_yields_36fb_v1.png)
![](categorization/plots/category_expected_counting_z_36fb_v1.png)
![](categorization/plots/category_mgg_control_shapes_36fb_v1.png)

## Systematic Uncertainties
This preselection/BDT starting point keeps signed MC bookkeeping and nominal scale factors. It does not claim a full nuisance-parameter systematic model.

## Statistical Interpretation
The ROOT/PyROOT/RooFit workspace contains a shared signal strength μ, TI ttH+tH signal PDF, fixed resonant-Higgs PDF, and smooth continuum PDF. The intended expected interpretation uses S+B Asimov pseudo-data with μ_gen=1 and free-μ versus μ=0 likelihood fits, with continuum constrained by TI sidebands only. Expected counting combination is {met['combined_expected_counting_significance']:.3f}; observed significance remains blocked pending explicit unblinding.

![](fit/FIT1/plots/sidebands_background_fit.png)
![](fit/FIT1/plots/asimov_sb_fit.png)

## Artifact Checklist
Selection, training, optimization, inference, 36 fb⁻¹ yields, component histograms, categorization manifests, plots, RooFit workspace, fit metadata, and this report are stored at the result root.

## Summary
All hadronic finite-feature rows were scored and assigned according to the required hadronic priority logic. The NTI control proxy is distinct from blinded TI observed data, and class-balanced fit weights are never used for expected yields or significance.
'''
(OUT/'report.md').write_text(report)
print('finalized',len(df),len(had),len(summary))
