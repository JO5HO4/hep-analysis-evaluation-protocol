# Analysis Documentation: Inclusive H -> gamma gamma

## Scope
This analysis is limited to a single inclusive category. All events passing the selection criteria are assigned to the `inclusive` category.

## Selection Criteria
- Number of photons $\ge 2$.
- Photon  > 25$ GeV.
- Photon $|\eta| < 2.37$ and $\notin (1.37, 1.52)$.
- Tight identification and isolation requirements.
- Kinematic cuts: ^1/m_{\gamma\gamma} > 0.35$ and ^2/m_{\gamma\gamma} > 0.25$.
- Mass window: 05 < m_{\gamma\gamma} < 160$ GeV.

## Background Estimation
The continuum background is modeled using an analytic function selected via a spurious-signal scan on the Sherpa yy prompt-diphoton MC sample.

## Statistical Interpretation
The central fit is performed using RooFit. The expected significance is derived from a signal-plus-background fit to Asimov pseudo-data generated with $\mu = 1$.
