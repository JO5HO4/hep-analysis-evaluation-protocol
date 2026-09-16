import sys, json
sys.path.insert(0,'/root/pipeline')
from experiment import run_config
res=[]
for fs in ["required_only","kinematic","kin_btag","full","full_rank"]:
    res.append(run_config({"name":f"fs={fs}","feature_set":fs,
        "sel_variants":[{"strategy":"greedy","max_cand":2},{"strategy":"greedy","max_cand":1}]}))
json.dump(res, open('/tmp/it1.json','w'), indent=1, default=str)
