# Workflow characterization: ttH diphoton BDT categorization

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Run identifiers covered (ordered): `20260904T210145Z-tth-diphoton-bd__MqqLxno`

This is descriptive workflow evidence only. It is not a workflow score, task-rubric reward, Harbor verifier reward, or authoritative outcome grade.

Rubric-coverage cross-reference: the companion `evaluation-report.md` independently evaluates every selected ttH criterion. This descriptive profile covers the same preserved run and explicitly cross-references `Q1`, `Q2`, `Q3`, `Q4`, `Q5`, `Q6`, `Q7`, `Q8`, `Q9`, `Q10`, `Q11`, `Q12`, `Q13`, `Q14`, `Q15`, `Q16`, `Q17`, `Q18`, `Q19`, `Q20`, `Q21`, `Q22`, `Q23`, `Q24`, `Q25`, `Q26`, `Q27`, `Q28`, `Q29`, `Q30`, `Q31`, `Q32`, `Q33`, `Q34`, `Q35`, `Q36`, `Q37`, and `Q38`; it assigns no rubric status or reward to them.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `tth-diphoton / Claude Code / lbl/cborg-coder / 20260904T210145Z-tth-diphoton-bd__MqqLxno` | `completed / 0.000000` | 7 | 1 | 1 | 0 | 0 | 0 | not established | not established | `0 / 2` preserved requested task artifact roots |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `haichenwangberkeley/tth-diphoton-bdt-categorization` |
| Agent / model | `claude-code / lbl/cborg-coder` |
| Run identifier | `20260904T210145Z-tth-diphoton-bd__MqqLxno` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 7 | `agent/claude-code.txt`: seven `Bash` tool-use records (target directory listing; `/root` listing; three broad file searches; submission listing; environment-variable read). |
| Failed-command count | 1 | `agent/claude-code.txt`: `ls -R /root/submission/tth-diphoton-bdt` explicitly returned exit code 2. The three search invocations expose incomplete-access diagnostics, but no nonzero exit status or explicit tool failure; they are not counted. |
| Distinct error signatures | 1 | `agent/claude-code.txt`: E1 below. |
| Analysis iterations | 0 | The seven commands only inspect the absent pipeline and environment; no distinct analysis configuration or produced result is evidenced. |
| Final iteration | not established | No analysis iteration generated a submitted final result. |
| Superseded iterations | 0 | No produced analysis result was subsequently replaced in the transcript. |
| Recovery count | 0 | The absent-source error was not followed by completion of the same input-inspection stage. |
| Tool categories | `shell`; `file inspection` | All recorded invocations are Bash listings/searches or `echo $TB_HYY_INPUTS`; no source editing, scientific computation, ROOT/RooFit, plotting, or package action is recorded. |
| Reproducibility attempt | not established | No clean-output rerun or stated agreement tolerance exists. |
| Artifact coverage | `0 / 2` preserved requested task artifact roots | `artifacts/manifest.json`: `/root/submission/tth-diphoton-bdt` and `/root/results/tth-diphoton-bdt` each have status `failed`. Expected but unavailable task outputs include submission source, results/tables, plots, workspace, and report. The third listed source, `/logs/artifacts`, is empty and is not a task output. |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `input_inspection` | `ls: cannot access '/root/submission/tth-diphoton-bdt': No such file or directory` | 1 | None; subsequent `/root` and `/root/submission` listings show the parent exists but is empty, and the final response requests the missing pipeline. | not recovered |

The transcript also records that global search commands encountered inaccessible system directories. Their individual command exit statuses are not exposed as nonzero and no diagnostic is a task-pipeline error, so they are not additional failed-command or error-signature counts.

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| No directly evidenced analysis iterations | not established | not established | No analysis result was produced | not established | `agent/claude-code.txt`; `agent/trajectory.json: final_metrics` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `input_inspection` | yes | no | E1 | no | `103.684 s` from first recorded target-directory invocation (21:03:06.962Z) to final response (21:04:50.646Z) | `agent/claude-code.txt` timestamps; final response reports the supplied pipeline absent. |

No other workflow stage is listed because the evidence does not identify actions for it. The available total pure agent-execution duration is `124.641067 s` (`result.json: agent_execution`); it is not assigned across unobserved stages.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Source-pipeline existence | failed: `/root/submission/tth-diphoton-bdt` absent; parent submission directory empty | `agent/claude-code.txt` target listing (exit 2), `/root` listing, and `/root/submission` listing. |
| Results-root availability | failed: `/root/results` listed empty | `agent/claude-code.txt` `/root` listing. |
| Input mount declaration | present but not analyzed: `TB_HYY_INPUTS=/data/GamGam` | `agent/claude-code.txt` environment-variable read; `result.json: config.agent.env`. |
| NaNs/infinities, duplicate IDs, invalid weights, empty categories, zero denominators, invalid model states, invalid fit states | not established | No source, data table, model, category, or fit execution was produced; inventory and verifier records contain none. |

## Supporting execution context

`result.json` records agent execution from `2026-09-04T21:02:46.151355Z` to `2026-09-04T21:04:50.792422Z`, total cost `$1.032273 USD`, and no Harbor `exception_info`. The trial nevertheless had verifier reward `0.000000`. `verifier/ctrf.json` and `verifier/score_report.json` report six failed verifier checks: missing submission module, preselected-events table, input-data contract, training metadata, and run manifest. These are execution/artifact facts, not judgments of workflow quality.
