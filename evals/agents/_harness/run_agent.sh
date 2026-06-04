#!/usr/bin/env bash
# Agnostic single-agent eval runner (repo-level, dev/CI only).
#   ./run_agent.sh <agent.json> [iteration]
#
# It is the per-agent analogue of each skill's run.sh:
#  - ALWAYS self-tests the deterministic grader against each case's golden return
#    and lays out a viewer run for it, so ./view.sh works without the `claude` CLI.
#  - If the `claude` CLI is present (and SELFTEST_ONLY is unset), it invokes the
#    agent IN ISOLATION on each case fixture — the agent's own role spec (the .md
#    body) as the prompt, its declared tools as the allowlist, a throwaway PHASE_DIR
#    as the sandbox — captures the structured return it prints, and grades it.
#  - Optionally (RUN_BASELINE=1) also runs a no-spec baseline for the benchmark/lift.
#
# Read-only agents (tools = Read/Grep/Glob, no Write/Edit) return via STDOUT, so the
# single-writer boundary holds by construction; the runner still snapshots the sandbox
# to verify nothing was mutated (readonly_boundary).
set -uo pipefail
HARNESS="$(cd "$(dirname "$0")" && pwd)"
AGENT_JSON="${1:?usage: run_agent.sh <agent.json> [iteration]}"
AGENT_JSON="$(cd "$(dirname "$AGENT_JSON")" && pwd)/$(basename "$AGENT_JSON")"
AGENT_DIR="$(dirname "$AGENT_JSON")"
cd "$AGENT_DIR"
ITER="${2:-1}"
RUNS="runs/iteration-${ITER}"; mkdir -p "$RUNS"
SCORE="$RUNS/scorecard.md"
REPO_ROOT="$(cd "$HARNESS/../../.." && pwd)"

# Agnostic config pulled from the agent's own spec + agent.json.
AGENT_NAME="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["agent"])' "$AGENT_JSON")"
SPEC_REL="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["agent_spec"])' "$AGENT_JSON")"
SKILL_REL="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("skill_dir",""))' "$AGENT_JSON")"
SPEC_ABS="$REPO_ROOT/$SPEC_REL"
SKILL_ABS="$REPO_ROOT/$SKILL_REL"
RET_FILE="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["return"].get("file","return.json"))' "$AGENT_JSON")"
RET_INSTR="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["return"].get("instructions",""))' "$AGENT_JSON")"
TOOLS="$(python3 -c 'import sys;sys.path.insert(0,sys.argv[2]);import agentlib;print(",".join(agentlib.parse_agent_spec(sys.argv[1])["tools"]))' "$SPEC_ABS" "$HARNESS")"

# --- Eval safety guard (identical intent to the skill runners) ----------------
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

echo "# Scorecard — ${AGENT_NAME} — iteration ${ITER}" > "$SCORE"
echo "" >> "$SCORE"
echo "| case | mode | structural | passed/total |" >> "$SCORE"
echo "|---|---|---|---|" >> "$SCORE"

write_meta() { # <run_dir> <eval_id> <prompt>
  python3 -c '
import json,sys
d,eid,prompt=sys.argv[1],sys.argv[2],sys.argv[3]
try: eid=int(eid)
except ValueError: pass
json.dump({"eval_id":eid,"prompt":prompt},open(d+"/eval_metadata.json","w"),indent=2)
' "$1" "$2" "$3"
}

snapshot() { # <dir> <out.json> — sha of every file under dir
  python3 -c '
import hashlib,json,os,sys
root,out=sys.argv[1],sys.argv[2]
h={}
for dp,_,fns in os.walk(root):
    for fn in fns:
        p=os.path.join(dp,fn)
        rel=os.path.relpath(p,root)
        try: h[rel]=hashlib.sha256(open(p,"rb").read()).hexdigest()
        except OSError: pass
json.dump(h,open(out,"w"))
' "$1" "$2"
}

