# Workflow characterization — Higgs → 4ℓ

Protocol: `workflow-characterization/v1`  
Generated: 2026-09-09  
Run identifiers: `20260829T161300Z-higgs-4l-signif__UJQmqEQ`

This is descriptive workflow evidence only. It contributes to neither the
manual rubric reward, Harbor verifier reward, nor an authoritative outcome
grade.

## Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / claude-code / claude-sonnet-5 / 20260829T161300Z-higgs-4l-signif__UJQmqEQ` | completed / 1.000000 | not established | 0 | 0 | 0 | 1 | 0 | 1 | not established | 6 / 6 |

## Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l-significance` |
| Agent / model | `claude-code / claude-sonnet-5` |
| Run identifier | `20260829T161300Z-higgs-4l-signif__UJQmqEQ` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

## Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | not established | The complete readable stream transcript is retained as `agent/claude-code.txt`, but its preserved event form does not provide an evaluator-verifiable normalized invocation count. `num_turns=15` is not substituted for commands. |
| Failed-command count | 0 | `trial.log` ends successfully; trial `result.json: exception_info=null`; transcript terminal result is `completed`; no recorded nonzero/tool-failure event. |
| Distinct error signatures | 0 | Same sources; the source cleanup was a self-review edit, not a recorded failed invocation. |
| Analysis iterations | 1 | One submitted configuration: 5M toys, seed 12345, 400-point profile scan, bounded scalar optimizer. `submission/analysis.py`, `run.sh`, and saved output. |
| Final iteration | 1 | The sole configuration generated `artifacts/root/results/results.json` and the retained diagnostics. |
| Superseded iterations | 0 | No distinct configuration/result replaced before submission is evidenced in transcript, source, or artifacts. |
| Recovery count | 0 | No direct error signature followed by completion of the same stage. |
| Tool categories | shell; source editing; Python/scientific computation; file inspection; plotting | `agent/claude-code.txt`, submitted Python/wrapper, saved JSON and PNGs. |
| Reproducibility attempt | not established | The transcript establishes an execution, but no rerun from a clean output location with a stated agreement tolerance. |
| Artifact coverage | 6 / 6 | Artifact manifest plus retained `run.sh`, `analysis.py`, `README.md`, `results.json`, and two diagnostic PNGs. Expected outputs are all readable; the manifest separately records `/logs/artifacts` as empty. |

## Error signatures and recoveries

No recorded error signatures. The agent narrative mentions removal of an unused
helper during self-review, but it does not describe a failed invocation and is
not counted as an error or recovery.

## Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | initial and final submitted configuration: 5,000,000 toys; seed 12345; profile scan of 400 points | executed output finite; verifier reward 1.0 | p=0.0002576; Z=3.4727; mu_hat=1.6239 on the saved input | final | `submission/analysis.py`, `run.sh`, `artifacts/root/results/results.json`, `verifier/score_report.json` |

## Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | not established | Transcript records reading the supplied counts; saved output preserves channel/count arrays. |
| setup | yes | yes | none | no | 17.854 s environment setup; 9.013 s agent setup | Trial `result.json: environment_setup,agent_setup`. |
| inference_or_selection | yes | yes | none | no | not established (entire agent execution 289.637 s) | `analysis.py` toy generation/test statistic; saved output; `result.json: agent_execution`. |
| fit | yes | yes | none | no | not established (included in agent execution) | `analysis.py: fit_mu`; saved mu outputs. |
| plotting | yes | yes | none | no | not established (included in agent execution) | Both retained PNGs and source plotting calls. |
| reporting | yes | yes | none | no | not established | `README.md`, saved JSON, and final transcript response. |

## Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Positive Poisson means for profile fit | checked; nonpositive means receive a large objective penalty | `submission/analysis.py: neg_logL_mu` |
| Input-array length consistency | checked with assertion | `submission/analysis.py: main` |
| Non-finite likelihoods | not established | No explicit check in the complete retained source/output/log/report set. |
| Failed interval crossings | not established | Source uses `brentq`, but no explicit failure-state check/report is retained. |
| RNG reproducibility | seed fixed to 12345 | `run.sh`; `analysis.py` |

The observed agent execution interval is 289.637 seconds. Individual stage
durations within that interval are not separately recorded, so they are not
inferred from artifact timestamps.
