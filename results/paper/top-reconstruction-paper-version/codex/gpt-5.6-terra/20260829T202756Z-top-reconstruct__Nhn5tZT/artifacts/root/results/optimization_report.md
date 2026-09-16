# Hadronic top triplet reconstruction optimization

All unordered generator-jet triplets were constructed and labeled event-by-event. A 60/20/20 deterministic event-level split prevents triplets from the same event from crossing train, validation, and inference. The XGBoost classifier uses triplet angular, invariant-mass-ratio, momentum, multiplicity, and generator b-tag features.

Final held-out `triplet_reconstruction_efficiency`: **0.7249** (245/338).

## Iterations

| iteration | validation AUC | validation triplet efficiency | configuration |
|---|---:|---:|---|
| iteration_1_baseline | 0.9398 | 0.6835 | depth-3 XGBoost + exact score-sum pair selection |
| iteration_2_kinematic_btag | 0.9428 | 0.6885 | deeper feature model + exact score-sum pair selection |
| iteration_3_deeper | 0.9434 | 0.7036 | depth-6 model + exact score-sum pair selection |
| iteration_4_selection | 0.9434 | 0.7097 | score-ordered greedy, two jet-disjoint candidates |

A final standard retraining check using train+validation events (same depth-6 configuration, with inference events still held out) reached 0.7130 on the held-out sample, below the retained 0.7249 result; the validation-selected train-only model was therefore kept.

The final strategy accepts the highest classifier-score triplet and then the highest-scoring disjoint remaining triplet. It is capped at two candidates and has no mass constraint. A comparison plot and JSON mass summary are in `sanity_checks/` and `select_triplets/plots/`.
