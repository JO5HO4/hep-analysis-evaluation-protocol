# tth-diphoton-bdt

Top-associated H->gamma gamma BDT categorization analysis.

This pipeline performs hadronic BDT categorization for the ttH and tH processes using ATLAS open-data GamGam samples.

## Directory Structure

- `analysis/`: Python modules for event selection, feature engineering, BDT training, and categorization.
- `config/`: Configuration files for the analysis.
- `data/`: Symlinks or copies of input data (not committed).
- `scripts/`: Entry-point scripts to run the full analysis.
- `tests/`: Unit tests for analysis code.

## Usage

Set the `TB_HYY_INPUTS` environment variable to point to the ATLAS open-data GamGam directory.

Run the analysis with:

```bash
python scripts/run_analysis.py
```

Results will be written to `/root/results/tth-diphoton-bdt`.
