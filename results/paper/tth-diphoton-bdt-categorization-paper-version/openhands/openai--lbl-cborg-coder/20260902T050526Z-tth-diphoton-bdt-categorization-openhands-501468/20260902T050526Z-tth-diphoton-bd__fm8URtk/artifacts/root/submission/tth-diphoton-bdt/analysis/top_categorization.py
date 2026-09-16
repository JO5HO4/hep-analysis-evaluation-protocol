import numpy as np
from typing import List, Dict, Any, Optional, Tuple

# Required hadronic category priority order
CATEGORY_ORDER = [
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
    "tH_had_4j1b",
    "tH_had_4j2b",
    "unassigned"
]

# BDT Features exactly as required
BDT_FEATURES = [
    "n_jets",
    "n_bjets",
    "h_pT",
    "h_eta",
    "m_jets"
]

def invariant_mass(objects):
    """
    Calculates the invariant mass of a system of objects.
    Expected object format: {'px': ..., 'py': ..., 'pz': ..., 'e': ...}
    """
    total_px = sum(obj.get('px', 0) for obj in objects)
    total_py = sum(obj.get('py', 0) for obj in objects)
    total_pz = sum(obj.get('pz', 0) for obj in objects)
    total_e = sum(obj.get('e', 0) for obj in objects)
    
    m2 = total_e**2 - (total_px**2 + total_py**2 + total_pz**2)
    return np.sqrt(m2) if m2 > 0 else 0.0

def build_jet_features(jets, btag_threshold=4):
    """
    Builds the 5 BDT features from selected jets.
    - n_jets: Number of central jets (|eta| <= 2.5)
    - n_bjets: Number of central jets with btag_quantile >= btag_threshold
    - h_pT: pT of the Higgs candidate (should be passed as an argument usually, 
            but here we follow the API signature if needed)
    - h_eta: eta of the Higgs candidate
    - m_jets: Invariant mass of the jets
    
    Wait, the required API is build_jet_features(jets, ...). 
    Let's refine this to calculate the jet-specific components.
    """
    central_jets = [j for j in jets if abs(j['eta']) <= 2.5]
    n_jets = len(central_jets)
    n_bjets = len([j for j in central_jets if j.get('jet_btag_quantile', 0) >= btag_threshold])
    
    # Invariant mass of central jets
    m_jets = invariant_mass(central_jets) if central_jets else 0.0
    
    return {
        "n_jets": n_jets,
        "n_bjets": n_bjets,
        "m_jets": m_jets
    }

def assign_top_category(event, score=None, thresholds=None):
    """
    Assigns a hadronic category to an event.
    - BDT categories (ttH_had_BDT1-4) are based on 'score' and 'thresholds'.
    - tH categories (tH_had_4j1b, tH_had_4j2b) are fallback cuts.
    """
    # Hadronic preselection: n_leptons == 0, n_jets >= 3, n_bjets >= 1
    # This is expected to be called only on hadronic-preselection events.
    
    # 1. BDT Category Assignment
    if score is not None and thresholds is not None:
        # thresholds is expected to be a sorted list of BDT score boundaries
        # e.g. [0.1, 0.3, 0.6] -> BDT1: [0.6, 1], BDT2: [0.3, 0.6), etc.
        # But we should check the exact definition of BDT1 vs BDT4.
        # Usually BDT1 is the highest score.
        
        sorted_thresholds = sorted(thresholds, reverse=True)
        if score >= sorted_thresholds[0]:
            return "ttH_had_BDT1"
        elif len(sorted_thresholds) > 1 and score >= sorted_thresholds[1]:
            return "ttH_had_BDT2"
        elif len(sorted_thresholds) > 2 and score >= sorted_thresholds[2]:
            return "ttH_had_BDT3"
        elif len(sorted_thresholds) > 3 and score >= sorted_thresholds[3]:
            return "ttH_had_BDT4"
        # If BDT boundaries are fewer, they might be assigned differently.
        # Let's handle the case where boundaries < 4.
        # If score < all thresholds, it proceeds to tH fallback.
        
        # Wait, if thresholds are [T1, T2, T3] where T1 > T2 > T3
        # Score >= T1 -> BDT1
        # T1 > Score >= T2 -> BDT2
        # T2 > Score >= T3 -> BDT3
        # T3 > Score -> Fallback
        
        # The requirements say "six hadronic categories: ttH_had_BDT1...4, tH_had_4j1b, tH_had_4j2b, plus unassigned"
        # I will implement a flexible check.
        
        # Let's re-evaluate based on the index.
        for i in range(min(4, len(sorted_thresholds))):
            if score >= sorted_thresholds[i]:
                return f"ttH_had_BDT{i+1}"

    # 2. tH Fallback Categories
    # Require: n_leptons == 0, exactly 4 central jets.
    n_leptons = event.get('n_leptons', 0)
    central_jets = [j for j in event.get('jets', []) if abs(j['eta']) <= 2.5]
    n_central_jets = len(central_jets)
    n_bjets_central = len([j for j in central_jets if j.get('jet_btag_quantile', 0) >= 4])
    
    if n_leptons == 0 and n_central_jets == 4:
        if n_bjets_central == 1:
            return "tH_had_4j1b"
        elif n_bjets_central >= 2:
            return "tH_had_4j2b"
            
    return "unassigned"

def stable_partition(event_id, seed=42, fractions=(0.6, 0.2, 0.2)):
    """
    Partitions events into (train, val, test) based on event_id.
    """
    # Use a hash of event_id for stability
    state = np.random.RandomState(seed)
    # This is a bit tricky with event_id as string/int. Let's normalize.
    # A simpler way to make it stable:
    import hashlib
    hash_val = int(hashlib.sha256(str(event_id).encode()).hexdigest(), 16)
    normalized_val = (hash_val % 10000) / 10000.0
    
    cum_frac = 0
    for i, frac in enumerate(fractions):
        cum_frac += frac
        if normalized_val < cum_frac:
            return ['train', 'val', 'test'][i]
    return 'test'

def optimize_bdt_boundaries(rows, config=None):
    """
    Iteratively optimize BDT boundaries to maximize significance.
    """
    # This will be implemented more fully in the pipeline, but let's provide the signature.
    # rows: DataFrame containing BDT scores and SM weights.
    # config: configuration for optimization.
    # Returns: list of accepted thresholds.
    
    # Placeholder implementation
    return []
