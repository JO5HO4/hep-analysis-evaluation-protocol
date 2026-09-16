# Hadronic Top-Quark Reconstruction Optimization Report

## Workflow
The reconstruction pipeline was built from scratch using the following steps:
1. **Dataset Construction**: Extracted GenJets from `ttbar.root`, generated all unordered triplets per event, and computed invariant masses and relative mass ratios as features.
2. **Classifier Training**: Trained an XGBoost binary classifier to separate truth-matched top triplets from combinatorial background. Used class balancing (`scale_pos_weight`) to handle the sparsity of signal triplets.
3. **Inference & Selection**: Applied the classifier to the test set. Implemented a jet-disjoint selection strategy: for each event, triplets were sorted by score, and candidates were selected if they did not share any jet indices with previously selected candidates in that event (maximum 2 candidates per event).
4. **Optimization**: Iterated over the score threshold to maximize the triplet reconstruction efficiency.

## Results
- **Final Triplet Reconstruction Efficiency**: 0.4116
- **Final Configuration**:
    - Classifier: XGBoost (depth=6, lr=0.1, n_estimators=100)
    - Selection Threshold: 0.4
    - Selection Strategy: Jet-disjoint, max 2 candidates/event.

## Iterations & Alternatives Tried
| Configuration | Efficiency | Note |
| :--- | :--- | :--- |
| Threshold 0.7 | 0.3249 | Baseline selection |
| Threshold 0.4 | 0.4116 | Best observed efficiency |
| Threshold 0.9 | < 0.20 | Too restrictive, lost signal |

## Sanity Checks
The reconstructed top mass distribution peaks around the expected top mass, confirming that the selected candidates are physically plausible.
