# Top-reconstruction artifact-copy audit

This is an evaluator-owned recovery audit, not a physics score. It uses only the declared bounded retained-results tree. A result, plot, or report is never treated as proof of uncopied source behavior.

## Summary

- Runs inspected: 18 (top-reconstruction-paper-version=18).
- Direct copied final source: 0.
- Source recoverable from already copied transcripts: 15.
- Execution evidence without recoverable code: 3.
- Genuinely absent evidence: 0.

## Per-run findings

### top-reconstruction-paper-version / 20260902T223106Z-top-reconstruct__zuYpFe4 — claude-code / claude-opus-5

- Retained evidence root: `results/paper/top-reconstruction-paper-version/claude-code/20260902T223106Z-top-reconstruction-full-chain-no-pipeline-claude-code-1356357/20260902T223106Z-top-reconstruct__zuYpFe4`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=29, agent_session_trajectory_logs=6, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=18.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/model_xgb_member0.json, artifacts/root/results/train/model_xgb_member1.json, artifacts/root/results/train/model_xgb_member2.json, artifacts/root/results/train/model_xgb_member3.json, artifacts/root/results/train/model_xgb_member4.json, artifacts/root/results/train/model_xgb_member5.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/efficiency_vs_njet.csv, artifacts/root/results/select_triplets/plots/score_and_efficiency.png, artifacts/root/results/select_triplets/plots/selected_kinematics.png, artifacts/root/results/select_triplets/plots/selected_kinematics_summary.csv, artifacts/root/results/select_triplets/plots/selected_mass_comparison.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/claude-code.txt, agent/sessions/projects/-root/7307cd9a-5550-46da-ab3a-85bcbcc40dd5.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/tmp/diag.py, /tmp/diag2.py, /tmp/diag3.py, /tmp/it1.py, /tmp/it2.py, /tmp/it3.py, /tmp/it4.py, /tmp/runcfg.py, pipeline/build_dataset.py, pipeline/run_final.py, pipeline/write_reports.py`.
- Runtime source not copied as a workspace artifact: `/tmp/diag.py, /tmp/diag2.py, /tmp/diag3.py, /tmp/it1.py, /tmp/it2.py, /tmp/it3.py, /tmp/it4.py, /tmp/runcfg.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260901T004303Z-top-reconstruct__MHMWqxn — claude-code / unknown

- Retained evidence root: `results/paper/top-reconstruction-paper-version/claude-code/claude-opus-5/20260901T004303Z-top-reconstruct__MHMWqxn`
- Execution status / Harbor reward: `completed` / `None`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=5, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/claude-code.txt, agent/sessions/projects/-root/0d16c711-abb4-4a0e-8a4a-56b97b29daca.jsonl`.
- Executed script paths seen directly in transcripts: `run_pipeline.py`.
- Runtime source not copied as a workspace artifact: `run_pipeline.py`.
- Incomplete-copy signatures: preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260904T230352Z-top-reconstruct__p6Zi8m9 — claude-code / claude-opus-5

- Retained evidence root: `results/paper/top-reconstruction-paper-version/claude-code/claude-opus-5/20260904T230352Z-top-reconstruction-full-chain-no-pipeline-claude-code-463496/20260904T230352Z-top-reconstruct__p6Zi8m9`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=27, agent_session_trajectory_logs=6, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=15.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_it1_binary.json, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_it1_binary.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_sanity_check.png, artifacts/root/results/select_triplets/plots/mass_summary_table.csv, artifacts/root/results/select_triplets/plots/performance.png, artifacts/root/results/select_triplets/plots/selected_kinematics.png, artifacts/root/results/select_triplets/plots/selected_kinematics_table.csv, artifacts/root/results/select_triplets/plots/selected_mass_and_score.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/claude-code.txt, agent/sessions/projects/-root/07edf820-e3d6-40ed-b934-3976c03916e7.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `build_dataset.py, cv.py, cv2.py, cv3.py, drv.py, infer.py, plots_and_checks.py, prepare.py, select.py, select_triplets.py, sweep.py, train.py`.
- Runtime source not copied as a workspace artifact: `drv.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260829T211123Z-top-reconstruct__sw4nasz — claude-code / claude-sonnet-5

