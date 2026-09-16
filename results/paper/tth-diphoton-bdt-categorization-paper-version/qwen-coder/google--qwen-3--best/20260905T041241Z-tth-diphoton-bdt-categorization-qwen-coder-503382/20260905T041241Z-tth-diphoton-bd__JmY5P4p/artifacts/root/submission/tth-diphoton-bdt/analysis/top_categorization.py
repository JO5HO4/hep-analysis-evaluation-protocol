import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import json
import yaml
import os

# Required constants
CATEGORY_ORDER = [
    'ttH_had_BDT1',
    'ttH_had_BDT2',
    'ttH_had_BDT3',
    'ttH_had_BDT4',
    'tH_had_4j1b',
    'tH_had_4j2b',
    'unassigned'
]

BDT_FEATURES = [
    'jet_pt_max',
    'jet_eta_max',
    'bjet_multiplicity',
    'diphoton_pt_jet_feature',
    'centrality_measure'
]

def build_jet_features(jets: pd.DataFrame, photons: pd.DataFrame) -> Dict[str, float]:
    """
    Build jet features for BDT training.
    
    Args:
        jets: DataFrame with jet properties (pt, eta, phi, btag_quantile)
        photons: DataFrame with photon properties (pt, eta, phi)
    
    Returns:
        Dictionary of jet features
    """
    if len(jets) == 0:
        return {
            'jet_pt_max': 0.0,
            'jet_eta_max': 0.0,
            'bjet_multiplicity': 0,
            'diphoton_pt': photons.iloc[0].pt if len(photons) > 0 else 0.0,
            'centrality_measure': 0.0
        }
    
    # Central jets (|eta| <= 2.5)
    central_jets = jets[abs(jets.eta) <= 2.5]
    forward_jets = jets[abs(jets.eta) > 2.5]
    
    # b-tagged jets (using quantile >= 4 as documented b-tag definition)
    bjets = jets[jets.btag_quantile >= 4]
    
    # Maximum jet pT
    jet_pt_max = float(jets.pt.max()) if len(jets) > 0 else 0.0
    
    # Maximum |eta| of jets
    jet_eta_max = float(jets.eta.abs().max()) if len(jets) > 0 else 0.0
    
    # b-jet multiplicity
    bjet_multiplicity = len(bjets)
    
    # Diphoton pT
    if len(photons) >= 2:
        diphoton_pt = invariant_mass(photons.iloc[0], photons.iloc[1])
    else:
        diphoton_pt = 0.0
    
    # Centrality measure: sum of central jet pT divided by sum of all jet pT
    total_jet_pt = jets.pt.sum() if len(jets) > 0 else 1.0  # Avoid division by zero
    centrality_measure = central_jets.pt.sum() / total_jet_pt
    
    # Return only jet-related features with appropriate names
    result = {
        'jet_pt_max': jet_pt_max,
        'jet_eta_max': jet_eta_max,
        'bjet_multiplicity': bjet_multiplicity,
        'diphoton_pt_jet_feature': float(diphoton_pt),
        'centrality_measure': centrality_measure
    }
    print(f"build_jet_features result: {result}")
    return result

def invariant_mass(obj1, obj2) -> float:
    """
    Calculate invariant mass of two objects.
    
    Args:
        obj1, obj2: Objects with pt, eta, phi, and optionally mass attributes
    
    Returns:
        Invariant mass
    """
    import math
    
    # Use default mass of 0 for photons
    m1 = getattr(obj1, 'mass', 0.0)
    m2 = getattr(obj2, 'mass', 0.0)
    
    pt1, eta1, phi1 = obj1.pt, obj1.eta, obj1.phi
    pt2, eta2, phi2 = obj2.pt, obj2.eta, obj2.phi
    
    # Calculate delta phi
    dphi = abs(phi1 - phi2)
    if dphi > math.pi:
        dphi = 2 * math.pi - dphi
    
    # Calculate invariant mass
    m_squared = m1*m1 + m2*m2 + 2*(math.cosh(eta1-eta2)*pt1*pt2 - math.cos(dphi)*pt1*pt2)
    return math.sqrt(max(m_squared, 0.0))

