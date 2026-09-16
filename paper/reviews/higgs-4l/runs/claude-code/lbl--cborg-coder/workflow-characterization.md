# Workflow characterization — higgs-4l

Protocol: `workflow-characterization/v1`. Generated: 2026-09-09. Run identifiers covered, in order: `higgs-4l / claude-code / lbl/cborg-coder / 20260902T192326Z-higgs-4l-signif__GJtrrcd`.

This is descriptive workflow evidence only; it contributes to neither the task rubric, the Harbor verifier reward, nor an outcome grade.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / claude-code / lbl/cborg-coder / 20260902T192326Z-higgs-4l-signif__GJtrrcd` | completed / 0.950000 | 5 | 0 | 0 | 0 | 1 | 0 | 1 | not established | 6 / 6 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `claude-code / lbl/cborg-coder` |
| Run identifier | `20260902T192326Z-higgs-4l-signif__GJtrrcd` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.950000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 5 recorded Bash invocations | `agent/claude-code.txt`: cat input; mkdir; Python import check; chmod+run; cat results |
| Failed-command count | 0 | The five Bash tool results are successful (`is_error:false`); the analysis invocation exited successfully. Its SyntaxWarnings were warnings, not a tool failure. |
| Distinct error signatures | 0 | No nonzero exit or explicit tool failure in `agent/claude-code.txt`. |
| Analysis iterations | 1 | One written `analysis.py` configuration, followed by one run producing the submitted `results.json`; no later changed configuration is recorded. |
| Final iteration | 1 | `agent/claude-code.txt`: `run.sh /root/data/four_lepton_counts.json /root/results/results.json`, then `cat` of the saved final result. |
| Superseded iterations | 0 | No earlier result-producing configuration or replaced result is recorded. |
| Recovery count | 0 | No error signature exists to be followed by completion of the same stage. |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection; package/environment management | Bash, Write, and successful NumPy/SciPy/Matplotlib import check in transcript; `analysis.py` produces both PNGs. |
| Reproducibility attempt | not established | The transcript has one run only; no clean-output rerun or tolerance comparison is recorded. |
| Artifact coverage | 6 / 6 | Present/readable required task outputs: `run.sh`, `analysis.py`, `README.md`, `results/results.json`, `diagnostics/q_distribution.png`, `diagnostics/mu_scan.png`. No unavailable/unreadable expected outputs identified. |

### Error signatures and recoveries

No data rows: no recorded invocation has a nonzero exit status or explicit tool failure. The Python execution emitted several `SyntaxWarning: invalid escape sequence` messages, but the tool result is `is_error:false`, the run completed, and the required plots/results were produced; under the protocol this is not a failed command or error signature.

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | Initial complete implementation: Poisson likelihood, 1e6 toys, mu scan, plots | Successful execution; saved numerical result | logL_b=-11.0827503203, p=0.000276, Z=3.4541647741, muhat=1.6239239239 | final | `agent/claude-code.txt` execution and result readback; `artifacts/root/results/results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| setup | yes | yes | none | no | 26.7 s from directory creation at 19:25:02.207Z through dependency check completion at 19:25:28.886Z | `agent/claude-code.txt` |
| input_inspection | yes | yes | none | no | 0.065 s recorded for `cat /root/data/four_lepton_counts.json` (19:24:49.003Z–19:24:49.068Z) | `agent/claude-code.txt` |
| fit | yes | yes | none | yes | 1.747 s recorded for analysis invocation (19:27:02.561Z–19:27:04.308Z); it generates likelihood/toy/profile results | `agent/claude-code.txt`; `artifacts/root/results/results.json` |
| plotting | yes | yes | none | no | included in the successful 1.747 s analysis invocation | `analysis.py:166-190`; two readable diagnostic PNGs |
| reporting | yes | yes | none | no | 22.040 s from README write request 19:27:28.275Z to final response 19:27:50.315Z (includes final narration) | `agent/claude-code.txt` |

The harness-level agent execution duration is separately established as 203.154581 s (`trial result.json: agent_execution`); it is not apportioned among stages beyond the directly timed transcript events.

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| Python package availability | NumPy, SciPy, and Matplotlib imports succeeded | `agent/claude-code.txt`: `python3 -c ...`, stdout `Imports successful` |
| Output-result readback | Saved JSON was read and contains eight finite headline fields | `agent/claude-code.txt`: `cat /root/results/results.json`; preserved `artifacts/root/results/results.json` |
| NaNs/infinities | not established | No explicit check in transcript or `analysis.py` |
| Duplicate IDs | not established | Counting-input task; no explicit duplicate-ID check in transcript or source |
| Invalid weights | not established | No weights are used and no explicit validation check is recorded |
| Empty categories / zero denominators | not established | No explicit check in transcript or source |
| Invalid model or fit states | not established | `analysis.py` has no non-finite/invalid-mean validation; its lower-crossing fallback sets zero rather than validating/reporting failure |
