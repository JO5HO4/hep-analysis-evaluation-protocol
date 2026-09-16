import numpy as np
from sklearn.model_selection import train_test_split

# Hadronic categories priority order
CATEGORY_ORDER = [
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
    "tH_had_4j1b",
    "tH_had_4j2b",
    "unassigned"
]

# Features used for BDT training (m_gammagamma is excluded)
BDT_FEATURES = ["n_jets", "n_btags", "ht", "pt_gammagamma", "m_jjj"]

def invariant_mass(objects):
    """
    Calculate invariant mass of a set of objects (e.g., photons, jets).
    Expects objects to have px, py, pz, E.
    """
    sum_px = sum(obj.px for obj in objects)
    sum_py = sum(obj.py for obj in objects)
    sum_pz = sum(obj.pz for obj in objects)
    sum_e = sum(obj.e for obj in objects)
    m2 = sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)
    return np.sqrt(max(0, m2))

def build_jet_features(jets, diphoton):
    """
    Build BDT features for an event.
    jets: list of jet objects with pT, eta, phi, m, btag
    diphoton: object with pT, eta, phi, m
    """
    n_jets = len(jets)
    n_btags = sum(1 for j in jets if j.btag >= 4)
    ht = sum(j.pt for j in jets)
    pt_gammagamma = diphoton.pt
    
    # m_jjj: invariant mass of the 3 leading jets
    if n_jets >= 3:
        # Sort jets by pT descending
        sorted_jets = sorted(jets, key=lambda x: x.pt, reverse=True)
        leading_3 = sorted_jets[:3]
        m_jjj = invariant_mass(leading_3)
    else:
        m_jjj = 0.0
        
    return {
        "n_jets": n_jets,
        "n_btags": n_btags,
        "ht": ht,
        "pt_gammagamma": pt_gammagamma,
        "m_jjj": m_jjj
    }

def assign_top_category(event, score=None, thresholds=None):
    """
    Assign event to a category based on BDT score and hadronic cuts.
    """
    # 1. Check hadronic preselection first
    if event.n_leptons != 0 or event.n_jets < 3 or event.n_btags < 1:
        return "unassigned"

    # 2. BDT Categories
    if score is not None and thresholds is not None:
        # Use available thresholds. If fewer than 3, BDT4 is the rest.
        if len(thresholds) >= 1 and score > thresholds[0]:
            return "ttH_had_BDT1"
        if len(thresholds) >= 2 and score > thresholds[1]:
            return "ttH_had_BDT2"
        if len(thresholds) >= 3 and score > thresholds[2]:
            return "ttH_had_BDT3"
        
        # If we are here, event fails BDT1-3. Check tH cuts.
        if event.n_leptons == 0 and event.n_central_jets == 4:
            if event.n_btags >= 2: return "tH_had_4j2b"
            if event.n_btags == 1: return "tH_had_4j1b"
        
        return "ttH_had_BDT4"

    return "unassigned"
def stable_partition(event_id, seed=42, fractions=(0.6, 0.2, 0.2)):
    """
    Partition events into training, validation, test based on event_id.
    """
    state = np.random.RandomState(seed)
    # Use a hash of event_id to ensure stability
    # Since event_id might be a string or int, we use a hash
    h = hash(str(event_id)) % 1000
    # This is not quite right for fractions. Let's use a simpler approach:
    # We'll assume the caller provides the list of IDs and we partition them.
    # But the API requires (event_id, ...).
    # Let's use a deterministic mapping:
    val = (hash(str(event_id)) & 0xFFFFFFFF) / 0x100000000
    
    cum_frac = 0
    for i, frac in enumerate(fractions):
        cum_frac += frac
        if val < cum_frac:
            return ["train", "val", "test"][i]
    return "test"

def optimize_bdt_boundaries(rows, config=None):
    """
    Iteratively optimize BDT boundaries.
    rows: DataFrame with 'bdt_score', 'weight', 'is_signal'
    """
    def calculate_significance(data):
        s = data.loc[data['is_signal'] == 1, 'weight'].sum()
        b = data.loc[data['is_signal'] == 0, 'weight'].sum()
        if b <= 0: return 0
        return s / np.sqrt(b)

    current_thresholds = []
    best_sig = calculate_significance(rows)
    improvements = []

    for i in range(3):
        best_t = None
        best_iter_sig = 0
        
        for t in np.linspace(0.1, 0.9, 50):
            if not current_thresholds:
                test_set = rows[rows['bdt_score'] > t]
            else:
                last_t = current_thresholds[-1]
                test_set = rows[(rows['bdt_score'] > t) & (rows['bdt_score'] <= last_t)]
            
            sig = calculate_significance(test_set)
            if sig > best_iter_sig:
                best_iter_sig = sig
                best_t = t
        
        if best_t is not None:
            rel_imp = (best_iter_sig - best_sig) / (best_sig + 1e-9)
            if rel_imp >= 0.05:
                current_thresholds.append(best_t)
                best_sig += best_iter_sig
                improvements.append(rel_imp)
            else:
                break
        else:
            break
            
    return sorted(current_thresholds, reverse=True), improvements
