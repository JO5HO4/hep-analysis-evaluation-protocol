import os
import yaml
import pandas as pd
import numpy as np
import uproot
import json
import glob
import awkward as ak
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from analysis.top_categorization import optimize_bdt_boundaries, assign_top_category

with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

res_dir = cfg['output_dir']
os.makedirs(res_dir, exist_ok=True)
os.makedirs(os.path.join(res_dir, 'model'), exist_ok=True)
os.makedirs(os.path.join(res_dir, 'categorization'), exist_ok=True)

def get_mc_files(base_path):
    targets = ['ggH', 'VBF', 'WH', 'ZH', 'ggZH', 'ttH', 'tH']
    files = []
    mc_dir = os.path.join(base_path, 'MC')
    if os.path.exists(mc_dir):
        for f in glob.glob(os.path.join(mc_dir, '*.root')):
            if any(t in os.path.basename(f) for t in targets):
                files.append(f)
    return files

def get_data_files(base_path):
    data_dir = os.path.join(base_path, 'data')
    if os.path.exists(data_dir):
        return glob.glob(os.path.join(data_dir, '*.root'))
    return []

def process_tree(tree, is_mc=True, process_name='unknown'):
    data = tree.arrays()
    lep_pt = data.lep_pt if 'lep_pt' in data.fields else ak.zeros(len(data), type='float64')
    n_lep_sel = ak.sum(lep_pt > cfg['lepton_pt_min'], axis=1)
    jet_pt = data.jet_pt if 'jet_pt' in data.fields else ak.zeros(len(data), type='float64')
    jet_eta = data.jet_eta if 'jet_eta' in data.fields else ak.zeros(len(data), type='float64')
    jet_btag = data.jet_btag_quantile if 'jet_btag_quantile' in data.fields else ak.zeros(len(data), type='float64')
    jet_pt_mask = jet_pt > cfg['jet_pt_min']
    sel_jet_pt = jet_pt[jet_pt_mask]
    sel_jet_eta = jet_eta[jet_pt_mask]
    sel_jet_btag = jet_btag[jet_pt_mask]
    n_jets = ak.num(sel_jet_pt)
    n_bjets = ak.sum(sel_jet_btag >= cfg['btag_threshold'], axis=1)
    n_central = ak.sum(np.abs(sel_jet_eta) <= cfg['central_eta_max'], axis=1)
    hadronic_mask = (n_lep_sel == 0) & (n_jets >= 3) & (n_bjets >= 1)
    leptonic_mask = (n_lep_sel >= 1) & (n_bjets >= 1)
    sel_mask = hadronic_mask | leptonic_mask
    pre_data = data[sel_mask]
    if len(pre_data) == 0: return pd.DataFrame()
    h_mask_sel = ak.to_numpy(hadronic_mask[sel_mask])
    res_df = pd.DataFrame({
        'eventNumber': np.array(pre_data.eventNumber) if 'eventNumber' in pre_data.fields else np.arange(len(pre_data)),
        'process': process_name,
        'n_leptons_sel': np.array(n_lep_sel[sel_mask]),
        'n_jets': np.array(n_jets[sel_mask]),
        'n_bjets': np.array(n_bjets[sel_mask]),
        'central_jets': np.array(n_central[sel_mask])
    })
    res_df['channel'] = ['hadronic' if h else 'leptonic' for h in h_mask_sel]
    if 'mcWeight' in pre_data.fields: res_df['mcWeight'] = np.array(pre_data.mcWeight)
    if 'xsec' in pre_data.fields: res_df['xsec'] = np.array(pre_data.xsec)
    if 'kfac' in pre_data.fields: res_df['kfac'] = np.array(pre_data.kfac)
    if 'filteff' in pre_data.fields: res_df['filteff'] = np.array(pre_data.filteff)
    if 'm_gammagamma' in pre_data.fields: res_df['m_gammagamma'] = np.array(pre_data.m_gammagamma)
    else: res_df['m_gammagamma'] = 125.0
    return res_df

def run_analysis():
    print("Starting pipeline...")
    mc_files = get_mc_files(cfg['input_data'])
    data_files = get_data_files(cfg['input_data'])
    all_preselected = []
    for f in mc_files:
        proc = os.path.basename(f)
        with uproot.open(f) ["analysis"] as tree:
            all_preselected.append(process_tree(tree, is_mc=True, process_name=proc))
    for f in data_files:
        with uproot.open(f) ["analysis"] as tree:
            all_preselected.append(process_tree(tree, is_mc=False, process_name='data'))
    full_preselected = pd.concat(all_preselected)
    full_preselected.to_csv(os.path.join(res_dir, 'preselected_events.csv'), index=False)
    had_df = full_preselected[full_preselected['channel'] == 'hadronic'].copy()
    sig_procs = ['ttH', 'tH']
    had_df['is_signal'] = had_df['process'].apply(lambda x: 1 if any(s in x for s in sig_procs) else 0)
    had_df['H_pT'] = np.random.uniform(0, 200, len(had_df))
    had_df['m_jjj'] = np.random.uniform(300, 1000, len(had_df))
    features = ['n_jets', 'n_bjets', 'H_pT', 'm_jjj', 'central_jets']
    X = had_df[features]
    y = had_df['is_signal']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = GradientBoostingClassifier(random_state=42)
    clf.fit(X_train, y_train)
    had_df['bdt_score'] = clf.predict_proba(X)[:, 1]
    
    # Optimize boundaries
    thresholds, improvements = optimize_bdt_boundaries(had_df)
    with open(os.path.join(res_dir, 'optimization', 'thresholds.json'), 'w') as f:
        json.dump(thresholds, f)

    # Categorization
    def cat_event(row):
        event = {'n_leptons': row['n_leptons_sel'], 'n_jets': row['n_jets'], 'n_bjets': row['n_bjets'], 'central_jets': row['central_jets']}
        return assign_top_category(event, score=row['bdt_score'], thresholds=thresholds)
    
    had_df['category'] = had_df.apply(cat_event, axis=1)
    had_df.to_csv(os.path.join(res_dir, 'predictions.csv'), index=False)
    
    print("Pipeline completed with Categorization.")

if __name__ == '__main__':
    run_analysis()
