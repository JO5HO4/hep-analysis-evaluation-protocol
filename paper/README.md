# Paper evidence inventory

This directory holds the selected latest Harbor job directories for the active
benchmark matrix.  Its layout follows `results/paper/top-reconstruction-paper-version`:

```
TASK-paper-version/AGENT/MODEL/RUN_ID/
```

Model directory names use `--` in place of `/`.  Qwen's identical Best and
Medium model is disambiguated with `--best` and `--medium`.

## Coverage

| Task | Free | Medium | Best | Total |
| --- | ---: | ---: | ---: | ---: |
| Higgs 4l significance | 5 | 5 | 5 | 15 |
| H→γγ (`tb-hyy`) | 5 | 5 | 0 | 10 |
| Top reconstruction | 5 | 5 | 5 | 15 |
| ttH diphoton BDT categorization | 5 | 5 | 0 | 10 |

The 50 copied jobs select rerun evidence over superseded attempts.  Free-tier
Higgs 4l and top-reconstruction evidence comes from
`results/free-tier-physics-20260902-rerun`; the other Free-tier jobs come from
`results/free-tier-physics-20260901`.  Medium-tier jobs come from Dongwon's
representative, remaining-15, and retry evidence roots; Best-tier Higgs comes
from Dongwon and Best-tier top reconstruction comes from Haichen.

The remaining ten matrix cells have not been run: all five Best-tier harnesses
for `tb-hyy`, and all five for `tth-diphoton-bdt-categorization`.

## Manual evidence reviews

Fresh Codex reviewers inspect the immutable bundles in `results/paper/` and
write non-authoritative rubric and workflow reports under `paper/reviews/`.
Each review covers every logical run in its selected task evidence root, not a
representative subset. Use [manual-review-prompt.md](manual-review-prompt.md)
for the exact review prompt and task-to-rubric mapping. Do not overwrite
historical reports when a rubric changes.

For a careful per-run review, use `scripts/manual-paper-review.sh`. It launches
one fresh Codex reviewer for one preserved run and writes the two Markdown
reports below `paper/reviews/`; a later Codex reviewer can synthesize those
per-run reports into a task-wide matrix report.
