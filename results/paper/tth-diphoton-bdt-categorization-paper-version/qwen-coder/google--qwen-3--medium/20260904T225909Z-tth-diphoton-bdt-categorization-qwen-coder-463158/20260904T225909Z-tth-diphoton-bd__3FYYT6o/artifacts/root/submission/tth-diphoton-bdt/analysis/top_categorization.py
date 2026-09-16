"""
Core module for top-associated H->gamma gamma categorization.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple

# Required constants
CATEGORY_ORDER = [
    "ttH_had_BDT1",
    "ttH_had_BDT2",
    "ttH_had_BDT3",
    "ttH_had_BDT4",
    "tH_had_4j1b",
    "tH_had_4j2b",
    "unassigned"
]

BDT_FEATURES = [
    "jet_pt_sum",
    "jet_eta_max",
    "bjet_pt_max",
    "bjet_eta_max",
    "diphoton_pt"
]


def build_jet_features(jets: pd.DataFrame, photons: pd.DataFrame) -> Dict[str, float]:
    """
    Build jet-related features for BDT.

    Args:
        jets: DataFrame with jet properties (pt, eta, btag_quantile)
        photons: DataFrame with diphoton system (for diphoton_pt)

    Returns:
        Dictionary of jet features
    """
    # Select jets with pt > 25 GeV
    selected_jets = jets[jets['pt'] > 25.0].copy()
    central_jets = selected_jets[abs(selected_jets['eta']) <= 2.5]
    bjets = selected_jets[selected_jets['btag_quantile'] >= 4]

    features = {
        "jet_pt_sum": selected_jets['pt'].sum(),
        "jet_eta_max": selected_jets['eta'].abs().max() if len(selected_jets) > 0 else 0.0,
        "bjet_pt_max": bjets['pt'].max() if len(bjets) > 0 else 0.0,
        "bjet_eta_max": bjets['eta'].abs().max() if len(bjets) > 0 else 0.0,
        "diphoton_pt": photons['pt'].iloc[0] if len(photons) > 0 else 0.0
    }
    return features


def invariant_mass(objects: pd.DataFrame) -> float:
    """
    Calculate invariant mass of a system of objects.

    Args:
        objects: DataFrame with 'pt', 'eta', 'phi', 'e' columns

    Returns:
        Invariant mass in GeV
    """
    if len(objects) == 0:
        return 0.0
    
    px = (objects['pt'] * np.cos(objects['phi'])).sum()
    py = (objects['pt'] * np.sin(objects['phi'])).sum()
    pz = (objects['pt'] * np.sinh(objects['eta'])).sum()
    e = objects['e'].sum()
    
    m2 = e**2 - px**2 - py**2 - pz**2
    return np.sqrt(m2) if m2 > 0 else 0.0


def assign_top_category(
    event: Dict,
    score: Optional[float] = None,
    thresholds: Optional[List[float]] = None
) -> str:
    """
    Assign top-associated category to an event.

    Args:
        event: Event dictionary with jet and lepton counts
        score: BDT score (for BDT categories)
        thresholds: List of BDT score thresholds [t1, t2, t3, t4] in descending order

    Returns:
        Category name
    """
    if thresholds is None:
        thresholds = [0.9, 0.8, 0.7, 0.6]  # Default thresholds

    n_leptons = event.get('n_leptons', 0)
    n_central_jets = event.get('n_central_jets', 0)
    n_bjets = event.get('n_bjets', 0)

    # Hadronic BDT categories
    if n_leptons == 0 and score is not None:
        if score >= thresholds[0]:
            return "ttH_had_BDT1"
        elif score >= thresholds[1]:
            return "ttH_had_BDT2"
        elif score >= thresholds[2]:
            return "ttH_had_BDT3"
        elif score >= thresholds[3]:
            return "ttH_had_BDT4"
    
    # Cut-based tH categories (only if not assigned to BDT category)
    if n_leptons == 0 and n_central_jets == 4:
        if n_bjets == 1:
            return "tH_had_4j1b"
        elif n_bjets >= 2:
            return "tH_had_4j2b"
    
    return "unassigned"


def stable_partition(
    event_id: int,
    seed: int = 42,
    fractions: Tuple[float, float, float] = (0.6, 0.2, 0.2)
) -> str:
    """
    Assign event to partition (train, validation, test) based on stable hash.

    Args:
        event_id: Stable event identifier
        seed: Random seed for reproducibility
        fractions: Fractions for (train, validation, test)

    Returns:
        Partition name: 'train', 'validation', or 'test'
    """
    np.random.seed(seed)
    # Use event_id to create a deterministic but seemingly random value
    hash_val = (event_id * 97 + seed) % 1000000
    rand = hash_val / 1000000.0
    
    train_frac, val_frac, test_frac = fractions
    if rand < train_frac:
        return "train"
    elif rand < train_frac + val_frac:
        return "validation"
    else:
        return "test"


def optimize_bdt_boundaries(
    rows: pd.DataFrame,
    config: Optional[Dict] = None
) -> List[float]:
    """
    Optimize BDT category boundaries iteratively.

    Args:
        rows: DataFrame with 'bdt_score' and 'weight' columns, and 'is_signal' boolean
        config: Configuration dictionary with 'min_improvement' etc.

    Returns:
        List of thresholds in descending order [t1, t2, t3, t4]
    """
    if config is None:
        config = {}
    
    min_improvement = config.get('min_improvement', 0.05)
    max_boundaries = config.get('max_boundaries', 10)
    
    # Sort rows by BDT score descending
    sorted_rows = rows.sort_values('bdt_score', ascending=False).copy()
    
    # Calculate cumulative yields
    sorted_rows['signal_weight'] = sorted_rows['weight'] * sorted_rows['is_signal']
    sorted_rows['bkg_weight'] = sorted_rows['weight'] * (1 - sorted_rows['is_signal'])
    
    sorted_rows['cumsum_signal'] = sorted_rows['signal_weight'].cumsum()
    sorted_rows['cumsum_bkg'] = sorted_rows['bkg_weight'].cumsum()
    
    # Calculate S/sqrt(B) for each possible split
    sorted_rows['significance'] = sorted_rows['cumsum_signal'] / np.sqrt(sorted_rows['cumsum_bkg'])
    
    thresholds = []
    prev_significance = 0.0
    
    for i in range(1, len(sorted_rows)):
        if len(thresholds) >= max_boundaries:
            break
            
        current_significance = sorted_rows.iloc[i-1]['significance']
        if current_significance == 0:
            continue
            
        improvement = (current_significance - prev_significance) / prev_significance if prev_significance > 0 else 1.0
        
        if improvement >= min_improvement:
            thresholds.append(sorted_rows.iloc[i]['bdt_score'])
            prev_significance = current_significance
        
    # Return up to 4 thresholds, descending order
    return sorted(thresholds, reverse=True)[:4]