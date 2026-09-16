## Evaluation Status and Missing-Evidence Policy

Each criterion must receive:

1. An **evaluation status** explaining the result.
2. A **binary reward** when the criterion was successfully evaluated.
3. An **observed value** supporting the result.

## Evidence Standard

The evaluator may use any readable run log, terminal transcript, source code,
saved table, plot, workspace, or report. The task-solving agent is not required
to produce a prescribed evidence schema or filename.

A criterion passes only when direct evidence establishes its condition; an
unsupported claim in a final response is not evidence. A criterion fails only
when direct evidence contradicts its condition. If neither exists, use
`missing` with reward 0: this means the claimed work cannot be verified, not
that a particular artifact was omitted.

When evidence conflicts, prefer the source produced closest to the actual
computation. If that does not resolve the conflict, use `missing` with reward
0 and state that the evidence conflicts. Source code alone establishes an implemented method, but does not establish
that a numeric result was produced or that the method was run. An evidence
source is usable when it opens or executes without error, directly supports the
condition, and contains finite values where the supporting value is numeric.
Plot appearance is not scored visually.

### Allowed Status Values

| Status | Definition | Binary reward |
|---|---|---:|
| `pass` | The required evidence exists and satisfies the desired condition. | 1 |
| `fail` | The required evidence exists and demonstrates that the desired condition was not satisfied. | 0 |
| `missing` | Evidence is absent, unreadable, incomplete, contradictory, or unavailable to the evaluator. | 0 |

### Status Decision Rules

Use `pass` when:

- The relevant evidence is present.
- The evidence is readable and internally consistent.
- The desired condition is explicitly satisfied.

Use `fail` when:

- The criterion was implemented or evaluated.
- Sufficient evidence exists to determine the outcome.
- The evidence shows that the desired condition was not satisfied.

Use `missing` when the agent did not attempt the required measurement, a
comparison or diagnostic was omitted, a required source cannot be opened, the
available evidence is incomplete or contradictory, or evaluator access fails.
State the concrete reason in the report; do not infer a pass or fail.

### Binary Reward Rule

For successfully evaluated criteria:

`reward_i = 1` when `status_i` is `pass`.

`reward_i = 0` when `status_i` is `fail` or `missing`.

### Section Weighting

Task-specific evaluation documents must organize their criteria into section
tables with these columns:

| Question | Desired answer | Scoring |
|---|---|---|
| The criterion to evaluate. | The condition required for a pass. | The binary, evidence-based rule used to assign the reward. |

Every category has equal weight in the report-level overall metric, regardless
of its number of questions. First calculate each category's pass fraction:

`category_pass_fraction_c = sum(rewards in category c) / number_of_criteria in category c`

Then calculate exactly one **overall equal-category reward** as the arithmetic
mean of the category pass fractions:

`overall_equal_category_reward = sum(category_pass_fraction_c) / number_of_categories`

This is distinct from the raw total reward: a category with fewer questions
has the same weight as a category with more questions. Do not add provisional
group weights or a second weighted-total formula to a task-specific criterion
document.

### Required Value Reporting

Every criterion must report the observed value that supports its yes/no result.
The binary reward answers whether the criterion passed; the observed value
shows by how much it passed or failed. A criterion that has no meaningful
numeric value may report a text value instead.

For a non-comparative quantity, report its value, unit, and definition. For
example, a cost criterion reports the actual amount in USD, even when the
binary answer is already `pass`.

For a comparison, report both values, the absolute delta, and a
direction-aware relative improvement percentage:

- Higher-is-better: `100 * (agent - reference) / abs(reference)`.
- Lower-is-better: `100 * (reference - agent) / abs(reference)`.
- If the reference is zero, report `null` for relative improvement unless a
  separate definition applies.

Positive relative improvement means the agent is better; negative means it is
worse. The percentage is explanatory evidence, not an additional reward.

### Required Evaluator Output

For every criterion, the evaluator must return:

```json
{
  "question_id": 1,
  "status": "pass",
  "reward": 1,
  "observed_value": {
    "value": 2.73,
    "unit": "USD",
    "definition": "Total reported cost of the agent run."
  },
  "comparison": null,
  "extracted_answer": "Both wall-clock and agent execution time were reported.",
  "evidence": [
    {
      "artifact": "run_summary.json",
      "location": "timing.wall_clock_seconds",
      "value": 413.2
    },
    {
      "artifact": "run_summary.json",
      "location": "timing.agent_execution_seconds",
      "value": 376.8
    }
  ],
  "reason": "Both required timing values are present and valid."
}
```

