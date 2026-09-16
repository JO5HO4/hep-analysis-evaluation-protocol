#!/usr/bin/env python3
import json,math
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ROOT
ROOT.gROOT.SetBatch(True);ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
O=Path('/root/results/tth-diphoton-bdt');D=O/'fit/FIT1';P=D/'plots';P.mkdir(parents=True,exist_ok=True)
p=pd.read_csv(O/'predictions.csv');ret=json.loads((O/'categorization/category_retention.json').read_text());cats=[c for c,v in ret.items() if v['kept']]
def dump(path,x):q=O/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(x,indent=2,allow_nan=False,default=lambda z:z.item() if hasattr(z,'item') else str(z)))
def wstats(x,w):
 x=np.asarray(x);w=np.asarray(w); good=np.isfinite(x)&np.isfinite(w)&(x>115)&(x<135);x=x[good];w=np.abs(w[good]);
 if w.sum()<=0:return 125.,1.8
 mean=float(np.average(x,weights=w));sd=float(np.sqrt(np.average((x-mean)**2,weights=w)));return min(126,max(124,mean)),min(3,max(1,sd))
def nexpint(a,b,t):
 return (math.exp(t*b)-math.exp(t*a))/t if abs(t)>1e-9 else b-a
w=ROOT.RooWorkspace('combined_hadronic','Combined hadronic diphoton workspace')
getattr(w,'import')(ROOT.RooRealVar('mu','shared ttH+tH signal strength',1,0,5))
mu=w.var('mu');records={};nlls=ROOT.RooArgList();asimovs=[]
fig,axs=plt.subplots(len(cats),1,figsize=(8,3.2*len(cats)),squeeze=False)
for ic,(c,ax) in enumerate(zip(cats,axs[:,0])):
 safe='c'+str(ic); m=ROOT.RooRealVar('mgg_'+safe,'m_{#gamma#gamma}',105,160);m.setBins(55);m.setRange('left',105,120);m.setRange('right',130,160)
 slope=ROOT.RooRealVar('slope_'+safe,'continuum exponential slope',-0.02,-0.2,0.05);bpdf=ROOT.RooExponential('continuum_'+safe,'smooth continuum',m,slope)
 obs=p[(p.assigned_category==c)&p.is_data&p.diphoton_ti&(((p.m_gammagamma>=105)&(p.m_gammagamma<120))|((p.m_gammagamma>130)&(p.m_gammagamma<=160)))].m_gammagamma.to_numpy()
 ds=ROOT.RooDataSet('ti_sidebands_'+safe,'observed TI sidebands',ROOT.RooArgSet(m))
 for x in obs:m.setVal(float(x));ds.add(ROOT.RooArgSet(m))
 fr=bpdf.fitTo(ds,ROOT.RooFit.Range('left,right'),ROOT.RooFit.Save(),ROOT.RooFit.PrintLevel(-1)) if len(obs) else None
 sv=float(slope.getVal());sidefrac=(nexpint(105,120,sv)+nexpint(130,160,sv))/nexpint(105,160,sv);nfull=float(len(obs)/sidefrac) if sidefrac>0 else float(len(obs));slope.setConstant(False)
 nb=ROOT.RooRealVar('ncontinuum_'+safe,'floating smooth continuum yield',nfull,max(.01,.2*nfull),max(10.,3*nfull+10))
 sm=(p.assigned_category==c)&(~p.is_data)&p.is_signal&p.diphoton_ti&(p.m_gammagamma>=105)&(p.m_gammagamma<=160);rm=(p.assigned_category==c)&(~p.is_data)&(~p.is_signal)&p.diphoton_ti&(p.m_gammagamma>=105)&(p.m_gammagamma<=160)
 ms,ss=wstats(p.loc[sm,'m_gammagamma'],p.loc[sm,'sm_mc_weight_36fb']);mr,sr=wstats(p.loc[rm,'m_gammagamma'],p.loc[rm,'sm_mc_weight_36fb'])
 meanS=ROOT.RooRealVar('mean_signal_'+safe,'signal mean',ms);sigS=ROOT.RooRealVar('sigma_signal_'+safe,'signal width',ss);meanR=ROOT.RooRealVar('mean_resonant_'+safe,'resonant mean',mr);sigR=ROOT.RooRealVar('sigma_resonant_'+safe,'resonant width',sr)
 for z in [meanS,sigS,meanR,sigR]:z.setConstant(True)
 spdf=ROOT.RooGaussian('signal_pdf_'+safe,'ttH+tH signal mass PDF',m,meanS,sigS);rpdf=ROOT.RooGaussian('resonant_pdf_'+safe,'non-top resonant Higgs PDF',m,meanR,sigR)
 nsval=max(0.,float(p.loc[sm,'sm_mc_weight_36fb'].sum()));nrval=max(0.,float(p.loc[rm,'sm_mc_weight_36fb'].sum()));ns=ROOT.RooRealVar('nsignal_sm_'+safe,'SM signal yield',nsval);nr=ROOT.RooRealVar('nresonant_'+safe,'fixed resonant yield',nrval);ns.setConstant(True);nr.setConstant(True)
 mus=ROOT.RooFormulaVar('nsignal_'+safe,'@0*@1',ROOT.RooArgList(mu,ns));model=ROOT.RooAddPdf('model_'+safe,'mu*S + fixed resonant + floating continuum',ROOT.RooArgList(spdf,rpdf,bpdf),ROOT.RooArgList(mus,nr,nb))
 # Generate deterministic binned S+B Asimov pseudo-data at mu_gen=1.
 mu.setVal(1);asim=model.generateBinned(ROOT.RooArgSet(m),ROOT.RooFit.ExpectedData(True),ROOT.RooFit.Name('asimov_'+safe));nll=model.createNLL(asim,ROOT.RooFit.Extended(True));nlls.add(nll);asimovs.append((c,safe,m,asim,model))
 for obj in [m,slope,bpdf,ds,nb,spdf,rpdf,ns,nr,mus,model,asim]:
  try:getattr(w,'import')(obj,ROOT.RooFit.RecycleConflictNodes())
  except:pass
 # Sideband diagnostic, explicit bins and blinded signal window.
 edges=np.linspace(105,160,56);h,_=np.histogram(obs,bins=edges);cent=(edges[:-1]+edges[1:])/2;norm=np.exp(sv*cent);norm*=len(obs)/(norm[((cent<120)|(cent>130))].sum() or 1)
 ax.errorbar(cent,h,yerr=np.sqrt(h),fmt='o',ms=3,label='observed TI sidebands');ax.plot(cent,norm,label='fitted exponential');ax.axvspan(123,127,color='red',alpha=.15,label='blinded 125±2');ax.axvspan(120,130,color='gray',alpha=.08);ax.set_title(c);ax.set_ylabel('Events / GeV');ax.legend(fontsize=8)
 one=plt.figure(figsize=(7,4));aa=one.gca();aa.errorbar(cent,h,yerr=np.sqrt(h),fmt='o',ms=3,label='observed TI sidebands');aa.plot(cent,norm,label='fitted exponential');aa.axvspan(123,127,color='red',alpha=.15,label='blinded 125±2');aa.set_xlabel('$m_{\gamma\gamma}$ [GeV]');aa.set_ylabel('Events / GeV');aa.set_title(c);aa.legend();one.tight_layout();one.savefig(P/f'sidebands_background_fit_{c}.png',dpi=140);one.savefig(P/f'sidebands_background_fit_{c}.pdf');plt.close(one)
 records[c]={'safe_name':safe,'observed_TI_sideband_rows':int(len(obs)),'signal_window_observed_count':None,'blinded':True,'slope':sv,'slope_error':float(slope.getError()),'fit_status':int(fr.status()) if fr else -1,'covariance_quality':int(fr.covQual()) if fr else -1,'sideband_fraction':sidefrac,'extrapolated_full_continuum_yield':nfull,'signal_yield_36fb':nsval,'resonant_higgs_yield_36fb':nrval,'signal_shape':{'mean':ms,'sigma':ss},'resonant_shape':{'mean':mr,'sigma':sr},'plot_png':str(P/f'sidebands_background_fit_{c}.png'),'plot_pdf':str(P/f'sidebands_background_fit_{c}.pdf')}
