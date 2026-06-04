#!/usr/bin/env bash
# Launch the SHARED eval-viewer on an iteration's runs (same viewer the skills use).
#   ./view.sh [iteration] [extra generate_review.py args]
#   ./view.sh 1 --static review.html   # headless/remote
set -euo pipefail
cd "$(dirname "$0")"
ITER="${1:-1}"; shift || true
WS="runs/iteration-${ITER}"
[ -d "$WS" ] || { echo "No $WS — run ./run.sh ${ITER} first."; exit 1; }
BENCH=()
[ -f "$WS/benchmark.json" ] && BENCH=(--benchmark "$WS/benchmark.json")
exec python3 ../../eval-viewer/generate_review.py "$WS" \
  --skill-name "hsb-teamwork agent: hsb-evidence-extractor" "${BENCH[@]}" "$@"
