"""Deterministic helpers for the hadronic top-associated H→γγ categorization."""
from __future__ import annotations
import hashlib, math

BDT_FEATURES = ("n_jets", "n_central_jets", "n_bjets", "ht_jets", "leading_jet_pt")
CATEGORY_ORDER = ("ttH_had_BDT1", "ttH_had_BDT2", "ttH_had_BDT3", "ttH_had_BDT4", "tH_had_4j1b", "tH_had_4j2b")

def build_jet_features(jets, pt_min=25.0, central_eta=2.5, btag_quantile=4):
    selected=[j for j in jets if float(j.get("pt",0))>pt_min]
    central=[j for j in selected if abs(float(j.get("eta",99)))<=central_eta]
    bjets=[j for j in selected if int(j.get("btag_quantile",-99))>=btag_quantile]
    return {"n_jets":len(selected),"n_central_jets":len(central),"n_forward_jets":len(selected)-len(central),
            "n_bjets":len(bjets),"ht_jets":sum(float(j.get("pt",0)) for j in selected),
            "leading_jet_pt":max([float(j.get("pt",0)) for j in selected],default=0.0)}

def invariant_mass(objects):
    px=py=pz=e=0.0
    for x in objects:
        pt,eta,phi=float(x["pt"]),float(x["eta"]),float(x["phi"])
        energy=float(x.get("e",pt*math.cosh(eta)))
        px+=pt*math.cos(phi);py+=pt*math.sin(phi);pz+=pt*math.sinh(eta);e+=energy
    return math.sqrt(max(0.,e*e-px*px-py*py-pz*pz))

def stable_partition(event_id, seed=20250308, fractions=(0.60,0.20,0.20)):
    h=int(hashlib.sha256(f"{seed}:{event_id}".encode()).hexdigest()[:16],16)/2**64
    if h < fractions[0]: return "train"
    if h < fractions[0]+fractions[1]: return "validation"
    return "test"

def assign_top_category(event, score=None, thresholds=None):
    thresholds=thresholds or []
    if event.get("channel")!="hadronic": return "unassigned"
    score=float(event.get("bdt_score",score if score is not None else -1))
    for i,t in enumerate(sorted(thresholds, reverse=True)[:4]):
        if score>=t: return f"ttH_had_BDT{i+1}"
    if int(event.get("n_central_jets",0))==4:
        if int(event.get("n_bjets",0))==1:return "tH_had_4j1b"
        if int(event.get("n_bjets",0))>=2:return "tH_had_4j2b"
    return "unassigned"

def optimize_bdt_boundaries(rows, config=None):
    """Greedy deterministic split optimizer using supplied score/signal/background weights."""
    import numpy as np
    c={"min_relative_improvement":.05,"max_splits":4,"grid_size":100}; c.update(config or {})
    a=list(rows); scores=np.array([float(r["bdt_score"]) for r in a]); sig=np.array([float(r.get("signal_weight",0)) for r in a]); bg=np.array([float(r.get("background_weight",0)) for r in a])
    candidates=np.linspace(.01,.99,c["grid_size"]-1); accepted=[]; history=[]
    def z(bounds):
      cuts=[0]+sorted(bounds)+[1]
      return math.sqrt(sum((S:=sig[(scores>=lo)&(scores<(hi if hi<1 else 1.000001))].sum())**2/max(bg[(scores>=lo)&(scores<(hi if hi<1 else 1.000001))].sum(),1e-9) for lo,hi in zip(cuts,cuts[1:])))
    prev=z([])
    for _ in range(c["max_splits"]):
      choices=[x for x in candidates if all(abs(x-y)>1e-9 for y in accepted)]
      best=max(choices,key=lambda x:z(accepted+[x])); now=z(accepted+[best]); rel=(now-prev)/max(prev,1e-12)
      if rel<c["min_relative_improvement"]: break
      accepted.append(float(best)); accepted.sort(reverse=True); history.append({"boundary":float(best),"expected_z":now,"relative_improvement":rel});prev=now
    return {"thresholds":accepted,"accepted_splits":history,"initial_expected_z":z([]),"final_expected_z":prev}
