# Manual Codex Review Prompt for Paper Evidence

Use this prompt with a fresh Codex agent to produce a paper-facing manual
review. The agent is an evidence reviewer: it manually inspects preserved
artifacts and does not use an extractor, report generator, or authoritative
grader.

```text
Review every logical run in the preserved paper evidence for TASK and write the
two reports below. Do not select a representative subset.

Evidence root: results/paper/TASK-PAPER-VERSION/
Rubric: RUBRIC
Workflow protocol: evaluation/workflow-characterization.md
Shared evidence policy: evaluation/evaluation_rubric.md
Output directory: paper/reviews/TASK/

Create:
1. evaluation-report.md — one complete cross-run rubric report using the
   documented report layout, criterion tables, and equal-category calculation
   in RUBRIC. Evaluate every logical `agent / model / run` represented in the
   evidence root. For every criterion and every run, give status, binary reward
   where applicable, observed value, exact evidence location, and concise
   reason. Include the status summary, per-group and overall equal-category
   results, per-criterion values, and Harbor status/verifier reward separately.
   State that the result is non-authoritative.
2. workflow-characterization.md — follow the Markdown tables in
   evaluation/workflow-characterization.md for every logical run in the same
   order as `evaluation-report.md`. Report workflow facts only; do not create a
   workflow score, rank, or weighted total.

This is an execution task, not a request for a review plan or a prose
explanation. Do not stop after describing evidence gaps, apologizing for a
conservative review, or proposing how a later reviewer could investigate.
Your completion condition is that both requested Markdown files exist and
cover every included logical run.

Manually inspect any readable log, terminal transcript, source code, saved
table, plot, workspace, or report. Do not require a filename that the task did
not require. Pass only with direct evidence; fail only with direct
contradictory evidence; otherwise use missing. If sources conflict, prefer
evidence closest to the computation or use missing.

Do the investigative work for every criterion. For every run, trace the
workflow through its execution metadata, terminal log, submitted source code,
task outputs, tables, plots, workspaces, and narrative reports before deciding
the criterion is missing. Do not mark an entire question range or rubric group
missing with one generic statement. Evaluate each criterion independently.

Before assigning any criterion `missing`, complete this per-run evidence audit:
1. Identify the actual artifact root from `result.json` and enumerate its
   readable logs, source, reports, tables, JSON outputs, plots, and workspaces.
2. Search those sources for the criterion's quantities, definitions, and
   configuration—not merely a preferred output filename.
3. Read the relevant source and execution output together when a criterion
   concerns both implementation and a produced result.
4. Record the exact positive or negative evidence in the report table.
5. Only then use `missing`, listing the concrete sources searched.

For example, a task-verifier reward of zero is execution context, not a reason
to discard readable physics evidence. A schema or provenance failure may be
reported separately while method, fit, yield, or plotting criteria still pass
when the bundle directly supports them.

Treat source code as evidence that a method was implemented and execution
outputs as evidence that it ran. Combine both when the criterion concerns a
method and its resulting measurement. Where a compatible evaluator-side
baseline can be run, run it rather than marking the comparison missing.

Use `missing` only after documenting the concrete searched locations and why
none directly establishes the criterion. The report must include this search
trail in the per-criterion evidence/reason column. Missing a convenient JSON
field or a preferred filename is never by itself sufficient reason for
`missing`.

Use evaluator-side baseline scripts only when compatible evaluator inputs are
available. Do not invent a baseline result, an outcome grade, or missing
evidence. Do not modify results/paper, task instructions, verifiers, grader,
or baseline definitions. Write only under paper/reviews/TASK/.

Treat one completed Harbor bundle as one logical run. Resolve the actual bundle
through its `result.json` and artifact root. Do not double-count convenience
links, wrapper-log directories, duplicated parent summaries, or superseded
attempts. At the beginning of both reports, list every included run and every
excluded path with the reason for exclusion.
```

## Task substitutions

| TASK | Evidence root | RUBRIC | Optional evaluator-side baseline |
|---|---|---|---|
| `top-reconstruction` | `results/paper/top-reconstruction-paper-version/` | `evaluation/top-reconstruction.md` | `evaluation/top-reconstruction-baseline/` |
| `tth-diphoton` | `results/paper/tth-diphoton-bdt-categorization-paper-version/` | `evaluation/ttH.md` | `evaluation/ttH-baseline/` |
| `higgs-4l` | `results/paper/higgs-4l-significance-paper-version/` | `evaluation/higgs_4l.md` | No reference calculator yet; mark its reference criteria `missing`. |

The historical `paper/top-reconstruction-manual-rubric-evaluation.md` is not a
current report: it predates the current rubric and must not be overwritten.
