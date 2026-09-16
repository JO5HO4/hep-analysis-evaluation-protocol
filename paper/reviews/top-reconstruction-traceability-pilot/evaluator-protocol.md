# Artifact-adaptive evaluator protocol (pilot)

This protocol evaluates a completed, preserved run without requiring the task-solving agent to emit a prescribed review schema. It is non-authoritative: its 31-question reward is distinct from Harbor verifier reward and any indexed outcome grade.

## Evidence model

The evaluator first makes a complete inventory within the bounded preserved-run tree. It then applies deterministic adapters to all plausible tables, JSON records, source files, logs, reports, and plots. Every answer is one of:

- `computed`: evaluator transformed discovered artifacts and calculated the result;
- `extracted`: direct preserved evidence establishes the result;
- `not_established_after_inventory`: exhaustive bounded discovery found no sufficient evidence;
- `invalid`: a discovered artifact is incompatible, ambiguous, or fails semantic validation.

`missing` is a presentation alias for the last two non-passing states; it is never inferred merely because one conventional filename is absent.

## Question routing

| Questions | Evaluator route |
|---|---|
| Q1–Q2 | Result metadata adapter. |
| Q3–Q5, Q7–Q9, Q12–Q13, Q29–Q30 | Source/report/log extraction with cited evidence. |
| Q6 | Partition-table adapter and event-ID intersection calculation. |
| Q10, Q16 | Selected-candidate adapter, multiplicity and jet-overlap calculation. |
| Q11 | Score/mass adapter and deterministic Pearson-correlation calculation. |
| Q14–Q15, Q26–Q28 | Reviewer-generated score/mass diagnostic inputs with explicit quantity, unit, candidate-count normalization, finite-value checks, and discovered final-inference partition. |
| Q17–Q25 | Reconstruct the labeled candidate universe from evaluator-owned raw ROOT input for the discovered final-inference event set, canonicalize the recovered agent selection, then run the evaluator-owned mass-greedy comparison. |
| Q31 | Per-candidate score adapter plus frozen held-out candidates; calculate AUC against the frozen classifier baseline on its fixed modulo-10 test partition. |

## Selection adapter

`artifact_adapters.py` accepts candidate-key aliases from Parquet, CSV, or JSON and canonicalizes selected candidates to `(event_id, i, j, k)`, sorting the three jet indices. It honors an explicit boolean selection flag when one exists; otherwise, only a filename that itself declares a selection is eligible. The adapter records source, transformation, and failure reason.

This is a reviewer transformation, not a solver contract. The evaluator must retain the source path and generated canonical table in its review record.

## Raw-input reconstruction adapter

For top reconstruction, the evaluator obtains its candidate universe from the fixed `ttbar_10k.root` source documented by task provenance. It discovers the run's final inference event set (preferring `inference_test` and excluding tuning/validation artifacts), enumerates every unordered GenJet triplet for those events, treats GenJets as massless four-vectors, calculates `m(jjj)`, and applies the raw truth-triplet labels. The generated candidate table and SHA-256 of the ROOT input are retained in evaluator-local state and named in each comparison record.

This avoids trusting an agent's saved candidate mass columns and works when those columns are absent. A comparison remains unavailable only when the final selection itself cannot be recovered or fails validation.

The raw reconstruction also derives the six mass-blind classifier features used by `gaussian-naive-bayes-mass-blind/v1`. An agent AUC is eligible only when its recovered inference score covers every reconstructed candidate; both AUCs then use the fixed event-ID-modulo test partition.

Q12 and Q30 intentionally remain extraction-only: the evaluator must find affirmative final-selection evidence of no hard mass window, and a complete reproducibility record including package versions. Missing fields are never inferred from their absence.
