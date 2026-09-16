# Artifact-copy audit for all retained paper results

This is an evaluator-owned recovery audit, not a physics score. It uses only the declared bounded retained-results tree. A result, plot, or report is never treated as proof of uncopied source behavior.

## Summary

- Runs inspected: 48 (higgs-4l-significance-paper-version=15, top-reconstruction-paper-version=18, tth-diphoton-bdt-categorization-paper-version=15).
- Direct copied final source: 26.
- Source recoverable from already copied transcripts: 15.
- Execution evidence without recoverable code: 6.
- Genuinely absent evidence: 1.

## Per-run findings

### higgs-4l-significance-paper-version / 20260829T171737Z-higgs-4l-signif__qUE9b6C — claude-code / claude-opus-5

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/claude-code/claude-opus-5/20260829T171737Z-higgs-4l-significance-claude-code-1534712/20260829T171737Z-higgs-4l-signif__qUE9b6C`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=0, copied_workspace_source=3, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/plots.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/claude-code.txt, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T161300Z-higgs-4l-signif__UJQmqEQ — claude-code / claude-sonnet-5

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/claude-code/claude-sonnet-5/20260829T161300Z-higgs-4l-significance-claude-code-1487708/20260829T161300Z-higgs-4l-signif__UJQmqEQ`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=0, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260902T192326Z-higgs-4l-signif__GJtrrcd — claude-code / cborg-coder

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/claude-code/lbl--cborg-coder/20260902T192326Z-higgs-4l-significance-claude-code-1370864/20260902T192326Z-higgs-4l-signif__GJtrrcd`
- Execution status / Harbor reward: `completed` / `0.95`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=6, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `/root/submission/analysis.py, analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T170234Z-higgs-4l-signif__G4rVSn2 — codex / gpt-5.6-sol

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/codex/gpt-5.6-sol/20260829T170234Z-higgs-4l-significance-codex-1524332/20260829T170234Z-higgs-4l-signif__G4rVSn2`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/08/29/rollout-2026-08-29T17-04-36-01a04e7a-f4bf-7441-9698-d1a132e714a6.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `none`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T160141Z-higgs-4l-signif__2b7sffY — codex / gpt-5.6-terra

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/codex/gpt-5.6-terra/20260829T160141Z-higgs-4l-significance-codex-1477637/20260829T160141Z-higgs-4l-signif__2b7sffY`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analyze.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/08/29/rollout-2026-08-29T16-03-41-01a04e43-3231-7f90-91e2-65d32a16e981.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `none`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260902T192326Z-higgs-4l-signif__Mmua7tm — codex / cborg-coder

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/codex/lbl--cborg-coder/20260902T192326Z-higgs-4l-significance-codex-1785193/20260902T192326Z-higgs-4l-signif__Mmua7tm`
- Execution status / Harbor reward: `completed` / `0.95`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/09/02/rollout-2026-09-02T19-24-33-01a06394-88a4-7883-990d-bc936c3f63f9.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `/root/submission/analysis.py, analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T174904Z-higgs-4l-signif__V5CzXRE — openhands / gpt-5.6-sol

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/openhands/gpt-5.6-sol/20260829T174904Z-higgs-4l-significance-openhands-1563552/20260829T174904Z-higgs-4l-signif__V5CzXRE`
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

### higgs-4l-significance-paper-version / 20260829T164001Z-higgs-4l-signif__CqRrCvf — openhands / gpt-5.6-terra

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/openhands/gpt-5.6-terra/20260829T164001Z-higgs-4l-significance-openhands-1515494/20260829T164001Z-higgs-4l-signif__CqRrCvf`
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

