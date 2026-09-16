# Workflow characterization — Higgs four-lepton significance

Protocol version: `workflow-characterization/v1`  
Generated: 2026-09-09  
Run identifiers: `higgs-4l / codex / gpt-5.6-terra / 20260829T160141Z-higgs-4l-signif__2b7sffY`

This is descriptive, non-scoring workflow evidence. It does not alter the Harbor reward or any task-scientific review result.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / codex / gpt-5.6-terra / 20260829T160141Z-higgs-4l-signif__2b7sffY` | completed / 1.000000 | 13 | 2 | 3 | 2 | 1 | 0 | 1 | rerun from `/tmp/four_lepton_repeat.json`; identical JSON | 6 / 6 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` (`haichenwangberkeley/higgs-4l-significance`) |
| Agent / model | `codex / gpt-5.6-terra` |
| Run identifier | `20260829T160141Z-higgs-4l-signif__2b7sffY` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 13 recorded `exec` tool invocations | `agent/trajectory.json: steps` (13 agent `exec` tool calls) |
| Failed-command count | 2 explicit tool failures | `agent/codex.txt` after items 10 and 11: two policy-rejected `rm`-containing invocations |
| Distinct error signatures | 3 | WebSocket 405 sequence and two distinct tool-policy rejections in `agent/codex.txt` |
| Analysis iterations | 1 | One final numerical configuration was executed; no directly evidenced distinct model/objective/feature/hyperparameter/selection/fit configuration |
| Final iteration | 1: 2M toys, seed 20260829, bounded μ profile | successful execution and final output, `agent/codex.txt` items 8 and 12; `results.json` |
| Superseded iterations | 0 | Repeat run used the same configuration and produced identical JSON; no replaced result configuration is evidenced |
| Recovery count | 2 | HTTPS fallback after WebSocket failure; validation rerun succeeding after command-policy rejection |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection; package/environment management | trajectory steps and `agent/codex.txt` items 2–12 |
| Reproducibility attempt | yes — clean alternate output path `/tmp/four_lepton_repeat.json`; byte-identical JSON | `agent/codex.txt` item 10 |
| Artifact coverage | 6 / 6 required deliverable outputs found; no expected artifact unreadable | `artifacts/manifest.json`; submission README/analyze.py/run.sh, results JSON, two diagnostics |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | setup | `HTTP 405 Method Not Allowed: WebSocket responses endpoint` | 7 connection diagnostics | Log explicitly records fallback to HTTPS; subsequent agent actions and successful run occur | recovered |
| E2 | reporting | `exec_command rejected: rm -f style commands are not permitted` | 1 | No successful cleanup command is recorded; final artifact collection nevertheless completed | not recovered |
| E3 | validation | `exec_command rejected: rm -rf style commands are not permitted` | 1 | Next validation invocation removes the rejected cleanup prefix and completes with `schema/numerical checks passed` | recovered |

`E1` is a transport diagnostic, not a failed agent shell/tool invocation, so it contributes to error signatures and recovery count but not the failed-command count. The two rejected shell/tool invocations are counted as failed commands.

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Final fixed configuration: 2,000,000 b-only toys; seed 20260829; bounded μ fit | schema fields, ordered interval, `n_toys >= 1e6` | final JSON and both plots generated; repeated JSON identical | final | `agent/codex.txt` items 8, 10, 12; `artifacts/root/results/results.json` |

The trajectory records source edits before first execution, but does not directly establish a previously executed distinct analysis configuration; these edits are not counted as superseded analysis iterations.

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | E1 | no | not established | package check at `agent/codex.txt` item 4; transport fallback at log start |
| input_inspection | yes | yes | none | no | not established | `agent/codex.txt` items 2–3 inspect data and establish three channels |
| data_preparation | yes | yes | none | no | not established | `submission/analyze.py:37-61`; source was added in trajectory file-change items |
| inference_or_selection | yes | yes | none | no | not established | 2M-toy likelihood ratio and p-value run, `agent/codex.txt` item 8; `results.json` |
| fit | yes | yes | none | no | not established | bounded μ minimization and crossings, `analyze.py:66-91`; `results.json:8-10` |
| plotting | yes | yes | none | no | not established | generated PNGs listed by `agent/codex.txt` item 8 and preserved under `submission/diagnostics/` |
| validation | yes | yes | E3 | no | not established | successful replacement validation command, `agent/codex.txt` item 12 |
| reporting | yes | yes | E2 | no | not established | final textual result summary, `agent/codex.txt` item 13 |

The manifest establishes whole-agent execution from `2026-08-29T16:03:26.971558Z` to `16:05:12.079883Z` (105.108325 s), but does not allocate durations to individual stages.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| input schema and equal lengths | required arrays nonempty and equal length | `submission/analyze.py:37-51` |
| NaNs / infinities | rejected before analysis | `submission/analyze.py:52-53` |
| invalid weights / Poisson means | no weights are part of this counting task; nonpositive backgrounds rejected and signal constrained nonnegative with one positive entry | `submission/analyze.py:56-60` |
| invalid observed counts | negative/non-integral counts rejected | `submission/analyze.py:54-55` |
| empty categories | empty channel list rejected | `submission/analyze.py:49-51` |
| zero denominators | positive background required before `log(sb/background)` | `submission/analyze.py:56-58,167` |
| invalid fit state / crossings | physical bounded optimizer; upper range expands; endpoint roots bracketed with `brentq` | `submission/analyze.py:66-91` |
| final result schema and numerical ordering | required fields present; `mu_lo < mu_hat < mu_hi`; `n_toys >= 1,000,000` | successful `agent/codex.txt` item 12 |
| reproducibility | rerun to alternate output was byte-identical | successful `agent/codex.txt` item 10 |

