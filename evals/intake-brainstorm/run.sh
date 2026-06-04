#!/usr/bin/env bash
# Eval runner for the hsb-teamwork:intake-brainstorm skill (repo-level, dev/CI only).
# Usage: ./run.sh [iteration]
# - Always self-tests the grader against the golden, and lays out a viewer run
#   for it (so ./view.sh works even without the `claude` CLI).
# - If the `claude` CLI is available, runs each eval case headlessly (with-skill,
#   and a no-skill baseline) and grades the outputs into a scorecard.
# - Emits the eval-viewer layout per run (outputs/ + eval_metadata.json +
#   grading.json) and a workspace benchmark.json. View with ./view.sh [iteration].
set -uo pipefail
cd "$(dirname "$0")"
ITER="${1:-1}"
RUNS="runs/iteration-${ITER}"
mkdir -p "$RUNS"
SCORE="$RUNS/scorecard.md"
REPO_ROOT="$(cd ../.. && pwd)"

# --- Eval safety guard -------------------------------------------------------
# An eval must TEST, never mutate the repo. The skill runs headlessly with broad
# permissions, so a `git` shim is prepended to PATH for the claude calls: it lets
# the skill READ git (session-root resolution uses `git rev-parse`) but hard-fails
# any history/working-tree mutation (commit, add, push, ...). This is what stops a
# headless run from committing to the repo. Flags like --disallowedTools do NOT
# block git under bypassPermissions, so we enforce it at the binary level.
REAL_GIT="$(command -v git)"
GIT_SHIM_DIR="$(mktemp -d)"
cat > "$GIT_SHIM_DIR/git" <<SHIM
#!/bin/sh
case "\$1" in
  commit|add|push|reset|checkout|switch|merge|rebase|stash|rm|mv|apply|am|cherry-pick|revert|restore|clean|gc|update-index|fetch|pull|clone|init|worktree|tag|branch|remote|config)
    echo "eval: 'git \$1' is disabled — eval tests must not mutate the repo" >&2; exit 13;;
  *) exec "$REAL_GIT" "\$@";;
esac
SHIM
chmod +x "$GIT_SHIM_DIR/git"
trap 'rm -rf "$GIT_SHIM_DIR"' EXIT
# -----------------------------------------------------------------------------

echo "# Scorecard — intake-brainstorm — iteration ${ITER}" > "$SCORE"
echo "" >> "$SCORE"
echo "| case | mode | structural | readiness | blocking |" >> "$SCORE"
echo "|---|---|---|---|---|" >> "$SCORE"

grade() { # <doc> -> echoes "PASS|FAIL\treadiness\tblocking" (exit 0 even when the doc FAILS the grader)
  # `|| true` swallows assertions.py's exit-1-on-fail so pipefail doesn't make a
  # legitimately-graded-but-failing doc look like a grade() error to the caller.
  { python3 assertions.py "$1" 2>/dev/null || true; } \
    | python3 -c "import json,sys;r=json.load(sys.stdin);print(('PASS' if r['pass'] else 'FAIL')+'\t'+str(r['readiness_pct'])+'%\t'+r['blocking_satisfied'])"
}

# write_meta <run_dir> <eval_id> <prompt> -> eval_metadata.json (read by the viewer)
write_meta() {
  python3 -c '
import json,sys
run_dir,eid,prompt=sys.argv[1],sys.argv[2],sys.argv[3]
try: eid=int(eid)
except ValueError: pass
json.dump({"eval_id":eid,"prompt":prompt},open(run_dir+"/eval_metadata.json","w"),indent=2)
' "$1" "$2" "$3"
}

# assemble_run <run_dir> <doc> -> outputs/target-document.md + grading.json
assemble_run() {
  mkdir -p "$1/outputs"
  cp "$2" "$1/outputs/target-document.md"
  python3 assertions.py "$1/outputs/target-document.md" --grading-json "$1/grading.json" >/dev/null 2>&1 || true
}