extract_json() { # stdin raw -> stdout first balanced {...} (or the raw text)
  python3 -c '
import sys,json,re
s=sys.stdin.read()
# strip code fences if any
m=re.search(r"```(?:json)?\s*(.*?)```",s,re.DOTALL)
cand=m.group(1) if m else s
i=cand.find("{")
if i<0: sys.stdout.write(s); sys.exit()
depth=0
for j in range(i,len(cand)):
    if cand[j]=="{":depth+=1
    elif cand[j]=="}":
        depth-=1
        if depth==0:
            blob=cand[i:j+1]
            try: json.loads(blob)
            except Exception: pass
            sys.stdout.write(blob); sys.exit()
sys.stdout.write(s)
'
}

# Per-case ids from agent.json
CASES="$(python3 -c 'import json,sys;print(" ".join(str(c["id"]) for c in json.load(open(sys.argv[1]))["cases"]))' "$AGENT_JSON")"

echo "== Self-test: grade each case golden return =="
for id in $CASES; do
  GOLD="golden/case-${id}.return.json"
  NAME="$(python3 -c 'import json,sys;c=[c for c in json.load(open(sys.argv[1]))["cases"] if str(c["id"])==sys.argv[2]][0];print(c.get("name","case-"+sys.argv[2]))' "$AGENT_JSON" "$id")"
  [ -f "$GOLD" ] || { echo "  (no golden for case $id — skipping self-test)"; continue; }
  GRUN="$RUNS/eval-${id}/golden"; mkdir -p "$GRUN/outputs"
  cp "$GOLD" "$GRUN/outputs/$RET_FILE"
  python3 "$HARNESS/grade.py" "$AGENT_JSON" "$id" "$GOLD" \
    --phase-dir "fixtures/case-${id}" --grading-json "$GRUN/grading.json" >/dev/null 2>&1 || true
  st=$(python3 -c 'import json,sys;r=json.load(open(sys.argv[1]));print(("PASS" if r["summary"]["failed"]==0 else "FAIL")+"\t"+str(r["summary"]["passed"])+"/"+str(r["summary"]["total"]))' "$GRUN/grading.json" 2>/dev/null || printf 'ERR\t-')
  IFS=$'\t' read -r v pt <<<"$st"
  echo "  case $id ($NAME): golden self-test $v ($pt)"
  write_meta "$GRUN" "$id" "SELF-TEST: grade the committed golden return for case '$NAME' (golden/case-${id}.return.json). No agent run — demonstrates the grader + viewer without the claude CLI."
  echo "| $NAME | golden (self-test) | $v | $pt |" >> "$SCORE"
done

