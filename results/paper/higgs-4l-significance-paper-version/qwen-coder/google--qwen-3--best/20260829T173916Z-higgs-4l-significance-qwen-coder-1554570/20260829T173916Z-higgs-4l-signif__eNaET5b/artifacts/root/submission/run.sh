#!/bin/bash

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 INPUT_JSON OUTPUT_JSON"
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_JSON="$2"

# Check if input file exists
if [ ! -f "$INPUT_JSON" ]; then
    echo "Error: Input file '$INPUT_JSON' not found."
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the analysis
echo "Running statistical analysis..."
python3 "$SCRIPT_DIR/analysis.py" "$INPUT_JSON" "$OUTPUT_JSON"

# Check if analysis completed successfully
if [ $? -ne 0 ]; then
    echo "Error: Analysis failed."
    exit 1
fi

# Create diagnostics directory
DIAGNOSTICS_DIR="$(dirname "$OUTPUT_JSON")/diagnostics"
mkdir -p "$DIAGNOSTICS_DIR"

# Run plotting script
echo "Generating diagnostic plots..."
python3 "$SCRIPT_DIR/plot_diagnostics.py"

# Check if plotting completed successfully
if [ $? -ne 0 ]; then
    echo "Warning: Plotting failed, but analysis results are available."
fi

echo "Analysis complete. Results saved to $OUTPUT_JSON"
echo "Diagnostic plots saved to $DIAGNOSTICS_DIR"