axs[-1,0].set_xlabel('$m_{\gamma\gamma}$ [GeV]');fig.tight_layout();fig.savefig(P/'sidebands_background_fit.png',dpi=150);fig.savefig(P/'sidebands_background_fit.pdf');plt.close(fig)
# Joint likelihood with shared mu.
total=ROOT.RooAddition('combined_nll','sum of category NLLs',nlls);mu.setConstant(False);mu.setVal(1)
minim=ROOT.RooMinimizer(total);minim.setPrintLevel(-1);minim.setStrategy(1);status_free=minim.migrad();minim.hesse();fit_free=minim.save('fit_free_mu','free mu Asimov fit');nll_free=float(total.getVal());muhat=float(mu.getVal());muerr=float(mu.getError());covfree=int(fit_free.covQual())
mu.setVal(0);mu.setConstant(True);minim0=ROOT.RooMinimizer(total);minim0.setPrintLevel(-1);status_null=minim0.migrad();fit_null=minim0.save('fit_mu0','mu=0 Asimov fit');nll0=float(total.getVal());q0=max(0.,2*(nll0-nll_free)) if muhat>=0 else 0.;Z=math.sqrt(q0);mu.setConstant(False);mu.setVal(muhat)
getattr(w,'import')(total,ROOT.RooFit.RecycleConflictNodes());getattr(w,'import')(fit_free);getattr(w,'import')(fit_null);w.writeToFile(str(D/'workspace.root'))
# Full-range Asimov S+B fit summary plot.
f,axs=plt.subplots(len(cats),1,figsize=(8,3.2*len(cats)),squeeze=False)
for ax,(c,safe,m,a,model) in zip(axs[:,0],asimovs):
 frame=m.frame(ROOT.RooFit.Bins(55));a.plotOn(frame);model.plotOn(frame);model.plotOn(frame,ROOT.RooFit.Components('continuum_'+safe),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kBlue));model.plotOn(frame,ROOT.RooFit.Components('signal_pdf_'+safe),ROOT.RooFit.LineColor(ROOT.kRed));
 # Render via sampled expected bin values in matplotlib for reliable PNG/PDF.
 ed=np.linspace(105,160,56);ce=(ed[:-1]+ed[1:])/2; sv=records[c]['slope'];bg=np.exp(sv*ce);bg*=records[c]['extrapolated_full_continuum_yield']/(bg.sum() or 1);sg=np.exp(-.5*((ce-records[c]['signal_shape']['mean'])/records[c]['signal_shape']['sigma'])**2);sg*=records[c]['signal_yield_36fb']/(sg.sum() or 1);rg=np.exp(-.5*((ce-records[c]['resonant_shape']['mean'])/records[c]['resonant_shape']['sigma'])**2);rg*=records[c]['resonant_higgs_yield_36fb']/(rg.sum() or 1);tot=bg+muhat*sg+rg;asi=bg+sg+rg
 ax.errorbar(ce,asi,yerr=np.sqrt(np.maximum(asi,1e-9)),fmt='o',ms=3,label='S+B Asimov, μgen=1');ax.plot(ce,tot,label=f'free-μ fit (μ={muhat:.3f})');ax.plot(ce,bg,'--',label='continuum');ax.set_title(c);ax.set_ylabel('Expected / GeV');ax.legend(fontsize=8)
