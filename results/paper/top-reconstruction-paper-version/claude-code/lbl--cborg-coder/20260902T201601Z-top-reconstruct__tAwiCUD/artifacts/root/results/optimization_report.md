# Hadronic Top Reconstruction Optimization Report

## Final Configuration
- **Classifier**: XGBoost binary classifier.
- **Features**: Per-triplet symmetric features:
    - DeltaR (min, mid, max)
    - Mass ratios (min, mid, max)
    - Triplet mass (m123)
    - Triplet pT (pt123)
    - Jet pT (min, mid, max)
    - Sum of jet pT
- **Training**:
    - Scale positive weight for class imbalance.
    - max_depth=6, learning_rate=0.05, n_estimators=200.
- **Selection Strategy**: Greedy disjoint selection of top 2 candidates per event based on classifier score.

## Performance
- **Final Triplet Reconstruction Efficiency**: 0.6333
- **Validation AUC**: 0.9067
- **Test AUC**: 0.9091

## Iteration History
1. **Baseline**: Used basic DeltaR and mass ratios. Efficiency: ~0.4488.
2. **Improved Features**: Added triplet mass, triplet pT, and individual jet pT. Efficiency: ~0.6237.
3. **Symmetric Features**: Used sorted (min/mid/max) values of DeltaR, mass ratios, and jet pT to provide permutation invariance. Efficiency: 0.6333.

## Conclusion
The use of symmetric features and inclusive kinematics (triplet mass and pT) significantly improved the recall of truth-matched triplets. The final pipeline achieves a reconstruction efficiency of 0.6333 while maintaining a physically plausible mass distribution.
