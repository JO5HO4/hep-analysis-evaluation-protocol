# RunRecord v1 — the execution → evaluation seam

Version: **run-record.v1** (frozen 2026-07-04). This file may not be edited;
a contract change is a new `run-record.v2.md`, agreed by both module owners.

A **RunRecord** is the single artifact execution produces for evaluation to
consume. Execution owns everything upstream of it (how runs are driven, how
outputs are captured); evaluation owns everything downstream (extraction,
scoring). The two modules share no other files, state, or vocabulary.

## Layout

```
${XDG_STATE_HOME:-~/.local/state}/terminal-bench-collider/captures/<run_id>/
├── record.json        identity + provenance (schema: run-record.v1.schema.json)
├── final_state/       the agent-under-test's collected output, normalized:
│                      the task.toml `artifacts` paths re-rooted at this
│                      directory (e.g. results/results.json, submission/…)
└── evidence/          OPTIONAL, human-facing only: verifier reward.txt,
                       test-stdout.txt, trial.log
```

The capture directory name equals `record.json`'s `run_id`. A capture is
**write-once**: producers must refuse to overwrite an existing capture.
No other top-level entries are permitted.

## record.json fields (all required unless marked optional)

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | `"run-record.v1"` | literal |
| `run_id` | string | execution run id; equals the capture directory name |
| `task` | string | task name from `task.toml` |
| `task_path` | string | repo-relative task directory |
| `agent` | string | benchmark agent (`oracle`, `codex`, …) |
| `model` | string or null | model name; null for model-free agents |
| `source_job_path` | string | Harbor job directory the capture came from |
| `trial` | string | trial directory name inside the job |
| `harbor_exit_code` | integer | Harbor process exit status |
| `verifier_reward` | number or null | the in-container task verifier's reward, if any (evidence, not a grade) |
| `created` | string | ISO-8601 UTC capture time |
| `notes` | string, optional | free-form provenance notes |

## Producer guarantees (execution)

1. `final_state/` contains **only what the benchmark agent produced** — the
   `task.toml` `artifacts` paths — never verifier internals, `hidden_data`,
   expected values, or anything from `tests/`.
2. `record.json` validates against `run-record.v1.schema.json`
   (`contracts/validate-run-record <dir>` must exit 0).
3. Captures are write-once and live outside Git (machine-local state dir);
   curated copies may be committed as grader fixtures.

## Consumer guarantees (evaluation)

1. Extractors read **only `final_state/`**, always via an isolated scratch
   copy — never the capture itself, never `evidence/` (verifier stdout can
   leak expected values), never the Harbor job tree.
2. Grade reports are written to `runs/grades/<run_id>.<spec_version>.json`.
   Evaluation never writes into `runs/manifests/`, Harbor job directories,
   or captures.
3. The only join key between execution records and evaluation results is
   `run_id`.

## Relationship to grader fixtures

A fixture case `grader/fixtures/<task>/<case>/` is a curated, committed copy
of a RunRecord's `final_state/` plus a human label file (`expected.json`).
The fixture pipeline is therefore: validate capture → copy `final_state/` →
label. Fixture labels record what the agent produced, never physics truth.
