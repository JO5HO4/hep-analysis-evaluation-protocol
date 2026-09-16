#!/bin/bash
set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 INPUT_JSON OUTPUT_JSON"
    exit 1
fi

INPUT_JSON=$1
OUTPUT_JSON=$2

python3 /root/submission/analysis.py "$INPUT_JSON" "$OUTPUT_JSON"