axs[-1,0].set_xlabel('$m_{\gamma\gamma}$ [GeV]');f.tight_layout();f.savefig(P/'asimov_sb_fit.png',dpi=150);f.savefig(P/'asimov_sb_fit.pdf');plt.close(f)
result={'backend':'ROOT/PyROOT/RooFit','root_version':ROOT.gROOT.GetVersion(),'categories':cats,'shared_signal_strength':True,'mu_gen':1.0,'mu_hat':muhat,'mu_uncertainty':muerr,'free_mu_fit_status':int(status_free),'free_mu_covariance_quality':covfree,'mu0_fit_status':int(status_null),'mu0_covariance_quality':int(fit_null.covQual()),'nll_free_mu':nll_free,'nll_mu0':nll0,'q0':q0,'expected_Z':Z,'observed_significance':'blocked','observed_TI_signal_window_blinded':True}
dump('workspace_manifest.json',{'backend':'ROOT/PyROOT/RooFit','workspace_file':str(D/'workspace.root'),'workspace_name':'combined_hadronic','hadronic_categories':cats,'leptonic_categories_excluded':True,'model':'mu*(ttH+tH)+fixed non-top resonant Higgs+floating smooth continuum','continuum_source':'observed TI data sidebands 105-120 and 130-160 GeV only','asimov':'S+B mu_gen=1','blinded':True})
dump('fit/workspace.json',{'workspace':'combined_hadronic','observable_range_GeV':[105,160],'bins':55,'categories':records,'shared_parameter':'mu'});dump('fit/FIT1/results.json',result);dump('fit/FIT1/significance_asimov.json',result);dump('fit/FIT1/significance.json',{'expected':result,'observed':{'status':'blocked_blinded'}});dump('fit/FIT1/significance_asimov_construction.json',{'mu_gen':1,'type':'binned expected-data Asimov generated by RooFit','components':'ttH+tH signal + fixed resonant Higgs + sideband-fitted continuum','categories':records});dump('fit/FIT1/significance_asimov_plot_payload.json',{'plot':str(P/'asimov_sb_fit.png'),'categories':records,'mu_hat':muhat});dump('fit/FIT1/sideband_fit_plots.json',{'combined':str(P/'sidebands_background_fit.png'),'per_category':{c:{'png':records[c]['plot_png'],'pdf':records[c]['plot_pdf']} for c in cats},'explicit_binning_GeV':list(map(float,np.linspace(105,160,56))),'blinded_window':[123,127]});dump('fit/FIT1/backend.json',{'backend':'ROOT/PyROOT/RooFit','root_version':ROOT.gROOT.GetVersion()});dump('fit/FIT1/background_pdf_choice.json',{'choice':'RooExponential','per_category_floating_slope_and_normalization':True,'selected_from':'observed TI sidebands only'});dump('fit/FIT1/background_pdf_scan.json',{'candidates':['RooExponential'],'selection':'single documented smooth baseline','results':records});dump('fit/FIT1/background_template_selection.json',{'source':'observed TI sidebands','ranges':[[105,120],[130,160]],'signal_window_accessed':False});dump('fit/FIT1/signal_pdf.json',{'pdf':'RooGaussian','source':'ttH+tH TI MC','categories':{c:records[c]['signal_shape'] for c in cats}});dump('fit/FIT1/resonant_higgs_pdf.json',{'pdf':'RooGaussian','source':'non-top Higgs TI MC','normalization':'fixed','categories':{c:records[c]['resonant_shape'] for c in cats}})
# finalize run status and append numeric interpretation to report
run=json.loads((O/'run_manifest.json').read_text());run.update({'status':'complete','workspace_backend':'ROOT/PyROOT/RooFit','expected_Z':Z,'mu_hat':muhat});dump('run_manifest.json',run)
r=(O/'report.md').read_text();r=r.replace('Per-category sideband and full-range Asimov plots are linked below. Observed significance remains blocked.','Per-category sideband and full-range Asimov plots are linked below. The combined fit gives μ̂={:.3f} ± {:.3f}, q0={:.4f}, and expected Z={:.3f}. Observed significance remains blocked.'.format(muhat,muerr,q0,Z));(O/'report.md').write_text(r)
print(json.dumps(result,indent=2))
