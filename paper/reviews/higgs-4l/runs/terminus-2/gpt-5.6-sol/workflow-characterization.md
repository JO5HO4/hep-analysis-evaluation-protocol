# Workflow characterization — higgs-4l

Protocol version: `workflow-characterization/v1`  
Generation date: 2026-09-09  
Run identifiers: `20260829T173058Z-higgs-4l-significance-terminus-2-1543955`

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / terminus-2 / gpt-5.6-sol / 20260829T173058Z-higgs-4l-significance-terminus-2-1543955` | completed / 1.000000 | 3 | 1 | 1 | 1 | 1 | 0 | 1 | not established | 6 / 6 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` (`haichenwangberkeley/higgs-4l-significance`) |
| Agent / model | `terminus-2 / gpt-5.6-sol` |
| Run identifier | `20260829T173058Z-higgs-4l-significance-terminus-2-1543955` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 1.000000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 3 agent command blocks | `agent/terminus_2.pane`; Harbor `trial.log` send-key records |
| Failed-command count | 1 (`file` unavailable) | final validation block in pane |
| Distinct error signatures | 1 | E1 below |
| Analysis iterations | 1 | one submitted configuration and one executed `results.json` |
| Final iteration | 1 | creation/execution command writes final source and output |
| Superseded iterations | 0 | no earlier produced result is recorded |
| Recovery count | 1 | `find` listing follows failed `file` inspection |
| Tool categories | shell; file inspection; source editing; Python/scientific computation; plotting | pane/source |
| Reproducibility attempt | not established | no clean-location rerun recorded |
| Artifact coverage | 6 / 6: README, launcher, source, results JSON, two diagnostics | inventory and pane `find` output |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | file inspection | `bash: file: command not found` | 1 | Same command block subsequently lists all generated files with `find` | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | initial/final configuration: N=1,000,000, seed 123456789, bounded μ fit | likelihood identities and both profile crossings asserted | all numerical and file checks passed | final | `agent/terminus_2.pane`; `results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| input_inspection | yes | yes | none | no | not established | first pane command prints counts and package versions |
| setup | yes | yes | none | yes | not established | source/launcher/README creation block |
| inference_or_selection | yes | yes | none | yes | not established | execution of `run.sh`; `results.json` |
| plotting | yes | yes | none | no | not established | two diagnostic PNGs listed in pane |
| validation | yes | yes | E1 | no | not established | compile, syntax, numerical assertions, artifact inspection block |
| reporting | yes | yes | none | yes | not established | README and JSON result written |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| input finite/nonnegative counts | validated before analysis | `analyze.py:validate` |
| invalid background/signal means | rejected before analysis | `analyze.py:validate` |
| likelihood identity | passed to `<1e-12` | final pane validation block |
| profile crossings | both passed to `<1e-8` | final pane validation block |
| toy count and evidence boolean | passed | final pane validation block |
| source/launcher syntax | `py_compile` and `bash -n` passed | final pane validation block |