def assign_top_category(
    event: Dict,
    score: Optional[float] = None,
    thresholds: Optional[List[float]] = None
) -> str:
    """
    Assign top category based on BDT score and thresholds.
    
    Args:
        event: Event dictionary with jet and lepton information
        score: BDT score (if already computed)
        thresholds: List of BDT thresholds for category boundaries
    
    Returns:
        Category name
    """
    # Default thresholds if not provided
    if thresholds is None:
        thresholds = [0.3, 0.5, 0.7, 0.9]
    
    # Check hadronic channel: zero leptons, at least 3 jets, at least 1 b-jet
    n_leptons = event.get('n_leptons', 0)
    n_jets = event.get('n_jets', 0)
    n_bjets = event.get('n_bjets', 0)
    
    is_hadronic = (n_leptons == 0) and (n_jets >= 3) and (n_bjets >= 1)
    
    if not is_hadronic:
        return 'unassigned'
    
    # For hadronic events, apply BDT categories first
    if score is not None:
        for i, threshold in enumerate(thresholds):
            if score >= threshold:
                return f'ttH_had_BDT{i+1}'
    
    # If BDT score not available or below all thresholds, check cut-based tH categories
    # Require exactly 4 central jets
    n_central_jets = event.get('n_central_jets', 0)
    if n_central_jets == 4:
        if n_bjets == 1:
            return 'tH_had_4j1b'
        elif n_bjets >= 2:
            return 'tH_had_4j2b'
    
    return 'unassigned'

def stable_partition(event_id: str, seed: int = 42, fractions: Dict[str, float] = None) -> str:
    """
    Partition events by stable event identifier.
    
    Args:
        event_id: Stable event identifier
        seed: Random seed for reproducibility
        fractions: Dictionary of partition fractions (e.g., {'train': 0.6, 'valid': 0.2, 'test': 0.2})
    
    Returns:
        Partition name (train, valid, test)
    """
    if fractions is None:
        fractions = {'train': 0.6, 'valid': 0.2, 'test': 0.2}
    
    # Create a deterministic hash from the event_id and seed
    hash_input = f"{event_id}_{seed}"
    hash_value = abs(hash(hash_input)) % 1000000  # Get a large integer
    
    # Normalize fractions to ensure they sum to 1.0
    total = sum(fractions.values())
    normalized_fractions = {k: v/total for k, v in fractions.items()}
    
    # Determine partition based on hash value
    cumulative = 0.0
    rand_val = (hash_value % 1000000) / 1000000.0  # Normalize to [0,1)
    
    for partition, fraction in normalized_fractions.items():
        cumulative += fraction
        if rand_val < cumulative:
            return partition
    
    return 'test'  # Default to test if something goes wrong

