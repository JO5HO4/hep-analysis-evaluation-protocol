# Workflow characterization — higgs-4l

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Run identifiers: `20260829T162334Z-higgs-4l-significance-terminus-2-1496619`

This descriptive profile is separate from the scientific rubric and Harbor verifier reward.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / terminus-2 / gpt-5.6-terra / 20260829T162334Z-higgs-4l-significance-terminus-2-1496619` | completed / 1.000000 | 3 | 0 | 0 | 0 | 2 | 1 | 2 | not established | 6 / 6 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` (`haichenwangberkeley/higgs-4l-significance`) |
| Agent / model | `terminus-2 / gpt-5.6-terra` |
| Run identifier | `20260829T162334Z-higgs-4l-significance-terminus-2-1496619` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 3 agent command blocks | `agent/trajectory.json: steps 2, 3, 4`; `agent/terminus_2.pane` |
| Failed-command count | 0 | All three recorded `bash_command` blocks have successful terminal output; no nonzero agent-shell exit or explicit tool failure is recorded. `trajectory.json`, `terminus_2.pane` |
| Distinct error signatures | 0 | No agent invocation has a recorded error diagnostic. Harness-side Podman copy warnings are not agent shell invocations. `trial.log`, trajectory |
| Analysis iterations | 2 | Initial run used `(N_extreme+1)/(N_toys+1)`; subsequent source edit changed it to `N_extreme/N_toys` and reran. `trajectory.json: steps 2 and 4`; pane |
| Final iteration | 2 | Final edit/rerun produced preserved `results.json` with p=0.000212. `trajectory.json: step 4`; `results.json` |
| Superseded iterations | 1 | The initial execution reported p=0.000212999787000213; the later direct-fraction configuration replaced it. `trajectory.json: steps 2 and 4` |
| Recovery count | 0 | No direct error signature followed by a same-stage completion. |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection | Terminal commands create/edit source, execute Python analysis, inspect JSON/files, and source generates PNGs. pane/source |
| Reproducibility attempt | not established | The final analysis was rerun after a configuration change, not from a clean output location; no clean-location agreement test is recorded. trajectory |
| Artifact coverage | 6 / 6: README, launcher, source, results JSON, two diagnostics | `artifacts/manifest.json`; bundle inventory |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | No agent shell/tool failure recorded | 0 | not applicable | not established |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial p-value convention: `(N_extreme+1)/(N_toys+1)` | JSON result and diagnostic-file listing | p=0.000212999787000213; Z=3.5234300215 | superseded | `trajectory.json: step 2 observation`; pane |
| 2 | Replaced p-value with direct `N_extreme/N_toys`; added 3σ boolean and asymmetric uncertainties | JSON pretty-print, executable test, diagnostic listing | p=0.000212; Z=3.5246766534; final output preserved | final | `trajectory.json: step 4`; `results.json`; pane |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none | yes | not established | Initial creation of `analyze.py`, `run.sh`, README, and output directories in trajectory step 2 |
| inference_or_selection | yes | yes | none | yes | not established | `run.sh` execution in steps 2 and 4; final `results.json` |
| plotting | yes | yes | none | no | not established | Both analysis executions generate diagnostics; final files listed in trajectory step 4 and preserved |
| validation | yes | yes | none | yes | not established | Step 3 prints initial JSON/files; step 4 pretty-prints final JSON and tests executable/listing |
| reporting | yes | yes | none | yes | not established | README and final results JSON written by source in steps 2/4 |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| equal-length, nonempty input arrays | rejected when invalid | `artifacts/root/submission/analyze.py:main` |
| nonnegative integral observed counts | rejected when invalid | `analyze.py:main` |
| positive background / nonnegative signal | rejected when invalid | `analyze.py:main` |
| final JSON validity | `python3 -m json.tool` succeeded | `agent/trajectory.json: step 4 observation`; pane |
| executable launcher | `test -x` reported `run.sh is executable` | trajectory step 4; pane |
| required diagnostics | both files listed after final run | trajectory step 4; `artifacts/root/submission/diagnostics/` |

No NaN/infinity-specific validation, duplicate-ID test, invalid-weight test, empty-category test, zero-denominator test, or explicit fit-crossing failure check is directly evidenced. This is a characterization of recorded workflow, not an inferred failure count or scientific score.
