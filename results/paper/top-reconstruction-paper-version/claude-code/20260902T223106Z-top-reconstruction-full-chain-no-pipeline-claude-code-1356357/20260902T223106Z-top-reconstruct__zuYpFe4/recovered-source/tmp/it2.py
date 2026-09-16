import sys, json
sys.path.insert(0,'/root/pipeline')
from experiment import run_config
SV=[{"strategy":"greedy","max_cand":2},{"strategy":"maxsum","max_cand":2}]
cfgs=[
 {"name":"kin_btag/es=eff","feature_set":"kin_btag"},
 {"name":"kin_btag/es=auc","feature_set":"kin_btag","es_metric":"auc"},
 {"name":"kin_btag/rankpair","feature_set":"kin_btag","objective":"rank:pairwise"},
 {"name":"kin_btag/rankndcg","feature_set":"kin_btag","objective":"rank:ndcg"},
 {"name":"kin_btag/spw=5","feature_set":"kin_btag","spw":5},
 {"name":"kin_btag/spw=22","feature_set":"kin_btag","spw":22},
 {"name":"kin_btag/eta.03d8","feature_set":"kin_btag","params":{"eta":0.03,"max_depth":8,"min_child_weight":10}},
 {"name":"kin_btag/eta.02d5","feature_set":"kin_btag","params":{"eta":0.02,"max_depth":5,"min_child_weight":3}},
 {"name":"kin_btag/d4","feature_set":"kin_btag","params":{"max_depth":4}},
 {"name":"kin_btag/d10","feature_set":"kin_btag","params":{"max_depth":10,"min_child_weight":20}},
]
res=[run_config(dict(c, sel_variants=SV)) for c in cfgs]
json.dump(res, open('/tmp/it2.json','w'), indent=1, default=str)
