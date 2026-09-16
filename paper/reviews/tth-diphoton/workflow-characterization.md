# ttH diphoton workflow characterization

Protocol `workflow-characterization/v1`, 2026-09-09. This is descriptive only:
it has no workflow score, rank, or weighted total. Included and excluded paths
are exactly those listed in `evaluation-report.md`.

| Run | Harbor status / verifier reward | Commands | Failed commands | Error signatures | Recoveries | Analysis iterations | Superseded iterations | Final iteration | Reproducibility | Artifact coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| R1--R15 | completed / 0.000000 | not established | not established | not established | not established | see profiles | not established | not established | not established | see profiles |

| Run | Tool categories / observed completed stages | Artifact coverage and directly evidenced validation |
|---|---|---|
| R1 | shell, source editing, Python, ROOT/RooFit, plotting; input inspection→preparation→training→optimization→fit→plotting→reporting | 72 outputs/12 sources; scalar-vectorized validation 0 mismatches; four threshold attempts |
| R2 | Python, ROOT/RooFit, plotting; training→optimization→fit→reporting | 61 outputs/6 sources |
| R3 | not established | no readable result root/source |
| R4 | Python, ROOT/RooFit, plotting; preparation→training→optimization→fit→plotting→reporting | 72 outputs/3 sources; saved AUC and fit checks |
| R5 | Python, ROOT/RooFit, plotting; training→fit→plotting→reporting | 75 outputs/2 sources |
| R6 | shell, source editing, Python; reporting | 35 outputs/8 sources |
| R7 | not established | no readable result root/source |
| R8 | source editing, Python | 3 sources, no saved result root |
| R9 | Python, file inspection; reporting | 13 outputs/3 sources |
| R10 | source editing, Python | 17 outputs/2 sources |
| R11 | Python, ROOT/RooFit, plotting; training→optimization→fit→plotting→reporting | 53 outputs/5 sources |
| R12 | shell, source editing, Python, ROOT/RooFit; training→fit→reporting | 35 outputs/8 sources |
| R13 | Python, ROOT/RooFit, plotting; preparation→training→optimization→fit→plotting→reporting | 70 outputs/5 sources; class-balance/fit checks, one accepted and one rejected split |
| R14 | Python, ROOT/RooFit, plotting; training→fit→plotting→reporting | 74 outputs/3 sources |
| R15 | source editing, Python; reporting | 5 outputs/5 sources |

For every run, `agent/`, `trial.log`, submitted source, artifact root and
`result.json` were inspected. No preserved transcript has a complete
exit-status-resolved command stream, so command, failure, error-signature and
recovery counts are `not established`, never inferred as zero. No clean-output
rerun with stated agreement tolerance is preserved.
