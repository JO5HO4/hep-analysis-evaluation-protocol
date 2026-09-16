# Four-lepton excess: Poisson counting analysis

A frequentist counting analysis of the H→ZZ*→4ℓ style dataset in
`/root/data/four_lepton_counts.json`. Three independent channels (`4mu`,
`2e2mu`, `4e`), each with an observed count `n`, an expected background `b`,
and an expected signal `s` at the Standard Model rate (μ = 1).

The analysis answers two questions:

1. **Is there evidence for a signal?** Test the background-only hypothesis
   against signal+background with a likelihood ratio, and get a p-value from
   background-only pseudo-experiments.
2. **How big is the signal?** Profile the signal strength μ (the multiplier on
   the SM signal yield) and quote a 68% CL interval.

## How to run

```sh
/root/submission/run.sh INPUT_JSON OUTPUT_JSON
```

e.g. the command used to produce `/root/results/results.json`:

```sh
/root/submission/run.sh /root/data/four_lepton_counts.json /root/results/results.json
```

Environment overrides:

| var | default | meaning |
| --- | --- | --- |
| `NTOYS` | `10000000` | number of background-only pseudo-experiments |
| `SEED` | `20260829` | PRNG seed (results are exactly reproducible) |
| `DIAGNOSTICS_DIR` | `<submission>/diagnostics` | where the PNGs are written |

Files:

- `analysis.py` — all of the statistics; writes the JSON.
- `plots.py` — the two diagnostic figures.
- `run.sh` — runs both.

Only `numpy`, `scipy`, and `matplotlib` are needed. Runtime is ~3 s for 10⁷
toys.

## Method

**1. Likelihood.** Each channel is an independent Poisson count, so

```
log L(μ) = Σ_i [ n_i·log(μ s_i + b_i) − (μ s_i + b_i) − log(n_i!) ]
```

evaluated with `gammaln` for the factorial term. `logL_b` is `log L(0)` and
`logL_sb` is `log L(1)`.

**2. Test statistic.** `q = −2(logL_sb − logL_b)`. The factorials cancel in the
difference, leaving

```
q = 2·Σ_i s_i − 2·Σ_i n_i·w_i,    w_i = log(1 + s_i/b_i)
```

so `q` is *affine and decreasing* in the counts: more signal-like data gives a
more negative `q`. The p-value is therefore the left tail,
`p = P(q_toy ≤ q_obs | background only)`.

**3. p-value.** 10⁷ background-only toys (Poisson draws with mean `b_i` per
channel), generated in batches of 2×10⁶ to bound memory, counting how many give
`q_toy ≤ q_obs`. The quoted uncertainty is the binomial error
`sqrt(p(1−p)/N)`.

Because `q` depends on the counts only through the single scalar `Σ n_i w_i`,
the p-value can also be computed **exactly** by enumerating the joint Poisson
lattice over the channel counts. This is done independently as a cross-check
(and is used as the significance fallback if zero toys pass, which would
otherwise give an infinite Z). It is skipped automatically if the lattice
exceeds 2×10⁷ points.

`significance = Φ⁻¹(1 − p)` (one-sided).

**4. Signal strength.** μ̂ from a bounded `minimize_scalar` on `−2 log L(μ)`,
subject to the physical floor `μ > max_i(−b_i/s_i)` where the Poisson mean would
go non-positive. The 68% CL interval comes from `brentq` on
`−2Δlog L(μ) − 1` on each side of the minimum, giving asymmetric errors.

## Output

`results.json` contains the eight required fields:

| field | meaning |
| --- | --- |
| `logL_b` | background-only log-likelihood of the observed data |
| `logL_sb` | signal+background log-likelihood of the observed data |
| `test_statistic` | observed `q = −2(logL_sb − logL_b)` |
| `p_value` | background-only p-value from the toys |
| `significance` | Gaussian significance Z |
| `mu_hat` | best-fit signal strength |
| `mu_lo` | lower edge of the ±1σ interval |
| `mu_hi` | upper edge of the ±1σ interval |

plus the echoed inputs (`channels`, `observed`, `background`, `signal`) and
diagnostics: `p_value_exact`, `p_value_uncertainty`, `n_toys`,
`n_toys_passing`, `p_value_source`, `p_value_used_for_Z`,
`significance_from_toys_only`, `q_min`, `evidence_3sigma`, `discovery_5sigma`,
`mu_err_up`, `mu_err_down`, `seed`.

`p_value` is the **toy** p-value; `p_value_exact` is the independent lattice
enumeration.

## Results on the provided dataset

Observed `[6, 5, 2]` in `[4mu, 2e2mu, 4e]`:

```
logL_b     = -11.082750
logL_sb    =  -5.815922
q          = -10.533656

p (toys)   = 2.590e-04 ± 5.1e-06   (2590 / 10,000,000)
p (exact)  = 2.540e-04
Z          = 3.471 sigma

mu         = 1.624  +0.743 / -0.615   (68% CL: [1.009, 2.367])
```

**The excess reaches the 3σ evidence threshold (Z = 3.47σ) but not the 5σ
discovery threshold.**

The measured signal strength is consistent with the Standard Model: μ = 1 lies
inside the 68% interval, though only just — the lower edge is μ_lo = 1.009.

The toy and exact p-values agree to within ~1σ of the toy's binomial error, as
expected.

## Diagnostics

- `diagnostics/test_statistic_distributions.png` — the distribution of `q` under
  background-only (blue) and signal+background (orange) on a log-y axis, with
  the observed value marked. Shows how far into the background left tail the
  data sits.
- `diagnostics/mu_scan.png` — the profile `−2Δlog L(μ)` with the `= 1` crossing
  that defines the 68% interval, the μ̂ marker, and the SM μ = 1 reference.

## Assumptions and generality

- Any number of channels is supported; the code reads whatever is in the JSON.
- Backgrounds are treated as **exactly known** (no nuisance parameters). Every
  channel must have `background > 0`.
- Channels are assumed independent.
- The asymptotic (Wilks) approximation is *not* used for the p-value — with
  counts this small it would be unreliable, which is why the toys and the exact
  enumeration are both computed. The 68% μ interval does use the
  `Δ(−2logL) = 1` convention.
