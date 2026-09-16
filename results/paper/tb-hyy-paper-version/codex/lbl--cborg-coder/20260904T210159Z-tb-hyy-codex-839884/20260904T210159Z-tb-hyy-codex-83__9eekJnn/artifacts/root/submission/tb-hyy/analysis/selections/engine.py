import awkward as ak
import numpy as np

CATEGORY_ORDER = ["inclusive"]

def apply_selection(events):
    """
    Applies the H -> gamma gamma selection criteria.
    Expects events as an awkward array with photon properties.
    """
    # Basic photon properties (Assuming typical naming)
    # pt: photon pT
    # eta: photon eta
    # tight_id: tight identification flag
    # tight_iso: tight isolation flag
    
    # 1. Photon Selection: at least two photons
    n_photons = ak.num(events.photon_pt)
    mask = (n_photons >= 2)
    
    # 2. pT > 25 GeV
    # We check all photons in the event. 
    # However, the contract usually means the two leading photons must pass.
    # Let's filter photons first.
    
    # Note: In a real analysis, we'd sort by pT.
    # Here we assume they are already sorted or we sort them.
    
    # Define a helper to check photon criteria
    def check_photon(pt, eta, tight_id, tight_iso):
        return (pt > 25) &                (np.abs(eta) < 2.37) &                ~((np.abs(eta) > 1.37) & (np.abs(eta) < 1.52)) &                (tight_id == 1) &                (tight_iso == 1)

    # Apply photon-level cuts
    photon_mask = check_photon(events.photon_pt, events.photon_eta, 
                               events.photon_tight_id, events.photon_tight_iso)
    
    # Keep only photons that pass
    filtered_pt = events.photon_pt[photon_mask]
    filtered_eta = events.photon_eta[photon_mask]
    
    # Require at least 2 photons pass the basic cuts
    mask = mask & (ak.num(filtered_pt) >= 2)
    
    # 3. Leading/Subleading pT/m_gg thresholds
    # m_gg is the diphoton mass
    m_gg = events.m_gg
    
    # We need the pt of the 1st and 2nd photon among those that passed
    # Since we can't easily index into filtered_pt for all events in one go with simple masks,
    # we use ak.first and ak.sorted.
    
    # Sorting is important
    sorted_pt = ak.sort(filtered_pt, ascending=False)
    
    # Ensure we have at least 2 photons after filtering before accessing
    mask = mask & (ak.num(sorted_pt) >= 2)
    
    # Leading pT / m_gg > 0.35
    # Subleading pT / m_gg > 0.25
    pt1 = sorted_pt[ak.slice(0, 1)][:, 0]
    pt2 = sorted_pt[ak.slice(1, 2)][:, 0]
    
    mask = mask & (pt1 / m_gg > 0.35) & (pt2 / m_gg > 0.25)
    
    return mask

def assign_category(events, selection_mask):
    """
    Assigns events to the inclusive category.
    """
    categories = {cat: np.zeros(len(events), dtype=bool) for cat in CATEGORY_ORDER}
    categories["inclusive"] = selection_mask
    return categories
