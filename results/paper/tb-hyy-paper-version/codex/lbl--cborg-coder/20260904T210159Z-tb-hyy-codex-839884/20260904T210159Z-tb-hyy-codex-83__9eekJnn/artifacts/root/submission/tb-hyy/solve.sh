#!/bin/bash
set -e

# Ensure we are in the right directory
cd /root/submission/tb-hyy

# Set python path to include the current directory for imports
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the analysis
python3 run_analysis.py

echo "Analysis complete. Results are in /root/results/tb-hyy"