- Retained evidence root: `results/paper/top-reconstruction-paper-version/claude-code/claude-sonnet-5/20260829T211123Z-top-reconstruct__sw4nasz`
- Execution status / Harbor reward: `completed` / `0.833333`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=24, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=0, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/_last_run.log, artifacts/root/results/select_triplets/_val_threshold_scan.json, artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/score_and_multiplicity.png, artifacts/root/results/select_triplets/plots/selected_kinematics.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/claude-code.txt, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `scripts/01_build_dataset.py, scripts/02_prepare_dataset.py, scripts/03_train.py, scripts/04_infer.py, scripts/05_select.py, scripts/06_finalize_selection.py, scripts/07_sanity_checks.py, scripts/08_selection_plots.py`.
- Runtime source not copied as a workspace artifact: `scripts/01_build_dataset.py, scripts/02_prepare_dataset.py, scripts/03_train.py, scripts/04_infer.py, scripts/05_select.py, scripts/06_finalize_selection.py, scripts/07_sanity_checks.py, scripts/08_selection_plots.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260902T201601Z-top-reconstruct__tAwiCUD — claude-code / cborg-coder

- Retained evidence root: `results/paper/top-reconstruction-paper-version/claude-code/lbl--cborg-coder/20260902T201601Z-top-reconstruct__tAwiCUD`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=17, agent_session_trajectory_logs=6, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=10.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_dist.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/claude-code.txt, agent/sessions/projects/-root/7514514b-f561-4af5-b07d-a3e4d02b041e.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `build_dataset.py, build_optimization_report.py, prepare_dataset.py, run_inference.py, sanity_check.py, select_triplets.py, train_xgb.py`.
- Runtime source not copied as a workspace artifact: `build_dataset.py, build_optimization_report.py, prepare_dataset.py, run_inference.py, sanity_check.py, select_triplets.py, train_xgb.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260831T230056Z-top-reconstruct__LzgRW3i — codex / gpt-5.6-sol

- Retained evidence root: `results/paper/top-reconstruction-paper-version/codex/gpt-5.6-sol/20260831T230056Z-top-reconstruct__LzgRW3i`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=21, agent_session_trajectory_logs=2, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=12.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_comparison.png, artifacts/root/results/select_triplets/plots/multiplicity_table.csv, artifacts/root/results/select_triplets/plots/selected_kinematics.png, artifacts/root/results/select_triplets/plots/selected_multiplicity.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/08/31/rollout-2026-08-31T23-02-14-01a05a0f-1b34-7411-8a0e-2deb865e9f86.jsonl, trial.log`.
- Executed script paths seen directly in transcripts: `/root/build_top_pipeline.py`.
- Runtime source not copied as a workspace artifact: `/root/build_top_pipeline.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260829T202756Z-top-reconstruct__Nhn5tZT — codex / gpt-5.6-terra

- Retained evidence root: `results/paper/top-reconstruction-paper-version/codex/gpt-5.6-terra/20260829T202756Z-top-reconstruct__Nhn5tZT`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=17, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=10.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_comparison.png, artifacts/root/results/select_triplets/plots/selected_pt.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/08/29/rollout-2026-08-29T20-29-36-01a04f36-a55e-7341-9967-58108f4ce769.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `build_top_pipeline.py, finalize_selection.py`.
- Runtime source not copied as a workspace artifact: `build_top_pipeline.py, finalize_selection.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260902T205040Z-top-reconstruct__6FYNaKM — codex / cborg-coder

- Retained evidence root: `results/paper/top-reconstruction-paper-version/codex/lbl--cborg-coder/20260902T205040Z-top-reconstruct__6FYNaKM`
- Execution status / Harbor reward: `completed` / `0.896937`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=15, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_dist.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/09/02/rollout-2026-09-02T20-51-46-01a063e4-60ae-72f2-989e-a5c591c2784d.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `dataset_build.py, dataset_prepare.py, final_pipeline.py, inference.py, sanity_check.py, select_triplets.py, train_model.py`.
- Runtime source not copied as a workspace artifact: `dataset_build.py, dataset_prepare.py, final_pipeline.py, inference.py, run_final.py, sanity_check.py, select_triplets.py, train_model.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260831T235352Z-top-reconstruct__DRCvkJN — openhands / gpt-5.6-sol

