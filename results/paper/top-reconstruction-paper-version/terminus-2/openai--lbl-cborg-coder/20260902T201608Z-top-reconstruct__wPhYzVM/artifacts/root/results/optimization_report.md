# Hadronic Top Reconstruction Optimization Report

## Workflow
1. **Dataset Build**: Extracted all GenJet triplets from `/root/data/ttbar.root` and calculated features: $\Delta R$ pairs and relative mass ratios $m_{ij}/m_{123}$.
2. **Data Splitting**: Split by event ID into Train (60%), Val (20%), and Test (20%) to avoid leakage.
3. **Classifier**: Trained an XGBoost classifier with `scale_pos_weight` to handle class imbalance. The model achieved a validation AUC of ~0.84.
4. **Selection Strategy**: Implemented a greedy selection per event. Triplets were sorted by classifier score, and the top 2 were selected provided they were jet-disjoint.

## Results
- **Final Triplet Reconstruction Efficiency**: 0.4542
- **Test AUC**: 0.8439
- **Constraints**: All events contain $\le 2$ candidates with mutually exclusive jet indices.

## Configurations Tried
- **Iteration 1 (Baseline)**: XGBoost with default parameters and greedy selection. Efficiency: 0.4542. This provided a strong starting point with a physically plausible mass distribution.

## Sanity Check
The reconstructed mass distribution shows a clear peak centered around the top quark mass, separating the selected candidates from the broad combinatorial background.