For a baseline-comparison criterion, replace `comparison: null` with:

```json
{
  "reference_name": "mass-greedy/v1",
  "reference_value": 0.388264,
  "absolute_delta": 0.021736,
  "relative_improvement_percent": 5.598,
  "direction": "higher_is_better"
}
```

## Required Markdown Report Layout

For the required manual-review workflow, see
[`evaluation_prompt.md`](evaluation_prompt.md). It defines the evidence
inspection standard that accompanies this report layout.

Render an evaluation report as a progressive drill-down: concise comparison
tables first, then increasingly detailed per-question material. Use one column
per evaluated `agent / model` run, with a stable, human-readable label such as
`Codex / gpt-5.6-sol`. Keep the same column order in every table.

Render every non-passing status as its binary reward of `0`.

### 1. Status Summary

This is the first table. It has one row per evaluated run, not one row per
category. The compact status columns have this fixed meaning:

| Column | Status | Reward |
|---|---|---:|
| `P` | `pass`: required evidence exists and satisfies the desired condition. | 1 |
| `F` | `fail`: required evidence exists and demonstrates that the desired condition was not satisfied. | 0 |
| `M` | `missing`: evidence is absent, unreadable, incomplete, contradictory, or unavailable to the evaluator. | 0 |

`Harbor status / verifier reward` is contextual execution evidence, not a
rubric score. It must be reported separately in the final column.

| Run | P | F | M | Harbor status / verifier reward |
|---|---:|---:|---:|---|
| Codex / gpt-5.6-sol | 24 | 3 | 8 | completed / 0.916667 |
| Claude Code / claude-opus-5 | 1 | 0 | 34 | agent API failure / 0.000000 |

### 2. Total Reward (Raw, No Averaging)

This is the second table. Each cell is the raw sum of all binary rewards, with
the denominator shown for context. Do not apply category weights or category
averages here.

| Summary | Codex / MODEL_A | Claude Code / MODEL_B |
|---|---:|---:|
| Total reward | 28 / 35 | 24 / 35 |

### 3. Overall Equal-Category Reward

This is the one overall normalized metric. It gives every rubric category
equal weight, even when categories contain different numbers of questions.
Compute each category's pass fraction, then take their arithmetic mean. Do not
show a per-category average table here; detailed per-question tables below are
the drill-down for this metric.

| Summary | Codex / MODEL_A | Claude Code / MODEL_B |
|---|---:|---:|
| Overall equal-category reward | 0.86 | 0.62 |

### 4. Per-Question Binary Rewards

This is the first detailed table. Each row is a rubric question; each cell is
`1`, `0`, or `ERR`. Include the category in the first column so readers can
locate the question in the rubric.

| Category | Question | Codex / MODEL_A | Claude Code / MODEL_B |
|---|---|---:|---:|
| Execution and Meta | Q1. Were both timing values reported? | 1 | 0 |
| ... | ... | ... | ... |

### 5. Per-Question Observed Values and Rewards

Repeat the question rows with a compact cell that presents the observed value
first and the binary reward second: `VALUE [REWARD]`. Preserve units. For
comparisons, include agent value, baseline value, and relative improvement:
`AGENT vs BASELINE (RELATIVE_IMPROVEMENT) [REWARD]`.

| Category | Question | Codex / MODEL_A | Claude Code / MODEL_B |
|---|---|---|---|
| Execution and Meta | Q2. Total cost | `$2.73 USD [1]` | `$4.18 USD [1]` |
| Baseline Comparison | Q23. Efficiency | `0.410 vs 0.388 (+5.6%) [1]` | `0.370 vs 0.388 (-4.7%) [0]` |
| ... | ... | ... | ... |

### 6. Per-Question Evidence and Reasoning

Finish with the most detailed tables, preferably one table per category to
keep columns readable. Each run cell must include the observed value, status,
reason, and concise artifact reference. Link to or name the exact artifact and
location; do not merely say “logs checked.”

| Question | Codex / MODEL_A | Claude Code / MODEL_B |
|---|---|---|
| Q23. Efficiency | `0.410 [pass]`; `evaluation_summary.json: metrics.efficiency`; baseline `0.388`; `+5.6%`. | `0.370 [fail]`; `evaluation_summary.json: metrics.efficiency`; baseline `0.388`; `-4.7%`. |

Optional appendices may contain full JSON records, raw artifact excerpts, and
all evidence locations. They must come after these six table layers.
