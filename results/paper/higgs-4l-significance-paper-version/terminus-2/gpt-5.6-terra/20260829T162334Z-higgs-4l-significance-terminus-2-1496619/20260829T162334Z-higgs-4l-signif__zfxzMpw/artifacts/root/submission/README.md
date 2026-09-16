# Four-lepton Poisson counting analysis

Run the reproducible analysis with:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

The input JSON has `channels`, `observed`, `background`, and `signal` arrays. Each channel is treated as an independent Poisson count. The program reports total Poisson log likelihoods (including `log(k!)`) for background and SM signal-plus-background, and the fixed-hypothesis statistic `q=-2(logL_sb-logL_b)`.

For the p-value, one million background-only Poisson toy datasets are generated with a fixed NumPy seed. Smaller values of this q are more signal-like, so the reported one-sided p-value is the fraction with `q_toy <= q_observed`. The p-value is the direct toy fraction `N_extreme/N_toys`, and the Gaussian-equivalent significance is `Phi^-1(1-p)`.

For the measurement, the likelihood is profiled as a function of physical signal strength `mu >= 0`, with means `background + mu*signal`. Numerical optimization finds `mu_hat`; the one-standard-deviation endpoints are where `-2 Delta log L=1`. If the lower crossing would be below physical `mu=0`, the lower edge is reported as zero.

Diagnostics are always regenerated at `submission/diagnostics/test_statistic_toys.png` and `submission/diagnostics/mu_profile.png`.

The output also includes `evidence_at_3sigma`, which directly records whether the toy-derived Gaussian significance is at least 3.
