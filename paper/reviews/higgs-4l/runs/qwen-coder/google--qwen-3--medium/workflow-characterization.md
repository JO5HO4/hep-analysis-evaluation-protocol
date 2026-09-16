# Workflow characterization — Higgs 4l

Generated 2026-09-09 under `workflow-characterization/v1`. This is descriptive workflow evidence only; it contributes to neither rubric reward, Harbor verifier reward, nor an authoritative outcome grade. The readable trial trajectory, session record, logs, source, result, diagnostics, artifact manifest, and verifier materials were inspected.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / qwen-coder / google--qwen-3--medium / 20260829T163057Z-higgs-4l-significance-qwen-coder-1506981` | completed / 0.750000 | 8 | 0 | 0 | 0 | 1 | 0 | 1 | not established | 2 / 2 declared preserved artifact roots; two diagnostics inside submission |

## Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` (`haichenwangberkeley/higgs-4l-significance`) |
| Agent / model | `qwen-coder / google--qwen-3--medium` |
| Run identifier | `20260829T163057Z-higgs-4l-significance-qwen-coder-1506981` (trial `20260829T163057Z-higgs-4l-signif__fLFVgoS`) |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.750000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 8 recorded shell/tool invocations | `agent/trajectory.json`, steps 2–9: two reads, one shell directory creation, three writes, two shell calls |
| Failed-command count | 0 | Shell calls in steps 3, 7, and 8 record exit code 0; all five file/tool calls report success. |
| Distinct error signatures | 0 | No invocation records a nonzero exit status or explicit tool failure in `trajectory.json`; logs/verifier report no execution exception. |
| Analysis iterations | 1 | One analysis configuration (`analyze.py`) was written and one successful analysis execution produced the saved final `results.json`. |
| Final iteration | 1 | `trajectory.json` step 8 runs the submitted wrapper successfully; step 9 reopens the resulting JSON. |
| Superseded iterations | 0 | No distinct executed analysis configuration/result preceding the final result is evidenced. |
| Recovery count | 0 | No direct error signature is evidenced, hence no same-stage recovery is evidenced. |
| Tool categories | file inspection; source editing; shell; Python/scientific computation; plotting | steps 2–9 show reads/writes/shell calls; step 8 successfully runs Python numerical analysis and produces named diagnostics. |
| Reproducibility attempt | not established | The transcript has one final execution, not a clean-output rerun with a stated numerical comparison tolerance. |
| Artifact coverage | 2 / 2 declared preserved artifact roots; diagnostics present inside submission | `artifacts/manifest.json` records submission directory and results file `ok`; it lists two diagnostic PNGs within preserved `artifacts/root/submission/diagnostics/`. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| not established | not established | no direct error signature | 0 | not applicable | not established |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial complete likelihood/toy/profile configuration | saved numerical output | `q=-10.5336556567`, `p=0.999774`, `mu_hat=1.6238865138` | final | `trajectory.json` steps 4 and 8–9; `artifacts/root/results/results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | 2.291 s to next recorded action | step 2 reads `/root/data/four_lepton_counts.json` |
| setup | yes | yes | none | yes (initial final configuration created) | 38.125 s from step 3 to step 7 | steps 3–7 create directories, source, wrapper, README, and executable permission |
| inference_or_selection | yes | yes | none | no | 36.425 s shared with plotting | step 8 runs `run.sh`; saved result JSON is preserved |
| plotting | yes | yes | none | no | not separately established (inside 36.425 s analysis invocation) | step 8 reports successful run; both diagnostic PNGs are preserved |
| reporting | yes | yes | none | no | 4.595 s from result read to final response | steps 9–10 reopen results and summarize them |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Required result-field inspection | eight required saved result fields displayed | `trajectory.json` step 9 and `artifacts/root/results/results.json` |
| Successful wrapper execution | wrapper exits 0 and reports result output | `trajectory.json` step 8 |
| Diagnostic artifact production | both requested PNG paths exist in preserved submission | `artifacts/root/submission/diagnostics/` and `verifier/score_report.json: diagnostics.files` |
| Invalid Poisson means | source returns `-inf` for `lam<=0`; no execution outcome for invalid input established | `artifacts/root/submission/analyze.py: log_poisson` |

The transcript does not establish checks for duplicate IDs, invalid weights, empty categories, zero denominators, NaNs/infinities, invalid fit states, or interval-crossing validity. Those absent checks are not converted into failed terminal commands or zero-valued workflow quantities.

## Criterion-ID coverage index

Scientific companion-review IDs: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32. Workflow descriptive IDs: W1 Terminal command count, W2 Failed-command count, W3 Distinct error signatures, W4 Analysis iterations/final lineage, W5 Recovery and reproducibility, W6 Artifact coverage.
