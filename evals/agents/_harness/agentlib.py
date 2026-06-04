#!/usr/bin/env python3
"""Agnostic helpers for the per-agent eval harness.

The harness is *agnostic*: instead of hardcoding each agent's contract, it derives
what it can from the agent's own declaration. This module is the single place that
reads an agent spec (`plugins/hsb-teamwork/agents/<name>.md`) and the run's fixtures,
so `grade.py` and `run_agent.sh` stay generic.

Two things are derived from the agent's own frontmatter (no per-agent config needed):
  - the **role prompt** (the markdown body) the runner injects to invoke the agent
    in isolation, and
  - whether the agent is **read-only** (its `tools:` list has no Write/Edit) — which
    is exactly the single-writer boundary the orchestration contract guarantees.

Plus a small reader for a phase's `sources-index.md`, used by the faithfulness
("grounded source") check to confirm a cited source actually exists.
"""
import os
import re

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}


def parse_agent_spec(path):
    """Read an agent .md: return {name, description, tools:[...], model, body, is_readonly}.

    `body` is the markdown after the frontmatter — the agent's role prompt, which the
    runner injects so the agent can be invoked standalone. `is_readonly` is True when
    the declared tools include no writing tool (the contract's read-only proposers).
    """
    text = open(path, encoding="utf-8").read()
    fm, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
    return {
        "name": fm.get("name", os.path.splitext(os.path.basename(path))[0]),
        "description": fm.get("description", ""),
        "tools": tools,
        "model": fm.get("model", ""),
        "body": body.strip(),
        "is_readonly": bool(tools) and not (set(tools) & WRITE_TOOLS),
    }


def sources_tokens(phase_dir):
    """Return the set of tokens that count as a real, citable source for grounding:
    the ids and filenames listed in `sources-index.md`, plus the actual filenames
    under `sources/`. A faithful `inferred` proposal must cite one of these.
    """
    tokens = set()
    idx = os.path.join(phase_dir, "sources-index.md")
    if os.path.isfile(idx):
        for line in open(idx, encoding="utf-8"):
            # table rows: `| S1 | brief.md | ... |` — harvest id-ish and file-ish cells
            for cell in (c.strip() for c in line.split("|")):
                if re.fullmatch(r"[A-Za-z]{1,4}\d{1,3}", cell):     # an id like S1, SRC12
                    tokens.add(cell)
                if re.search(r"\.\w{1,5}$", cell) and " " not in cell:  # a filename
                    tokens.add(cell)
                    tokens.add(os.path.splitext(cell)[0])
    src = os.path.join(phase_dir, "sources")
    if os.path.isdir(src):
        for fn in os.listdir(src):
            tokens.add(fn)
            tokens.add(os.path.splitext(fn)[0])
    return {t for t in tokens if t}


if __name__ == "__main__":  # tiny self-describe for debugging
    import json
    import sys
    if len(sys.argv) == 2:
        print(json.dumps(parse_agent_spec(sys.argv[1]), indent=2, ensure_ascii=False))