### higgs-4l-significance-paper-version / 20260902T201549Z-higgs-4l-signif__hJL9JqC — openhands / lbl/cborg-coder

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/openhands/openai--lbl-cborg-coder/20260902T201549Z-higgs-4l-significance-openhands-1286844/20260902T201549Z-higgs-4l-signif__hJL9JqC`
- Execution status / Harbor reward: `completed` / `0.95`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=84, terminal_recordings=0, native_tool_call_telemetry=110, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/completions/openai__lbl__cborg-coder-1788380392.1162794.json, agent/completions/openai__lbl__cborg-coder-1788380400.403381.json, agent/completions/openai__lbl__cborg-coder-1788380403.4228106.json, agent/completions/openai__lbl__cborg-coder-1788380406.8962562.json, agent/completions/openai__lbl__cborg-coder-1788380415.1544724.json, agent/openhands.trajectory.json, agent/sessions/ef06bef0-6979-4a-dabaddfb174bc54/event_cache/50-75.json, agent/sessions/ef06bef0-6979-4a-dabaddfb174bc54/events/65.json, agent/sessions/ef06bef0-6979-4a-dabaddfb174bc54/events/66.json, agent/sessions/ef06bef0-6979-4a-dabaddfb174bc54/events/67.json, agent/sessions/ef06bef0-6979-4a-dabaddfb174bc54/events/68.json, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `analysis.py, app.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T173916Z-higgs-4l-signif__eNaET5b — qwen-coder / qwen-3

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/qwen-coder/google--qwen-3--best/20260829T173916Z-higgs-4l-significance-qwen-coder-1554570/20260829T173916Z-higgs-4l-signif__eNaET5b`
- Execution status / Harbor reward: `completed` / `0.5875`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=3, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/plot_diagnostics.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/25a6cee7-e3ca-4655-b6ad-61e69a02ed3f.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/analysis.py, /root/submission/plot_diagnostics.py, analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T163057Z-higgs-4l-signif__fLFVgoS — qwen-coder / qwen-3

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/qwen-coder/google--qwen-3--medium/20260829T163057Z-higgs-4l-significance-qwen-coder-1506981/20260829T163057Z-higgs-4l-signif__fLFVgoS`
- Execution status / Harbor reward: `completed` / `0.75`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analyze.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/675f6484-b944-477b-a537-6599cdca96ff.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/analyze.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260902T192318Z-higgs-4l-signif__D2WKKsA — qwen-coder / cborg-coder

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/qwen-coder/lbl--cborg-coder/20260902T192318Z-higgs-4l-significance-qwen-coder-1513207/20260902T192318Z-higgs-4l-signif__D2WKKsA`
- Execution status / Harbor reward: `completed` / `0.6875`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/run.sh, artifacts/root/submission/run_analysis.py`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/8cea31c7-5512-42cf-bd37-dbbdd23456c1.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/run_analysis.py, run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T173058Z-higgs-4l-signif__b52MA8E — terminus-2 / gpt-5.6-sol

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/terminus-2/gpt-5.6-sol/20260829T173058Z-higgs-4l-significance-terminus-2-1543955/20260829T173058Z-higgs-4l-signif__b52MA8E`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analyze.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `none`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260829T162334Z-higgs-4l-signif__zfxzMpw — terminus-2 / gpt-5.6-terra

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/terminus-2/gpt-5.6-terra/20260829T162334Z-higgs-4l-significance-terminus-2-1496619/20260829T162334Z-higgs-4l-signif__zfxzMpw`
- Execution status / Harbor reward: `completed` / `1.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analyze.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `none`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### higgs-4l-significance-paper-version / 20260902T192401Z-higgs-4l-signif__VjiGH5o — terminus-2 / lbl/cborg-coder

- Retained evidence root: `results/paper/higgs-4l-significance-paper-version/terminus-2/openai--lbl-cborg-coder/20260902T192401Z-higgs-4l-significance-terminus-2-1410561/20260902T192401Z-higgs-4l-signif__VjiGH5o`
- Execution status / Harbor reward: `completed` / `0.7`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=1, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/analysis.py, artifacts/root/submission/run.sh`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/analysis.py, analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

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

