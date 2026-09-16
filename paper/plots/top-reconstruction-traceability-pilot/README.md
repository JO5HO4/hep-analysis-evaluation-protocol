# Top-reconstruction traceability-pilot figures

These descriptive figures are generated from the machine-readable pilot records
under `paper/reviews/top-reconstruction-traceability-pilot/`. They do not
replace the Harbor verifier reward and do not constitute an authoritative
physics outcome grade.

- `01-rubric-status-heatmap`: all 31 evaluation-protocol questions by retained run.
- `02-review-reward-and-evidence-coverage`: evidence status plus the separately reported Harbor verifier reward and non-authoritative review fraction.
- `03-baseline-efficiency-fake-ratio`: evaluator-side selection comparison to `mass-greedy/v2-n-top-2`.
- `04-fake-mass-sculpting`: evaluator-side fake-mass diagnostic using a fixed 0–400 GeV, 40-bin histogram.
- `05-protocol-area-coverage`: established, failed, and not-established question results grouped by protocol area.
- `06-overall-descriptive-ranking`: equal-topic pass-fraction ranking, explicitly non-authoritative.
- `07-topic-breakdown-heatmap`: per-run pass fraction within each evaluation-protocol topic.

Regenerate with:

```bash
python paper/reviews/top-reconstruction-traceability-pilot/figures/generate_pilot_figures.py
```
