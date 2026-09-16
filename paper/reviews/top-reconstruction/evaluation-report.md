# Manual top-reconstruction rubric evaluation

Generated 2026-09-09. This is a manual, evidence-backed **non-authoritative** review, not an indexed outcome grade. Harbor status and verifier reward are execution context only.

## Included and excluded evidence

Included logical trials, in stable order: Claude/cborg `tAwiCUD`; Claude/opus `p6Zi8m9`; Claude/sonnet `sw4nasz`; Codex/cborg `6FYNaKM`; Codex/sol `LzgRW3i`; Codex/terra `Nhn5tZT`; OpenHands/sol `DRCvkJN`; OpenHands/terra `qvptHf2`; OpenHands/cborg `cXMdcuS`; Qwen/cborg `nqv9SXY`; Qwen/Best `7vNThUn`; Qwen/Medium `WZoC7Fw`; Terminus/sol `GewouzN`; Terminus/terra `jSysaoA`; Terminus/cborg `wPhYzVM`.

Excluded: `claude-code/claude-opus-5/20260901T004303Z-top-reconstruct__MHMWqxn/` (API-error attempt) and `claude-code/20260902T223106Z-top-reconstruction-full-chain-no-pipeline-claude-code-1356357/` (earlier completed Opus attempt), both superseded by selected Best Opus. Parent results, locks, wrapper/scheduler logs, and retry catalogues are convenience evidence, not trials.

Notation: P/1 pass; F/0 direct contradiction; M/0 missing/incomplete evidence. `R/<ID>/` means the exact selected bundle root under the evidence directory. Every selected run was inspected through `result.json`, `trial.log`, verifier files, readable agent transcript, and `artifacts/root/`.

## Status summary

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Claude/cborg/tAwiCUD | 10 | 1 | 20 | completed/.916667 |
| Claude/opus/p6Zi8m9 | 14 | 1 | 16 | completed/.916667 |
| Claude/sonnet/sw4nasz | 24 | 3 | 4 | completed/.833333 |
| Codex/cborg/6FYNaKM | 7 | 1 | 23 | completed/.896937 |
| Codex/sol/LzgRW3i | 23 | 3 | 5 | completed/.916667 |
| Codex/terra/Nhn5tZT | 23 | 2 | 6 | completed/.916667 |
| OpenHands/sol/DRCvkJN | 1 | 0 | 30 | completed/.000000 |
| OpenHands/terra/qvptHf2 | 1 | 0 | 30 | completed/.000000 |
| OpenHands/cborg/cXMdcuS | 6 | 0 | 25 | completed/.083333 |
| Qwen/cborg/nqv9SXY | 6 | 0 | 25 | completed/.166667 |
| Qwen/Best/7vNThUn | 12 | 0 | 19 | completed/.350805 |
| Qwen/Medium/WZoC7Fw | 12 | 0 | 19 | completed/.833333 |
| Terminus/sol/GewouzN | 23 | 3 | 5 | completed/.916667 |
| Terminus/terra/jSysaoA | 22 | 3 | 6 | completed/.916667 |
| Terminus/cborg/wPhYzVM | 6 | 0 | 25 | completed/.346174 |

## Raw and equal-category rewards

The final column is the arithmetic mean of the nine Group I--IX pass fractions, not an outcome grade.

| Run | Raw total | Equal-category reward |
|---|---:|---:|
| ClC | 10 / 31 | .407 |
| ClO | 14 / 31 | .526 |
| ClS | 24 / 31 | .727 |
| CoC | 7 / 31 | .285 |
| CoS | 23 / 31 | .705 |
| CoT | 23 / 31 | .662 |
| OHS | 1 / 31 | .056 |
| OHT | 1 / 31 | .056 |
| OHC | 6 / 31 | .285 |
| QwC | 6 / 31 | .285 |
| QwB | 12 / 31 | .448 |
| QwM | 12 / 31 | .448 |
| TeS | 23 / 31 | .705 |
| TeT | 22 / 31 | .649 |
| TeC | 6 / 31 | .285 |

## Per-question binary rewards

Columns: ClC, ClO, ClS, CoC, CoS, CoT, OHS, OHT, OHC, QwC, QwB, QwM, TeS, TeT, TeC.

