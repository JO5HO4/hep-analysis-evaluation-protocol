# Fixed-Structure Manual Evaluation Prompt

Use this prompt for a manual, evidence-backed evaluation of **any** task
rubric. It preserves the progressive six-layer report layout of
`paper/top-reconstruction-manual-rubric-evaluation.md`, but derives the runs,
categories, questions, and observed quantities from the selected task rubric.

The structure is deterministic for a given rubric and set of runs. Never
remove a table, question row, run column, or required cell because evidence is
missing. Put the required placeholder in that fixed position instead.

## Inputs

- Shared policy: `evaluation/evaluation_rubric.md`
- Selected task rubric: `TASK_RUBRIC_PATH`
- Raw run bundles: `RESULTS_ROOT`
- Report destination: `REPORT_PATH`

## Evidence and scoring method

1. Review every supplied run independently. Inspect `result.json`, `trial.log`,
   verifier files, artifact manifests, saved reports, relevant data products,
   and plots. Do not score from a listing, filename, public summary, or prior
   report.
2. Extract every numbered question and category from `TASK_RUBRIC_PATH` in
   source order. The rubric is the sole authority for the report's categories,
   question rows, observed quantities, comparison requirements, and scoring.
3. For every question and run, record the shared-policy status, binary reward
   when evaluable, observed value with unit and definition, evidence path and
   location, and concise reason. Compute required quantities from saved
   artifacts; perform the documented evaluator-side baseline comparison where
   the task rubric requires one.
4. Keep Harbor completion status, Harbor verifier reward, and rubric result as
   separate fields. A Harbor reward is never a rubric answer.
5. Do not invent a threshold, metric, baseline value, artifact, or evidence.

## Deterministic ordering

Build a run registry before writing the report. Its order is immutable across
every table in the report:

1. Sort cohorts by their first appearance in explicitly supplied run metadata.
   Treat absent cohort metadata as the single cohort `Unspecified`.
2. Within each cohort, sort by normalized `agent`, then normalized `model`,
   then run ID/path as a deterministic tie-breaker. Preserve every supplied
   run, including failed and early-terminated runs.
3. Construct each label as `AGENT / MODEL`; append ` / RUN_ID` only when
   needed to make labels unique. Use exactly that label everywhere.
4. Keep categories and questions in their source order from `TASK_RUBRIC_PATH`.
   Never sort them alphabetically or group them by outcome.

The number of run columns and question rows is therefore allowed to differ for
different tasks, but it must be identical in all corresponding tables within
one report. A task with more observed-value questions receives more rows in
the same observed-value table; it does not receive an ad hoc extra table or a
different layout.

## Placeholder policy

Use these literal values. Do not leave any cell blank, substitute an em dash,
or silently convert missing evidence into zero.

- Numeric observation unavailable: `NaN` (or `NaN / NaN` for an
  agent/reference comparison), followed by the applicable reward/status.
- Required artifact absent or unreadable: `N/A [M]` in observed-value tables;
  name the missing artifact in the evidence table.
- Run did not perform the requested measurement: `N/A [N]`.
- Ambiguous result with an unset threshold: retain the measured value and use
  `[0; A]`; if it cannot be measured, use `NaN [0; A]`.
- Evaluator-side error: `ERR` in reward tables, `N/A [ERR]` in observed-value
  tables, and `missing` in evidence tables. Its raw and overall
  totals are `N/A`.
- Harbor status or verifier reward unavailable: `N/A`.
- A cohort has no runs only when the caller explicitly declares it. Render its
  tables with the single fixed column `N/A`; do not omit the cohort.

## Required report layout

Use exactly the six numbered sections below, in exactly this order. The
Markdown table headers, separator rows, and column ordering are fixed. Replace
angle-bracket tokens with values; they describe a generated list, not literal
output text. Do not emit extra summary or observation tables.

# Manual <TASK> rubric evaluation

State that this is a manual, evidence-backed review and whether it is an
indexed outcome grade. State unresolved task thresholds and data limitations
in prose before Section 1.

## 1. Status summary

Render one table per cohort, in registry order. The status rows and their
order are immutable:

### <COHORT>

| Status | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---:|---:|---:|---:|
| P | <count> | <count> | ... | <count> |
| F | <count> | <count> | ... | <count> |
| N | <count> | <count> | ... | <count> |
| M | <count> | <count> | ... | <count> |
| A | <count> | <count> | ... | <count> |
| E | <count> | <count> | ... | <count> |
| Harbor status / verifier reward | <value> | <value> | ... | <value> |

