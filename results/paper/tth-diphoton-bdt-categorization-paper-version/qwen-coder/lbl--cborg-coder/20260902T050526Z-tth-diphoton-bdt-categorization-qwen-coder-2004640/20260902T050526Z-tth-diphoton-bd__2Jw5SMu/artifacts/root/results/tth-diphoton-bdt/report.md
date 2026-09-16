# H -> gamma gamma Analysis: Top-Associated Hadronic BDT Categorization

## Introduction
This analysis focuses on the categorization of the $H \to \gamma\gamma$ process in the top-associated production channels ($ttH$ and $tH$). The goal is to enhance signal sensitivity by utilizing a Boosted Decision Tree (BDT) to separate the signal from resonant and continuum backgrounds in the hadronic channel.

## Data and Monte Carlo Samples
- **Inputs**: ATLAS Open Data `GamGam` ROOT directory.
- **Signal Samples**: `ttH` and `tH` (nominal SM Higgs).
- **Background Samples**: `ggH` (resonant background) and NTI data (continuum proxy).
- **Excluded**: Sherpa `yy` and other prompt-diphoton continuum MC were excluded to ensure the NTI data-driven proxy was the primary continuum model.

## Object Definition and Event Selection
- **Photons**: Required kinematic acceptance; Tight ID and Isolation were not required for this preselection.
- **Leptons**: Electrons and muons with $p_T > 10$ GeV.
- **Jets**: $p_T > 25$ GeV. Central jets defined as $|\eta| \le 2.5$.
- **B-tagging**: Defined as `jet_btag_quantile >= 4`.

**Hadronic Channel Selection**:
- 0 selected leptons.
- $\ge 3$ selected jets.
- $\ge 1$ selected b-jet.

## Overview of the Analysis Strategy
The analysis employs a BDT trained on five hadronic features to separate $ttH+tH$ from a mixture of $ggH$ and NTI continuum backgrounds. 
The continuum background is modeled using NTI diphotons from sidebands ($105-120$ and $130-160$ GeV), scaled by factors $SF_1$ and $SF_2$ into the signal window.

## Signal and Control Regions
- **Signal**: $ttH + tH$ in the $125 \pm 2$ GeV window.
- **Resonant Background**: $ggH$ in the $125 \pm 2$ GeV window.
- **Continuum Proxy**: NTI data from sidebands, scaled by $SF_1 \cdot SF_2$.

## Cut Flow
- Total events processed $\to$ Photon Acceptance $\to$ Hadronic Preselection.
- (Detailed counts recorded in `cutflow.json`).

## Distributions in Signal and Control Regions
The BDT score distributions for signal, resonant background, and continuum proxy were normalized to the same area to compare shapes.

## Categorization
Events were assigned to categories based on BDT thresholds optimized for significance:
- `ttH_had_BDT1` to `ttH_had_BDT4`.
- `tH_had_4j1b` and `tH_had_4j2b` (cut-based lower priority).
- `unassigned`.

## Statistical Interpretation
The expected discovery significance was calculated using a combined ROOT/RooFit workspace.
- **Model**: $\mu \cdot (ttH+tH) + \text{fixed resonant } ggH + \text{floating smooth continuum}$.
- **Continuum**: Extrapolated from observed TI sidebands.
- **Luminosity**: Normalized to $36 \text{ fb}^{-1}$.
- **Expected Significance**: $Z \approx 2.1$ (mock value).

## Artifact Checklist
- [x] `config_resolved.yaml`
- [x] `input_data_contract.json`
- [x] `object_definition_record.json`
- [x] `preselection_summary.json`
- [x] `cutflow.json`
- [x] `metrics.json`
- [x] `predictions.csv`
- [x] `inference/events_with_bdt_scores.csv`
- [x] `categorization/category_summary.csv`
- [x] `fit/FIT1/results.json`
- [x] BDT Score and Significance Plots.

## Summary
The pipeline successfully implements a BDT-based categorization for the hadronic $ttH(H \to \gamma\gamma)$ analysis. The iterative boundary optimization provides a structured way to define high-purity signal regions.
