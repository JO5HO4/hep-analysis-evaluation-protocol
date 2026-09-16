import sys, json
sys.path.insert(0,'/root/pipeline')
from cv import cv_config
cfg=json.loads(sys.argv[1]); out=sys.argv[2]
r,oof=cv_config(cfg)
json.dump(r, open(out,'w'), indent=1, default=str)
