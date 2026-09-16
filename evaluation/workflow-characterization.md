# Workflow Characterization Protocol

This protocol describes how an agent worked on a benchmark task: its attempts,
errors, recoveries, iteration pattern, and resource use. It is separate from
task-scientific evaluation.

Workflow characterization never contributes to a task rubric reward, Harbor
verifier reward, or authoritative outcome grade. It is descriptive evidence
for comparing agent behavior across tasks and models.

## Evidence policy

Use the flexible evidence policy in
[evaluation_rubric.md](evaluation_rubric.md). The evaluator may inspect any
readable run log, terminal transcript, source code, saved result, plot,
workspace, or report. The task-solving agent is not required to emit a special
workflow file or schema.

Record an observed value only when direct evidence establishes it. Otherwise
record `not established`; never infer a count from an absence of evidence.
Conflicting direct evidence is recorded as `missing` together with both
sources.

## Required workflow profile

Produce one profile per benchmark trial. Use the following facts and exact
definitions.

| Field | Definition |
|---|---|
| Trial outcome | Harbor completion state and verifier reward, reported as execution context rather than workflow quality. |
| Terminal command count | Number of recorded shell or tool invocations in the trial transcript. Exclude messages that contain no invocation. |
| Failed-command count | Number of recorded invocations with a nonzero exit status or explicit tool failure. Do not count an invocation whose outcome is unknown. |
| Distinct error signatures | Number of unique tuples `(error type, normalized first diagnostic line)`. Normalize absolute paths, timestamps, numeric IDs, and run IDs to placeholders before comparison. |
| Analysis iterations | Number of directly evidenced attempts with a distinct analysis configuration. Configurations differ when at least one of model family, objective, feature set, hyperparameter, split seed, selection rule, category boundary, or fit setting differs. |
| Final iteration | The directly evidenced iteration that generated the submitted final result; otherwise `not established`. |
| Superseded iterations | Evidenced iterations that produced a result but were replaced by a later iteration before final submission. |
| Recovery count | Number of distinct error signatures followed by direct evidence that the same workflow stage subsequently completed. Count each signature at most once. |
| Data-validation checks | Names and outcomes of explicit checks for NaNs/infinities, duplicate IDs, invalid weights, empty categories, zero denominators, and invalid model or fit states. |
| Tool categories used | Set drawn from: shell, source editing, Python/scientific computation, ROOT/RooFit, plotting, file inspection, package/environment management, and other. |
| Stage timing | Available duration for each workflow stage; record unknown stages as `not established`, not zero. |
| Reproducibility attempt | Whether direct evidence shows a rerun from a clean output location and whether its headline results agree within a stated tolerance. |
| Artifact coverage | `found required task outputs / expected required task outputs`, with unavailable or unreadable expected outputs listed separately. This is task-contract context, not a physics score. |

## Workflow stages

Assign an action to exactly one of these stages when direct evidence identifies
its purpose: `setup`, `input_inspection`, `data_preparation`, `training`,
`validation`, `optimization`, `inference_or_selection`, `fit`, `plotting`,
`reporting`, or `unknown`.

An error recovery requires the same named stage before and after the error.
For example, a failed training invocation followed by successful training
counts as one recovery; a successful plotting command does not recover a
training failure.

## Timeline

Present an ordered stage timeline when ordering evidence is available:

```text
setup → input inspection → data preparation → training → validation
→ optimization → inference/selection → fit → plotting → reporting
```

For each observed stage, report whether it was attempted, completed, had one
or more error signatures, changed the final configuration, and has a known
duration. Omit unobserved stages rather than marking them failed.

## Derived descriptive quantities

These quantities are optional and must never be interpreted as rewards:

- `error_to_iteration_ratio = failed_command_count / max(1, analysis_iterations)`
- Final-result fraction of wall time, when stage durations and total wall time
  are both directly established.
- Fraction of iterations that were superseded, when iteration identities are
  directly established.

Do not rank agents by any one workflow quantity. Use the profile to explain
tradeoffs: for example, a low-error run may be incomplete, while a recovered
error may represent productive debugging.

## Required Markdown Report Layout

The evaluator produces reproducible Markdown workflow reports from the
protocol. These are evaluator outputs, not artifacts required from the
task-solving agent. A report must state the protocol version
`workflow-characterization/v1`, the generation date, and the ordered list of
run identifiers it covers.

For a set of runs, produce a summary Markdown file followed by a Markdown
profile for each run. Keep runs in the same stable order in every table:
task, agent, model, then run identifier in lexical order. Render unavailable
values as `not established` and conflicting evidence as `missing`; do not
replace either with zero.

### 1. Cross-run workflow summary

Use one row per run and these columns:

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `TASK / AGENT / MODEL / RUN_ID` | `completed / 1.000000` | 42 | 3 | 2 | 2 | 4 | 3 | 4 | `not established` | `18 / 18` |

The summary is descriptive. It must not show a workflow score, rank, pass
fraction, or weighted total.

### 2. Per-run workflow profile

Every run receives the following sections in this order.

#### Run identity

| Field | Value |
|---|---|
| Task | `TASK` |
| Agent / model | `AGENT / MODEL` |
| Run identifier | `RUN_ID` |
| Protocol version | `workflow-characterization/v1` |
| Harbor status / verifier reward | `STATUS / REWARD` |

#### Workflow metrics

| Metric | Observed value | Evidence location |
|---|---|---|
| Terminal command count | `VALUE` | `SOURCE` |
| Failed-command count | `VALUE` | `SOURCE` |
| Distinct error signatures | `VALUE` | `SOURCE` |
| Analysis iterations | `VALUE` | `SOURCE` |
| Final iteration | `VALUE` | `SOURCE` |
| Superseded iterations | `VALUE` | `SOURCE` |
| Recovery count | `VALUE` | `SOURCE` |
| Tool categories | `VALUE` | `SOURCE` |
| Reproducibility attempt | `VALUE` | `SOURCE` |
| Artifact coverage | `VALUE` | `SOURCE` |

#### Error signatures and recoveries

| ID | Stage | Normalized error signature | Occurrences | Recovery evidence | Status |
|---|---|---|---:|---|---|
| `E1` | `training` | `TYPE: normalized diagnostic` | 2 | `SOURCE` | `recovered` |

Use `not established` when the transcript does not expose an exit status or
diagnostic. Do not infer an error from an incomplete result.

#### Iteration lineage

| Iteration | Changed property | Common validation metric | Result | Final / superseded | Evidence location |
|---|---|---|---|---|---|
| 1 | `score threshold` | `reconstruction efficiency` | `0.31` | `superseded` | `SOURCE` |

This table records only directly evidenced changes and results. It is valid for
an iteration table to have no data rows.

#### Stage timeline

| Stage | Attempted | Completed | Error signatures | Final configuration changed | Duration | Evidence location |
|---|---|---|---|---|---|---|
| `training` | `yes` | `yes` | `E1` | `yes` | `12 min` | `SOURCE` |

Use the fixed stage vocabulary from this protocol. Include observed stages only;
do not convert unobserved stages into failed stages.

#### Validation checks

| Check | Outcome | Evidence location |
|---|---|---|
| `duplicate IDs` | `none found` | `SOURCE` |

Include each directly evidenced check for NaNs/infinities, duplicate IDs,
invalid weights, empty categories, zero denominators, invalid model states, or
invalid fit states.
