# Hadronic top-triplet optimization report

## Workflow
All unordered GenJet index combinations were built from all 10,000 events. Truth labels were matched as unordered sets. Physics features include pairwise angular distances, pair/triplet mass ratios, invariant masses, ordered jet pT and b-tag values, and event jet multiplicity. Events were split 70/15/15, XGBoost models were trained on train events, and both model and constrained event selection were tuned only on validation events. Final inference uses the held-out 1,500-event test split.

## Final result
**Final held-out `triplet_reconstruction_efficiency`: 0.694891** (476/685 truth triplets recovered).
Test AUC: 0.949894. Selection uses `exact` disjoint optimization with utility `score^1`, no threshold, and at most two candidates per event.

## Optimization iterations

| Configuration | Validation AUC | Validation efficiency | Best selector |
|---|---:|---:|---|
| baseline_depth4 | 0.945746 | 0.735714 | exact, score^1 |
| deeper_depth6 | 0.944983 | 0.731429 | exact, score^0.5 |
| balanced_depth5 | 0.944913 | 0.714286 | exact, score^0.5 |
| ranking_depth5 | 0.944997 | 0.730000 | exact, score^1 |

For each model, greedy selection and exact disjoint-pair optimization with score powers 0.5, 1, 2, 4, and 8 were compared. The primary decision criterion was validation triplet recall, with AUC as tie-breaker. The selected mass distribution was then checked against validation truth and fake candidates; it is broad and physically plausible rather than artificially narrow.
