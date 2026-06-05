#!/usr/bin/env python3
"""Self-tests for pipeline_graph.validate — assert each invariant actually fires.

Run: python3 tools/test_pipeline_graph.py   (exit 0 = all pass)
Also validates every shipped skills/*/pipeline*.yaml as a smoke test.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pipeline_graph as pg  # noqa: E402

HERE = Path(__file__).parent
SKILLS = HERE.parent / "skills"


def expect(name: str, graph: dict, code: str | None):
    """code=None means the graph must be valid; otherwise that code must appear."""
    errors = pg.validate(graph)
    codes = " ".join(errors)
    if code is None:
        assert not errors, f"{name}: expected VALID, got: {codes}"
    else:
        assert code in codes, f"{name}: expected '{code}', got: {codes or '(none)'}"
    print(f"  ok  {name}")


def base() -> dict:
    """A minimal valid graph."""
    return {
        "external_inputs": ["template"],
        "section_datums": ["sec-a"],
        "file_writers": {"doc.md": "writer"},
        "nodes": {
            "validator": {"reads": ["template"], "decides": ["valid"]},
            "drafter": {"reads": ["valid"], "decides": ["sec-a"]},
            "writer": {"reads": ["sec-a"], "decides": ["doc"], "persists": "doc.md"},
        },
        "reconciliations": [],
    }


def main() -> int:
    print("invariant tests:")
    expect("valid baseline", base(), None)

    # 1. single physical writer: owner doesn't declare persists
    g = base(); g["nodes"]["drafter"]["persists"] = None
    g["file_writers"]["extra.md"] = "drafter"
    expect("single-writer (missing persists)", g, "[single-writer]")

    # 2. single logical decider: two nodes decide the same datum
    g = base(); g["nodes"]["writer"]["decides"] = ["doc", "sec-a"]
    expect("single-decider (two deciders)", g, "[single-decider]")

    # 3. dangling read
    g = base(); g["nodes"]["drafter"]["reads"] = ["nope"]
    expect("dangling-read", g, "[dangling-read]")

    # 4. cycle
    g = base()
    g["nodes"]["drafter"]["reads"] = ["doc"]   # drafter <- doc (writer) <- sec-a (drafter)
    expect("cycle", g, "[cycle]")

    # 5. provisional without a reconciliation
    g = base()
    g["nodes"]["drafter"]["provisional_on"] = ["valid"]
    expect("unreconciled-provisional", g, "[unreconciled-provisional]")

    # 5b. provisional WITH a reconciliation -> valid
    g = base()
    g["nodes"]["drafter"]["provisional_on"] = ["valid"]
    g["reconciliations"] = [{"when": "valid == X", "redisposition": ["sec-a"],
                             "to": "decided", "via": "writer"}]
    expect("provisional + reconciliation (valid)", g, None)

    print("\nshipped graphs:")
    graphs = sorted(SKILLS.glob("*/pipeline*.yaml"))
    assert graphs, "no shipped pipeline graphs found"
    for gp in graphs:
        errors = pg.validate(pg.load(gp))
        assert not errors, f"{gp} invalid: {errors}"
        print(f"  ok  {gp.relative_to(SKILLS)}")

    print("\nall tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
