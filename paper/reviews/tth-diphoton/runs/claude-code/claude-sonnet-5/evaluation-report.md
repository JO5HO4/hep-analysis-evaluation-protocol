# Manual evidence evaluation — tth-diphoton / Claude Code / claude-sonnet-5

Non-authoritative review under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`. This is review evidence, not an outcome grade. The preserved trial completed with Harbor verifier reward `0.000000`; that context is reported separately and does not erase readable physics evidence.

## Scope and audit

Run: `20260908T203904Z-tth-diphoton-bd__mmgsDbk` (`haichenwangberkeley/tth-diphoton-bdt-categorization`; `claude-code / claude-sonnet-5`). Harbor completion is established by `result.json`; verifier reward is `0.000000` in `verifier/reward.txt` and `verifier/score_report.json`.

The audit opened the result metadata, `trial.log`, `agent/claude-code.txt`, `agent/trajectory.json`, verifier outputs, all submitted Python/YAML source, `report.md`, JSON/CSV results, readable Parquet tables, workspace JSON/ROOT manifest, plot payloads, and PNG/PDF inventory under `artifacts/root/`. Parquet checks established 340,018 selected rows, all three partitions nonempty, and one partition per stable event ID. Missing results below record the searched artifact families; no status follows merely from a preferred filename being absent.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude Code / claude-sonnet-5 | 28 | 4 | 6 | completed / 0.000000 |

## Total reward

| Summary | Claude Code / claude-sonnet-5 |
|---|---:|
| Total reward | 28 / 38 |

## Overall equal-category reward

| Summary | Claude Code / claude-sonnet-5 |
|---|---:|
| Overall equal-category reward | 0.633 |

Category fractions, used only for that normalized summary: Execution/Documentation 2/3; Object/Preselection 4/4; Training 5/6; Categorization 5/5; Workspace/Fit 7/9; Inclusive baseline 0/3; Plotting 2/3; Validation 3/4; Fixed-quantile baseline 0/1.

## Per-question rewards and evidence

| Group | ID | Status | Reward | Observed value and exact evidence/reason |
|---|---|---|---:|---|
| Execution | Q1 | pass | 1 | Wall clock `3,210.169 s` (`result.json: started_at/finished_at`); pure agent execution `3,079.868 s` (`agent_execution` timestamps), both finite. |
| Execution | Q2 | pass | 1 | `$17.4933573 USD`, `result.json:agent_result.cost_usd`. |
| Execution | Q3 | fail | 0 | `results/.../report.md` is readable but contains only Scope, Blinding, BDT, Categorization, RooFit, and Artifacts; it directly lacks required narrative sections such as Introduction, Cut Flow, Systematic Uncertainties, and Summary. |
| Objects | Q4 | pass | 1 | `object_definition_record.json:photon` sets tight-ID and tight-isolation requirements false; TI/NTI retained as bookkeeping. |
| Objects | Q5 | pass | 1 | `preselection_summary.json:overall.hadronic`: 272,376 raw rows; signed MC `0.8732749415 /fb`, hence `31.43789789` at 36/fb; process scope is nominal-Higgs MC plus observed data. |
| Objects | Q6 | pass | 1 | `preselection_summary.json:definitions` and `object_definition_record.json` give photon `pT>25`, acceptance/crack veto/no tight ID/iso; lepton `pT>10`; jet `pT>25`; zero leptons, >=3 jets, >=1 `jet_btag_quantile>=4`. |
| Objects | Q7 | pass | 1 | `preselection_summary.json:by_process` gives raw and signed per-fb weighted hadronic entries separately for VBF, WH, ZH, ggH, ggZH, tH, and ttH (36/fb normalization follows the stated per-fb definition). |
| Training | Q8 | pass | 1 | `model/training_metadata.json` identifies `sklearn.ensemble.GradientBoostingClassifier`; recorded terminal package check in `agent/claude-code.txt` gives `sklearn 1.9.0`. |
| Training | Q9 | fail | 0 | Final list is `[n_jets_central,n_bjets,jet_ht,leading_jet_pt,dijet_mass_leading]` (`training_metadata.json` and source); verifier directly reports `selection_api` BDT_FEATURES mismatch. |
| Training | Q10 | pass | 1 | Held-out test weighted AUC `0.7844370525`, `metrics.json:bdt_weighted_roc_auc_by_partition.test`. |
| Training | Q11 | pass | 1 | `training_metadata.json` identifies `ttH+tH` signal and ggH-TI plus NTI-sideband background. |
| Training | Q12 | pass | 1 | `class_balance_check.json` records pre-balance signal/background sums `0.354425079/41.039346817`, signal factor `115.791317531`, and equal post-balance sums; source keeps classifier weights separate from yields. |
| Training | Q13 | pass | 1 | `preselected_events.parquet` has train/val/test counts 204,368/67,806/67,844; direct table grouping found every stable event ID has partition-nunique `1`; `top_categorization.py:stable_partition` hashes `(seed,event_id)`. |
| Categorization | Q14 | pass | 1 | `categorization_manifest.json:category_order` lists BDT1–BDT4, `tH_had_4j1b`, `tH_had_4j2b`, and `unassigned`. |
| Categorization | Q15 | pass | 1 | `analysis/top_categorization.py:assign_top_category` evaluates BDT labels first, then cut-based tH only after BDT failure. |
| Categorization | Q16 | pass | 1 | `optimization/accepted_splits.json`: accepted gains `44.6105%` and `6.9587%`; rejected next gain `2.26845%`; `thresholds.json` states minimum `0.05`. |
| Categorization | Q17 | pass | 1 | Highest retained BDT1: ttH `1.472244763`; all-Higgs sum `1.544214046`, purity `0.95339`, from `categorization/category_component_yields.json`. |
| Categorization | Q18 | pass | 1 | Second-highest BDT2: ttH `3.042759295`; all-Higgs sum `3.766314092`, purity `0.80789`, same artifact. |
| Workspace/Fit | Q19 | pass | 1 | `workspace_manifest.json` records PyROOT/RooFit workspace and `fit/FIT1`; `significance_asimov_construction.json` records deterministic `mu=1` Asimov construction. |
| Workspace/Fit | Q20 | fail | 0 | `fit/FIT1/backend.json` explicitly says independent per-category fits with `mu_<category>`; `fit/workspace.json` confirms per-category parameters, contradicting shared mu. |
| Workspace/Fit | Q21 | pass | 1 | `background_pdf_choice.json` gives exponential/Chebychev1/Chebychev2 candidates, AIC values, chosen model, and each fitted category. |
| Workspace/Fit | Q22 | pass | 1 | `background_pdf_scan.json` and `report.md` establish TI-data sidebands 105–120 and 130–160 GeV and extrapolation over 105–160 GeV. |
| Workspace/Fit | Q23 | pass | 1 | `backend.json` and `significance_asimov_construction.json` state analytic S+B Asimov construction at `mu=1`. |
| Workspace/Fit | Q24 | fail | 0 | `fit/FIT1/results.json`: BDT2 `mu_hat=0.989631649`, so `abs(mu_hat-1)=0.010368351>0.01`, despite successful statuses/covariance; direct contradiction. |
| Workspace/Fit | Q25 | pass | 1 | `category_yields_36fb.json` gives finite 123–127 GeV NTI continuum proxy yields in four retained categories (1.20860, 8.28083, 12.53041, 0.961679) and states 36/fb/category scope. |
| Workspace/Fit | Q26 | pass | 1 | Same artifact gives finite retained-category resonant yields (0.0682135, 0.702696, 0.901486, 0.0734511) at 36/fb. |
| Workspace/Fit | Q27 | pass | 1 | `significance_asimov.json` and `results.json` give finite per-category q0/Z; e.g. BDT1 `q0=1.884492196`, `Z=1.372768078`, satisfying Z²=q0; combined Z `1.831202450`. |
| Inclusive baseline | Q28 | missing | 0 | Searched saved fit/output tree and evaluator baseline records; no compatible same-frozen-table `inclusive-hadronic-constant-sideband/v1` rerun exists. |
| Inclusive baseline | Q29 | missing | 0 | Same concrete absence: no compatible evaluator-owned baseline mu-uncertainty comparison. |
| Inclusive baseline | Q30 | missing | 0 | Same concrete absence: neither compatible Z nor uncertainty pair exists for a Pareto test. |
| Plotting | Q31 | pass | 1 | Machine-readable `plots/score_by_component_histograms.json`, `categorization/histograms/category_mgg_control_histograms.json`, `fit/FIT1/*plot_payload.json`, plus PNG/PDF inventory establish quantities, GeV/event labels and finite nonempty bins. |
| Plotting | Q32 | pass | 1 | Source `run_pipeline.py:stage_score_shape_plots` and histogram JSON identify BDT shapes as area-normalized and category/fit histograms as expected events or events/bin. |
| Plotting | Q33 | missing | 0 | Searched report, metrics, plot payloads, and source. AUC partitions are recorded, but no required performance plot identifies an evaluated partition. |
| Validation | Q34 | missing | 0 | Searched source, report, metrics, optimization files, all plot payloads, predictions/inference tables; no finite BDT-score versus m-gammagamma correlation or sculpting diagnostic was produced. |
| Validation | Q35 | pass | 1 | `optimization/accepted_splits.json` records three distinct category-boundary configurations on validation data with common expected-significance metric: base, boundary 0.68, then 0.87 (and a rejected 0.95 candidate). |
| Validation | Q36 | pass | 1 | `class_balance_check.json`: pre ratio `0.00863623` (signal/background), post ratio `1.00000000`, with explicit signal scaling treatment. |
| Validation | Q37 | pass | 1 | `config_resolved.yaml`, `training_metadata.json`, `thresholds.json`, `input_data_contract.json`, transcript package checks, and `fit/FIT1/backend.json` together give feature list, hyperparameters, thresholds, seeds 2024/42, versions, and input identifiers. |
| Fixed quantile baseline | Q38 | missing | 0 | Searched evaluator baseline records and saved continuous-score/fit outputs; no same-frozen-table `fixed-score-quantiles-4/v1` result with compatible assumptions exists. |

## Interpretation

The raw manual reward is `28/38`; the equal-category reward is `0.633`. These are non-authoritative review summaries only. The readable artifacts support extensive executed analysis work, while Q3, Q9, Q20, and Q24 are direct failures; Q28–Q30, Q33–Q34, and Q38 remain missing because the requisite comparison or diagnostic was not established.