### tth-diphoton-bdt-categorization-paper-version / 20260908T234508Z-tth-diphoton-bd__UezeyUP — claude-code / claude-opus-5

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/claude-code/claude-opus-5/20260908T234508Z-tth-diphoton-bdt-categorization-claude-code-2290597/20260908T234508Z-tth-diphoton-bd__UezeyUP`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=73, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=0, copied_workspace_source=11, model_report_metadata=18.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/bdt_model.pkl, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/bdt.py, artifacts/root/submission/tth-diphoton-bdt/analysis/categorization.py, artifacts/root/submission/tth-diphoton-bdt/analysis/common.py, artifacts/root/submission/tth-diphoton-bdt/analysis/fitting.py, artifacts/root/submission/tth-diphoton-bdt/analysis/inputs.py, artifacts/root/submission/tth-diphoton-bdt/analysis/plotting.py, artifacts/root/submission/tth-diphoton-bdt/analysis/preselection.py, artifacts/root/submission/tth-diphoton-bdt/analysis/report.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/run_analysis.py`.
- Transcript evidence paths: `agent/claude-code.txt, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `rt.py, run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260908T203904Z-tth-diphoton-bd__mmgsDbk — claude-code / claude-sonnet-5

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/claude-code/claude-sonnet-5/20260908T203904Z-tth-diphoton-bdt-categorization-claude-code-1272923/20260908T203904Z-tth-diphoton-bd__mmgsDbk`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=62, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=0, copied_workspace_source=5, model_report_metadata=16.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/bdt_model.joblib, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.parquet`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.parquet, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/data_io.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/analysis/workspace.py, artifacts/root/submission/tth-diphoton-bdt/run_pipeline.py`.
- Transcript evidence paths: `agent/claude-code.txt, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `run_pipeline.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260904T210145Z-tth-diphoton-bd__MqqLxno — claude-code / cborg-coder

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/claude-code/lbl--cborg-coder/20260904T210145Z-tth-diphoton-bdt-categorization-claude-code-461040/20260904T210145Z-tth-diphoton-bd__MqqLxno`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **genuinely_absent_evidence**; classification: **genuinely_absent_evidence**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=7, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=0, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `none`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `none`.
- Runtime source not copied as a workspace artifact: ``.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: No safe recovery rule: retain the explicit missing-evidence record.

### tth-diphoton-bdt-categorization-paper-version / 20260905T022547Z-tth-diphoton-bd__MPttiyG — codex / gpt-5.6-sol

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/codex/gpt-5.6-sol/20260905T022547Z-tth-diphoton-bdt-categorization-codex-711347/20260905T022547Z-tth-diphoton-bd__MPttiyG`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=73, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=3, model_report_metadata=16.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/bdt_model.pkl, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/run_analysis.py`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/09/05/rollout-2026-09-05T02-26-58-01a06f63-fbd1-7063-bb50-0f9d763e745a.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260902T213233Z-tth-diphoton-bd__zWiAt8N — codex / gpt-5.6-terra

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/codex/gpt-5.6-terra/20260902T213233Z-tth-diphoton-bdt-categorization-codex-1340268/20260902T213233Z-tth-diphoton-bd__zWiAt8N`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=76, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=15.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/run_analysis.py`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/09/02/rollout-2026-09-02T21-33-50-01a0640a-e452-7552-9e00-bccf77d67060.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260902T032120Z-tth-diphoton-bd__CwT2jxX — codex / cborg-coder

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/codex/lbl--cborg-coder/20260902T032120Z-tth-diphoton-bdt-categorization-codex-1361431/20260902T032120Z-tth-diphoton-bd__CwT2jxX`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=36, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=6, model_report_metadata=8.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/preselection.py, artifacts/root/submission/tth-diphoton-bdt/run_pipeline.py, artifacts/root/submission/tth-diphoton-bdt/utils/bdt_utils.py, artifacts/root/submission/tth-diphoton-bdt/utils/data_utils.py, artifacts/root/submission/tth-diphoton-bdt/utils/stats_utils.py`.
- Transcript evidence paths: `agent/codex.txt, agent/sessions/2026/09/02/rollout-2026-09-02T03-22-07-01a06023-66bd-7240-b05f-b5a91b46cfb0.jsonl, agent/trajectory.json, trial.log`.
- Executed script paths seen directly in transcripts: `run_pipeline.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260905T044026Z-tth-diphoton-bd__cMU3hZC — openhands / gpt-5.6-sol

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/openhands/gpt-5.6-sol/20260905T044026Z-tth-diphoton-bdt-categorization-openhands-512532/20260905T044026Z-tth-diphoton-bd__cMU3hZC`
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

