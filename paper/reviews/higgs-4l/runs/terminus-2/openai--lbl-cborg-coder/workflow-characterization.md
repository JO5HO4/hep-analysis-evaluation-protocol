# Workflow characterization — higgs-4l

Protocol: `workflow-characterization/v1`. Generated 2026-09-09. This descriptive profile is separate from rubric rewards, Harbor reward, and any outcome grade.

Run identifiers, ordered: `higgs-4l / terminus-2 / openai/lbl/cborg-coder / 20260902T192401Z-higgs-4l-significance-terminus-2-1410561`.

## 1. Cross-run workflow summary

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `higgs-4l / terminus-2 / openai/lbl/cborg-coder / 20260902T192401Z-higgs-4l-significance-terminus-2-1410561` | completed / 0.700000 | 8 | 0 | 1 | 1 | 1 | 0 | 1 | not established | 6 / 6 |

## 2. Per-run workflow profile

### Run identity

| Field | Value |
|---|---|
| Task | `higgs-4l` |
| Agent / model | `terminus-2 / openai/lbl/cborg-coder` |
| Run identifier | `20260902T192401Z-higgs-4l-significance-terminus-2-1410561` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `completed / 0.700000` |

### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | 8 recorded `bash_command` invocations | `agent/trajectory.json: steps 2–4` (two input/setup commands, four create/run commands, two README/result commands) |
| Failed-command count | 0 | The pane returns to a prompt after each of the eight recorded invocations; no agent shell command has a nonzero status or tool failure. `agent/terminus_2.pane`; `agent/trajectory.json` |
| Distinct error signatures | 1 | `podman cp failed: copying ... extended attributes ... protocol error`, normalized by path/container ID; `job.log`/`trial.log` |
| Analysis iterations | 1 | One submitted analysis configuration was written, executed, and its result printed. `agent/trajectory.json`, `agent/terminus_2.pane` |
| Final iteration | 1 | The sole executed `analysis.py` generated the preserved `results.json`. `agent/terminus_2.pane`; `artifacts/root/results/results.json` |
| Superseded iterations | 0 | No alternate configuration/result is directly evidenced in trajectory, pane, source, results, or logs. |
| Recovery count | 1 | Artifact upload reports the signature then says it retried with tar stream; subsequent trajectory and collected artifacts are present. `job.log`, `trial.log`, artifact inventory |
| Tool categories | shell; source editing; Python/scientific computation; plotting; file inspection | Shell commands inspect input/create files/run program/read result; Python imports NumPy/SciPy/Matplotlib and saves PNGs. `trajectory.json`, `submission/analysis.py` |
| Reproducibility attempt | not established | One execution is recorded. No clean-output rerun or headline comparison appears in pane, trajectory, logs, or artifacts. |
| Artifact coverage | 6 / 6 | Required task outputs found: `run.sh`, `README.md`, `analysis.py`, `results/results.json`, `diagnostics/q_dist.png`, `diagnostics/mu_scan.png`. `artifacts/manifest.json`, bounded inventory |

### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| E1 | `setup` | `podman cp failed: copying ... extended attributes ... protocol error` | 3 | Each logged failure is followed by `retrying upload with tar stream`; the final preserved agent trajectory and full artifact set exist. `job.log`, `trial.log`, `artifacts/` | recovered |

### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | initial and only likelihood/toy/profile configuration | not established | `results.json` with q=−10.5336556567, p=0.999741, μhat=1.6238866986 | final | `agent/terminus_2.pane`; `artifacts/root/results/results.json` |

### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `setup` | yes | yes | E1 | yes | not established | directory creation in `trajectory.json`; artifact recovery in `job.log` |
| `input_inspection` | yes | yes | none | no | not established | `cat /root/data/four_lepton_counts.json` in pane/trajectory |
| `fit` | yes | yes | none | yes | not established | `analysis.py` optimization and executed output in pane |
| `plotting` | yes | yes | none | yes | not established | `analysis.py` saves both PNGs; artifact inventory |
| `reporting` | yes | yes | none | yes | not established | README creation and printed `results.json` in pane/trajectory |

### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| NaNs/infinities | not established; no explicit check | submitted source and transcript searched |
| Invalid Poisson means | not established; no explicit check | submitted source and transcript searched |
| Failed interval crossings | not established; no explicit check | submitted source and transcript searched |
