#!/usr/bin/env python3
"""Validate and schedule a declarative hsb-teamwork pipeline graph.

A pipeline.yaml declares the agents (nodes), the logical datums each one reads and
decides, the physical file each writer owns, the provisional (draft-before-it-exists)
edges, and the reconciliation rules that settle them. This tool turns that declaration
into machine-checked invariants and a computed schedule, so ordering and conflict-safety
stop being prose the orchestrator has to get right by hand.

Invariants enforced (any failure exits non-zero):
  1. single physical writer   — each file in `file_writers` has exactly one owner, and
                                 that owner node declares `persists:` it.
  2. single logical decider    — each datum is decided by exactly one node. (A datum
                                 decided by two nodes is the override class: it would
                                 have caught the readiness quadruplication and the
                                 derived-section dual-author.)
  3. no dangling reads         — every datum read is decided somewhere, is an external
                                 input, or is a section datum.
  4. acyclic on hard edges     — `reads` edges (not `provisional_on`) form a DAG.
  5. provisional ⇒ reconciled  — every `provisional_on` edge has a matching
                                 `reconciliations` rule. This mechanically enforces the
                                 "effort/ADRs drafted before the verdict" fix.

Usage:
  pipeline_graph.py PIPELINE.yaml            # validate; print the schedule
  pipeline_graph.py PIPELINE.yaml --mermaid  # also emit a Mermaid diagram
  pipeline_graph.py PIPELINE.yaml --quiet     # validate only (CI); print nothing on pass
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pipeline_graph.py needs PyYAML (pip install pyyaml)")


class GraphError(Exception):
    pass


def load(path: Path) -> dict:
    with path.open() as fh:
        return yaml.safe_load(fh)


def reads_of(node: dict, sections: list[str]) -> list[str]:
    """Explicit reads plus the expansion of `reads_all_sections`."""
    reads = list(node.get("reads", []) or [])
    if node.get("reads_all_sections"):
        reads += [s for s in sections if s not in reads]
    return reads


def validate(g: dict) -> list[str]:
    """Return the list of invariant violations (empty = valid)."""
    errors: list[str] = []
    nodes: dict[str, dict] = g.get("nodes", {}) or {}
    externals = set(g.get("external_inputs", []) or [])
    sections = list(g.get("section_datums", []) or [])
    file_writers: dict[str, str] = g.get("file_writers", {}) or {}
    reconciliations = g.get("reconciliations", []) or []

    # --- 2. single logical decider ------------------------------------------------
    decided_by: dict[str, list[str]] = {}
    for name, node in nodes.items():
        for datum in node.get("decides", []) or []:
            decided_by.setdefault(datum, []).append(name)
    for datum, deciders in sorted(decided_by.items()):
        if len(deciders) > 1:
            errors.append(
                f"[single-decider] datum '{datum}' is decided by {len(deciders)} nodes: "
                f"{', '.join(sorted(deciders))} (exactly one allowed)"
            )
    decided = set(decided_by)

    # --- 1. single physical writer ------------------------------------------------
    for f, owner in sorted(file_writers.items()):
        if owner not in nodes:
            errors.append(f"[single-writer] file '{f}' owned by unknown node '{owner}'")
            continue
        if nodes[owner].get("persists") != f:
            errors.append(
                f"[single-writer] file '{f}' lists owner '{owner}', but that node does "
                f"not declare `persists: {f}`"
            )
    for name, node in nodes.items():
        pf = node.get("persists")
        if pf and file_writers.get(pf) != name:
            errors.append(
                f"[single-writer] node '{name}' persists '{pf}' but file_writers does "
                f"not name it the owner"
            )

    # --- 3. no dangling reads -----------------------------------------------------
    known = decided | externals | set(sections)
    for name, node in nodes.items():
        for datum in reads_of(node, sections):
            if datum not in known:
                errors.append(
                    f"[dangling-read] node '{name}' reads '{datum}', which no node "
                    f"decides and which is not an external input"
                )

    # --- 4. acyclic on hard edges -------------------------------------------------
    # Edge producer(datum) -> consumer for every hard read.
    adj: dict[str, set[str]] = {n: set() for n in nodes}
    indeg: dict[str, int] = {n: 0 for n in nodes}
    for name, node in nodes.items():
        for datum in reads_of(node, sections):
            for producer in decided_by.get(datum, []):
                if name not in adj[producer]:
                    adj[producer].add(name)
                    indeg[name] += 1
    order, queue = [], sorted([n for n, d in indeg.items() if d == 0])
    indeg_work = dict(indeg)
    while queue:
        n = queue.pop(0)
        order.append(n)
        for m in sorted(adj[n]):
            indeg_work[m] -= 1
            if indeg_work[m] == 0:
                queue.append(m)
        queue.sort()
    if len(order) != len(nodes):
        stuck = sorted(set(nodes) - set(order))
        errors.append(f"[cycle] hard `reads` edges form a cycle among: {', '.join(stuck)}")

    # --- 5. provisional ⇒ reconciled ---------------------------------------------
    for name, node in nodes.items():
        for dep in node.get("provisional_on", []) or []:
            outputs = set(node.get("decides", []) or [])
            covered = any(
                dep in str(r.get("when", ""))
                and outputs & set(r.get("redisposition", []) or [])
                for r in reconciliations
            )
            if not covered:
                errors.append(
                    f"[unreconciled-provisional] node '{name}' is provisional_on "
                    f"'{dep}' but no reconciliation rule re-dispositions its output "
                    f"when '{dep}' resolves"
                )

    return errors


def schedule(g: dict) -> list[list[str]]:
    """Greedy level-order schedule on hard edges: each level runs in parallel."""
    nodes = g.get("nodes", {}) or {}
    sections = list(g.get("section_datums", []) or [])
    decided_by: dict[str, list[str]] = {}
    for name, node in nodes.items():
        for datum in node.get("decides", []) or []:
            decided_by.setdefault(datum, []).append(name)

    indeg = {n: 0 for n in nodes}
    deps: dict[str, set[str]] = {n: set() for n in nodes}
    for name, node in nodes.items():
        for datum in reads_of(node, sections):
            for producer in decided_by.get(datum, []):
                if producer not in deps[name]:
                    deps[name].add(producer)
    indeg = {n: len(deps[n]) for n in nodes}

    levels, placed = [], set()
    while len(placed) < len(nodes):
        ready = sorted(n for n in nodes if n not in placed and deps[n] <= placed)
        if not ready:
            break  # cycle; validate() reports it
        levels.append(ready)
        placed |= set(ready)
    return levels


def fmt_schedule(g: dict) -> str:
    nodes = g.get("nodes", {}) or {}
    provisional = {n for n, nd in nodes.items() if nd.get("provisional_on")}
    out = ["Computed schedule (each batch runs in parallel; batches run in order):", ""]
    for i, batch in enumerate(schedule(g), 1):
        out.append(f"  batch {i}:")
        for n in batch:
            tags = []
            if nodes[n].get("governs"):
                tags.append("GOVERNS")
            if nodes[n].get("fanout"):
                tags.append(f"fanout:{nodes[n]['fanout']}")
            if n in provisional:
                tags.append(f"PROVISIONAL on {','.join(nodes[n]['provisional_on'])}")
            suffix = f"   [{'; '.join(tags)}]" if tags else ""
            out.append(f"    - {n}{suffix}")
    recon = g.get("reconciliations", []) or []
    if recon:
        out += ["", "Reconciliations (fire when a provisional datum resolves):"]
        for r in recon:
            out.append(
                f"    - when {r['when']} -> re-dispose {', '.join(r['redisposition'])} "
                f"to '{r['to']}' via {r['via']}"
            )
    return "\n".join(out)


def mermaid(g: dict) -> str:
    nodes = g.get("nodes", {}) or {}
    sections = list(g.get("section_datums", []) or [])
    decided_by: dict[str, list[str]] = {}
    for name, node in nodes.items():
        for datum in node.get("decides", []) or []:
            decided_by.setdefault(datum, []).append(name)

    def nid(n: str) -> str:
        return n.replace("-", "_")

    lines = ["```mermaid", "flowchart TD"]
    # group by phase
    phases: dict[str, list[str]] = {}
    for name, node in nodes.items():
        phases.setdefault(node.get("phase", "other"), []).append(name)
    for phase, members in phases.items():
        lines.append(f"  subgraph {phase}")
        for n in sorted(members):
            lines.append(f"    {nid(n)}[{n}]")
        lines.append("  end")
    # hard edges
    seen = set()
    for name, node in nodes.items():
        for datum in reads_of(node, sections):
            for producer in decided_by.get(datum, []):
                key = (producer, name)
                if key not in seen:
                    seen.add(key)
                    lines.append(f"  {nid(producer)} --> {nid(name)}")
    # provisional (soft) edges, dashed
    for name, node in nodes.items():
        for dep in node.get("provisional_on", []) or []:
            for producer in decided_by.get(dep, []):
                lines.append(f"  {nid(producer)} -.provisional.-> {nid(name)}")
    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pipeline", type=Path)
    ap.add_argument("--mermaid", action="store_true", help="emit a Mermaid diagram")
    ap.add_argument("--quiet", action="store_true", help="print nothing on success (CI)")
    args = ap.parse_args()

    g = load(args.pipeline)
    errors = validate(g)
    if errors:
        print(f"INVALID: {args.pipeline} ({len(errors)} violation(s))", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"VALID: {args.pipeline}")
        print(f"  nodes: {len(g.get('nodes', {}))}  "
              f"datums decided: {sum(len(n.get('decides', []) or []) for n in g['nodes'].values())}  "
              f"files: {len(g.get('file_writers', {}))}")
        print()
        print(fmt_schedule(g))
        if args.mermaid:
            print()
            print(mermaid(g))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
