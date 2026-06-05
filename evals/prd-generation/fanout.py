#!/usr/bin/env python3
"""Fan-out detector for a headless prd-generation run.

Grades *how* the PRD got merged, not the document itself. assertions.py can pass on
an artifact the model produced inline — so without this, the eval can't tell an
orchestrated merge (the skill spawning its subagents) from a model that read the two
halves and one-shot the file while narrating a pipeline that never ran.

Input: a stream-json trace (one JSON object per line) from
    claude -p --output-format stream-json --verbose ...
Output (stdout): a single JSON verdict object. Exit 0 always (it reports, it doesn't gate).

Verdict fields:
  agents                  – sorted list of distinct subagent_type values spawned
  distinct                – len(agents)
  core_covered            – which of the CORE pipeline agents were spawned
  max_parallel_in_turn    – most Task calls emitted in a single assistant message
                            (>= 2 proves same-turn parallel fan-out)
  parallel_turns          – how many assistant turns spawned >= 2 agents
  total_spawns            – total Task calls across the run
  reconciler_present      – whether the Reconciler ran (the merge-defining proposer:
                            the PRD reconciles the two halves, it doesn't just staple them)
  inheritor_fanout_in_turn  – most hsb-stage-inheritor calls in a single turn
                            (>= 2 proves Part A ∥ Part B inherited in parallel)
  synthesizer_fanout_in_turn – most hsb-synthesizer calls in a single turn
                            (>= 2 proves the derived sections fanned out)
  fanout_pass             – True iff >=3 CORE agents ran AND at least one turn
                            spawned >= 2 agents in parallel
"""
import json
import sys

# The subagent_types a real merge must go through. We require coverage of most of
# these, not all, so an honest headless run that skips an optional agent (e.g.
# glossary-keeper) still passes. The merge maps onto the Inheritor (carries each
# half), the Synthesizer (composes the derived sections), and the Reconciler
# (resolves the scope) — all reused engine agents (no new agents for this skill).
CORE = {
    "hsb-source-indexer",
    "hsb-template-analyst",
    "hsb-stage-inheritor",
    "hsb-synthesizer",
    "hsb-reconciler",
    "hsb-doc-updater",
}

# Claude Code's subagent-spawn tool is "Task"; accept "Agent" too for forward-compat.
SPAWN_TOOLS = {"Task", "Agent"}

INHERITOR = "hsb-stage-inheritor"   # fans out per PART (A from the RP, B from the TA)
SYNTHESIZER = "hsb-synthesizer"     # fans out per derived SECTION


def parse(path):
    seen = set()
    total_spawns = 0
    parallel_turns = 0
    max_in_turn = 0
    inheritor_fanout_in_turn = 0
    synthesizer_fanout_in_turn = 0
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
            inheritors_here = 0
            synthesizers_here = 0
            for t in tasks:
                st = (t.get("input") or {}).get("subagent_type")
                if st:
                    seen.add(st)
                    if st == INHERITOR:
                        inheritors_here += 1
                    if st == SYNTHESIZER:
                        synthesizers_here += 1
            inheritor_fanout_in_turn = max(inheritor_fanout_in_turn, inheritors_here)
            synthesizer_fanout_in_turn = max(synthesizer_fanout_in_turn, synthesizers_here)
    covered = CORE & seen
    return {
        "agents": sorted(seen),
        "distinct": len(seen),
        "core_covered": sorted(covered),
        "max_parallel_in_turn": max_in_turn,
        "parallel_turns": parallel_turns,
        "total_spawns": total_spawns,
        "reconciler_present": "hsb-reconciler" in seen,
        "inheritor_fanout_in_turn": inheritor_fanout_in_turn,
        "synthesizer_fanout_in_turn": synthesizer_fanout_in_turn,
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
