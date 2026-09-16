# Top-Reconstruction Mass Baseline

This is a small, self-contained reference implementation for comparisons in
the top-reconstruction evaluation rubric. It is a physics-motivated baseline,
not the task verifier and not an authoritative outcome scorer.

## Selector definition: `mass-greedy/v2-n-top-2`

For every event, rank all triplet candidates by increasing

`abs(triplet_mass - 172.5 GeV)`

Break ties deterministically by the canonical sorted jet-index triplet. Walk
that ranking from best to worst, accepting a candidate only when none of its
jets has already been used. Stop after two selected candidates, matching the
rubric constraint `N_top <= 2`.

The baseline deliberately does not use the candidate classifier `score`, truth
labels, or any learned quantity. It therefore supplies a simple mass-only
comparison for a learned or score-based selector.

`classifier_baseline.py` additionally defines the frozen,
mass-blind `gaussian-naive-bayes-mass-blind/v1` classifier comparison. It uses
only the three angular-separation and three mass-ratio features, with a fixed
event-ID modulo-10 train/validation/test split. Its development reference is
`classifier_baseline_results.json`; like the selector result, it is not a
hidden-test score or authoritative outcome grade.

## Reproducing the results

Run from the repository root:

```bash
python evaluation/top-reconstruction-baseline/evaluate.py \
  --input DEVELOPMENT_TRIPLETS.parquet \
  --output evaluation/top-reconstruction-baseline/baseline_results.json
```

For an evaluator-side comparison, provide a labeled candidate table and the
agent's saved selected-candidate Parquet:

```bash
python evaluation/top-reconstruction-baseline/compare.py \
  --candidates LABELED_CANDIDATES.parquet \
  --agent-selection AGENT_SELECTED_CANDIDATES.parquet \
  --output comparison.json
```

`baseline_results.json` is generated solely from the labeled development data.
It is a development reference, not a hidden-test score. The selector accepts
unlabeled inputs too, but efficiency, purity, fake-rate, and truth-matched mass
statistics can only be calculated when `is_truth` is present.

## Comparison protocol

The evaluator independently runs this baseline on the same frozen, labeled
evaluation sample as the agent's saved selection, then compares the two using
the metric definitions in the results file. The task-solving agent is not
asked to run, report, or discuss the baseline. The baseline report
intentionally has no b-quark-inclusion result: the task input contains triplet
jet indices and a triplet truth label, but no b-quark matching information.

`compare.py` reports a directional comparison for reconstruction efficiency,
purity, fake-to-true ratio, F1, candidate-level selection accuracy, balanced
selection accuracy, truth-matched selected-mass bias, and mass resolution. Raw
selection accuracy should be read alongside balanced accuracy because the
candidate labels are imbalanced. ROC AUC is intentionally unavailable: the
task saves selected candidates rather than an agent-generated continuous score
for every candidate.

Every comparison record includes the agent value, baseline value, unit,
absolute delta, and direction-aware `relative_improvement_percent`. Positive
percentages mean the agent is better; the value is `null` when the baseline is
zero because a percentage would be undefined.

It also records a non-authoritative fake-mass-sculpting diagnostic.  Its
reference is every labeled fake candidate before selection.  The reference,
agent selection, and `mass-greedy/v2-n-top-2` use the same fixed unweighted
0--400 GeV, 40-bin histogram.  The record reports modal-bin-center shift from
the unbiased fake mode and population-standard-deviation width retention.
An agent is marked better only when its shift is no larger and its retention
is no smaller, with one strict improvement; no threshold or outcome score is
introduced.

## Contents

- `baseline_selector.py`: deterministic `mass-greedy/v2-n-top-2` implementation.
- `evaluate.py`: writes a JSON report and optional selected-candidate Parquet.
- `compare.py`: evaluator-side baseline and Pareto comparison of an agent output.
- `baseline_results.json`: reproducible development-sample reference results.
- `test_baseline_selector.py`: selector invariants and tie-breaking tests.