| Criterion | ClC | ClO | ClS | CoC | CoS | CoT | OHS | OHT | OHC | QwC | QwB | QwM | TeS | TeT | TeC |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Q1 timing | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q2 USD cost | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q3 classifier | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q4 features | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| Q5 feature exploration | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q6 splits | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q7 ML setup exploration | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q8 selection method | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q9 selection exploration | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q10 Ntop <=2 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q11 score-mass correlation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q12 no mass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| Q13 pipeline optimization | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q14 score distribution | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| Q15 mass comparison | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| Q16 jet disjointness | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q17 mass bias | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q18 mass resolution | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q19 efficiency | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q20 purity | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q21 fake/true | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q22 F1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q23 accuracy | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q24 balanced accuracy | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q25 Pareto | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| Q26 plot labels | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| Q27 histogram normalization | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q28 plot partition | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| Q29 imbalance | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Q30 reproducible config | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q31 frozen AUC | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Per-criterion observed values, evidence locations, and reasons

| Criteria | Observed value, status/reward, exact inspected source and reason |
|---|---|
| Q1 | P/1 all: finite trial and agent intervals in every `R/<ID>/result.json:{started_at,finished_at,agent_execution}`. |
| Q2 | P/1: ClC $2.395707, ClO $8.845189, ClS $4.071828, CoS $0.809560, CoT $0.598514, TeS $0.589839, TeT $0.280413 in each `result.json:agent_result.cost_usd`. M/0 elsewhere: field null. |
| Q3-Q4 | P cells: `artifacts/root/results/train/training_report_xgb.json:{model_type|model|objective,features|feature_columns}` (and `optimization_summary.json:{classifier_type,feature_set}`) directly show XGBoost/binary training and final features. OHS/OHT lack a task-result tree; OHC/QwC/TeC lack final-feature evidence, so Q4 M. |
| Q5,Q7,Q13 | P cells: named alternatives and common validation outputs in `optimization_summary.json:iterations` or `optimization_report.md`. QwB has one baseline iteration; QwM/QwC/OHC/TeC omit required alternatives, so M. |
| Q6 | P: nonempty `dataset_prepare/{train,val,test}.parquet` plus split/count evidence in training reports. OHS/OHT have no outputs. |
| Q8-Q10,Q16 | P: `select_triplets/selection_report.json` plus opened selected/event Parquet establishes algorithm, max two/event, and no shared jets. OHS/OHT have no selection. |
| Q11 | M/0 all: searched reports, tables, plots, and narrative; no named correlation method, sample, and finite score--mass correlation. |
| Q12 | F/0 where direct final feature lists contain `triplet_mass`/`m123` (ClC, ClO, ClS, CoC, CoS, CoT, TeS, TeT). P/1 QwB/QwM: recorded six angular/mass-ratio features and selection reports show no raw-mass input/window. Others M. |
| Q14-Q15,Q26,Q28 | P: opened `select_triplets/plots/` and companion `selection_report.json`/`inference_report_xgb.json` establish quantity, scope/count, finite value and, where required, test partition. Missing one element gives M; filename alone was never credited. |
| Q17-Q25 | I ran `evaluation/top-reconstruction-baseline/compare.py` to stdout using each compatible saved `dataset_prepare/test.parquet` and `select_triplets/selected_triplets.parquet`. Eligible agent/baseline values (bias GeV; resolution GeV; efficiency; purity; fake/true; F1; accuracy; balanced; Pareto): ClS 7.576/2.050;26.713/24.369;.7649/.4064;.3738/.1679;1.676/4.957;.5021/.2376;.9344/.8872;.8535/.6577;true. CoS 6.128/2.073;20.070/19.743;.7309/.4199;.2848/.1636;2.511/5.111;.4099/.2355;.9124/.8865;.8256/.6633;true. CoT 6.507/1.375;24.416/26.289;.7249/.3905;.2893/.1558;2.457/5.417;.4135/.2228;.9189/.8925;.8259/.6518;true. TeS 8.542/3.584;20.510/18.166;.6949/.4088;.2887/.1698;2.464/4.889;.4079/.2399;.9143/.8900;.8095/.6601;true. TeT 7.271/3.118;22.406/22.057;.7024/.4228;.2840/.1709;2.522/4.851;.4044/.2434;.9139/.8906;.8127/.6668;true. Thus Q17 fails all eligible; Q18 passes only CoT; Q19-Q25 pass all eligible. Other cells M: no compatible labeled candidate input; ClC explicitly lacks `triplet_mass`. |
| Q27 | M/0 all: no inspected source establishes statistical unit for every required histogram. |
| Q29 | P/1 ClS/CoS/TeS: ratio/count and declared handling in `training_report_xgb.json:{class_counts,scale_pos_weight}` or `optimization_report.md`; others omit one requirement. |
| Q30 | M/0 all: partial configurations exist, but none jointly prove feature list, hyperparameters, selection, split/model seed, package versions, and input identifiers. |
| Q31 | M/0 all: frozen classifier comparison needs continuous agent scores on the modulo-10 evaluator partition. `compare.py` records ROC AUC unavailable for saved binary selections; no compatible score record was found. |
