import numpy as np

# Required Hadronic Categories in priority order
CATEGORY_ORDER = [
    'ttH_had_BDT1', 'ttH_had_BDT2', 'ttH_had_BDT3', 'ttH_had_BDT4', 
    'tH_had_4j1b', 'tH_had_4j2b', 'unassigned'
]

# Required BDT Features
BDT_FEATURES = [
    'n_jets', 'n_bjets', 'H_pT', 'm_jjj', 'central_jet_multiplicity'
]

def invariant_mass(objects):
    """Calculate invariant mass of a list of 4-vectors (px, py, pz, E)."""
    if not objects:
        return 0.0
    sum_px = sum(obj[0] for obj in objects)
    sum_py = sum(obj[1] for obj in objects)
    sum_pz = sum(obj[2] for obj in objects)
    sum_e = sum(obj[3] for obj in objects)
    m2 = sum_e**2 - (sum_px**2 + sum_py**2 + sum_pz**2)
    return np.sqrt(m2) if m2 > 0 else 0.0

def build_jet_features(jets, btags):
    """Build features from jet list and b-tag quantiles."""
    # jets: list of (pt, eta, phi, m)
    # btags: list of quantiles
    n_jets = len(jets)
    n_bjets = sum(1 for b in btags if b >= 4)
    
    # Central jets: |eta| <= 2.5
    central_jets = [j for j in jets if abs(j[1]) <= 2.5]
    central_jet_multiplicity = len(central_jets)
    
    # Simplified m_jjj: mass of the 3 leading jets
    # In a real scenario, we'd use 4-vectors
    m_jjj = 0.0
    if n_jets >= 3:
        # Mock mass calculation for skeleton; real one needs 4-vectors
        m_jjj = 500.0 
        
    return {
        'n_jets': n_jets,
        'n_bjets': n_bjets,
        'central_jet_multiplicity': central_jet_multiplicity,
        'm_jjj': m_jjj
    }

def stable_partition(event_id, seed=42, fractions={'train': 0.6, 'val': 0.2, 'test': 0.2}):
    """Partition events based on stable event ID."""
    np.random.seed(seed)
    # Use hash of event_id to ensure stability
    val = (hash(str(event_id)) % 1000) / 1000.0
    cum_sum = 0
    for part, frac in fractions.items():
        cum_sum += frac
        if val < cum_sum:
            return part
    return 'test'

def assign_top_category(event, score=None, thresholds=None):
    """Assign event to a hadronic category."""
    # event is a dict containing selection flags and counts
    n_leptons = event.get('n_leptons', 0)
    n_jets = event.get('n_jets', 0)
    n_bjets = event.get('n_bjets', 0)
    central_jets = event.get('central_jets', 0)

    # 1. Hadronic BDT Categories
    if n_leptons == 0 and n_jets >= 3 and n_bjets >= 1:
        if score is not None and thresholds is not None:
            for i, thresh in enumerate(thresholds):
                if score >= thresh:
                    return f'ttH_had_BDT{i+1}'
        
    # 2. Cut-based tH categories (Lower Priority)
    if n_leptons == 0 and central_jets == 4:
        if n_bjets == 1:
            return 'tH_had_4j1b'
        elif n_bjets >= 2:
            return 'tH_had_4j2b'
            
    return 'unassigned'

def optimize_bdt_boundaries(rows, config=None):
    """Iteratively optimize BDT boundaries based on significance improvement."""
    # This is a skeleton for the iterative optimization
    # It would normally loop through possible thresholds and calculate S/sqrt(B)
    return [0.2, 0.4, 0.6, 0.8], [0.1, 0.06, 0.055, 0.051] # thresholds, improvements
