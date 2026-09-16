#!/usr/bin/env bash
# Runs the four-lepton counting-experiment analysis.
# Usage: ./run.sh INPUT_JSON OUTPUT_JSON
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 INPUT_JSON OUTPUT_JSON" >&2
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_JSON="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIAG_DIR="${SCRIPT_DIR}/diagnostics"

mkdir -p "$(dirname "$OUTPUT_JSON")" "$DIAG_DIR"

python3 "${SCRIPT_DIR}/analysis.py" "$INPUT_JSON" "$OUTPUT_JSON" \
    --diagnostics "$DIAG_DIR" \
    --ntoys 5000000 \
    --seed 12345
