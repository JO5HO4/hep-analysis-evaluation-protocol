#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <INPUT_JSON> <OUTPUT_JSON>"
    exit 1
fi
python3 /root/submission/run_analysis.py "$1" "$2"
