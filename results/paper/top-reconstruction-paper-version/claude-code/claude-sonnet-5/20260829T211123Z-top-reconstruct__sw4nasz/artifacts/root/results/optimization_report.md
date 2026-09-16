# ttbar Hadronic Top Reconstruction — Optimization Report

## Pipeline overview

1. **Dataset build** (`scripts/01_dataset_build.py`): read `/root/data/ttbar.root`,
   form all jet triplets per event, compute kinematic/topological features
   (pairwise mass ratios, dR's, b-tag info, triplet mass/pt/eta/phi, etc.),
   and label each triplet `is_truth` by matching to the true hadronic top's
   jet indices. Output: `dataset_build/triplets_raw.parquet` (105,784 triplets
   across 8,665 events; 4,25% signal rate).
2. **Event-level split** (`scripts/02_split.py`): manual numpy-RNG event-level
   train/val/test split (no sklearn available), 70/15/15 by event count
   (6,065 / 1,299 / 1,301 events), preserving all triplets from an event in a
   single split to avoid leakage.
3. **Training** (`scripts/03_train.py`): gradient-boosted binary classifier
   (XGBoost) on triplet features, with `is_truth` as target.
4. **Inference** (`scripts/04_infer.py`): score every triplet in a split.
5. **Selection** (`scripts/05_select.py`, finalized in `scripts/06_finalize_selection.py`):
   pick at most 2 jet-disjoint triplets per event, maximizing the primary
   metric `triplet_reconstruction_efficiency`.
6. **Sanity checks** (`scripts/07_sanity_checks.py`) and **selection plots**
   (`scripts/08_selection_plots.py`).

## Primary metric

`triplet_reconstruction_efficiency = (# truth triplets selected) / (# truth triplets in the inference sample)`,
evaluated on the held-out **test** split (never used for training or for any
tuning decision).

**Final result: `triplet_reconstruction_efficiency = 0.7649`** (527 / 689
truth triplets recovered on the test split; see `select_triplets/selection_report.json`).

## Iteration 1 — classifier hyperparameters (val split, AUC)

Manual rank-sum AUC (no sklearn) computed on the validation split for several
XGBoost configs, holding features and split fixed:

| config                          | max_depth | scale_pos_weight | val AUC |
|----------------------------------|-----------|-------------------|---------|
| default                          | 6         | auto (22.76)      | 0.9577  |
| depth7                           | 7         | auto (22.76)      | 0.9586  |
| depth3                           | 3         | auto (22.76)      | 0.9553  |
| spw=1 (no reweighting)           | 5         | 1.0               | 0.9586  |
| **spw=11 (chosen)**              | 5         | 11.0              | **0.9588** |

Class imbalance (~4.25% positive) was handled via `scale_pos_weight` rather
than downsampling, since downsampling would discard information without a
clear benefit for a boosted-tree model. `scale_pos_weight=11` (half of the
"auto" ratio 22.76) gave a small but consistent AUC improvement over both the
untuned default and the fully-reweighted config, and was adopted for the
final model (`train/model_xgb.json`, `train/training_report_xgb.json`).
Final test-split AUC with this model: **0.9576** (`infer/inference_report_xgb.json`),
closely matching the validation AUC — no evidence of overfitting to validation.

## Iteration 2 — selection algorithm (val split, efficiency)

Two selection strategies were compared, both respecting the two hard
constraints (≤2 candidates/event, mutually jet-disjoint):

- **Greedy**: sort candidates by score descending within an event; take the
  top one, then the next-highest-scoring candidate disjoint from it.
- **Optimal**: exhaustively enumerate all valid single/pair combinations
  per event (small combinatorics — at most a few dozen triplets/event) and
  pick the jet-disjoint set of size ≤2 that maximizes the **summed classifier
  score**.

Scanned over thresholds `[0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]` on
the validation tuning set (`select_triplets/_val_threshold_scan.json`):

| method  | best efficiency | threshold range achieving it |
|---------|------------------|-------------------------------|
| greedy  | 0.7418           | 0.00–0.01                     |
| optimal | 0.7561           | 0.00–0.03                     |

The optimal method beat greedy by ~1.4–1.5 efficiency points at every
threshold tested. This makes sense: greedy's first pick can "use up" a jet
that would have enabled a better-scoring pair, whereas the exact per-event
enumeration always finds the truly best-scoring disjoint set. A manual
brute-force cross-check on the val tuning set confirmed 527/697 (optimal) vs
517/697 (greedy) truth triplets recovered, with 18 events where the two
methods disagreed. **Optimal selection was adopted as the final method.**

## Iteration 3 — score threshold (val split, efficiency vs. purity)

With the optimal method fixed, a fine-grained threshold scan found that
efficiency stays flat at its ceiling (0.7561) for thresholds up to **0.03**,
then starts to drop (0.032 → 0.7547, and continuing to decline through higher
thresholds, e.g. 0.7418@thr=0.01 for greedy or ~0.35@thr=0.9 for either
method at very high cuts). Raising the threshold from 0.0 to 0.03 removes
roughly 18% of low-confidence noise selections and improves purity from
~0.32 to ~0.39, with **no loss of efficiency**. **`threshold = 0.03` was
adopted as final.**

## Final configuration

| parameter                | value    |
|---------------------------|----------|
| classifier                | XGBoost, max_depth=5, eta=0.08, scale_pos_weight=11.0, best_iteration=187 |
| selection method           | optimal (exact per-event disjoint-set score-sum maximization) |
| score threshold            | 0.03     |
| max candidates/event       | 2        |

## Final test-split results

- `triplet_reconstruction_efficiency` = **0.7649** (527 / 689 truth triplets recovered)
- selection purity = 0.3738 (527 / 1410 selected triplets are truth-matched)
- event selection multiplicity: 118 events with 0 selected, 956 with 1, 227 with 2
- mean selected candidates/event = 1.084

## Mass sanity check

Truth-matched selected candidates have mean invariant mass ≈167 GeV, std≈27 GeV,
consistent with the PDG top mass (172.76 GeV) and a physically reasonable
width — not an artificially narrow spike. Fake/combinatorial selected
candidates show a broader, higher, right-shifted mass distribution
(mean≈199 GeV, std≈68 GeV), as expected for accidental jet combinations. See
`sanity_checks/interpretation.md` and `sanity_checks/mass_sanity_plots.png`
for full details, and `select_triplets/plots/` for kinematics distributions
(pt, eta, phi, mass, score, selection multiplicity) of the final selected
candidates.

## Artifacts

- `dataset_build/triplets_raw.parquet`, `dataset_prepare/{train,val,test}.parquet`
- `train/model_xgb.json`, `train/training_report_xgb.json`
- `infer/inference_test_xgb.parquet`, `infer/inference_report_xgb.json` (test split, official)
- `select_triplets/selected_triplets.parquet`, `select_triplets/event_selection.parquet`,
  `select_triplets/selection_report.json`, `select_triplets/plots/`
- `sanity_checks/mass_sanity_summary.json`, `sanity_checks/interpretation.md`,
  `sanity_checks/mass_sanity_plots.png`
- `optimization_report.md` (this file), `optimization_summary.json`

Scratch/diagnostic files prefixed with `_` (`infer/_tuning_val_xgb.parquet`,
`infer/_tuning_val_report.json`, `select_triplets/_val_threshold_scan.json`,
`select_triplets/_last_run.log`) were used only for validation-split tuning
and are not part of the required artifact set.
