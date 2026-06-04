#!/usr/bin/env python3
"""Fan-out detector for a headless readiness-package run.

Grades *how* the document got built, not the document itself. assertions.py can
pass on an artifact the model produced inline — so without this, the eval can't
tell an orchestrated run (the skill spawning its subagents) from a model that
read the template and one-shot the file while narrating a pipeline that never ran.

Input: a stream-json trace (one JSON object per line) from
    claude -p --output-format stream-json --verbose ...
Output (stdout): a single JSON verdict object. Exit 0 always (it reports, it
doesn't gate the runner).

Verdict fields:
  agents                – sorted list of distinct subagent_type values spawned
  distinct              – len(agents)
  core_covered          – which of the CORE pipeline agents were spawned
  max_parallel_in_turn  – most Task calls emitted in a single assistant message
                          (>= 2 proves same-turn parallel fan-out)
  parallel_turns        – how many assistant turns spawned >= 2 agents
  total_spawns          – total Task calls across the run
  fanout_pass           – True iff >=3 CORE agents ran AND at least one turn
                          spawned >= 2 agents in parallel
"""
import json
import sys

# The subagent_types a real Phase 1-2 run must go through. We require coverage of
# most of these, not all, so an honest headless run that skips an optional agent
# (e.g. glossary-keeper) still passes.
CORE = {
    "intake-source-indexer",
    "intake-template-analyst",
    "readiness-inheritor",
    "readiness-drafter",
    "intake-doc-updater",
}

# Claude Code's subagent-spawn tool is "Task"; accept "Agent" too for forward-compat.
SPAWN_TOOLS = {"Task", "Agent"}


def parse(path):
    seen = set()
    total_spawns = 0
    parallel_turns = 0
    max_in_turn = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "assistant":
                continue
            blocks = (ev.get("message") or {}).get("content") or []
            tasks = [
                b for b in blocks
                if b.get("type") == "tool_use" and b.get("name") in SPAWN_TOOLS
            ]
            n = len(tasks)
            if n == 0:
                continue
            total_spawns += n
            max_in_turn = max(max_in_turn, n)
            if n >= 2:
                parallel_turns += 1
            for t in tasks:
                st = (t.get("input") or {}).get("subagent_type")
                if st:
                    seen.add(st)
    covered = CORE & seen
    return {
        "agents": sorted(seen),
        "distinct": len(seen),
        "core_covered": sorted(covered),
        "max_parallel_in_turn": max_in_turn,
        "parallel_turns": parallel_turns,
        "total_spawns": total_spawns,
        "fanout_pass": len(covered) >= 3 and max_in_turn >= 2,
    }


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: fanout.py <trace.jsonl>"}))
        return
    try:
        print(json.dumps(parse(sys.argv[1])))
    except FileNotFoundError:
        print(json.dumps({"error": "trace not found", "fanout_pass": False,
                          "distinct": 0, "max_parallel_in_turn": 0}))


if __name__ == "__main__":
    main()
