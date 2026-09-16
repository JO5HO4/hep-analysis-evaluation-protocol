#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 INPUT_JSON OUTPUT_JSON" >&2
  exit 2
fi
exec python3 "$(dirname "$(readlink -f "$0")")/analyze.py" "$1" "$2"
