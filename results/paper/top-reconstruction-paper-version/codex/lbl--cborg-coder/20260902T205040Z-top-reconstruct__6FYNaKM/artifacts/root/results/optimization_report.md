# Hadronic Top-Quark Reconstruction Optimization Report

## Workflow
The hadronic top-quark reconstruction pipeline was built from scratch using the following steps:
1. **Dataset Construction**: Extracted all possible triplets of GenJets from the ROOT ntuple. Computed physically motivated features including $\Delta R$ between pairs and relative invariant masses.
2. **Model Training**: Used an XGBoost binary classifier to separate truth-matched top triplets from combinatorial background.
3. **Selection Strategy**: Implemented a greedy selection process that picks the highest-scoring triplets per event, ensuring that selected triplets are jet-disjoint and limited to a maximum of two per event.
4. **Optimization**: Iterated on the feature set and classifier configuration to improve the triplet reconstruction efficiency.

## Final Configuration
- **Features**: `dr_ab`, `dr_ac`, `dr_bc`, `mij_over_m123_ab`, `mij_over_m123_ac`, `mij_over_m123_bc`, `triplet_mass`, `triplet_pt`.
- **Model**: XGBoost Classifier with `n_estimators=100`, `max_depth=5`, and `scale_pos_weight` for class imbalance.
- **Selection**: Greedy selection of top 2 disjoint triplets by score.

## Results
- **Final Triplet Reconstruction Efficiency**: 0.6136

## Optimization History
| Iteration | Changes | Efficiency | AUC |
|-----------|----------|-------------|-----|
| 1 | Baseline features (dR, rel mass), greedy selection | 0.4577 | 0.8450 |
| 2 | Added `triplet_mass` to features, tuned XGBoost | 0.6136 | 0.9065 |

The addition of the triplet invariant mass and triplet $p_T$ significantly improved the classifier's ability to identify true top decays, leading to a substantial increase in the reconstruction efficiency.
