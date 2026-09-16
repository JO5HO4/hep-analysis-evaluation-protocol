import uproot
import numpy as np

tree = uproot.open('/data/GamGam/MC/ttH_preselection.root')['analysis']
data = tree.arrays(['lep_pt', 'jet_pt', 'jet_btag_quantile'], library='pd').head(20)

for i, row in data.iterrows():
    lp = row['lep_pt']
    jp = row['jet_pt']
    jb = row['jet_btag_quantile']
    
    n_lep = len(lp) if isinstance(lp, (list, np.ndarray)) else 0
    n_jet = len(jp) if isinstance(jp, (list, np.ndarray)) else 0
    n_bjet = sum(1 for b in jb if b >= 4) if isinstance(jb, (list, np.ndarray)) else 0
    
    print(f"Event {i}: n_lep={n_lep}, n_jet={n_jet}, n_bjet={n_bjet} | PassHad={ (n_lep==0 and n_jet>=3 and n_bjet>=1) }, PassLep={ (n_lep>=1 and n_bjet>=1) }")
