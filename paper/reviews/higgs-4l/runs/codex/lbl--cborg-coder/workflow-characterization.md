# Workflow characterization — higgs-4l

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Ordered run identifiers: `20260902T192326Z-higgs-4l-significance-codex-1785193/20260902T192326Z-higgs-4l-signif__Mmua7tm`

This is descriptive workflow evidence only. It is not a workflow score, task-rubric reward, Harbor verifier reward, or authoritative outcome grade.

Criterion IDs covered by the paired evidence review: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / Codex / lbl/cborg-coder / 20260902T192326Z-higgs-4l-signif__Mmua7tm` | `completed / 0.950000` | 10 | 0 | 0 | 0 | 2 | 1 | 2 | not established | `6 / 6` |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/higgs-4l-significance` |
| Agent / model | `codex / lbl/cborg-coder` |
| Run identifier | `20260902T192326Z-higgs-4l-significance-codex-1785193/20260902T192326Z-higgs-4l-signif__Mmua7tm` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.950000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 10 | `agent/trajectory.json` steps 4, 6–14: ten `exec_command` invocations; plan updates excluded. |
| Failed-command count | 0 | Each recorded `exec_command` observation in trajectory steps 4, 6–14 has successful completion / exit code 0. |
| Distinct error signatures | 0 | No terminal invocation has nonzero exit or explicit tool failure. Pre-tool transport WebSocket errors in `agent/codex.txt` are not terminal/tool invocations under this protocol. |
| Analysis iterations | 2 | First execution produced `p_value=0.999748` / negative Z; source tail comparison was then changed from `>=` to `<=`, followed by final execution producing `p_value=0.000247`. |
| Final iteration | 2 | `agent/trajectory.json` steps 11–13: tail edit, rerun, and final result readback. |
| Superseded iterations | 1 | Iteration 1 result was read at step 10 then superseded by the tail-convention edit at step 11. |
| Recovery count | 0 | The scientific correction followed a successful command/result, not a failed command or explicit tool failure; no qualifying error signature exists. |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection | Shell commands create/read/edit files and run wrapper; source writes/edit; Python stack executes analysis; code creates PNG plots; `cat` inspects input/result. |
| Reproducibility attempt | not established | Two executions use the same output location after a source correction; no clean-output rerun with a stated agreement tolerance is recorded. |
| Artifact coverage | `6 / 6` | Required deliverables inferred from task prompt: executable `run.sh`, source `analysis.py`, README, result JSON, q diagnostic PNG, profile PNG—all present in `artifacts/root`. No expected output was unreadable. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| — | — | No qualifying terminal/tool error signature established | 0 | not applicable | not established |

`agent/codex.txt` records WebSocket HTTP 405 connection errors before fallback to HTTPS. They are not counted here because the protocol defines command failures from recorded shell/tool invocations; the run proceeded to successful agent commands and Harbor completion.

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial tail rule `q_toys >= q_obs` | p-value / Z | `p=0.999748`, `Z=-3.4786214488` | superseded | `agent/trajectory.json` steps 9–10 |
| 2 | Tail rule corrected to `q_toys <= q_obs` | p-value / Z | `p=0.000247`, `Z=3.4839888865` | final | `agent/trajectory.json` steps 11–13; `artifacts/root/results/results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | command duration `<0.0001 s` | `agent/trajectory.json` step 4 reads the counts JSON. |
| setup | yes | yes | none | no | command duration `<0.0001 s` | trajectory step 6 creates `submission/diagnostics`. |
| unknown | yes | yes | none | yes | not established | trajectory steps 7–8 write `analysis.py` and `run.sh`; code authoring has no dedicated protocol stage. |
| inference_or_selection | yes | yes | none | yes | iteration 1 `1.5196 s`; final iteration `1.1556 s` | trajectory steps 9 and 12 run `run.sh`; step 11 changes tail convention between them. |
| plotting | yes | yes | none | no | included in analysis executions; separate duration not established | `analysis.py` plot calls and both PNGs in `artifacts/root/submission/diagnostics/`. |
| reporting | yes | yes | none | no | command duration `<0.0001 s` | trajectory step 14 writes README; final agent message at step 16 reports results. |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Tail-convention result check | Initial wrong-tail output observed, then corrected and rerun successfully | `agent/trajectory.json` steps 10–13. |
| NaNs/infinities | not established | Searched final source, results JSON, README, trajectory, trial/verifier outputs; no explicit check. |
| Duplicate IDs | not applicable / not established | Counting-input task has no event-ID table; no duplicate-ID check is recorded. |
| Invalid weights | not applicable / not established | Counting-input task has no weights; no such check is recorded. |
| Empty categories | not established | No explicit category-emptiness check in source or execution output. |
| Zero denominators | not established | No explicit denominator validation in source or execution output. |
| Invalid model or fit states | not established | Source clamps nonpositive means and has a root-search safety return, but does not record a validation outcome. |

## Evidence basis and interpretation notes

The terminal transcript is the primary workflow source (`agent/trajectory.json`; corroborated by `agent/codex.txt`). The trial result establishes timing and completion; `artifacts/manifest.json` establishes what was preserved; submitted code and `results.json` distinguish the initial and final analyses. The 10-command count includes only agent shell/tool invocations, not Harbor wrapper commands, messages, plan updates, or verifier execution. The two analysis iterations differ in the statistical tail comparison and both produced an observed result, so the first is a directly evidenced superseded iteration. No reproducibility rerun from a clean output location is preserved.
