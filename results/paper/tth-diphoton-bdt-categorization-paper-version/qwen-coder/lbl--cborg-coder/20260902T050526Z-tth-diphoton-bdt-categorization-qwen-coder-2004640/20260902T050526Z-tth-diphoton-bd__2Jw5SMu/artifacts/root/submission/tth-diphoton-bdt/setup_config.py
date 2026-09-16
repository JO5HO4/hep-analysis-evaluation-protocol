import yaml
import os

config = {
    "input": {
        "env_var": "TB_HYY_INPUTS",
        "layout": {
            "mc": "MC/",
            "data": "data/"
        }
    },
    "selection": {
        "photon": {
            "pt_min": [20, 15], # Example values, will be refined
        },
        "lepton": {
            "pt_min": 10,
        },
        "jet": {
            "pt_min": 25,
            "central_eta": 2.5,
            "btag_quantile_min": 4,
        },
        "hadronic_channel": {
            "n_leptons": 0,
            "n_jets_min": 3,
            "n_btags_min": 1,
        }
    },
    "bdt": {
        "features": ["n_jets", "n_btags", "ht", "pt_gammagamma", "m_jjj"],
        "signal_processes": ["ttH", "tH"],
        "background_processes": ["ggH", "NTI"],
        "mass_window": [123, 127],
        "sidebands": {
            "low": [105, 120],
            "high": [130, 160]
        }
    },
    "normalization": {
        "lumi": 36.0, # fb^-1
    }
}

with open('/root/submission/tth-diphoton-bdt/config_resolved.yaml', 'w') as f:
    yaml.dump(config, f)
