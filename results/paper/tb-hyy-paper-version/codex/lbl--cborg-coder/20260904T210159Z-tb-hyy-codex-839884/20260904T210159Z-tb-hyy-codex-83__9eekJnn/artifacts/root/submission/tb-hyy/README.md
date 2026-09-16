# H -> gamma gamma Analysis Pipeline

This repository contains a self-contained pipeline for the inclusive  \to \gamma\gamma$ analysis.

## Execution
To run the analysis, execute the steering script:
```bash
bash /root/submission/tb-hyy/solve.sh
```

## Input Data
The pipeline expects ROOT files in the following layout:
- `MC/`: ATLAS open-data GamGam Monte Carlo files.
- `data/gamgam_data/`: ATLAS open-data observed-data files.

Inputs are sourced from the `TB_HYY_INPUTS` environment variable or a symlink at `/root/submission/tb-hyy/input`.

## Outputs
Results are written to `/root/results/tb-hyy`.
