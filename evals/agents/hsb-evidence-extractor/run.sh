#!/usr/bin/env bash
# Thin wrapper -> the shared agnostic runner. Usage: ./run.sh [iteration]
#   SELFTEST_ONLY=1 ./run.sh   # grader self-test only (no claude CLI)
#   RUN_BASELINE=1  ./run.sh   # also run the no-spec baseline (benchmark/lift)
set -euo pipefail
cd "$(dirname "$0")"
exec ../_harness/run_agent.sh agent.json "${1:-1}"
