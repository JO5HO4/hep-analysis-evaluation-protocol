# Higgs four-lepton paper-version evidence

This directory contains one complete, clean Harbor job bundle for every
agent/model cell in the active benchmark matrix. Best and Medium jobs are the
retained tier representatives. Free-tier jobs use the later 2026-09-02 reruns
for every agent.

Directory names are filesystem-safe model IDs: `/` is represented as `--`.
Qwen Best and Medium both use `google/qwen-3`, so their directories carry the
`--best` and `--medium` suffixes.

Each copied job completed one trial with zero harness errors. Verifier reward
is preserved as task-output evidence and is not a claim of an authoritative
physics outcome grade.

| Agent | Best reward | Medium reward | Free rerun reward |
| --- | ---: | ---: | ---: |
| `codex` | 1.0000 | 1.0000 | 0.9500 |
| `claude-code` | 1.0000 | 1.0000 | 0.9500 |
| `terminus-2` | 1.0000 | 1.0000 | 0.7000 |
| `qwen-coder` | 0.5875 | 0.7500 | 0.6875 |
| `openhands` | 0.0000 | 0.0000 | 0.9500 |
