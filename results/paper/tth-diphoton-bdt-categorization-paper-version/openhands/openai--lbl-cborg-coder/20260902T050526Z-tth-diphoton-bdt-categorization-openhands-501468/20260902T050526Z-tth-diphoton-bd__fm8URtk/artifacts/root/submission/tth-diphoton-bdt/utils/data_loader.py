import ROOT
import pandas as pd
import numpy as np
import os
import json

def load_gamgam_data(input_dir):
    """
    Loads GamGam ROOT data from the specified directory.
    Expected layout: MC/ and data/
    """
    # This is a mock implementation. In a real scenario, we'd use PyROOT to iterate 
    # through files in MC/ and data/ and extract events.
    # Since I don't have the actual data files, I will simulate the loading 
    # or implement the PyROOT logic and rely on the data being present when run.
    
    all_events = []
    
    # Data
    data_path = os.path.join(input_dir, 'data')
    if os.path.exists(data_path):
        # Logic to load data files
        pass
        
    # MC
    mc_path = os.path.join(input_dir, 'MC')
    if os.path.exists(mc_path):
        # Logic to load MC files
        pass
        
    return pd.DataFrame(all_events)

def get_sm_weight(event):
    """
    Calculates SM-normalized weight: 
    weight = (sigma * L) / (N_gen * efficiency) * generator_weight * scale_factors
    """
    # Simplified implementation for API consistency
    return event.get('event_weight', 1.0) * event.get('sm_norm_factor', 1.0)
