import sys, json; sys.path.insert(0,'/root/work')
from cv import eval_cv
eval_cv("E_d3_seeds5_k5", {"max_depth":3,"lr":0.03}, k=5, n_seeds=5)
eval_cv("E_d3_seeds1_k10", {"max_depth":3,"lr":0.03}, k=10, n_seeds=1)
eval_cv("E_d3_seeds5_k10", {"max_depth":3,"lr":0.03}, k=10, n_seeds=5)
