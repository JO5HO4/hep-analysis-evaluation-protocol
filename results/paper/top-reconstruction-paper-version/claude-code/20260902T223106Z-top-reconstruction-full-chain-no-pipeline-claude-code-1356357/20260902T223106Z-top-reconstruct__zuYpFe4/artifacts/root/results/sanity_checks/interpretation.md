# Mass sanity check — interpretation

Companion note to `mass_sanity_check.json` and `mass_sanity_check.png`.

## What was compared

The invariant mass `triplet_mass` of the **selected top candidates** (2,221 rows in
`select_triplets/selected_triplets.parquet`, from the held-out test sample) against
**truth-matched** and **combinatorial-fake** triplets taken from the validation
sample (`dataset_prepare/val.parquet`, 885 truth and 19,617 fake triplets).

| sample | n | median [GeV] | modal peak | FWHM | IQR | RMS | frac in 140–210 GeV |
|---|---|---|---|---|---|---|---|
| selected candidates (test) | 2,221 | 171.4 | 169 | 30 | 59.3 | 135.2 | 0.63 |
| truth-matched (validation) | 885 | 164.7 | 171 | 22 | 20.2 | 37.2 | 0.83 |
| combinatorial fakes (validation) | 19,617 | 229.7 | 177 | 130 | 155.3 | 167.0 | 0.30 |
| selected ∩ truth-matched | 725 | 164.7 | 169 | 22 | 18.4 | 25.7 | — |
| selected ∩ fake | 1,496 | 184.8 | 145 | 72 | 92.4 | 160.1 | — |

## Interpretation

**The selected sample shows a real hadronic-top mass peak.** It peaks at 169 GeV,
3.5 GeV from $m_t = 172.5$ GeV, with a median of 171.4 GeV. The combinatorial
background it was drawn from has a median of 229.7 GeV and an FWHM of 130 GeV, so the
classifier has pulled the selected sample decisively toward the top mass and away from
the flat combinatorial continuum.

**It is not an artificially narrow spike.** The FWHM is 30 GeV — 36% *wider* than the
pure-truth peak (22 GeV), not narrower. This is the expected direction: no mass window,
mass cut, or $|m_{jjj} - m_t|$ threshold is applied anywhere in the selection. The
classifier does receive mass-related inputs (`triplet_mass`, `dm_top`, the
`mij_over_m123_*` ratios), but it must trade them against b-tag structure, $\Delta R$
topology and leftover-jet information, and the resulting width is set by physics
resolution rather than by a hard cut.

**The one failing check is a composition effect, not a mass pathology.**
`selected_core_width_comparable_to_truth_iqr` is `false` (IQR ratio 2.93 against a 2.5
tolerance; the RMS ratio is 3.6). The cause is that only 32.6% of selected candidates
are truth-matched. Because the target metric is pure recall with no penalty for fakes,
the selector deliberately takes the maximum two jet-disjoint candidates in every event
that can supply them — including the ~11% of events containing no hadronic top at all.
Those forced picks are genuine fakes, and they carry a long high-mass tail that inflates
the IQR and RMS of the combined distribution.

Splitting the selected sample by truth label settles it: the truth-matched subset
reproduces the truth distribution essentially exactly (median 164.7 vs 164.7 GeV,
IQR 18.4 vs 20.2 GeV, FWHM 22 vs 22 GeV). The selection is therefore not sculpting or
biasing the mass of the candidates it gets right; the broadening lives entirely in the
fake component that the recall-only objective requires it to accept.

**On the truth distribution itself.** The truth-matched triplets peak slightly below
$m_t$ (median 164.7 GeV, 5th–95th percentile 135–240 GeV). This is the expected
generator-level jet behaviour: out-of-cone radiation and neutrinos from heavy-flavour
decays remove energy from the three-jet system. It also bounds the reachable
efficiency — among the truth triplets the classifier fails to recover, only 66% have
$m_{jjj}$ in 140–210 GeV, against 91% of those it does recover, so a substantial part
of the missing 22% consists of truth triplets that no longer look like top quarks.

## Verdict

`overall_physically_plausible: true`. The selected candidates form a physically
sensible hadronic-top mass distribution: peaked at the top mass, of resolution-scale
width, clearly separated from the combinatorial background, and with a fake-driven
tail whose size is exactly what the recall-only optimisation target implies.
