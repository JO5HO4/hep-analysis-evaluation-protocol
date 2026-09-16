# Four-lepton Poisson counting analysis

Run the analysis with:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

The input must contain equal-length `channels`, `observed`, `background`, and
`signal` arrays. The script evaluates the full Poisson log likelihood (including
the factorial term) for the background-only and fixed Standard Model
signal-plus-background hypotheses.

The fixed-hypothesis statistic is

```text
q = -2 log[L(s+b)/L(b)].
```

Thus, more signal-like data have smaller (usually more negative) values of `q`.
The background p-value is the fraction of 2,000,000 deterministic background
pseudo-experiments satisfying `q_toy <= q_observed`; `Z` is computed as
`Phi^-1(1-p)`. The JSON also records the toy count, tail count, seed, and tail
definition so the Monte Carlo result is fully reproducible.
The reported `p_value_mc_se` is its binomial Monte Carlo standard error. For a
pathological empirical endpoint (`p_value` exactly zero or one), the infinite
plug-in significance is represented by JSON `null`.

For the signal-strength measurement, the channel means are
`mu * signal[i] + background[i]`. The code maximizes the joint likelihood on
the physical domain `mu >= 0` and solves for the two `-2 Delta log L = 1`
crossings. If a lower crossing does not occur before the physical boundary,
`mu_lo` is reported as zero.

Each run writes these diagnostic plots under `diagnostics/`:

- `test_statistic_distribution.png`: background-toy statistic distribution,
  with the observation marked.
- `mu_likelihood_scan.png`: signal-strength likelihood profile, its minimum,
  and its one-standard-deviation crossings.

Requirements are Python 3, NumPy, SciPy, and Matplotlib.
