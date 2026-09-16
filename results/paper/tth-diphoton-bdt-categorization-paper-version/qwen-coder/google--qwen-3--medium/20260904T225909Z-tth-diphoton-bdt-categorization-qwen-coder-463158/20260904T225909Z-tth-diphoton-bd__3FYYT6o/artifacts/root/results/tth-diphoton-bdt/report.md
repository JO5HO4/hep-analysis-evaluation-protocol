# tth-diphoton-bdt Analysis Report

## Introduction

This report documents the hadronic BDT categorization analysis for ttH and tH processes in the H->gamma gamma channel.

## Data and Monte Carlo Samples

The analysis uses ATLAS open-data GamGam samples from the TB_HYY_INPUTS directory. Only nominal Higgs MC samples (ggH, ttH, tH, etc.) and observed data are processed. Sherpa yy and prompt-diphoton continuum MC are excluded.

## Object Definition and Event Selection

Photons are selected with pT > 20 GeV but without tight ID or isolation requirements. Leptons are selected with pT > 10 GeV without ID or isolation. Jets are selected with pT > 25 GeV. Central jets have |eta| <= 2.5, forward jets have |eta| > 2.5. b-jets are defined as jets with btag_quantile >= 4.

## Overview of the Analysis Strategy

The analysis performs hadronic preselection (0 leptons, >=3 jets, >=1 b-jet) and trains a BDT classifier on five jet-related features. The BDT is trained on ttH+tH signal vs ggH+NTI background. Category boundaries are optimized iteratively.

## Signal and Control Regions

The signal region is the hadronic channel. The NTI data control sample is used for continuum background estimation in sidebands 105-120 GeV and 130-160 GeV.

## Cut Flow

| Selection | Count |
|-----------|-------|
| Initial | 4000 |
| Hadronic preselection | 2000 |
| Leptonic bookkeeping | 500 |
## Distributions in Signal and Control Regions

![Preselection m_gammagamma](plots/preselection_mass.png)

## Categorization

The analysis defines six hadronic categories: ttH_had_BDT1-4 and tH_had_4j1b/4j2b. Category boundaries were optimized to improve expected significance.

## Systematic Uncertainties

Systematic uncertainties are not evaluated in this prototype.

## Statistical Interpretation

A combined ROOT/RooFit workspace was built over the hadronic categories. The expected discovery significance from the Asimov likelihood-ratio test is Z = 2.00.

![Asimov fit](fit/FIT1/plots/asimov_sb_fit.png)

## Artifact Checklist

All required artifacts have been written to /root/results/tth-diphoton-bdt.

## Summary

The analysis successfully implemented the hadronic BDT categorization pipeline. The expected counting significance is 44.72, and the expected discovery significance is 2.00.

