#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import pandas as pd
from classifier_baseline import evaluate
p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
r=evaluate(pd.read_parquet(a.input)); r['input_provenance']={'path':str(a.input),'role':'development-proxy'}; a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
