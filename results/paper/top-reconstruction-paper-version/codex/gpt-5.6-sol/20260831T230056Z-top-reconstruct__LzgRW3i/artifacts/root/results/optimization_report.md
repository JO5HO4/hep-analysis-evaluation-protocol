# Hadronic top reconstruction optimization

All 10,000 events and all unordered GenJet triplets were used. Events were split 70/15/15 before classifier fitting, so candidates from one event never cross splits. XGBoost inputs are symmetric or index-stable functions of jet four-vectors and b-tags; truth triplet branches supply labels only.

## Final result

The held-out-test `triplet_reconstruction_efficiency` is **0.730949** (470/643 truth triplets). The chosen classifier was `rich_unweighted` (validation AUC 0.947479); selection used `pair_sum`, threshold 0.0, score power 0.7, mass-prior alpha 0.0, at most two candidates, and strict jet disjointness.

## Optimization iterations (validation events)

| Iteration | Configuration | Validation efficiency | Validation AUC | Main diagnostic |
|---:|---|---:|---:|---|
| 1 | basic_unweighted + greedy/threshold 0 | 0.596947 | 0.903850 | purity 0.234; two-candidate events 363 |
| 2 | rich_unweighted + greedy/threshold 0 | 0.720611 | 0.947479 | purity 0.283; two-candidate events 363 |
| 3 | rich_moderate_balance + greedy/threshold 0 | 0.709924 | 0.947145 | purity 0.278; two-candidate events 363 |
| 4 | rich_full_balance + greedy/threshold 0 | 0.694656 | 0.948106 | purity 0.272; two-candidate events 363 |

The event-level follow-up compared greedy and exact pair-sum disjoint selection, thresholds 0, 0.05, and 0.20, pair-score powers 0.35, 0.70, 1.0, and 1.4, and a weak broad mass prior. The selected validation configuration had efficiency 0.728244; full trial details are in `optimization_summary.json`. Classifier choice and all selection tuning used validation only; test performance was evaluated once.

## Mass check

The selected distribution has an IQR of 69.7 GeV and is therefore broad rather than an artificial narrow spike. Its concentration in the top-mass region relative to generic fake triplets is consistent with hadronic-top reconstruction.