echo "== Self-test: grading the golden =="
if g=$(grade golden/queue-voting.target-document.md); then
  IFS=$'\t' read -r st rd bl <<<"$g"
  echo "golden: $st readiness=$rd blocking=$bl"
  echo "| golden (self-test) | fixture | $st | $rd | $bl |" >> "$SCORE"
fi
# Always lay out a viewer run for the golden so ./view.sh is demonstrable
# without the claude CLI (it appears under the Outputs tab).
# eval_id -1 keeps it an integer (the viewer sorts runs by eval_id and cannot
# compare a string id against the integer ids of the live cases); -1 sorts first.
GRUN="$RUNS/golden-selftest"; mkdir -p "$GRUN"
write_meta "$GRUN" -1 "Self-test: grade the committed golden target document (golden/queue-voting.target-document.md). No agent run — this populates the eval-viewer so it can be demonstrated without the claude CLI."
assemble_run "$GRUN" golden/queue-voting.target-document.md

if ! command -v claude >/dev/null 2>&1; then
  echo ""
  echo "NOTE: 'claude' CLI not found — skipping live runs."
  echo "To run the cases: install Claude Code, ensure the hsb-teamwork plugin is"
  echo "available (this repo symlinks it into .claude/), then re-run ./run.sh."
  echo "" >> "$SCORE"
  echo "_Live cases skipped (claude CLI not found). Self-test only._" >> "$SCORE"
  echo "Wrote $SCORE"
  echo "View the golden self-test: ./view.sh ${ITER}   (headless: ./view.sh ${ITER} --static review.html)"
  exit 0
fi

# Iterate cases from evals.json.
# Fields are joined with the ASCII Unit Separator (\x1f), NOT a tab: tab is an IFS
# *whitespace* char, so `read` collapses consecutive tabs and an empty `seed` field
# would shift the prompt into `seed`, leaving the prompt empty (claude -p "" errors).
# \x1f is non-whitespace, so empty fields are preserved.
python3 -c '
import json
for e in json.load(open("evals.json"))["evals"]:
    print("\x1f".join([str(e["id"]), e["name"], e.get("seed","") or "", e["prompt"]]))
' | while IFS=$'\x1f' read -r id name seed prompt; do
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
      ( cd "$REPO_ROOT" && PATH="$GIT_SHIM_DIR:$PATH" claude -p --permission-mode bypassPermissions "Do NOT use any skill or plugin. $p" ) </dev/null >"$OUT/agent.log" 2>&1 || true
    else
      ( cd "$REPO_ROOT" && PATH="$GIT_SHIM_DIR:$PATH" claude -p --permission-mode bypassPermissions "$p" ) </dev/null >"$OUT/agent.log" 2>&1 || true
    fi
    if [ -f "$OUT/target-document.md" ]; then
      res=$(grade "$OUT/target-document.md") || res=$'FAIL\t-\t-'
      IFS=$'\t' read -r st rd bl <<<"$res"
      # Emit the eval-viewer layout for this run.
      write_meta "$OUT" "$id" "$p"
      assemble_run "$OUT" "$OUT/target-document.md"
    else
      st="NO-OUTPUT"; rd="-"; bl="-"
    fi
    echo "| $name | $mode | $st | $rd | $bl |" >> "$SCORE"
  done
done

# Aggregate a benchmark.json for the viewer's Benchmark tab (skipped if no graded runs).
if python3 ../eval-viewer/make_benchmark.py "$RUNS" --skill "hsb-teamwork:intake-brainstorm" > "$RUNS/benchmark.json" 2>/dev/null; then
  echo "Wrote $RUNS/benchmark.json"
else
  rm -f "$RUNS/benchmark.json"
fi

echo ""
echo "Wrote $SCORE"
echo "View results: ./view.sh ${ITER}   (headless/remote: ./view.sh ${ITER} --static review.html)"
echo "Next: have an LLM grade each with_skill/outputs/target-document.md against rubric.md"
echo "(Layer 2, qualitative) and append the 1-5 scores to the scorecard."
