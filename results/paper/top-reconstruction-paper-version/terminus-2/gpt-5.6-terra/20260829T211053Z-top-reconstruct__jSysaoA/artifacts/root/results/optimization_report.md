# Hadronic top triplet reconstruction optimization

## Workflow

All unordered GenJet index triplets were built from the complete 10,000-event ntuple. Truth labels were matched as unordered jet-index sets. Events were split exclusively by `event_id mod 5`: 60% training, 20% validation, and 20% held-out inference. The XGBoost classifier used angular separations, pair-mass ratios, triplet/pair masses, ordered jet pT, and generator b-tag observables.

## Final result

Final held-out **triplet_reconstruction_efficiency: 0.702368** (623/887 truth triplets recovered).

The retained configuration is the depth-5 XGBoost baseline and `pairmax` selection: exhaustively choose the highest summed-score singleton or pair of mutually jet-disjoint triplets, with at most two candidates per event and no score threshold. No threshold was used because triplet-level recall is the specified primary target. The held-out collection has 2194 selected candidates in 1726 events; all jet-overlap and multiplicity constraints were explicitly checked.

## Optimization iterations

### Event selection strategies (validation)

| Configuration | Triplet reconstruction efficiency | Truth selected |
|---|---:|---:|
| one | 0.621964 | 589 |
| greedy | 0.709609 | 672 |
| pairmax | 0.713833 | 676 |

### Classifier variants with pairmax selection (validation)

| Configuration | Best iteration | Validation AUC | Triplet reconstruction efficiency |
|---|---:|---:|---:|
| baseline (depth 5, eta 0.07) | 127 | 0.935469 | 0.713833 |
| shallow (depth 4, eta 0.07) | 200 | 0.935489 | 0.706441 |
| deep_slow (depth 6, eta 0.045) | 144 | 0.935317 | 0.707497 |

The baseline was retained: although the shallow model had essentially tied candidate AUC, its event-level disjoint-selection recall was lower. Training detail is in `train/training_report_xgb.json`, variant data in `train/model_variant_comparison.json`, and held-out inference details in `infer/inference_report_xgb.json`.

## Mass sanity check

`select_triplets/plots/triplet_mass_comparison.png` compares selected held-out masses against validation truth and combinatorial candidates. The selected mass distribution has median 173.1 GeV and broad 5--95% range 131.8--412.4 GeV; no artificially narrow mass-window cut was applied. Numerical comparison and interpretation are in `sanity_checks/mass_sanity_report.json` and `sanity_checks/mass_sanity_note.md`.
