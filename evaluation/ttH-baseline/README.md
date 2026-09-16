# ttH inclusive hadronic baseline

`inclusive-hadronic-constant-sideband/v1` is an evaluator-side reference for
the ttH diphoton task. It applies the hadronic-preselection flag in a trusted
event table, assigns every selected event to one `inclusive_hadronic` analysis
category, and deliberately ignores BDT scores and agent-assigned categories.

It constructs a binned signal-plus-background Asimov sample over the diphoton
mass range. Signal and resonant-Higgs templates use the table's 36 fb^-1 model
weight. The continuum template is a constant rate estimated only from observed
tight-ID/tight-isolation data in the documented sidebands. A binned Poisson
profile-likelihood calculation reports `mu_hat`, `mu_uncertainty`, `q0`, and
expected `Z` in a machine-readable JSON result.

## Run the baseline

```bash
python evaluation/ttH-baseline/evaluate.py \
  --input EVALUATOR_EVENTS.csv \
  --input-role trusted-evaluator \
  --output evaluation/ttH-baseline/baseline_results.json \
  --selected-output /tmp/tth-inclusive-hadronic.parquet
```

`EVALUATOR_EVENTS.csv` must be evaluator-owned, not an agent submission. It
needs hadronic-preselection, mass, component, model-weight, observed-data, and
photon-TI columns; `baseline.py` validates the exact required fields.

`baseline_results.json` is a development-proxy result generated from a
preserved run artifact. Its provenance explicitly records that status; replace
it with a `trusted-evaluator` result before using it for an agent comparison.

## Fixed-quantile category baseline

`fixed-score-quantiles-4/v1` holds a supplied continuous BDT score fixed and
assigns four empirical score-quantile categories. It then applies the same
per-category constant-sideband Asimov calculation and combines the category
likelihood information. This tests boundary optimization, rather than BDT
training. Generate it with:

```bash
python evaluation/ttH-baseline/evaluate_quantiles.py \
  --input EVALUATOR_EVENTS_WITH_BDT_SCORE.csv \
  --output evaluation/ttH-baseline/fixed_quantile_baseline_results.json
```

The checked-in result is a development proxy and cannot be used as an
authoritative outcome grade.

## Compare an agent fit

```bash
python evaluation/ttH-baseline/compare.py \
  --events EVALUATOR_EVENTS.csv \
  --agent-fit AGENT_SIGNIFICANCE_ASIMOV.json \
  --output comparison.json
```

The comparison is valid only when both fits use the same frozen evaluator
sample and compatible assumptions. This baseline is development evidence, not
the task verifier or an authoritative outcome scorer.
