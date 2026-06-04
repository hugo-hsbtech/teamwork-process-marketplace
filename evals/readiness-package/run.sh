#!/usr/bin/env bash
# Eval runner for the hsb-teamwork:readiness-package skill (repo-level, dev/CI only).
# Usage: ./run.sh [iteration]
# - Always self-tests the grader against the golden.
# - If the `claude` CLI is available, runs each eval case headlessly (with-skill,
#   and a no-skill baseline) and grades the outputs into a scorecard.
# - If not, explains how to run the cases and still reports the self-test.
set -uo pipefail
cd "$(dirname "$0")"
ITER="${1:-1}"
RUNS="runs/iteration-${ITER}"
mkdir -p "$RUNS"
SCORE="$RUNS/scorecard.md"
REPO_ROOT="$(cd ../.. && pwd)"

echo "# Scorecard — readiness-package — iteration ${ITER}" > "$SCORE"
echo "" >> "$SCORE"
echo "| case | mode | structural | readiness | blocking |" >> "$SCORE"
echo "|---|---|---|---|---|" >> "$SCORE"

grade() { # <doc> -> echoes "PASS|FAIL\treadiness\tblocking"
  python3 assertions.py "$1" 2>/dev/null \
    | python3 -c "import json,sys;r=json.load(sys.stdin);print(('PASS' if r['pass'] else 'FAIL')+'\t'+str(r['readiness_pct'])+'%\t'+r['blocking_satisfied'])"
}

echo "== Self-test: grading the golden =="
if g=$(grade golden/seat-management.readiness-document.md); then
  IFS=$'\t' read -r st rd bl <<<"$g"
  echo "golden: $st readiness=$rd blocking=$bl"
  echo "| golden (self-test) | fixture | $st | $rd | $bl |" >> "$SCORE"
fi

if ! command -v claude >/dev/null 2>&1; then
  echo ""
  echo "NOTE: 'claude' CLI not found — skipping live runs."
  echo "To run the cases: install Claude Code, ensure the hsb-teamwork plugin is"
  echo "available (this repo symlinks it into .claude/), then re-run ./run.sh."
  echo "" >> "$SCORE"
  echo "_Live cases skipped (claude CLI not found). Self-test only._" >> "$SCORE"
  echo "Wrote $SCORE"; exit 0
fi

# Iterate cases from evals.json
python3 -c '
import json
for e in json.load(open("evals.json"))["evals"]:
    print("\t".join([str(e["id"]), e["name"], e.get("seed","") or "", e["prompt"]]))
' | while IFS=$'\t' read -r id name seed prompt; do
  for mode in with_skill baseline; do
    OUT="$RUNS/eval-${id}/${mode}"; mkdir -p "$OUT"
    [ -n "$seed" ] && cp "$seed" "$OUT/seed.md" 2>/dev/null || true
    p="${prompt//\{OUT\}/$OUT}"
    echo "== eval $id ($name) [$mode] =="
    # NOTE: redirect claude's stdin from /dev/null. This loop is fed by a pipe
    # (the python3 case list), and `claude -p` reads stdin — without </dev/null it
    # drains the remaining case lines, so the loop runs only once AND the agent
    # receives the leaked lines as instructions (running the wrong cases). See the
    # case-list pipe at the `| while read` above.
    if [ "$mode" = "baseline" ]; then
      # Baseline: same task, explicitly WITHOUT the skill, from a clean cwd.
      ( cd "$REPO_ROOT" && claude -p "Do NOT use any skill or plugin. $p" ) </dev/null >"$OUT/agent.log" 2>&1 || true
    else
      ( cd "$REPO_ROOT" && claude -p "$p" ) </dev/null >"$OUT/agent.log" 2>&1 || true
    fi
    if [ -f "$OUT/readiness-document.md" ]; then
      res=$(grade "$OUT/readiness-document.md") || res="FAIL\t-\t-"
      IFS=$'\t' read -r st rd bl <<<"$res"
    else
      st="NO-OUTPUT"; rd="-"; bl="-"
    fi
    echo "| $name | $mode | $st | $rd | $bl |" >> "$SCORE"
  done
done

echo ""
echo "Wrote $SCORE"
echo "Next: have an LLM grade each with_skill/readiness-document.md against rubric.md"
echo "(Layer 2, qualitative) and append the 1-5 scores to the scorecard."
