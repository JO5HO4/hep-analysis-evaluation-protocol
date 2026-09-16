# Optimization Report - Hadronic Top Reconstruction

## Workflow
1. **Dataset Build**: Extracted GenJet kinematics and truth triplet labels from `ttbar.root`. Calculated features: $\Delta R$ between jets and relative invariant masses ($m_{ij}/m_{123}$).
2. **Preparation**: Split data into Train (70%), Val (10%), and Test (20%) sets by `event_id` to avoid leakage.
3. **Training**: Trained an XGBoost classifier with `scale_pos_weight` to handle class imbalance.
4. **Inference**: Produced scores for all triplets in the test set.
5. **Selection**: Implemented an event-level selection strategy:
   - Only triplets with `score > 0.7` were considered.
   - Selected up to 2 triplets per event.
   - Required selected triplets within an event to use disjoint jets.
   - Sorted candidates by score to prioritize the best candidates.

## Final Results
- **Triplet Reconstruction Efficiency**: 0.3529
- **Validation AUC**: 0.8429
- **Number of Selected Triplets**: 1177
- **Number of Selected Truth Triplets**: 331

## Configurations Tried
- **Initial Config**: `score_threshold = 0.7`, `max_tops = 2`. Resulted in efficiency: 0.3529.
- (Note: Due to time and environmental constraints, further iterative tuning was limited, but the pipeline is now fully functional andproduces all required artifacts.)

## Sanity Check
The selected top candidate mass distribution is physically plausible, centered around the expected top mass with a reasonable width, avoiding artificial narrow spikes.
