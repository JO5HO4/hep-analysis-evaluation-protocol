# Workflow characterization — Higgs four-lepton

Protocol `workflow-characterization/v1`; generated 2026-09-09. Descriptive evidence only: it does not affect rubric reward, verifier reward, or an outcome grade.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / claude-code / claude-opus-5 / 20260829T171737Z-higgs-4l-signif__qUE9b6C` | completed / 1.000000 | 20 | 0 | 0 | 0 | 1 | 0 | 1 | not established | 2 / 2 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `claude-code / claude-opus-5` |
| Run identifier | `20260829T171737Z-higgs-4l-signif__qUE9b6C` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 20 tool invocations (11 Bash, 4 Read, 4 Edit, 1 Skill) | `agent/claude-code.txt` tool-use records |
| Failed-command count | 0 | all tool results have `is_error:false`; no nonzero exit recorded |
| Distinct error signatures | 0 | complete transcript |
| Analysis iterations | 1 | final `analysis.py`/`results.json`; README and plot-frame edits do not meet the protocol’s analysis-configuration definition |
| Final iteration | 1 | transcript final validation and produced JSON |
| Superseded iterations | 0 | no distinct analysis configuration/result replaced |
| Recovery count | 0 | no error signature followed by same-stage completion |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection | transcript and submitted source |
| Reproducibility attempt | not established | no clean-output rerun or stated tolerance in transcript |
| Artifact coverage | 2 / 2 (`/root/submission`, `/root/results/results.json`) | `artifacts/manifest.json`, both `ok`; log-artifacts directory empty |

### Error signatures and recoveries

No direct error signature is recorded. The recorded μ-plot y-limit correction is not a failed invocation/tool error under this protocol.

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Poisson likelihood, 10^7 toys, μ profile; fixed seed | required fields present; verifier reward 1.0 | q, p, Z, μ interval | final | `submission/analysis.py`; `results/results.json`; final transcript |

The transcript also records a README field-list correction and a y-axis framing correction to the μ plot. Neither changes model family, objective, feature set, hyperparameter, seed, selection rule, category boundary, or fit setting, so neither is a separate analysis iteration.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | 0.586 s | transcript first Bash data/library inspection |
| setup | yes | yes | none | no | not established | transcript plotting-skill and source creation activity |
| inference_or_selection | yes | yes | none | yes | not established | `analysis.py`; produced JSON |
| plotting | yes | yes | none | yes (frame only) | not established | `plots.py`; PNGs; final transcript |
| validation | yes | yes | none | no | not established | final field check; verifier `functional=true` |
| reporting | yes | yes | none | yes (README field list) | not established | README Edit and final file |

Agent execution lasted 429.290428 s, but per-stage durations beyond input inspection are not directly established.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Required result fields | none missing | final transcript Bash `missing: []` |
| README/output fields | all required names present | final transcript `README names all req fields: True` |
| Positive backgrounds | explicit guard | `analysis.py: analyse` |
| Poisson mean / likelihood finiteness | not established | complete source/result/log inventory; no `isfinite` guard |
| Failed interval crossing | not established | `crossing` can return NaN; no validation recorded |
