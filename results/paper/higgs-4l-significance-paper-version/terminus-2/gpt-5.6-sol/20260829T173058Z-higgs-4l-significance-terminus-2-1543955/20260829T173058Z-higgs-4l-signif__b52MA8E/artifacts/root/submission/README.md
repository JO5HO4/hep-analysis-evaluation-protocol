# Four-lepton counting analysis

Run with:

```bash
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

The program validates the channel arrays and computes summed Poisson log-likelihoods including the `log(k!)` terms. The fixed-hypothesis statistic is

`q = -2 [log L(s+b) - log L(b)]`.

One million background-only pseudo-experiments are generated with NumPy's `default_rng` using seed 123456789. With this sign convention, signal-like outcomes have **smaller** q, so the reported empirical p-value is the fraction `q_toy <= q_observed`; Z is `norm.isf(p)`. If no toy enters the tail, a half-toy convention is used only to keep the reported Z finite (the p-value itself remains zero).

For signal strength, the Poisson likelihood with means `b_i + mu*s_i` is optimized over the physical region `mu >= 0`. Brent root finding locates the two `-2 delta log L = 1` crossings; if a lower crossing does not occur in the physical region, `mu_lo=0` is used. The output also includes uncertainty differences, toy metadata, and a 3-sigma evidence boolean beyond the required fields.

Each run writes diagnostic PNGs to `diagnostics/test_statistic_distribution.png` and `diagnostics/mu_profile_likelihood.png` beside this code. Scientific dependencies are NumPy, SciPy, and Matplotlib.
