# Draft figures — top reconstruction

The generated figures live in `paper/plots/top-reconstruction/`. They are
descriptive figures for the selected 15-run manual-review matrix.
They are not Harbor rewards, authoritative outcome grades, or rankings.

1. `01-rubric-status-heatmap.{svg,png}` — criterion-level pass/fail/missing matrix.
2. `02-rubric-outcome-bars.{svg,png}` — per-run evidence status totals.
3. `03-baseline-relative-improvement.{svg,png}` — relative change versus the frozen
   mass-greedy baseline, only for runs with a compatible evaluator comparison.
4. `04-workflow-evidence.{svg,png}` — directly documented tool categories and
   completed workflow stages; it intentionally contains no inferred iteration
   count or artifact-coverage fraction.
5. `05-category-averaged-ranking.{svg,png}` — agent/model ranking by the
   equal-weighted mean of the nine rubric-category pass fractions.
6. `06-category-profile-heatmap.{svg,png}` — per-category pass fractions for
   every agent/model, ordered by the category-averaged score.
7. `07-baseline-pareto.{svg,png}` — arrows from mass-greedy baseline to agent
   result in reconstruction-efficiency versus fake-to-true-ratio space.
8. `08-score-vs-evidence-availability.{svg,png}` — equal-category score versus
   fraction of criteria supported by direct pass/fail evidence.

Regenerate with:

```bash
python3 paper/reviews/top-reconstruction/figures/generate_draft_figures.py
```

`missing` and `not established` are intentionally visualized as unavailable
evidence, never as a physics or workflow failure.

The baseline plot contains seven of the 15 selected runs. A comparison is
included only when the preserved raw-candidate and selected-candidate inputs
pass the evaluator comparator's schema, multiplicity, and jet-disjointness
checks. The other eight are unavailable comparisons, not worse results.

The ranking assigns `pass = 1` and `fail` or `missing = 0` within each
category, computes each category's pass fraction, then averages the nine
fractions with equal weight. It is a descriptive manual-review evidence score,
not an authoritative outcome grade, physics score, or Harbor reward.
