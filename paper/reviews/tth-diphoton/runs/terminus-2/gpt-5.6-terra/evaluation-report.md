# Manual evidence review — ttH diphoton

Non-authoritative review of exactly one preserved trial, under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`. This natural-language rubric is not an indexed evaluation specification and this report creates no outcome grade.

| Field | Value |
|---|---|
| Task / run | `haichenwangberkeley/tth-diphoton-bdt-categorization` / `20260902T205321Z-tth-diphoton-bd__sfftAQT` |
| Agent / model | `terminus-2 / gpt-5.6-terra` |
| Harbor status / verifier reward | `completed / 0.000000` |
| Evidence audited | result/config/log/trajectory, verifier output, both submitted Python files, all readable JSON/CSV tables, report, workspace records, and plot payloads/files below `artifacts/root` |

The zero verifier reward is execution context only. The verifier directly identifies a feature-API mismatch; it does not negate independently readable results. Conversely, saved numerical fit JSON is not treated as a real fit where the executed source shows it was written as a template.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Terminus 2 / gpt-5.6-terra | 15 | 7 | 16 | completed / 0.000000 |

| Summary | Terminus 2 / gpt-5.6-terra |
|---|---:|
| Total reward | 15 / 38 |
| Overall equal-category reward | 0.4241 |

Category pass fractions (Groups I–IX) are `3/3, 4/4, 3/6, 2/5, 0/9, 0/3, 2/3, 1/4, 0/1`; their arithmetic mean is the sole normalized metric above.

## Per-criterion evidence

`P`, `F`, and `M` mean pass, direct failure, and missing respectively; every non-pass has reward 0. Paths below are relative to the preserved trial's `artifacts/root/results/tth-diphoton-bdt/` unless stated otherwise.

| ID | Status / reward | Observed value and exact evidence |
|---|---:|---|
| Q1 | P / 1 | Wall time `1524.971 s` (`result.json: started_at/finished_at`); agent execution `1378.988 s` (`agent_execution`). |
| Q2 | P / 1 | `$0.79612203 USD`, `result.json:agent_result.cost_usd`. |
| Q3 | P / 1 | `report.md` is readable and contains the required report-topic headings, linked plots, selection, training, categorization, and statistical narrative. |
| Q4 | P / 1 | `object_definition_record.json:photons` and `preselection_summary.json:photon_definition`: no tight-ID or isolation at preselection. |
| Q5 | P / 1 | `preselection_summary.json:channel_counts`: hadronic raw `286845`, signed 36-fb model-weight sum `216378.280645`; scope is all listed nominal Higgs MC plus data. |
| Q6 | P / 1 | `object_definition_record.json` and `run_analysis.py:21-28`: photons `pT>25`, `|eta|<2.37`, lepton `pT>10`, jets `pT>25`, zero leptons, >=3 jets, >=1 `jet_btag_quantile>=4`. |
| Q7 | P / 1 | `preselection_summary.json:counts` gives raw and weighted hadronic yields separately for VBF, WH, ZH, ggH, ggZH, tH, ttH (e.g. ttH `58009`, `20.297328`). |
| Q8 | M / 0 | Source imports `sklearn.ensemble.GradientBoostingClassifier`, but no saved sklearn/package version was found in source, resolved config, metadata, report, log, or trajectory. |
| Q9 | F / 0 | `model/training_metadata.json:features` is `[n_jets,n_bjets,leading_jet_pt,subleading_jet_pt,ht_jets]`; verifier `score_report.json:selection_api.errors` directly reports the required `BDT_FEATURES` API mismatch. |
| Q10 | M / 0 | No held-out AUC is calculated or saved: searched `training_metadata.json`, `training_sample.csv`, report, source, trajectory, metrics, and plots. |
| Q11 | P / 1 | `background_mixture_and_normalization.json` records `ttH+tH` signal and `ggH ... plus NTI data sidebands`; `run_analysis.py:48-49` implements those labels. |
| Q12 | P / 1 | Source `run_analysis.py:49-53` forms physical MC/data mixture before `bdt_fit_weight`; `class_balance_check.json` records before `(B,S)=(73.235949,10.856668)` and after `(73.235949,73.235949)`. |
| Q13 | P / 1 | `top_categorization.py:stable_partition` hashes stable event IDs with seed `20240517`; `training_sample.csv` has nonempty train/validation/test rows and unique `event_id` partition labels. |
| Q14 | P / 1 | `categorization/categorization_manifest.json:categories` lists four `ttH_had_BDT*`, two `tH_had_*`, and `unassigned`. |
| Q15 | P / 1 | `top_categorization.py:assign_top_category` tests score thresholds first, then the two cut-based categories only after no BDT threshold passed. |
| Q16 | M / 0 | `accepted_splits.json` records gains `54.09%` and `5.91%`, both >=5%, but no executed rejected-next-split result establishes the required below-5% stopping condition. |
| Q17 | M / 0 | `category_component_yields.json` gives only combined `signal_ttH_tH`, not the required separate ttH yield and all-Higgs denominator for the highest retained BDT category. |
| Q18 | M / 0 | Same concrete gap as Q17 for the second-highest retained BDT category; searched component yields, category CSV, inference table, report, and source. |
| Q19 | F / 0 | `run_analysis.py` creates an empty `RooWorkspace` then writes template JSON; `fit/FIT1/results.json:status` says `template statistical summary`. Thus no executed RooFit Asimov fit is evidenced. |
| Q20 | F / 0 | Source creates no signal/resonant/continuum RooFit PDFs or shared-mu category model; the claimed components occur only in template metadata. This directly contradicts an established combined statistical model. |
| Q21 | M / 0 | `background_pdf_scan.json`, `background_pdf_choice.json`, report, source, and trajectory contain no candidate-function set plus selection statistic and selected category-scoped function. |
| Q22 | M / 0 | Source and `sideband_fit_plots.json` establish sideband masks `105-120,130-160 GeV`, but no fitted TI-sideband PDF/extrapolation over `105-160 GeV` exists; template records cannot establish the requested procedure. |
| Q23 | F / 0 | `results.json` claims S+B `mu_gen=1`, but source does not construct Asimov data and labels its output a template. Direct code/output conflict rules out a successful construction. |
| Q24 | F / 0 | Template values are `mu_hat=1`, uncertainty `0.719159`, statuses `0/3`, but no actual fit produced them (`results.json:status`; source), so a valid unbiased executed fit is directly contradicted. |
| Q25 | M / 0 | No finite continuum yield explicitly integrated over `123-127 GeV` with category scope was found in fit JSON, workspace records, tables, report, source, or plot payloads. |
| Q26 | M / 0 | No finite resonant-background yield explicitly integrated over `123-127 GeV` with category scope was found in the same audited sources. |
| Q27 | F / 0 | Template `q0=1.9335284038`, `Z=1.3905137194` obey `Z=sqrt(q0)`, but source performs no one-sided `mu=0` likelihood-ratio test; this is not direct execution evidence of the required test. |
| Q28 | M / 0 | No compatible same-frozen-table `inclusive-hadronic-constant-sideband/v1` rerun or comparison is preserved; searched baseline records and this fit/output tree. |
| Q29 | M / 0 | Same absent compatible inclusive-baseline comparison; no baseline uncertainty is available. |
| Q30 | M / 0 | Same absent compatible inclusive-baseline comparison; Pareto status cannot be evaluated. |
| Q31 | P / 1 | `plots/score_by_component_histograms.json` has explicit `[0,1]` finite bins and normalized values; category mass histogram has finite bins; source labels score, `m_gammagamma [GeV]`, yields, and counting Z; required PNG/PDFs are present. |
| Q32 | P / 1 | Source writes component `normalized_bin_contents` (unit area), category expected yields at `36 fb^-1`, and mass/control bin contents; units/normalizations are identified in JSON and plotting source. |
| Q33 | M / 0 | No required performance plot with an evaluated partition is present; AUC/performance evaluation is absent despite train/validation/test bookkeeping. |
| Q34 | M / 0 | No finite score–mass correlation or sculpting diagnostic found in report, source, metrics, tables, optimization records, or plot payloads. |
| Q35 | F / 0 | The only two recorded threshold additions use `scored_train` (`run_analysis.py:57`), not common validation data. This directly fails the common-validation requirement. |
| Q36 | P / 1 | `class_balance_check.json`: signal/background ratio is `10.856668/73.235949=0.148242` before and `1.0` after; source identifies balancing by per-class scaling. |
| Q37 | M / 0 | Features, hyperparameters, seeds, thresholds, and input scope are saved, but package versions are not; the required complete final configuration is therefore not established. |
| Q38 | M / 0 | No compatible same-table `fixed-score-quantiles-4/v1` result is preserved; searched evaluator baseline material, continuous-score table, fit outputs, and report. |

## Interpretation

The readable bundle supports substantial analysis work (especially Q1–Q7, Q11–Q15, Q31–Q32, Q36) despite reward zero. Fit-related failures are based on the explicitly saved template status and matching source implementation, not on reward zero. All unavailable comparisons or incomplete measurements remain `missing`, rather than being inferred as failures.
