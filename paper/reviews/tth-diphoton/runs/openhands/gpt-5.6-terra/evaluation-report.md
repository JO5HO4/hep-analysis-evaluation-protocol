# Manual evidence evaluation: OpenHands / gpt-5.6-terra

Non-authoritative review of `haichenwangberkeley/tth-diphoton-bdt-categorization`, trial `20260902T220657Z-tth-diphoton-bd__E6LHpiw`, under `evaluation/ttH.md` and `evaluation/evaluation_rubric.md`. This is not an outcome grade. Harbor completed with verifier reward `0.000000`.

## Audit scope

Opened the complete preserved bundle: `result.json`, `config.json`, `trial.log`, `lock.json`, `verifier/{ctrf.json,score_report.json,test-stdout.txt,reward.txt}`, `artifacts/manifest.json`, all readable submitted source, the complete `agent/` transcript/events/completions, and the artifact inventory. The inventory contains three submitted-source files and records `/root/results/tth-diphoton-bdt` collection as `failed`; consequently there are no saved result tables, JSON/CSV/Parquet outputs, plots, workspaces, or report to inspect. The trajectory records a source-generation/compile command with exit 0, then `run_analysis.py` timing out repeatedly; `openhands.txt` ends `AgentStuckInLoopError`.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| OpenHands / gpt-5.6-terra | 7 | 4 | 27 | completed / 0.000000 |

| Summary | OpenHands / gpt-5.6-terra |
|---|---:|
| Total reward | 7 / 38 |
| Overall equal-category reward | 0.19 |

`0.19 = (2/3 + 2/4 + 1/6 + 2/5 + 0/9 + 0/3 + 0/3 + 0/4 + 0/1) / 9`.

## Per-criterion evidence

| ID | Status / reward | Observed value and direct evidence |
|---|---|---|
| Q1 | pass / 1 | Wall clock `910.043951 s` (`result.json: started_at, finished_at`); agent execution `781.610226 s` (`agent_execution.started_at, finished_at`). |
| Q2 | pass / 1 | `$0.36829518 USD` (`result.json: agent_result.cost_usd`). |
| Q3 | missing / 0 | No produced `report.md` or narrative: artifact manifest says result-root collection failed; searched all logs, transcript, source, verifier and inventory. |
| Q4 | pass / 1 | Generated source in `agent/openhands.trajectory.json` event 37 selects photons kinematically without tight-ID/isolation; its intended object record says both are not required. This is implementation evidence only. |
| Q5 | missing / 0 | No executed preselection table/summary gives a hadronic raw count and 36-fb^-1 yield. Searched result root inventory, transcript, source and verifier. |
| Q6 | pass / 1 | Event-37 source implements two kinematic photons; lepton `pT>10`; jet `pT>25`; `nlep==0`, `n_jets>=3`, `n_bjets>=1`; saved `top_categorization.py` defines b tags as `jet_btag_quantile >= 4`. |
| Q7 | missing / 0 | No produced process-separated preselection yields; result-root collection failed. |
| Q8 | missing / 0 | Source names `HistGradientBoostingClassifier` and `requirements.txt` names `scikit-learn`, but no package version is recorded. |
| Q9 | fail / 0 | Saved `analysis/top_categorization.py:BDT_FEATURES` is `n_jets,n_central_jets,n_bjets,ht_jets,leading_jet_pt`, not the required `ht_jets,m_all_jets,n_jets,n_central_jets,n_btags`; verifier records the same mismatch. |
| Q10 | missing / 0 | No held-out AUC output; no produced training metadata/table. |
| Q11 | pass / 1 | Event-37 source sets `SIGNAL={'ttH','tH'}` and forms training background from ggH TI-window and NTI data sidebands. |
| Q12 | missing / 0 | Source sketches physical weights and balancing, but no produced before/after class sums establish the requested records. |
| Q13 | missing / 0 | Saved helper hashes stable event IDs into train/validation/test, but no result table establishes nonempty, pairwise-disjoint partitions. |
| Q14 | pass / 1 | Saved `CATEGORY_ORDER` contains the six required hadronic names; `assign_top_category` returns `unassigned`. |
| Q15 | pass / 1 | Saved `assign_top_category` loops BDT thresholds before the two central-jet tH branches. |
| Q16 | missing / 0 | Helper encodes a 5% rule, but no executed thresholds or accepted relative gains exist. |
| Q17 | missing / 0 | No retained-category yields/purity output. |
| Q18 | missing / 0 | No retained-category yields/purity output. |
| Q19 | missing / 0 | No saved RooFit workspace or executed Asimov fit; result-root collection failed. |
| Q20 | fail / 0 | Event-37 source creates a workspace containing only `m` and `mu`; it constructs no per-category `ttH+tH`, fixed resonant, and floating continuum PDF model. |
| Q21 | fail / 0 | Source lists only an `exponential` candidate and supplies no function-selection statistic. |
| Q22 | fail / 0 | Source labels a flat surrogate as a fitted continuum (`polyfit(... ones ...,0)`), rather than performing the required TI-sideband PDF fit/extrapolation. |
| Q23 | missing / 0 | A source intention to write `mu_gen:1` is not direct execution evidence; no Asimov artifact exists. |
| Q24 | missing / 0 | No executed fit result/covariance evidence. |
| Q25 | missing / 0 | No 123–127 GeV continuum yield/category scope output. |
| Q26 | missing / 0 | No 123–127 GeV resonant yield/category scope output. |
| Q27 | missing / 0 | No executed finite `q0`/`Z` pair. |
| Q28 | missing / 0 | No compatible same-frozen-sample inclusive baseline rerun or agent fit output. |
| Q29 | missing / 0 | No compatible same-frozen-sample inclusive baseline rerun or agent fit output. |
| Q30 | missing / 0 | No compatible same-frozen-sample comparison. |
| Q31 | missing / 0 | No required plots or machine-readable finite bins were produced/preserved. |
| Q32 | missing / 0 | No required histogram artifacts establish normalization. |
| Q33 | missing / 0 | No produced performance plot identifies an evaluated partition. |
| Q34 | missing / 0 | No finite score--mass correlation or diagnostic result. |
| Q35 | missing / 0 | Transcript has one generated configuration, not two attempts with a common validation metric. |
| Q36 | missing / 0 | No finite pre-/post-balancing ratios were produced. |
| Q37 | missing / 0 | No final artifact records all configuration fields and input identifiers. |
| Q38 | missing / 0 | No compatible fixed-score-quantiles-4/v1 same-sample comparison. |

All missing judgments follow searches of the enumerated bundle roots, logs, source, reports/tables/plots/workspace inventory, and verifier output; they are not inferred from a preferred filename alone. Verifier reward remains execution context, separate from this evidence review.
