"""Core deterministic top-associated diphoton categorization utilities."""
from __future__ import annotations
import hashlib, math
import numpy as np

BDT_FEATURES = ["n_jets", "n_bjets", "ht_jets", "leading_jet_pt", "min_dr_gam_jet"]
CATEGORY_ORDER = ["ttH_had_BDT1", "ttH_had_BDT2", "ttH_had_BDT3", "ttH_had_BDT4", "tH_had_4j1b", "tH_had_4j2b"]
DEFAULT_THRESHOLDS = [0.75, 0.50, 0.25, 0.0]

def _get(o, key, default=0.0):
    return o.get(key, default) if isinstance(o, dict) else getattr(o, key, default)

def invariant_mass(objects):
    """Invariant mass from objects having pt, eta, phi and either e or mass (consistent units)."""
    E=px=py=pz=0.0
    for o in objects:
        pt=float(_get(o,"pt")); eta=float(_get(o,"eta")); phi=float(_get(o,"phi"))
        mass=float(_get(o,"mass",_get(o,"m",0.0)))
        en=float(_get(o,"e",math.sqrt(max(0.0,(pt*math.cosh(eta))**2+mass**2))))
        E+=en; px+=pt*math.cos(phi); py+=pt*math.sin(phi); pz+=pt*math.sinh(eta)
    return math.sqrt(max(0.0,E*E-px*px-py*py-pz*pz))

def build_jet_features(jets, photons=None, pt_min=25.0, central_eta=2.5, btag_quantile=4):
    """Build the five BDT inputs and documented jet counts from selected pT>25 GeV jets."""
    js=[j for j in jets if float(_get(j,"pt"))>pt_min]
    central=[j for j in js if abs(float(_get(j,"eta")))<=central_eta]
    forward=[j for j in js if abs(float(_get(j,"eta")))>central_eta]
    b=[j for j in js if int(_get(j,"btag_quantile",_get(j,"btag",0)))>=btag_quantile]
    mindr=9.0
    for p in photons or []:
        for j in js:
            de=float(_get(p,"eta"))-float(_get(j,"eta")); dp=abs(float(_get(p,"phi"))-float(_get(j,"phi"))) ; dp=min(dp,2*math.pi-dp)
            mindr=min(mindr,math.hypot(de,dp))
    return {"n_jets":len(js),"n_central_jets":len(central),"n_forward_jets":len(forward),"n_bjets":len(b),
            "ht_jets":sum(float(_get(j,"pt")) for j in js),"leading_jet_pt":max([float(_get(j,"pt")) for j in js] or [0.0]),
            "min_dr_gam_jet":mindr}

def stable_partition(event_id, seed=1729, fractions=(0.6,0.2,0.2)):
    """Stable hash partition independent of input or row order."""
    if not math.isclose(sum(fractions),1.0,rel_tol=0,abs_tol=1e-9): raise ValueError("fractions must sum to one")
    h=int.from_bytes(hashlib.sha256(f"{seed}:{event_id}".encode()).digest()[:8],"big")/2**64
    c=0.0
    for name,f in zip(("train","validation","test"),fractions):
        c+=f
        if h<c: return name
    return "test"

def assign_top_category(event, score=None, thresholds=None):
    """Apply BDT categories first, then lower-priority exactly-four-central-jet tH cuts."""
    if not bool(_get(event,"passes_hadronic_preselection",True)): return "unassigned"
    if int(_get(event,"n_leptons",0))!=0: return "unassigned"
    s=float(score if score is not None else _get(event,"bdt_score",float("nan")))
    th=list(thresholds or DEFAULT_THRESHOLDS)
    while len(th)<4: th.append(0.0)
    if math.isfinite(s):
        for cat,t in zip(CATEGORY_ORDER[:4],th[:4]):
            if s>=float(t): return cat
    if int(_get(event,"n_central_jets",0))==4:
        nb=int(_get(event,"n_bjets",0))
        if nb==1: return "tH_had_4j1b"
        if nb>=2: return "tH_had_4j2b"
    return "unassigned"

def _z(s,b):
    s=max(0.0,float(s)); b=max(1e-12,float(b))
    return math.sqrt(max(0.0,2*((s+b)*math.log1p(s/b)-s)))

def optimize_bdt_boundaries(rows, config=None):
    """Greedy boundary addition maximizing quadrature Asimov Z; accept only >=5% improvement.

    Rows may be records or a DataFrame and must provide score, signal/yield indicator and
    physical (not class-balanced) significance weights. Deterministic candidate grid is used.
    """
    cfg={"min_relative_improvement":0.05,"max_categories":4,"min_background":0.8,"candidate_quantiles":np.linspace(.05,.95,37).tolist()}
    if config: cfg.update(config)
    def col(name,alts=()):
        if hasattr(rows,"columns"):
            for n in (name,)+alts:
                if n in rows.columns:return np.asarray(rows[n])
        out=[]
        for r in rows:
            out.append(_get(r,name,next((_get(r,a,None) for a in alts if _get(r,a,None) is not None),None)))
        return np.asarray(out)
    score=col("bdt_score",("score",)).astype(float); sig=col("is_signal",("signal",)).astype(bool)
    w=col("significance_model_weight_36fb",("yield_weight","weight")).astype(float)
    ok=np.isfinite(score)&np.isfinite(w); score,sig,w=score[ok],sig[ok],w[ok]
    cand=sorted(set(float(x) for x in np.quantile(score,cfg["candidate_quantiles"]))) if len(score) else []
    bounds=[]
    def total_z(bs):
        edges=[-np.inf]+sorted(bs)+[np.inf]; z2=0.0
        for lo,hi in zip(edges[:-1],edges[1:]):
            m=(score>=lo)&(score<hi); s=w[m&sig].sum(); b=w[m&~sig].sum()
            if b>=cfg["min_background"]: z2+=_z(s,b)**2
        return math.sqrt(z2)
    prev=total_z(bounds); accepted=[]
    while len(bounds)<cfg["max_categories"]-1:
        choices=[]
        for x in cand:
            if x in bounds: continue
            z=total_z(bounds+[x]); choices.append((z,x))
        if not choices: break
        best,x=max(choices,key=lambda q:(q[0],q[1])); rel=(best-prev)/prev if prev>0 else (float("inf") if best>0 else 0)
        if rel+1e-12<cfg["min_relative_improvement"]: break
        bounds.append(x); bounds.sort(); accepted.append({"boundary":x,"expected_z":best,"previous_z":prev,"relative_improvement":rel})
        prev=best
    # category thresholds are descending; pad only for API assignment bookkeeping
    return {"boundaries":sorted(bounds),"thresholds_descending":sorted(bounds,reverse=True)+[0.0],"accepted_splits":accepted,
            "final_expected_z":prev,"stop_rule":"best additional relative improvement < 5%","config":cfg}
