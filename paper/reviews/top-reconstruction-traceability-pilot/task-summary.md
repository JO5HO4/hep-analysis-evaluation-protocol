# Top-reconstruction traceability pilot: task summary

This task is reviewed in linked groups because one meeting table cannot safely collapse execution accounting, saved technical evidence, attempted workflow, and evaluator diagnostics into one score.

| Group | What the linked technical note establishes |
|---|---|
| Execution context | Run identity, completion state, and Harbor verifier reward. [Detailed run evidence](index.md) |
| Evidence coverage | Exhaustive, bounded inventory and indexed evidence search. [Detailed run evidence](index.md) |
| Classifier and selection | Saved classifier and selected-triplet artifacts, when present. [Detailed run evidence](index.md) |
| Attempt traceability | Hypothesis, action/configuration, observed result, and decision without inventing lineage. [Detailed run evidence](index.md) |
| QC and baseline diagnostics | Static inspection, agent-executed checks, reviewer-executed QC, and same-sample mass-greedy comparison. [Detailed run evidence](index.md) |
| Fake-mass sculpting | Raw modal-bin shift and width retention relative to all fake candidates before selection. [Detailed run evidence](index.md) |

The baseline uses `mass-greedy/v2-n-top-2`. Its fixed unweighted histogram is 0–400 GeV in 40 bins. An agent is called better only when its modal shift is no larger and width retention no smaller, with one strict improvement. This is a diagnostic comparison, with no threshold and no authoritative score.

The 31-question protocol assigns 1 for `pass` and 0 for `fail` or `missing`, then reports the review fraction in each technical note and portfolio row. Execution status, Harbor verifier reward, this non-authoritative review reward, and an authoritative outcome grade are explicitly separate. No authoritative grade is produced by this pilot.
