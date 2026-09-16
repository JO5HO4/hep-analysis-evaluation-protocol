"""Deterministic hadronic ttH/tH diphoton categorisation utilities."""
from __future__ import annotations
import hashlib, math

BDT_FEATURES = ["n_jets", "n_bjets", "jet_ht", "lead_jet_pt", "central_jet_fraction"]
CATEGORY_ORDER = ["ttH_had_BDT1", "ttH_had_BDT2", "ttH_had_BDT3", "ttH_had_BDT4", "tH_had_4j1b", "tH_had_4j2b"]

def invariant_mass(objects):
    px=sum(float(o["pt"])*math.cos(float(o["phi"])) for o in objects); py=sum(float(o["pt"])*math.sin(float(o["phi"])) for o in objects)
    pz=sum(float(o["pt"])*math.sinh(float(o["eta"])) for o in objects); e=sum(float(o.get("e",float(o["pt"])*math.cosh(float(o["eta"])))) for o in objects)
    return math.sqrt(max(0.,e*e-px*px-py*py-pz*pz))

def build_jet_features(jets, btag_quantile=4):
    selected=[j for j in jets if float(j["pt"])>25]; central=[j for j in selected if abs(float(j["eta"]))<=2.5]
    bjets=[j for j in selected if float(j.get("btag",-99))>=btag_quantile]; pts=sorted((float(j["pt"]) for j in selected),reverse=True)
    return {"n_jets":len(selected),"n_bjets":len(bjets),"jet_ht":sum(pts),"lead_jet_pt":pts[0] if pts else 0.,"central_jet_fraction":len(central)/len(selected) if selected else 0.,"n_central_jets":len(central),"n_forward_jets":len(selected)-len(central)}

def stable_partition(event_id, seed=20260902, fractions=(.6,.2,.2)):
    u=int(hashlib.sha256(f"{seed}:{event_id}".encode()).hexdigest()[:16],16)/2**64
    return "train" if u<fractions[0] else ("validation" if u<fractions[0]+fractions[1] else "test")

def assign_top_category(event, score=None, thresholds=None):
    thresholds=list(thresholds or [.85,.70,.55])+[.35]*3
    nlep=int(event.get("n_leptons",event.get("N_leptons",999)))
    if nlep==0 and score is not None:
        if score>=thresholds[0]: return "ttH_had_BDT1"
        if score>=thresholds[1]: return "ttH_had_BDT2"
        if score>=thresholds[2]: return "ttH_had_BDT3"
        if score>=.35: return "ttH_had_BDT4"
    if nlep==0 and int(event.get("n_central_jets",0))==4:
        if int(event.get("n_bjets",0))==1:return "tH_had_4j1b"
        if int(event.get("n_bjets",0))>=2:return "tH_had_4j2b"
    return "unassigned"

def optimize_bdt_boundaries(rows, config=None):
    config=config or {}; minimum=float(config.get("min_relative_improvement",.05)); candidates=config.get("candidates",[round(.35+.03*i,2) for i in range(21)])
    def z(bounds):
        edges=[-1]+sorted(bounds)+[2]; z2=0
        for lo,hi in zip(edges[:-1],edges[1:]):
            s=sum(float(r["weight"]) for r in rows if lo<=float(r["score"])<hi and r["is_signal"]); b=sum(float(r["weight"]) for r in rows if lo<=float(r["score"])<hi and not r["is_signal"])
            if s>0 and b>0:z2+=2*((s+b)*math.log1p(s/b)-s)
        return math.sqrt(max(z2,0))
    bounds=[]; previous=z(bounds); accepted=[]
    while len(bounds)<3:
        available=[(z(bounds+[c]),c) for c in candidates if c not in bounds]
        if not available:break
        best,c=max(available); rel=(best-previous)/previous if previous else (float("inf") if best else 0)
        if rel<minimum:break
        bounds.append(c); bounds.sort(); accepted.append({"boundary":c,"z_before":previous,"z_after":best,"relative_improvement":rel}); previous=best
    return {"thresholds":sorted(bounds,reverse=True),"accepted_splits":accepted,"final_expected_z":previous,"min_relative_improvement":minimum}
