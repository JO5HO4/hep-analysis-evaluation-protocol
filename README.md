# HEP analysis evaluation protocol

Standalone development repository for the artifact-adaptive evaluation protocol
and the retained paper evidence used to exercise it.

## Contents

- `evaluation/` contains the evaluation prompts, rubrics, task notes, and
  evaluator-side baseline implementations.
- `prompts/` contains task-local prompt copies that motivate the protocol.
- `paper/reviews/` contains the non-authoritative evidence reviews, including
  the top-reconstruction traceability pilot and its 31-question protocol.
- `paper/plots/` contains figures generated from the machine-readable review
  records.
- `results/paper/` contains retained, clean paper-run evidence organized by
  task, harness, and model.
- `contracts/` contains the RunRecord v1 interface reference used to keep
  execution evidence distinct from evaluation.

## Scope and interpretation

This is an evaluation-development repository, not a benchmark execution
repository. Harbor verifier rewards are preserved as execution evidence. The
traceability reviews and evaluator-side comparisons are explicitly
non-authoritative and must not be presented as task outcome grades.

The top-reconstruction pilot uses an exhaustive but bounded evidence inventory:
each retained run is evaluated from its preserved evidence tree, without an
agent-output schema requirement. The evaluator reconstructs comparison inputs
where possible and records missing evidence explicitly.

## Regenerating the pilot plots

```bash
python paper/reviews/top-reconstruction-traceability-pilot/generate.py
python paper/reviews/top-reconstruction-traceability-pilot/figures/generate_pilot_figures.py
python paper/reviews/top-reconstruction-traceability-pilot/validate.py
```

The generator needs the Python dependencies declared by the included evaluator
modules, plus `matplotlib`, `pandas`, `pyarrow`, and `uproot`. It may retrieve
the documented evaluator-owned raw comparison sample; that machine-local cache
is intentionally not versioned here.

## Export provenance

Initial contents were exported from the retained paper evidence and
evaluation-development material in the collider benchmark workspace at source
revision `743442d8bc24165d732dd96bd772ead93a7038b6`. Host-specific absolute
paths have been redacted from the export.