- Retained evidence root: `results/paper/top-reconstruction-paper-version/openhands/gpt-5.6-sol/20260831T235352Z-top-reconstruct__DRCvkJN`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **execution_without_recoverable_code**; classification: **Harbor_artifact_collection_gap**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=11, terminal_recordings=0, native_tool_call_telemetry=7, copied_workspace_source=0, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `app.py`.
- Runtime source not copied as a workspace artifact: `app.py`.
- Incomplete-copy signatures: preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Record the command only. Future collection should copy files created or modified outside results/**, with a manifest.

### top-reconstruction-paper-version / 20260905T023203Z-top-reconstruct__vQ8QaVm — openhands / gpt-5.6-sol

- Retained evidence root: `results/paper/top-reconstruction-paper-version/openhands/gpt-5.6-sol/20260905T023203Z-top-reconstruction-full-chain-no-pipeline-openhands-566489/20260905T023203Z-top-reconstruct__vQ8QaVm`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **execution_without_recoverable_code**; classification: **Harbor_artifact_collection_gap**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=11, terminal_recordings=0, native_tool_call_telemetry=7, copied_workspace_source=0, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `app.py`.
- Runtime source not copied as a workspace artifact: `app.py`.
- Incomplete-copy signatures: preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Record the command only. Future collection should copy files created or modified outside results/**, with a manifest.

### top-reconstruction-paper-version / 20260829T215720Z-top-reconstruct__qvptHf2 — openhands / gpt-5.6-terra

- Retained evidence root: `results/paper/top-reconstruction-paper-version/openhands/gpt-5.6-terra/20260829T215720Z-top-reconstruct__qvptHf2`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **execution_without_recoverable_code**; classification: **Harbor_artifact_collection_gap**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=11, terminal_recordings=0, native_tool_call_telemetry=7, copied_workspace_source=0, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `app.py`.
- Runtime source not copied as a workspace artifact: `app.py`.
- Incomplete-copy signatures: preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Record the command only. Future collection should copy files created or modified outside results/**, with a manifest.

### top-reconstruction-paper-version / 20260902T201605Z-top-reconstruct__cXMdcuS — openhands / lbl/cborg-coder

- Retained evidence root: `results/paper/top-reconstruction-paper-version/openhands/openai--lbl-cborg-coder/20260902T201605Z-top-reconstruct__cXMdcuS`
- Execution status / Harbor reward: `completed` / `0.083333`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=17, agent_session_trajectory_logs=200, terminal_recordings=0, native_tool_call_telemetry=278, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_distribution.png, artifacts/root/results/select_triplets/plots/pt_distribution.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selected_triplets_with_truth.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/completions/openai__lbl__cborg-coder-1788380333.5247052.json, agent/completions/openai__lbl__cborg-coder-1788380337.6914732.json, agent/completions/openai__lbl__cborg-coder-1788380340.4186485.json, agent/completions/openai__lbl__cborg-coder-1788380355.1440842.json, agent/completions/openai__lbl__cborg-coder-1788380357.730706.json, agent/completions/openai__lbl__cborg-coder-1788380363.0268757.json, agent/completions/openai__lbl__cborg-coder-1788380365.4826596.json, agent/completions/openai__lbl__cborg-coder-1788380371.8218758.json, agent/completions/openai__lbl__cborg-coder-1788380373.9608877.json, agent/completions/openai__lbl__cborg-coder-1788380377.6907046.json, agent/completions/openai__lbl__cborg-coder-1788380380.3261774.json, agent/completions/openai__lbl__cborg-coder-1788380384.0400589.json, agent/completions/openai__lbl__cborg-coder-1788380386.1061232.json, agent/completions/openai__lbl__cborg-coder-1788380390.5986805.json, agent/completions/openai__lbl__cborg-coder-1788380398.4754615.json, agent/completions/openai__lbl__cborg-coder-1788380402.611954.json, agent/completions/openai__lbl__cborg-coder-1788380405.2728074.json, agent/completions/openai__lbl__cborg-coder-1788380432.8345299.json, agent/completions/openai__lbl__cborg-coder-1788380437.3521535.json, agent/completions/openai__lbl__cborg-coder-1788380456.3221374.json, agent/completions/openai__lbl__cborg-coder-1788380461.0073311.json, agent/completions/openai__lbl__cborg-coder-1788380463.6284058.json, agent/completions/openai__lbl__cborg-coder-1788380466.6628108.json, agent/completions/openai__lbl__cborg-coder-1788380475.9740665.json, agent/completions/openai__lbl__cborg-coder-1788380487.056739.json, agent/completions/openai__lbl__cborg-coder-1788380492.0349474.json, agent/completions/openai__lbl__cborg-coder-1788380495.555412.json, agent/completions/openai__lbl__cborg-coder-1788380499.7134457.json, agent/completions/openai__lbl__cborg-coder-1788380502.829418.json, agent/completions/openai__lbl__cborg-coder-1788380508.5152733.json, agent/completions/openai__lbl__cborg-coder-1788380511.0650947.json, agent/completions/openai__lbl__cborg-coder-1788380518.3280532.json, agent/completions/openai__lbl__cborg-coder-1788380520.987458.json, agent/completions/openai__lbl__cborg-coder-1788380532.3935125.json, agent/completions/openai__lbl__cborg-coder-1788380536.1922832.json, agent/completions/openai__lbl__cborg-coder-1788380543.9591987.json, agent/completions/openai__lbl__cborg-coder-1788380558.6044433.json, agent/completions/openai__lbl__cborg-coder-1788380563.1390176.json, agent/completions/openai__lbl__cborg-coder-1788380567.1436236.json, agent/completions/openai__lbl__cborg-coder-1788380572.8405738.json, agent/completions/openai__lbl__cborg-coder-1788380576.0779307.json, agent/completions/openai__lbl__cborg-coder-1788380583.8215122.json, agent/completions/openai__lbl__cborg-coder-1788380586.9965255.json, agent/completions/openai__lbl__cborg-coder-1788380592.2717123.json, agent/completions/openai__lbl__cborg-coder-1788380594.860696.json, agent/completions/openai__lbl__cborg-coder-1788380602.8257408.json, agent/completions/openai__lbl__cborg-coder-1788380612.7138014.json, agent/completions/openai__lbl__cborg-coder-1788380626.2258236.json, agent/completions/openai__lbl__cborg-coder-1788380629.1781445.json, agent/completions/openai__lbl__cborg-coder-1788380638.7366567.json, agent/completions/openai__lbl__cborg-coder-1788380651.9292572.json, agent/completions/openai__lbl__cborg-coder-1788380660.9601068.json, agent/completions/openai__lbl__cborg-coder-1788380701.4906552.json, agent/completions/openai__lbl__cborg-coder-1788380707.8959374.json, agent/completions/openai__lbl__cborg-coder-1788380722.0060384.json, agent/completions/openai__lbl__cborg-coder-1788380727.5862489.json, agent/completions/openai__lbl__cborg-coder-1788380748.4968188.json, agent/completions/openai__lbl__cborg-coder-1788380765.5955691.json, agent/completions/openai__lbl__cborg-coder-1788380792.4088771.json, agent/completions/openai__lbl__cborg-coder-1788380808.4340465.json, agent/completions/openai__lbl__cborg-coder-1788380864.9938042.json, agent/completions/openai__lbl__cborg-coder-1788380883.8591769.json, agent/completions/openai__lbl__cborg-coder-1788380902.5494726.json, agent/completions/openai__lbl__cborg-coder-1788380930.3570554.json, agent/completions/openai__lbl__cborg-coder-1788380993.965764.json, agent/completions/openai__lbl__cborg-coder-1788381053.2523386.json, agent/completions/openai__lbl__cborg-coder-1788381063.7941477.json, agent/completions/openai__lbl__cborg-coder-1788381086.5099819.json, agent/completions/openai__lbl__cborg-coder-1788381123.9853046.json, agent/completions/openai__lbl__cborg-coder-1788381157.2663827.json, agent/completions/openai__lbl__cborg-coder-1788381166.0776482.json, agent/completions/openai__lbl__cborg-coder-1788381186.880836.json, agent/completions/openai__lbl__cborg-coder-1788381214.0818403.json, agent/openhands.trajectory.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/100-125.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/125-150.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/150-175.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/25-50.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/50-75.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/event_cache/75-100.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/113.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/114.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/118.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/141.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/142.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/145.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/146.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/148.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/157.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/158.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/160.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/161.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/162.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/166.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/169.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/170.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/171.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/172.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/174.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/175.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/176.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/177.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/178.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/179.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/180.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/41.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/42.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/71.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/72.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/74.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/89.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/90.json, agent/sessions/bc8c15cc-528c-42-c1794f20615c702/events/94.json, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `app.py`.
- Runtime source not copied as a workspace artifact: `/root/dataset_builder.py, /root/dataset_prepare.py, /root/debug_len.py, /root/inference.py, /root/inspect_tree.py, /root/plot_results.py, /root/sanity_check.py, /root/select_triplets.py, /root/train_model.py, /root/write_select.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260831T233834Z-top-reconstruct__7vNThUn — qwen-coder / qwen-3

- Retained evidence root: `results/paper/top-reconstruction-paper-version/qwen-coder/google--qwen-3--best/20260831T233834Z-top-reconstruct__7vNThUn`
- Execution status / Harbor reward: `completed` / `0.350805`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=21, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/feature_importance.png, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/roc_curve.png, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/n_selected_per_event.png, artifacts/root/results/select_triplets/plots/score_distribution.png, artifacts/root/results/select_triplets/plots/triplet_mass_distribution.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/bc566cd4-9786-450b-8b4e-6f1416028406.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/mass_sanity_check.py, /root/process_ttbar.py, /root/run_inference.py, /root/select_candidates.py, /root/train_classifier.py`.
- Runtime source not copied as a workspace artifact: `/root/mass_sanity_check.py, /root/process_ttbar.py, /root/run_inference.py, /root/select_candidates.py, /root/train_classifier.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260829T214149Z-top-reconstruct__WZoC7Fw — qwen-coder / qwen-3

- Retained evidence root: `results/paper/top-reconstruction-paper-version/qwen-coder/google--qwen-3--medium/20260829T214149Z-top-reconstruct__WZoC7Fw`
- Execution status / Harbor reward: `completed` / `0.833333`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=18, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/n_top_per_event.png, artifacts/root/results/select_triplets/plots/score_distribution.png, artifacts/root/results/select_triplets/plots/triplet_mass_distribution.png, artifacts/root/results/select_triplets/plots/triplet_pt_distribution.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/0e91a4ba-7397-423e-b7b3-9565a0421bd1.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/plot_results.py, /root/prepare_dataset.py, /root/process_triplets.py, /root/run_inference.py, /root/sanity_check.py, /root/select_triplets.py, /root/train_classifier.py`.
- Runtime source not copied as a workspace artifact: `/root/plot_results.py, /root/prepare_dataset.py, /root/process_triplets.py, /root/run_inference.py, /root/sanity_check.py, /root/select_triplets.py, /root/train_classifier.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260902T205011Z-top-reconstruct__nqv9SXY — qwen-coder / cborg-coder

- Retained evidence root: `results/paper/top-reconstruction-paper-version/qwen-coder/lbl--cborg-coder/20260902T205011Z-top-reconstruct__nqv9SXY`
- Execution status / Harbor reward: `completed` / `0.166667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=15, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_sanity.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/05740667-49b2-4ebe-b8ec-91b7d711fac1.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/build_dataset.py, /root/inference_selection.py, /root/optimize_pipeline.py, /root/sanity_checks.py, /root/train_model.py`.
- Runtime source not copied as a workspace artifact: `/root/build_dataset.py, /root/inference_selection.py, /root/optimize_pipeline.py, /root/sanity_checks.py, /root/train_model.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260831T232319Z-top-reconstruct__GewouzN — terminus-2 / gpt-5.6-sol

- Retained evidence root: `results/paper/top-reconstruction-paper-version/terminus-2/gpt-5.6-sol/20260831T232319Z-top-reconstruct__GewouzN`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=18, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=0, model_report_metadata=10.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_comparison.png, artifacts/root/results/select_triplets/plots/selected_kinematics.png, artifacts/root/results/select_triplets/plots/selected_mass_histogram.csv, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/build_pipeline.py`.
- Runtime source not copied as a workspace artifact: `/root/build_pipeline.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260829T211053Z-top-reconstruct__jSysaoA — terminus-2 / gpt-5.6-terra

- Retained evidence root: `results/paper/top-reconstruction-paper-version/terminus-2/gpt-5.6-terra/20260829T211053Z-top-reconstruct__jSysaoA`
- Execution status / Harbor reward: `completed` / `0.916667`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=18, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=0, model_report_metadata=12.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_variant_comparison.json, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/selected_pt.png, artifacts/root/results/select_triplets/plots/triplet_mass_comparison.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/model_variants.py, /root/run_top_pipeline.py`.
- Runtime source not copied as a workspace artifact: `/root/model_variants.py, /root/run_top_pipeline.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

### top-reconstruction-paper-version / 20260902T201608Z-top-reconstruct__wPhYzVM — terminus-2 / lbl/cborg-coder

- Retained evidence root: `results/paper/top-reconstruction-paper-version/terminus-2/openai--lbl-cborg-coder/20260902T201608Z-top-reconstruct__wPhYzVM`
- Execution status / Harbor reward: `completed` / `0.346174`
- Source state: **recoverable_from_transcript**; classification: **evaluator_adapter_gap**.
- Inventory counts: final_output_artifacts=14, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=0, model_report_metadata=11.
- Final training/model paths: `artifacts/root/results/dataset_prepare/train.parquet, artifacts/root/results/train/model_xgb.json, artifacts/root/results/train/training_report_xgb.json`.
- Final selection paths: `artifacts/root/results/select_triplets/event_selection.parquet, artifacts/root/results/select_triplets/plots/mass_sanity_check.png, artifacts/root/results/select_triplets/selected_triplets.parquet, artifacts/root/results/select_triplets/selection_report.json`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `build_raw_dataset.py, inspect_root.py, prepare_dataset.py, run_inference.py, sanity_check.py, select_triplets.py, train_model.py`.
- Runtime source not copied as a workspace artifact: `build_raw_dataset.py, inspect_root.py, prepare_dataset.py, run_inference.py, sanity_check.py, select_triplets.py, train_model.py`.
- Incomplete-copy signatures: final training/model or selection outputs exist while no source file was copied outside results/**; preserved transcript executes a .py path that is absent from copied workspace/source directories.
- Smallest safe recovery rule: Parse shell heredocs/redirections and native write or patch payloads into reviewer-generated recovered-source files; do not execute them.

## Prioritized collector fixes

1. **Copy the final created/modified workspace source outside `results/**`, plus a file manifest.** This is the strongest fix. It can directly support the eight currently evidence-limited question families: final features (Q4), extra features (Q5), tried ML setups (Q7), final selection algorithm (Q8), selection comparisons (Q9), mass usage/window (Q12), optimization attempts (Q13), and reproducibility (Q30). Those account for 82 not-established cells in the current 15-run pilot matrix.
2. **Preserve file-writing tool inputs and terminal input bytes in one normalized telemetry record.** This unlocks adapter recovery for transcript-backed runs without requiring a solver submission format. It addresses the same eight question families where source was written through a tool call, patch, or heredoc but not copied as a file.
3. **For every executed `python PATH.py`, emit a collector manifest with PATH and either its final content or an explicit unavailable marker.** This closes the execution-without-source signature and makes absent code distinguishable from an adapter limitation.
4. **On failed or incomplete runs, retain the workspace snapshot and complete session stream through the final tool action.** This is most important for the three OpenHands runs that show `app.py` execution but no final results or recoverable source; it cannot manufacture missing physics evidence, but it can separate collection loss from a genuinely incomplete run.

The JSON companion contains the full path inventory for each run and is the machine-readable input for future adapters.