def optimize_bdt_boundaries(rows: pd.DataFrame, config: Optional[Dict] = None) -> List[float]:
    """
    Optimize BDT category boundaries iteratively.
    
    Args:
        rows: DataFrame with BDT scores and event information
        config: Configuration dictionary with optimization parameters
    
    Returns:
        List of optimized BDT thresholds
    """
    if config is None:
        config = {
            'min_improvement': 0.05,  # 5% relative improvement threshold
            'max_boundaries': 10,      # Maximum number of boundaries
            'initial_thresholds': [0.5]  # Starting point for optimization
        }
    
    # Extract BDT scores and labels
    scores = rows['bdt_score'].values
    labels = rows['label'].values  # 1 for signal, 0 for background
    weights = rows['weight'].values
    
    # Sort by score for efficient boundary finding
    sorted_indices = np.argsort(scores)
    sorted_scores = scores[sorted_indices]
    sorted_labels = labels[sorted_indices]
    sorted_weights = weights[sorted_indices]
    
    # Initialize with no boundaries
    thresholds = []
    best_significance = 0.0
    
    # Track the improvement history
    improvements = []
    
    # Iteratively add boundaries while improvement is significant
    for boundary_idx in range(config['max_boundaries']):
        best_new_threshold = None
        best_new_significance = best_significance
        
        # Try different threshold positions
        for i in range(1, len(sorted_scores) - 1):
            # Skip if this score is the same as the previous one
            if sorted_scores[i] == sorted_scores[i-1]:
                continue
            
            # Calculate significance with this new threshold
            threshold = sorted_scores[i]
            # Skip if this threshold is too close to existing ones
            if any(abs(threshold - t) < 1e-6 for t in thresholds):
                continue
            
            # Create categories with this threshold
            # We'll have n+1 categories with n thresholds
            n_categories = len(thresholds) + 2
            category_masks = []
            
            # First category: score < first threshold
            if len(thresholds) == 0:
                mask = sorted_scores < threshold
            else:
                mask = sorted_scores < thresholds[0]
            category_masks.append(mask)
            
            # Middle categories: threshold[i] <= score < threshold[i+1]
            for j in range(len(thresholds) - 1):
                mask = (sorted_scores >= thresholds[j]) & (sorted_scores < thresholds[j+1])
                category_masks.append(mask)
            
            # Last category: score >= last threshold
            if len(thresholds) == 0:
                mask = sorted_scores >= threshold
            else:
                mask = sorted_scores >= thresholds[-1]
            category_masks.append(mask)
            
            # If we're adding a new threshold, insert it appropriately
            if len(thresholds) > 0:
                # Find where to insert the new threshold
                insert_idx = 0
                for j, t in enumerate(thresholds):
                    if threshold < t:
                        break
                    insert_idx = j + 1
                
                # Recalculate category masks with the new threshold
                category_masks = []
                prev_threshold = -np.inf
                
                for j, t in enumerate(thresholds):
                    if j == insert_idx:
                        # Insert our new threshold here
                        mask = (sorted_scores >= prev_threshold) & (sorted_scores < threshold)
                        category_masks.append(mask)
                        prev_threshold = threshold
                    
                    mask = (sorted_scores >= prev_threshold) & (sorted_scores < t)
                    category_masks.append(mask)
                    prev_threshold = t
                
                # Last category
                mask = sorted_scores >= prev_threshold
                category_masks.append(mask)
            
            # Calculate signal and background in each category
            sig_counts = []
            bkg_counts = []
            
            for mask in category_masks:
                sig_weight = np.sum(sorted_weights[mask & (sorted_labels == 1)])
                bkg_weight = np.sum(sorted_weights[mask & (sorted_labels == 0)])
                sig_counts.append(sig_weight)
                bkg_counts.append(bkg_weight)
            
            # Calculate expected significance (approximate)
            significance = 0.0
            for s, b in zip(sig_counts, bkg_counts):
                if b > 0:
                    # Use simple S/sqrt(B) approximation
                    significance += s / np.sqrt(b) if s > 0 else 0.0
                elif s > 0:
                    # If no background, use large significance
                    significance += s * 1000.0
            
            if significance > best_new_significance:
                best_new_significance = significance
                best_new_threshold = threshold
        
        # Check for improvement
        if best_new_threshold is not None:
            improvement = (best_new_significance - best_significance) / max(best_significance, 1e-10)
            improvements.append({
                'boundary': boundary_idx + 1,
                'threshold': float(best_new_threshold),
                'significance': float(best_new_significance),
                'improvement': float(improvement)
            })
            
            if improvement >= config['min_improvement']:
                # Add the new threshold and maintain sorted order
                if len(thresholds) == 0:
                    thresholds = [best_new_threshold]
                else:
                    # Insert in sorted order
                    insert_idx = 0
                    for i, t in enumerate(thresholds):
                        if best_new_threshold < t:
                            break
                        insert_idx = i + 1
                    thresholds.insert(insert_idx, best_new_threshold)
                
                best_significance = best_new_significance
            else:
                # Improvement is less than threshold, stop adding boundaries
                break
        else:
            # No valid threshold found, stop
            break
    
    # Save the improvement history
    if 'improvement_output' in config:
        with open(config['improvement_output'], 'w') as f:
            json.dump(improvements, f, indent=2)
    
    return thresholds
