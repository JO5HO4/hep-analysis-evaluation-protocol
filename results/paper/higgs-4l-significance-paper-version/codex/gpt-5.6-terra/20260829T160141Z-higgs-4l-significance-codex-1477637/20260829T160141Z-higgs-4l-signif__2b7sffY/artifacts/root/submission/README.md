# Four-lepton Poisson counting analysis

Run the full analysis with:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

For the supplied data:

```bash
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

The input JSON must contain equally long `channels`, `observed`, `background`, and
`signal` arrays.  Channels are treated as independent Poisson measurements.  The
script writes the requested likelihood, test-statistic, toy-Monte-Carlo p-value,
Gaussian significance, and signal-strength fit fields, along with a few
reproducibility diagnostics (`n_toys`, seed, tail count, and the binomial
Monte-Carlo standard error `p_value_mc_se`).

## Method

For an observed channel count `k` and mean `lambda`, the implementation uses
`log P(k|lambda) = -lambda + k log(lambda) - log(k!)`, summed across channels.
The reported observed statistic is

`q = -2 [log L(signal + background) - log L(background)]`.

With this sign convention, **smaller** q is more signal-like.  Two million
background-only Poisson toy datasets are generated with a fixed seed, and the
p-value is the fraction with `q_toy <= q_observed` (ties included).  It is
converted to the one-sided Gaussian significance using `Phi^-1(1-p)`.

For the signal-strength measurement, the likelihood uses means
`background[i] + mu * signal[i]` and is maximized for physical `mu >= 0`.
The scan is expressed as `-2 Delta log L(mu)`, and its 1-sigma endpoints are
the crossings at one.  If a lower crossing would lie below the physical
boundary, the lower edge is reported as zero.

Diagnostic PNGs are always written to `submission/diagnostics/`:

- `test_statistic_toys.png`: the background-only toy q distribution and observed q.
- `mu_profile_scan.png`: the profile-likelihood curve and the one-sigma level.

Dependencies available in the execution environment are Python 3, NumPy, SciPy,
and Matplotlib.
