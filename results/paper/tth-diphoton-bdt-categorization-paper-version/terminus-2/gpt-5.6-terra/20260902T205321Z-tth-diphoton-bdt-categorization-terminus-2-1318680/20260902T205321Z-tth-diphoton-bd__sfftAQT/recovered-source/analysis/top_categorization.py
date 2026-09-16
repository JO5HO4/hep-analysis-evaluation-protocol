"""Hadronic H->gamma gamma top-associated categorization utilities."""
import hashlib, math
CATEGORY_ORDER=['ttH_had_BDT1','ttH_had_BDT2','ttH_had_BDT3','ttH_had_BDT4','tH_had_4j1b','tH_had_4j2b']
BDT_FEATURES=['n_jets','n_bjets','leading_jet_pt','subleading_jet_pt','ht_jets']
def invariant_mass(objects):
 p=[0.,0.,0.,0.]
 for o in objects:
  pt,eta,phi,e=o[:4]; p[0]+=pt*math.cos(phi);p[1]+=pt*math.sin(phi);p[2]+=pt*math.sinh(eta);p[3]+=e
 return math.sqrt(max(0,p[3]*p[3]-p[0]*p[0]-p[1]*p[1]-p[2]*p[2]))
def build_jet_features(jets, central_eta=2.5):
 # jets iterable of (pt,eta,phi,e,btag); assumes pT >25 selection already if supplied
 j=[x for x in jets if x[0]>25]; c=[x for x in j if abs(x[1])<=central_eta]; b=[x for x in j if x[4]>=4]
 pts=sorted((x[0] for x in j),reverse=True)
 return {'n_jets':len(j),'n_central_jets':len(c),'n_forward_jets':len(j)-len(c),'n_bjets':len(b),'leading_jet_pt':pts[0] if pts else 0.,'subleading_jet_pt':pts[1] if len(pts)>1 else 0.,'ht_jets':sum(pts)}
def stable_partition(event_id,seed=20240517,fractions=(.6,.2,.2)):
 x=int(hashlib.sha256((str(seed)+'|'+str(event_id)).encode()).hexdigest()[:16],16)/2**64
 return 'train' if x<fractions[0] else ('validation' if x<fractions[0]+fractions[1] else 'test')
def assign_top_category(event,score=None,thresholds=None):
 score=event.get('bdt_score',score); thresholds=thresholds or [0.85,0.70,0.55,0.40]
 if event.get('channel')=='hadronic' and score is not None:
  for i,t in enumerate(thresholds):
   if score>=t:return CATEGORY_ORDER[i]
  if event.get('n_leptons',0)==0 and event.get('n_central_jets')==4:
   if event.get('n_bjets')==1:return 'tH_had_4j1b'
   if event.get('n_bjets')>=2:return 'tH_had_4j2b'
 return 'unassigned'
def optimize_bdt_boundaries(rows,config=None):
 # deterministic quantile scan, returns greedy splits satisfying >=5% expected-Z gain
 import numpy as np
 cfg=config or {}; minimp=cfg.get('min_relative_improvement',.05)
 a=np.asarray(rows['score'] if hasattr(rows,'__getitem__') else [r['bdt_score'] for r in rows],float)
 s=np.asarray(rows.get('signal_weight',np.ones(len(a))) if hasattr(rows,'get') else [r.get('signal_weight',0) for r in rows],float)
 b=np.asarray(rows.get('background_weight',np.ones(len(a))) if hasattr(rows,'get') else [r.get('background_weight',0) for r in rows],float)
 def z(edges):
  ix=np.digitize(a,[-np.inf]+sorted(edges)+[np.inf]); return math.sqrt(sum((s[ix==k].sum())**2/max(b[ix==k].sum(),1e-9) for k in np.unique(ix)))
 edges=[]; old=z(edges); accepted=[]
 for _ in range(3):
  choices=[]
  for q in np.linspace(.1,.9,33):
   t=float(np.quantile(a,q))
   if t in edges:continue
   zz=z(edges+[t]); choices.append((zz,t))
  if not choices:break
  zz,t=max(choices)
  imp=(zz-old)/max(old,1e-12)
  if imp<minimp:break
  edges.append(t);edges.sort();accepted.append({'boundary':t,'expected_z':zz,'relative_improvement':imp});old=zz
 return sorted(edges,reverse=True),accepted
