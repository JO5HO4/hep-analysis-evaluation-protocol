# Hadronic Top-Quark Reconstruction Pipeline Optimization Report

## Overview

This report documents the end-to-end hadronic top-quark reconstruction pipeline developed to identify truth-matched triplet candidates from combinatorial background. The pipeline consists of:

1. Data processing to extract all possible jet triplets from the ROOT ntuple
2. Feature engineering including ΔR values and mass ratios
3. Training an XGBoost binary classifier to distinguish truth-matched from background triplets
4. Implementing a selection strategy with jet-disjoint constraints

## Final Configuration

- **Classifier**: XGBoost with binary:logistic objective
- **Features**: dr_ab, dr_ac, dr_bc, mij_over_m123_ab, mij_over_m123_ac, mij_over_m123_bc
- **Training**: 60/20/20 split of available events, balanced sampling
- **Selection strategy**: Greedy selection by classifier score with jet-disjoint constraint
- **Constraints**: At most 2 top candidates per event, no shared jets between candidates

## Results

- **Final triplet reconstruction efficiency**: 0.6967 (69.67%)
- **Total truth triplets in test sample**: 900
- **Selected truth triplets**: 627
- **Total selected triplets**: 6,865
- **Validation AUC**: 0.7962

## Optimization Process

This implementation represents the first iteration of the pipeline. The following configuration choices were made:

1. **Feature selection**: Used ΔR values and mass ratios as these are known to be discriminating variables for top quark reconstruction
2. **Classifier choice**: XGBoost was selected as it typically performs well on structured data with good interpretability
3. **Selection strategy**: Implemented a greedy approach that selects the highest-scoring triplets first while respecting the jet-disjoint constraint

## Future Improvements

Potential improvements that could be explored in future iterations include:

1. **Feature engineering**: Adding additional kinematic variables such as jet pT ratios, angular separations, or topness variables
2. **Classifier optimization**: Hyperparameter tuning of the XGBoost model or trying alternative algorithms like neural networks
3. **Selection strategy**: Implementing more sophisticated selection algorithms that consider global event properties
4. **Data augmentation**: Using data from additional simulated events to improve classifier training

The current pipeline achieves reasonable performance with a reconstruction efficiency of 69.67%, which could be improved with further optimization.