run_one() { # <id> <name> <mode: agent|baseline>
  local id="$1" name="$2" mode="$3"
  local fix="fixtures/case-${id}"
  [ -d "$fix" ] || { echo "  (no fixtures for case $id) "; return; }
  local OUT="$RUNS/eval-${id}/${mode}"; mkdir -p "$OUT/outputs"
  local SBX; SBX="$(mktemp -d)"
  cp -r "$fix/." "$SBX/" 2>/dev/null || true
  snapshot "$SBX" "$OUT/snap_before.json"
  local task; task="$(python3 -c 'import json,sys;c=[c for c in json.load(open(sys.argv[1]))["cases"] if str(c["id"])==sys.argv[2]][0];print(c["prompt"].replace("{OUT}",sys.argv[3]))' "$AGENT_JSON" "$id" "$SBX")"
  local header="You are being run as a STANDALONE agent for evaluation. Stay strictly within your role.
Injected paths: SKILL_DIR=${SKILL_ABS} ; PHASE_DIR=${SBX} .
Read only what your role specifies under PHASE_DIR/SKILL_DIR. Do NOT write any file.
${RET_INSTR}
"
  local prompt
  if [ "$mode" = "baseline" ]; then
    # No role spec — generic instruction only (the lift baseline).
    prompt="${header}
--- TASK ---
${task}"
  else
    prompt="${header}
--- YOUR ROLE SPEC ---
$(cat "$SPEC_ABS")
--- TASK ---
${task}"
  fi
  # Pre-approve the agent's declared (read-only) tools via --allowedTools and use the
  # DEFAULT permission mode. We deliberately avoid --permission-mode bypassPermissions:
  # it maps to --dangerously-skip-permissions, which Claude Code blocks under root (the
  # case in many CI/remote containers). Allowlisting the read tools is enough — headless
  # `-p` auto-approves listed tools and auto-denies anything else (no hang, no prompt).
  # Feed the prompt via STDIN (most robust across CLI versions; passing it as a
  # positional arg alongside --allowedTools proved brittle). --print reads stdin.
  local raw
  raw="$( printf '%s' "$prompt" | ( cd "$SBX" && PATH="$GIT_SHIM_DIR:$PATH" timeout 420 claude -p --allowedTools "$TOOLS" ) 2>"$OUT/agent.log" )"
  printf '%s' "$raw" | extract_json > "$OUT/outputs/$RET_FILE"
  snapshot "$SBX" "$OUT/snap_after.json"
  rm -rf "$SBX"
  python3 "$HARNESS/grade.py" "$AGENT_JSON" "$id" "$OUT/outputs/$RET_FILE" \
    --phase-dir "$fix" --snapshot-before "$OUT/snap_before.json" \
    --snapshot-after "$OUT/snap_after.json" --grading-json "$OUT/grading.json" >/dev/null 2>&1 || true
  local st
  st=$(python3 -c 'import json,sys;r=json.load(open(sys.argv[1]));print(("PASS" if r["summary"]["failed"]==0 else "FAIL")+"\t"+str(r["summary"]["passed"])+"/"+str(r["summary"]["total"]))' "$OUT/grading.json" 2>/dev/null || printf 'NO-OUTPUT\t-')
  local v pt; IFS=$'\t' read -r v pt <<<"$st"
  write_meta "$OUT" "$id" "[$mode] $task"
  echo "  case $id ($name) [$mode]: $v ($pt)"
  echo "| $name | $mode | $v | $pt |" >> "$SCORE"
}

if ! command -v claude >/dev/null 2>&1 || [ -n "${SELFTEST_ONLY:-}" ]; then
  echo ""
  echo "NOTE: live agent runs skipped (no 'claude' CLI or SELFTEST_ONLY set)."
  echo "" >> "$SCORE"
  echo "_Live runs skipped; golden self-test only._" >> "$SCORE"
  echo "Wrote $SCORE"
  echo "View: ./view.sh ${ITER}   (headless: ./view.sh ${ITER} --static review.html)"
  exit 0
fi

echo ""
echo "== Live: invoke ${AGENT_NAME} in isolation (tools: ${TOOLS}) =="
for id in $CASES; do
  NAME="$(python3 -c 'import json,sys;c=[c for c in json.load(open(sys.argv[1]))["cases"] if str(c["id"])==sys.argv[2]][0];print(c.get("name","case-"+sys.argv[2]))' "$AGENT_JSON" "$id")"
  run_one "$id" "$NAME" agent
  [ -n "${RUN_BASELINE:-}" ] && run_one "$id" "$NAME" baseline
done

# Optional benchmark (agent vs baseline lift) when baselines were produced.
if [ -n "${RUN_BASELINE:-}" ] && python3 "$HARNESS/make_benchmark.py" "$RUNS" --agent "$AGENT_NAME" --evals "$AGENT_JSON" > "$RUNS/benchmark.json" 2>/dev/null; then
  echo "Wrote $RUNS/benchmark.json"
else
  rm -f "$RUNS/benchmark.json"
fi

echo ""
echo "Wrote $SCORE"
echo "View: ./view.sh ${ITER}   (headless: ./view.sh ${ITER} --static review.html)"
echo "Next: have an LLM grade each agent/outputs/${RET_FILE} against rubric.md (Layer 2) and append 1-5 scores."
