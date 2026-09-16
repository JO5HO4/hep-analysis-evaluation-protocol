import sys, json
sys.path.insert(0,'/root/pipeline')
from experiment import run_config
SV=[{"strategy":"greedy","max_cand":2},{"strategy":"maxsum","max_cand":2}]
cfgs=[
 {"name":"base kin_btag","feature_set":"kin_btag"},
 {"name":"kin_btag x5seeds","feature_set":"kin_btag","n_seeds":5},
 {"name":"kin_btag x5 +refit","feature_set":"kin_btag","n_seeds":5,"refit_trainval":True},
 {"name":"full_rank x5 +refit","feature_set":"full_rank","n_seeds":5,"refit_trainval":True},
 {"name":"kin_btag x5 refit esauc","feature_set":"kin_btag","n_seeds":5,"refit_trainval":True,"es_metric":"auc"},
]
res=[run_config(dict(c, sel_variants=SV)) for c in cfgs]
json.dump(res, open('/tmp/it3.json','w'), indent=1, default=str)
