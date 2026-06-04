#!/usr/bin/env bash
# Launch the eval-viewer on an iteration's runs.
#   ./view.sh [iteration] [extra generate_review.py args]
# Live server (opens a browser):   ./view.sh 1
# Headless / remote (no browser):  ./view.sh 1 --static review.html
set -euo pipefail
cd "$(dirname "$0")"
ITER="${1:-1}"; shift || true
WS="runs/iteration-${ITER}"
[ -d "$WS" ] || { echo "No $WS — run ./run.sh ${ITER} first."; exit 1; }
BENCH=()
[ -f "$WS/benchmark.json" ] && BENCH=(--benchmark "$WS/benchmark.json")
exec python3 ../eval-viewer/generate_review.py "$WS" \
  --skill-name "hsb-teamwork:origination-brainstorm" "${BENCH[@]}" "$@"
