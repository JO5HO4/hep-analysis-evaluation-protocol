# Task Description: Inclusive H -> gamma gamma Analysis

This task implements a single-category, inclusive analysis of the Higgs boson decaying to two photons using ATLAS open-data.

## Objectives
- Implement a selection pipeline for diphoton events.
- Perform a spurious-signal scan using Sherpa prompt-diphoton Monte Carlo to select the optimal background PDF.
- Calculate the expected significance and signal strength using S+B Asimov pseudo-data with $\mu_{gen}=1$.
- Produce diagnostic fit plots and cutflow tables.

## Physics Contract
- **Photon Selection**:
    - $\ge 2$ photons.
    -  > 25$ GeV.
    - $|\eta| < 2.37$, excluding .37 < |\eta| < 1.52$.
    - Tight identification and isolation.
    - Leading photon /m_{\gamma\gamma} > 0.35$, subleading $> 0.25$.
- **Mass Window**: 05-160$ GeV.
- **Blinding**: 20-130$ GeV.
- **Sidebands**: 05-120$ GeV and 30-160$ GeV.
- **Statistical Backend**: ROOT/PyROOT/RooFit.
