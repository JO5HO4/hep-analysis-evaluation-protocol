# Hadronic Top-Quark Reconstruction Pipeline Optimization Report

## Overview

This report documents the development of an end-to-end hadronic top-quark reconstruction pipeline using machine learning to identify true top-quark decay triplets from combinatorial background. The pipeline consists of four main stages:

1. **Dataset Building**: Extracting jet information from the ROOT file and generating all possible triplets of jets per event
2. **Training**: Training an XGBoost binary classifier to distinguish truth-matched top triplets from combinatorial background
3. **Inference**: Applying the trained model to score triplets in the test dataset
4. **Selection**: Selecting final top-quark candidates with event-level constraints (at most two per event, no shared jets)

## Final Configuration and Results

The final configuration achieved a **triplet reconstruction efficiency of 46.38%**, which means that 435 out of 938 truth-matched triplets in the test sample were successfully recovered by our selection algorithm.

Key aspects of the final configuration:

- **Feature Set**: Six physics-motivated features derived from jet kinematics:
  - Pairwise delta R values (dr_ab, dr_ac, dr_bc)
  - Ratios of pairwise invariant masses to total triplet mass (mij_over_m123_ab, mij_over_m123_ac, mij_over_m123_bc)
- **Classifier**: XGBoost with the following hyperparameters:
  - max_depth: 6
  - learning_rate: 0.1
  - subsample: 0.8
  - colsample_bytree: 0.8
  - early_stopping_rounds: 50
- **Selection Strategy**: Greedy selection by classifier score with jet-disjoint constraint within each event (maximum of two candidates per event)
- **Data Split**: 60% train, 20% validation, 20% test (by event)

## Optimization Iterations

This implementation represents our first complete iteration of the pipeline. We started with a basic configuration and focused on getting a working end-to-end system. The current efficiency of 46.38% provides a solid baseline for future optimization.

## Next Steps for Improvement

Several avenues could be explored to improve the reconstruction efficiency:

1. **Feature Engineering**: Adding additional physics-motivated features such as:
   - Triplet invariant mass
   - Jet pT fractions within the triplet
   - Angular correlations beyond delta R
   - Event-wide jet multiplicity and kinematic properties

2. **Classifier Optimization**: 
   - Hyperparameter tuning of the XGBoost model
   - Trying alternative algorithms (e.g., neural networks, random forests)
   - Addressing class imbalance (truth triplets are ~4.2% of all triplets)

3. **Selection Strategy**: 
   - Exploring alternative selection algorithms beyond greedy scoring
   - Optimizing the maximum number of candidates per event
   - Implementing score thresholds or other filtering criteria

4. **Data Usage**: 
   - Using more events for training to improve classifier generalization
   - Exploring different train/validation/test splits
   - Implementing data augmentation techniques

## Conclusion

We have successfully implemented a complete hadronic top-quark reconstruction pipeline that achieves a reconstruction efficiency of 46.38%. The selected candidates have a mean invariant mass of 204.4 GeV, which is physically plausible for top-quark candidates (expected mass ~172.5 GeV). The mass distribution is not an artificially narrow spike, indicating that our selection is not overfitting to a specific mass value.

This baseline implementation provides a solid foundation for further optimization. Future work should focus on feature engineering and classifier optimization to improve the reconstruction efficiency while maintaining physical plausibility of the selected candidates.