`P/F/M` mean `pass/fail/missing`. The final row is contextual execution
information.

## 2. Total reward (raw, no averaging)

Use one table for all cohorts. The columns are the stable agent labels with
cohort disambiguators when necessary; the denominator is the task rubric's
total number of numbered questions.

| Cohort | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---:|---:|---:|---:|
| <COHORT_1> | <passed> / <question_count> | <passed> / <question_count> | ... | <value> |
| <COHORT_2> | <value> | <value> | ... | <value> |
| ... | ... | ... | ... | ... |

Cells for runs outside the row's cohort are `N/A`; do not remove their
columns. An evaluator error makes that run's cell `N/A`.

## 3. Overall equal-category reward

Use one table with the identical columns and cohort rows from Section 2.
Compute the arithmetic mean of the category pass fractions exactly as defined
by the shared policy. Never insert a per-category-average table here.

| Cohort | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---:|---:|---:|---:|
| <COHORT_1> | <overall> | <overall> | ... | <value> |
| <COHORT_2> | <value> | <value> | ... | <value> |
| ... | ... | ... | ... | ... |

## 4. Per-question binary rewards

Render one table per cohort, in registry order. Each numbered rubric question
has exactly one row; category names repeat as needed. Question rows remain in
task-rubric source order, regardless of whether the question is an
observation, a comparison, or a binary check.

### <COHORT>

| Category | Question | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---|---:|---:|---:|---:|
| <CATEGORY_1> | Q<id>. <question text> | <1/0/ERR> | <1/0/ERR> | ... | <value> |
| <CATEGORY_1> | Q<id>. <question text> | <1/0/ERR> | <1/0/ERR> | ... | <value> |
| <CATEGORY_2> | Q<id>. <question text> | <1/0/ERR> | <1/0/ERR> | ... | <value> |
| ... | ... | ... | ... | ... | ... |

## 5. Per-question observed values and rewards

Render one table per cohort, with exactly the same rows, row order, columns,
and column order as that cohort's Section 4 table. This is the fixed location
for every observation question, including any additional observation questions
defined by another task. Each cell is `OBSERVED_VALUE [REWARD]`; preserve
units. For comparisons use
`AGENT vs REFERENCE (RELATIVE_IMPROVEMENT) [REWARD]`. For text observations,
use `TEXT [REWARD]`.

### <COHORT>

| Category | Question | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---|---|---|---|---|
| <CATEGORY_1> | Q<id>. <question text> | <value [reward]> | <value [reward]> | ... | <value> |
| <CATEGORY_1> | Q<id>. <question text> | <value [reward]> | <value [reward]> | ... | <value> |
| <CATEGORY_2> | Q<id>. <question text> | <value [reward]> | <value [reward]> | ... | <value> |
| ... | ... | ... | ... | ... | ... |

## 6. Evidence and reasoning

Render one table per category, in task-rubric source order. Each category
table has every question in that category, in source order, and every run in
the stable cohort/run registry order. Each run cell contains: observed value;
status; concise reason; and exact `artifact: location` reference. Never merge
questions into range rows, even when they use the same evidence.

### <CATEGORY>

| Question | <RUN_1> | <RUN_2> | ... | <RUN_N> |
|---|---|---|---|---|
| Q<id>. <question text> | <value [status]; artifact: location; reason> | <value [status]; artifact: location; reason> | ... | <value> |
| Q<id>. <question text> | <value [status]; artifact: location; reason> | <value [status]; artifact: location; reason> | ... | <value> |

### Exact artifact roots

List the concrete artifact roots and exact files inspected for each supplied
run in registry order. Write `N/A` for an unavailable root; do not omit it.

## Final validation before writing `REPORT_PATH`

Reject and rewrite the report if any of these differ within the same report:

1. The six section headings or their order.
2. The registry-derived cohort and run ordering.
3. The Section 4 and Section 5 category/question rows.
4. The task-rubric category and question source order in Section 6.
5. The exact status-row order in Section 1.
6. A required table cell that is blank or lacks an observed value,
   `NaN`, `N/A`, or `ERR` placeholder.

This validation allows a different task to have a different number of
categories, runs, and observation questions. It does not allow that variation
to change the report's six-layer schema or ordering rules.
