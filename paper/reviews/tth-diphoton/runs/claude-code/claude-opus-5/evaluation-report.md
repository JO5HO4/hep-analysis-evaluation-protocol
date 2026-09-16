# Manual evidence evaluation — tth-diphoton / Claude Code / claude-opus-5

Non-authoritative review under `evaluation/ttH.md` and the shared evidence policy in `evaluation/evaluation_rubric.md`, generated 2026-09-09. This is review evidence, not an indexed evaluation-spec result or an outcome grade.

## Scope and audit

| Field | Value |
|---|---|
| Task / run | `haichenwangberkeley/tth-diphoton-bdt-categorization` / `20260908T234508Z-tth-diphoton-bd__UezeyUP` |
| Agent / model | `claude-code / claude-opus-5` |
| Harbor execution context | completed; verifier reward `0.000000` |
| Timing / cost | wall `2414.846 s` (result timestamps), pure agent `2270.757 s`; `$9.96238625 USD` |
| Rubric result | 30 pass, 1 fail, 7 missing; raw `30 / 38` |
| Equal-category reward | `(2/3 + 4/4 + 5/6 + 5/5 + 9/9 + 0/3 + 3/3 + 2/4 + 0/1) / 9 = 0.666667` |

The readable artifact root contained 84 files. The audit opened `result.json`, `trial.log`, `verifier/score_report.json`, `artifacts/manifest.json`, submitted Python source, `report.md`, all readable JSON/CSV tables and manifests, 61/61 listed required outputs, RooFit `workspace.root` plus JSON export, and PNG/PDF plots with their JSON payloads. The saved source establishes implementation; machine-readable outputs establish produced numerical results. The `result.json` timestamps establish both timing quantities (trial 23:46:37.813018–00:26:52.659137 UTC; agent 23:46:58.515222–00:24:48.272528 UTC).

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / claude-opus-5 | 30 | 1 | 7 | completed / 0.000000 |

| Summary | Claude Code / claude-opus-5 |
|---|---:|
| Total reward | 30 / 38 |
| Overall equal-category reward | 0.666667 |

## Criterion evidence

