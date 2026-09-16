#!/usr/bin/env bash
# Usage: run.sh INPUT_JSON OUTPUT_JSON
# Runs the full four-lepton counting analysis and writes the results JSON.
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "usage: $0 INPUT_JSON OUTPUT_JSON" >&2
    exit 2
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# NTOYS / SEED may be overridden from the environment.
exec python3 "$HERE/analysis.py" "$1" "$2" \
    --ntoys "${NTOYS:-10000000}" \
    --seed "${SEED:-20260829}" \
    --diagnostics "${DIAGNOSTICS_DIR:-$HERE/diagnostics}"
