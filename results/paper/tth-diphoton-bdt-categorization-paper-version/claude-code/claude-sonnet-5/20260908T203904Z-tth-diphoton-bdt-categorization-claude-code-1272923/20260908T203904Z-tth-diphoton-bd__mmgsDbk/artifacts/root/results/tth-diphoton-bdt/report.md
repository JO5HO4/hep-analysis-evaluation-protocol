# ttH/tH diphoton hadronic-category BDT analysis report

## Scope

Nominal Higgs signal MC (VBF, WH, ZH, ggH, ggZH, tH, ttH) and observed data only.
Sherpa gamma-gamma continuum MC and any other non-nominal-Higgs MC files present under the inputs
directory are excluded (see `input_data_contract.json`, `rejected_mc_files_not_nominal_higgs`).
Photon tight-ID and isolation are **not** required in the preselection (see `object_definition_record.json`).

## Blinding

Observed TI (tight-tight, both photons pass tight ID + isolation) data in the 125 +/- 2 GeV signal
window is never inspected, counted, summed, or plotted anywhere in this pipeline. A wider 120-130 GeV
display-blind window is additionally applied to TI data in control-shape plots only. NTI data is never
blinded and is used as the continuum-background proxy (ABCD method, SF1=0.02621,
SF2=0.09918, SF1*SF2=0.002599).

## BDT

Features: ['n_jets_central', 'n_bjets', 'jet_ht', 'leading_jet_pt', 'dijet_mass_leading']. Deterministic `GradientBoostingClassifier` trained on the stable-hashed
train partition (ttH+tH signal vs. ggH-TI + NTI-sideband background). Boundaries optimized greedily
on the validation partition, accepting a new boundary only when quadrature-summed Asimov significance
improves by >= 5%.
Accepted boundaries: [0.87, 0.68].

## Categorization (36 fb^-1 re-normalized)

Categories kept after the >= 0.8 expected
background event retention threshold: ['ttH_had_BDT1', 'ttH_had_BDT2', 'tH_had_4j1b', 'tH_had_4j2b'].
Categories merged into `unassigned`: ['ttH_had_BDT3', 'ttH_had_BDT4'].
Combined expected counting significance Z (36 fb^-1): 1.5234.

## RooFit background/signal modelling and Asimov significance

Per retained category: TI-sideband (105-120, 130-160 GeV) background shape scan
(exponential / Chebychev order 1 / order 2, AIC-selected), extrapolated into the full 105-160 GeV
fit range; fixed-shape Gaussian signal (ttH+tH TI MC) and fixed-shape, fixed-normalization Gaussian
resonant-Higgs background (non-top Higgs TI MC); combined into a RooFit extended model and fit to a
deterministic analytic Asimov dataset (mu floating, then mu=0 fixed) to obtain the discovery test
statistic q0 and Z = sqrt(q0). See `fit/FIT1/` for full per-category results; categories are combined
via quadrature sum of Z (see `fit/FIT1/backend.json` for why a single RooSimultaneous fit is not used
in this ROOT build).

Combined expected Asimov significance Z (36 fb^-1): 1.8312.

## Artifacts

See `run_manifest.json` for the full run configuration and `workspace_manifest.json` /
`fit/workspace.json` for the RooFit workspace contents.
