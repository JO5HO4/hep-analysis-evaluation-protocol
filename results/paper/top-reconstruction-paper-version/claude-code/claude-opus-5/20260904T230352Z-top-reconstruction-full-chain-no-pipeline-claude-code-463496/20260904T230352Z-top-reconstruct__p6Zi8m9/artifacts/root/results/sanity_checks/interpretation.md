# Mass sanity check — interpretation

**Verdict: PASS.** The selected candidates form a physically plausible reconstructed hadronic-top
mass distribution: a peak at the top mass with a realistic detector-and-combinatorics width and a
high-mass tail. It is not an artificially narrow spike.

Companion data: `mass_sanity_check.json` (this directory) and
`../select_triplets/plots/mass_sanity_check.png`.

## The numbers

| Sample | n | mean | median | 68 % half-width | frac in 130–210 GeV |
|---|---|---|---|---|---|
| Selected candidates (test) | 2 221 | 208.3 | 171.9 | 55.5 | 0.671 |
| ↳ selected **and** truth-matched | 736 | 166.4 | 164.5 | 13.8 | 0.940 |
| ↳ selected **and** fake | 1 485 | 229.1 | 187.7 | 71.9 | 0.537 |
| Truth triplets (val) | 885 | 171.3 | 164.7 | 17.4 | 0.881 |
| Fake triplets (val) | 19 617 | 275.6 | 229.7 | 121.8 | 0.340 |
| All triplets (test) | 22 021 | 271.0 | 224.1 | 119.7 | 0.360 |

Histogram peaks: **selected 167.5 GeV**, truth 162.5 GeV, against a reference m_t = 172.5 GeV.

## Reading it

**The peak is in the right place.** The selected distribution peaks at 167.5 GeV, within ~5 GeV of
the generated top mass and consistent with the truth-triplet peak at 162.5 GeV. Both sit slightly
below 172.5 GeV, which is the expected direction: these are generator-level jets, so out-of-cone
radiation and neutrinos from heavy-flavour decays inside the b-jet remove energy from the triplet
and pull the reconstructed mass down. A peak *above* the top mass, or one exactly at 172.5 GeV with
no offset, would have been the suspicious result.

**The width is physical, not a spike.** The 68 % half-width of the full selected sample is 55.5 GeV
and the truth-matched subset is 13.8 GeV. The spike test in the JSON requires a half-width of at
least 5 GeV and a non-delta-like shape; the observed widths clear that by a wide margin. The
13.8 GeV width of correctly-reconstructed candidates is the genuine jet-resolution smearing of a
three-jet mass, and the 55.5 GeV width of the full selection is that peak sitting on top of the
combinatorial background from the 67 % of selections that are wrong.

**The two-component structure is exactly what it should be.** Splitting the selection by truth match
separates cleanly: the 736 truth-matched selections are a real top peak (median 164.5 GeV, 94 %
inside 130–210 GeV), while the 1 485 fakes are broad and shifted high (median 187.7 GeV). Because
the efficiency metric carries no precision penalty, the selector deliberately emits two candidates
whenever the event allows it, so this fake component is expected and is not a defect — it is the
price of maximizing recall.

**The classifier learned physics, not a mass window.** This is the most informative comparison in
the table. Random combinatorics (all test triplets) have a median mass of 224.1 GeV. The fakes the
classifier actually *chose* have a median of 187.7 GeV — much more top-like than a random triplet,
but not artificially pinned to 172.5 GeV. If the model had simply learned "select triplets whose
mass is near 172.5", the selected-fake distribution would be a narrow spike at the top mass and the
selected distribution would be far too narrow overall. Instead the model is picking candidates that
are top-like in b-tag content, ΔR structure, W-subsystem mass and decay angles, and their mass comes
out approximately right as a *consequence*. That is the correct causal direction, and it is why the
mass observable remains usable as an independent cross-check rather than being circular.

## Caveats

- The truth/fake reference distributions are taken from the **validation** split, per the task
  specification, while the selected candidates come from the test split. The two splits are
  statistically equivalent (both 1 733 events from the same event-level random partition), so the
  comparison is fair, but they are not the same events.
- The high-mass tail extends well past 400 GeV. This is entirely the fake component in high-jet-
  multiplicity events, where a triplet can accidentally combine three hard, widely-separated jets.
  It is expected and is not evidence of a reconstruction bug.
