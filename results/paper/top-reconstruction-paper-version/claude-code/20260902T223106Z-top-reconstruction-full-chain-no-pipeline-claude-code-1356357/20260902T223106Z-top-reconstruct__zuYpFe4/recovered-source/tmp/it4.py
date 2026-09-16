import sys, json
sys.path.insert(0,'/root/pipeline')
from cv import cv_config
cfgs=[
 {"name":"CV kin_btag (1-stage)","feature_set":"kin_btag"},
 {"name":"CV full_rank (1-stage)","feature_set":"full_rank"},
 {"name":"CV kin_btag TWO-STAGE","feature_set":"kin_btag","two_stage":True},
 {"name":"CV full_rank TWO-STAGE","feature_set":"full_rank","two_stage":True},
]
out=[]
for c in cfgs:
    r,_=cv_config(c); out.append(r)
json.dump(out, open('/tmp/it4.json','w'), indent=1, default=str)
