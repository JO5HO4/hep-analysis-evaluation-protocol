#!/bin/bash
# Entry point for four-lepton Higgs search statistical analysis

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 INPUT_JSON OUTPUT_JSON"
    echo "Example: $0 /root/data/four_lepton_counts.json /root/results/results.json"
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_JSON="$2"

# Check if input file exists
if [ ! -f "$INPUT_JSON" ]; then
    echo "Error: Input file '$INPUT_JSON' not found."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_JSON")"

# Run the Python analysis script
python3 /root/submission/analyze.py "$INPUT_JSON" "$OUTPUT_JSON"

# Check if analysis completed successfully
if [ $? -eq 0 ]; then
    echo "Analysis completed successfully. Results written to $OUTPUT_JSON"
else
    echo "Error: Analysis failed."
    exit 1
fi