### tth-diphoton-bdt-categorization-paper-version / 20260902T220657Z-tth-diphoton-bd__E6LHpiw — openhands / gpt-5.6-terra

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/openhands/gpt-5.6-terra/20260902T220657Z-tth-diphoton-bdt-categorization-openhands-1288434/20260902T220657Z-tth-diphoton-bd__E6LHpiw`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=0, agent_session_trajectory_logs=60, terminal_recordings=0, native_tool_call_telemetry=75, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `none`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py`.
- Transcript evidence paths: `agent/completions/gpt-5.6-terra-1788386937.1674619.json, agent/completions/gpt-5.6-terra-1788386940.7150903.json, agent/completions/gpt-5.6-terra-1788386947.3449576.json, agent/completions/gpt-5.6-terra-1788386949.6092267.json, agent/completions/gpt-5.6-terra-1788386952.325491.json, agent/completions/gpt-5.6-terra-1788386956.2320514.json, agent/completions/gpt-5.6-terra-1788386960.3305478.json, agent/completions/gpt-5.6-terra-1788386965.0333543.json, agent/completions/gpt-5.6-terra-1788386971.0655248.json, agent/completions/gpt-5.6-terra-1788386978.147201.json, agent/completions/gpt-5.6-terra-1788386985.1115744.json, agent/completions/gpt-5.6-terra-1788386996.9787486.json, agent/completions/gpt-5.6-terra-1788387053.473256.json, agent/completions/gpt-5.6-terra-1788387060.4764376.json, agent/completions/gpt-5.6-terra-1788387064.4642348.json, agent/completions/gpt-5.6-terra-1788387187.1862574.json, agent/completions/gpt-5.6-terra-1788387310.6555755.json, agent/completions/gpt-5.6-terra-1788387433.7778597.json, agent/completions/gpt-5.6-terra-1788387559.410134.json, agent/openhands.trajectory.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/event_cache/0-25.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/event_cache/25-50.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/13.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/14.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/15.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/16.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/25.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/26.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/27.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/28.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/29.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/30.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/31.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/32.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/33.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/34.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/35.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/36.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/37.json, agent/sessions/6b5c4ea8-3715-47-28da8a9717decc3/events/38.json, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `app.py, run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260902T050526Z-tth-diphoton-bd__fm8URtk — openhands / lbl/cborg-coder

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/openhands/openai--lbl-cborg-coder/20260902T050526Z-tth-diphoton-bdt-categorization-openhands-501468/20260902T050526Z-tth-diphoton-bd__fm8URtk`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=13, agent_session_trajectory_logs=81, terminal_recordings=0, native_tool_call_telemetry=107, copied_workspace_source=3, model_report_metadata=6.
- Final training/model paths: `none`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/run.py, artifacts/root/submission/tth-diphoton-bdt/utils/data_loader.py`.
- Transcript evidence paths: `none`.
- Executed script paths seen directly in transcripts: `/root/submission/tth-diphoton-bdt/run.py, app.py, jp.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260905T041241Z-tth-diphoton-bd__JmY5P4p — qwen-coder / qwen-3

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/google--qwen-3--best/20260905T041241Z-tth-diphoton-bdt-categorization-qwen-coder-503382/20260905T041241Z-tth-diphoton-bd__JmY5P4p`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=17, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=2, model_report_metadata=5.
- Final training/model paths: `none`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/analyze.py`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/e5b4acb0-1965-4c62-a3f6-604b8b3fdbf4.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/tth-diphoton-bdt/analyze.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260904T225909Z-tth-diphoton-bd__3FYYT6o — qwen-coder / qwen-3

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/google--qwen-3--medium/20260904T225909Z-tth-diphoton-bdt-categorization-qwen-coder-463158/20260904T225909Z-tth-diphoton-bd__3FYYT6o`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=54, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=3, model_report_metadata=15.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/scripts/run_analysis.py`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/d553197b-f982-4793-9896-cfa7b9af4b30.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/tth-diphoton-bdt/scripts/run_analysis.py, scripts/run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260902T050526Z-tth-diphoton-bd__2Jw5SMu — qwen-coder / cborg-coder

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/qwen-coder/lbl--cborg-coder/20260902T050526Z-tth-diphoton-bdt-categorization-qwen-coder-2004640/20260902T050526Z-tth-diphoton-bd__2Jw5SMu`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=35, agent_session_trajectory_logs=3, terminal_recordings=0, native_tool_call_telemetry=1, copied_workspace_source=7, model_report_metadata=7.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/generate_metadata.py, artifacts/root/submission/tth-diphoton-bdt/run_bdt.py, artifacts/root/submission/tth-diphoton-bdt/run_categorization.py, artifacts/root/submission/tth-diphoton-bdt/run_fit.py, artifacts/root/submission/tth-diphoton-bdt/run_preselection.py, artifacts/root/submission/tth-diphoton-bdt/setup_config.py`.
- Transcript evidence paths: `agent/qwen-sessions/-root/chats/2735a643-a8bd-42ef-b535-3799eb356eb7.jsonl, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/tth-diphoton-bdt/generate_metadata.py, /root/submission/tth-diphoton-bdt/run_bdt.py, /root/submission/tth-diphoton-bdt/run_categorization.py, /root/submission/tth-diphoton-bdt/run_fit.py, /root/submission/tth-diphoton-bdt/run_preselection.py, /root/submission/tth-diphoton-bdt/setup_config.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260905T033334Z-tth-diphoton-bd__u5KdDyp — terminus-2 / gpt-5.6-sol

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/terminus-2/gpt-5.6-sol/20260905T033334Z-tth-diphoton-bdt-categorization-terminus-2-998027/20260905T033334Z-tth-diphoton-bd__u5KdDyp`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=71, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=5, model_report_metadata=16.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/bdt_model.joblib, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.pdf, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/__init__.py, artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/scripts/build_workspace.py, artifacts/root/submission/tth-diphoton-bdt/scripts/postprocess.py, artifacts/root/submission/tth-diphoton-bdt/scripts/run_analysis.py`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `scripts/build_workspace.py, scripts/postprocess.py, scripts/run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260902T205321Z-tth-diphoton-bd__sfftAQT — terminus-2 / gpt-5.6-terra

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/terminus-2/gpt-5.6-terra/20260902T205321Z-tth-diphoton-bdt-categorization-terminus-2-1318680/20260902T205321Z-tth-diphoton-bd__sfftAQT`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=75, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=3, model_report_metadata=15.
- Final training/model paths: `artifacts/root/results/tth-diphoton-bdt/categorization/histograms/bdt_score_model_component_histograms.json, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.pdf, artifacts/root/results/tth-diphoton-bdt/categorization/plots/bdt_score_model_components_with_boundaries_36fb_v1.png, artifacts/root/results/tth-diphoton-bdt/model/background_mixture_and_normalization.json, artifacts/root/results/tth-diphoton-bdt/model/class_balance_check.json, artifacts/root/results/tth-diphoton-bdt/model/training_metadata.json, artifacts/root/results/tth-diphoton-bdt/model/training_sample.csv`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/fit/FIT1/background_template_selection.json, artifacts/root/results/tth-diphoton-bdt/plots/preselection_channels.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_mass.png, artifacts/root/results/tth-diphoton-bdt/plots/preselection_processes.png, artifacts/root/results/tth-diphoton-bdt/preselected_events.csv, artifacts/root/results/tth-diphoton-bdt/preselection_summary.json`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/finalize_compliance.py, artifacts/root/submission/tth-diphoton-bdt/run_analysis.py`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `finalize_compliance.py, run_analysis.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

### tth-diphoton-bdt-categorization-paper-version / 20260905T003430Z-tth-diphoton-bd__st37ant — terminus-2 / lbl/cborg-coder

- Retained evidence root: `results/paper/tth-diphoton-bdt-categorization-paper-version/terminus-2/openai--lbl-cborg-coder/20260905T003430Z-tth-diphoton-bdt-categorization-terminus-2-372893/20260905T003430Z-tth-diphoton-bd__st37ant`
- Execution status / Harbor reward: `completed` / `0.0`
- Source state: **recoverable_final_code**; classification: **none**.
- Inventory counts: final_output_artifacts=5, agent_session_trajectory_logs=1, terminal_recordings=2, native_tool_call_telemetry=0, copied_workspace_source=4, model_report_metadata=6.
- Final training/model paths: `none`.
- Final selection paths: `artifacts/root/results/tth-diphoton-bdt/preselected_events.csv`.
- Copied source recoverable now: `artifacts/root/submission/tth-diphoton-bdt/analysis/top_categorization.py, artifacts/root/submission/tth-diphoton-bdt/debug_preselection.py, artifacts/root/submission/tth-diphoton-bdt/final_stage.py, artifacts/root/submission/tth-diphoton-bdt/run_pipeline.py`.
- Transcript evidence paths: `agent/recording.cast, agent/terminus_2.pane, agent/trajectory.json`.
- Executed script paths seen directly in transcripts: `/root/submission/tth-diphoton-bdt/debug_preselection.py, /root/submission/tth-diphoton-bdt/run_pipeline.py, final_stage.py, run_pipeline.py`.
- Runtime source not copied as a workspace artifact: `none`.
- Incomplete-copy signatures: none observed.
- Smallest safe recovery rule: Read the copied source artifact directly; retain its path in the evidence ledger.

## Prioritized collector fixes

1. **Copy the final created/modified workspace source outside `results/**`, plus a file manifest.** This is the strongest fix. It can directly support the eight currently evidence-limited question families: final features (Q4), extra features (Q5), tried ML setups (Q7), final selection algorithm (Q8), selection comparisons (Q9), mass usage/window (Q12), optimization attempts (Q13), and reproducibility (Q30). Those account for 82 not-established cells in the current 15-run pilot matrix.
2. **Preserve file-writing tool inputs and terminal input bytes in one normalized telemetry record.** This unlocks adapter recovery for transcript-backed runs without requiring a solver submission format. It addresses the same eight question families where source was written through a tool call, patch, or heredoc but not copied as a file.
3. **For every executed `python PATH.py`, emit a collector manifest with PATH and either its final content or an explicit unavailable marker.** This closes the execution-without-source signature and makes absent code distinguishable from an adapter limitation.
4. **On failed or incomplete runs, retain the workspace snapshot and complete session stream through the final tool action.** This is most important for the three OpenHands runs that show `app.py` execution but no final results or recoverable source; it cannot manufacture missing physics evidence, but it can separate collection loss from a genuinely incomplete run.

The JSON companion contains the full path inventory for each run and is the machine-readable input for future adapters.
