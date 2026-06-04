#!/usr/bin/env python3
"""Fan-out detector for a headless origination-brainstorm run.

Grades *how* the document got built, not the document itself. assertions.py can
pass on an artifact the model produced inline — so without this, the eval can't
tell an orchestrated run (the skill spawning its subagents) from a model that read
the template and one-shot the file while narrating a pipeline that never ran. It
also measures whether independent agents went out in the same turn, since spawning
one at a time and awaiting each is what makes a run drag.

Input: a stream-json trace (one JSON object per line) from
    claude -p --output-format stream-json --verbose ...
Output (stdout): a single JSON verdict object. Exit 0 always (it reports, it
doesn't gate the runner).

Verdict fields:
  agents                – sorted list of distinct subagent_type values spawned
  distinct              – len(agents)
  core_covered          – which of the CORE pipeline agents were spawned
  max_parallel_in_turn  – most Agent calls emitted in a single assistant message
                          (>= 2 proves same-turn parallel fan-out)
  parallel_turns        – how many assistant turns spawned >= 2 agents
  total_spawns          – total Agent calls across the run
  strategist_extractor_in_turn – whether Strategist and Evidence Extractor were
                          spawned together in one turn (the loop's parallel pair)
  fanout_pass           – True iff >=3 CORE agents ran AND at least one turn
                          spawned >= 2 agents in parallel
"""
import json
import sys

# The subagent_types a real origination run goes through. We require coverage of
# most of these, not all, so an honest headless run that skips an optional agent
# (e.g. glossary-keeper, gap-reporter) still passes. Unlike readiness, origination
# has no triage gate and no per-section drafter fan-out — its capture loop is
# interactive — so the parallel levers here are the Strategist ∥ Extractor pair and
# the production trio, plus incremental auditing across iterations.
CORE = {
    "hsb-source-indexer",
    "hsb-template-analyst",
    "hsb-question-strategist",
    "hsb-evidence-extractor",
    "hsb-ledger-writer",
    "hsb-doc-updater",
    "hsb-confidence-auditor",
}

# Claude Code's subagent-spawn tool is "Task"; accept "Agent" too for forward-compat.
SPAWN_TOOLS = {"Task", "Agent"}

# The capture loop's parallel pair (read-only proposers); both in one turn is the
# cheap, always-available lever against slow runs.
LOOP_PAIR = {"hsb-question-strategist", "hsb-evidence-extractor"}


def parse(path):
    seen = set()
    total_spawns = 0
    parallel_turns = 0
    max_in_turn = 0
    strategist_extractor_in_turn = False
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
            here = set()
            for t in tasks:
                st = (t.get("input") or {}).get("subagent_type")
                if st:
                    seen.add(st)
                    here.add(st)
            if LOOP_PAIR <= here:
                strategist_extractor_in_turn = True
    covered = CORE & seen
    return {
        "agents": sorted(seen),
        "distinct": len(seen),
        "core_covered": sorted(covered),
        "max_parallel_in_turn": max_in_turn,
        "parallel_turns": parallel_turns,
        "total_spawns": total_spawns,
        "strategist_extractor_in_turn": strategist_extractor_in_turn,
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