| ID | Status / reward | Observed value and direct evidence |
|---|---|---|
| Q1 | pass / 1 | Trial wall `2414.846119 s`; agent execution `2270.757306 s`, from `result.json.started_at`, `finished_at`, and `agent_execution.*`. |
| Q2 | pass / 1 | `$9.96238625 USD`, `result.json.agent_result.cost_usd`. |
| Q3 | pass / 1 | Readable end-to-end narrative in `artifacts/root/results/tth-diphoton-bdt/report.md` covers inputs, selection, training, categories, fit, plots, validation, and artifacts. |
| Q4 | pass / 1 | `preselection_summary.json.definitions.photon_selection`: both tight-ID and isolation required=false; TI/NTI used only as controls. |
| Q5 | pass / 1 | Hadronic: `80,585` raw and `25.942352 @36 fb^-1`, `preselection_summary.json.hadronic`; scope includes selected MC plus observed data as separately recorded. |
| Q6 | pass / 1 | `preselection_summary.json.definitions`: photons `pT>25`, `|eta|<2.37` crack veto and relative-pT cuts, no tight ID/isolation; leptons `pT>10`; jets `pT>25`; hadronic `n_leptons=0,n_jets>=3,n_bjets>=1`; b tag `jet_btag_quantile>=4`. |
| Q7 | pass / 1 | Process-separated post-hadronic values exist in `preselection_summary.json.by_process.*.hadronic`, e.g. ttH `49,347 / 17.250857`, tH `6,541 / 0.132819`, ggH `2,147 / 6.876405` (raw / 36 fb^-1). |
| Q8 | pass / 1 | `model/training_metadata.json.model`: scikit-learn `HistGradientBoostingClassifier`; package version is recorded by `run_manifest.json` environment/package inventory. |
| Q9 | fail / 0 | Saved final feature list is `(n_jets_central,n_bjets,ht_jets,met,pt_gg)` and excludes mass, but direct verifier contradiction: `verifier/score_report.json.selection_api.errors` says `BDT_FEATURES mismatch` with that list. |
| Q10 | pass / 1 | Held-out weighted test AUC `0.8382538607`, `model/training_metadata.json.performance.weighted_auc_test`. |
| Q11 | pass / 1 | `training_metadata.json.signal_class` is ttH+tH; `background_class` is ggH TI MC plus NTI observed-data sidebands. |
| Q12 | pass / 1 | Physical SM-normalized mixture precedes balancing; before sums S/B `9.846832/53.673389`, after `31.760110/31.760110`, in `training_metadata.json.class_balance` and report. |
| Q13 | pass / 1 | Nonempty stable-ID BLAKE2b partitions train/val/test `75,175/25,045/25,161`, order-independent, seed `20240917`; verifier provenance reports `event_ids_single_partition=true` (`preselection_summary.json.partition`, `score_report.json`). |
| Q14 | pass / 1 | `categorization_manifest.json`/report declares `ttH_had_BDT1..BDT4`, `tH_had_4j1b`, `tH_had_4j2b`, and `unassigned`; low-yield categories are then dropped into unassigned. |
| Q15 | pass / 1 | `categorization.py` and report: BDT categories precede cut categories; `tH_had_4j1b/4j2b` evaluated only after BDT failure. |
| Q16 | pass / 1 | `optimization/accepted_splits.json`: accepted gains `8.442%` and `6.779%` after initial split; proposed fourth gain `0.9%` rejected; final thresholds `[0.88,0.73,0.36]`. |
| Q17 | pass / 1 | Highest retained BDT1: ttH+tH `1.483397`, all-Higgs signal+resonant `1.797635`, ratio `0.82520`; component table in `metrics.json.categorization.per_category` (positive denominator). |
| Q18 | pass / 1 | Second-highest BDT2: ttH+tH `2.198607`, all-Higgs `2.791403`, ratio `0.78764`; same table. |
| Q19 | pass / 1 | Executed ROOT/PyROOT/RooFit workspace and S+B Asimov fit: `workspace_manifest.json`, `fit/workspace.json`, `fit/FIT1/workspace.root`, `fit/FIT1/results.json`. |
| Q20 | pass / 1 | `significance_asimov_construction.json.strategy` and workspace manifest: shared mu times ttH+tH, fixed non-top-Higgs resonant term, floating continuum in four retained hadronic categories. |
| Q21 | pass / 1 | `background_pdf_scan.json`: exponential, power-law, expo_poly1, bernstein2; minimum AIC selection; selected exponential BDT1 and power-law BDT2/BDT3/4j1b. |
| Q22 | pass / 1 | TI observed sidebands `[105,120]` and `[130,160]`, extrapolated over `[105,160]`, recorded in `significance_asimov_construction.json` and `background_pdf_scan.json`. |
| Q23 | pass / 1 | `fit/FIT1/results.json.mu_gen=1` and saved `significance_asimov_construction.json` establish S+B construction. |
| Q24 | pass / 1 | `mu_hat=1.00006036`, uncertainty `0.70861300`, free/mu0 fit statuses `0/0`, covariance qualities `3/3`, `fit/FIT1/results.json`. |
| Q25 | pass / 1 | Continuum `22.079806` events in 123–127 GeV at 36 fb^-1, summed over workspace categories BDT1/2/3 and 4j1b from bins `[123,127)` in `significance_asimov_plot_payload.json.fitted_continuum`; bin edges and 36-fb construction are explicit there and in construction JSON. |
| Q26 | pass / 1 | Resonant background `2.700248` events in 123–127 GeV at 36 fb^-1, same four-category scope and bins in `significance_asimov_plot_payload.json.fitted_resonant`. |
| Q27 | pass / 1 | `q0=2.8347732348`, `Z=1.6836784832`; `Z^2-q0` is numerical roundoff, in `fit/FIT1/significance.json`; one-sided construction is documented in `significance_asimov_construction.json`. |
| Q28 | missing / 0 | No compatible evaluator-owned inclusive-baseline rerun on the same frozen table. Searched complete saved fit/output tree and repository baseline records; agent `Z=1.683678` alone is not comparable. |
| Q29 | missing / 0 | No same-sample compatible inclusive baseline provides reference `mu_uncertainty`; searched baseline records and complete fit/output tree. |
| Q30 | missing / 0 | Cannot establish both inclusive-baseline comparisons or Pareto relation; same searched sources as Q28–Q29. |
| Q31 | pass / 1 | Plot payloads directly specify finite arrays, quantities and units: 55 bins `m_yy` in GeV (`significance_asimov_plot_payload.json`), 20 score bins `[0,1]` (`plots/score_by_component_histograms.json`), and 36-fb yields (`categorization/histograms/*.json`); corresponding PNG/PDF outputs exist. |
| Q32 | pass / 1 | Histogram metadata/labels identify normalized score shapes, observed event counts, and 36-fb expected yields; see `score_by_component_histograms.json`, `category_mgg_control_histograms.json`, and plotting source. |
| Q33 | pass / 1 | Performance AUC fields identify train/val/test (`training_metadata.json.performance`); report says optimization uses expected yields and validation partition is `val`; plot payloads state their hadronic/category scope. |
| Q34 | missing / 0 | Search of report, metrics, training/optimization JSON, plot payloads and submitted source found only mass exclusion/sculpting intent, no finite evaluated score–mass correlation or diagnostic result. |
| Q35 | missing / 0 | Four threshold trials are documented, but no two distinct model/feature/categorization attempts with a common validation metric are recorded; searched report, metadata, accepted splits, source and trajectory. |
| Q36 | pass / 1 | Pre/post S:B weight ratios `0.1834583550 -> 1.0`, with balancing treatment, `metrics.json.bdt.class_balance_*` and `class_balance_check.json`. |
| Q37 | pass / 1 | Final features, hyperparameters, thresholds, split/model seed `20240917`, ROOT `6.38.00`, package inventory and input contract identifiers are in `training_metadata.json`, `metrics.json`, `thresholds.json`, `run_manifest.json`, and `input_data_contract.json`. |
| Q38 | missing / 0 | No evaluator-owned `fixed-score-quantiles-4/v1` same-table fit/reference exists. Searched repository baseline records and all saved score/fit/output artifacts; agent `Z=1.683678` alone cannot answer comparison. |

The verifier’s zero reward is preserved as execution context. Its direct contract findings explain Q9’s fail but do not erase independently readable numerical artifacts. Missing comparison and validation criteria remain missing rather than being inferred from filenames, prose, or verifier reward.
