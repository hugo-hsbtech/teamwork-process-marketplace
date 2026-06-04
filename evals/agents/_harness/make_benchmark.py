#!/usr/bin/env python3
"""Build benchmark.json (eval-viewer Benchmark tab) for a per-agent workspace.

Scans <workspace>/eval-<id>/<config>/grading.json for configs agent|baseline and
aggregates pass rates into the shape the viewer expects, so the Benchmark tab shows
the **lift** of the agent's role spec over a no-spec baseline. Mirrors
eval-viewer/make_benchmark.py but for the agent harness's config names.

Usage: make_benchmark.py <workspace> [--agent NAME] [--evals agent.json]
Prints JSON to stdout; exits 1 if no graded runs are found.
"""
import datetime
import glob
import json
import os
import statistics
import sys

CONFIGS = ["agent", "baseline"]  # column order in the viewer


def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main():
    args = sys.argv[1:]
    agent = "agent"
    evals_path = None
    if "--agent" in args:
        i = args.index("--agent"); agent = args[i + 1]; del args[i:i + 2]
    if "--evals" in args:
        i = args.index("--evals"); evals_path = args[i + 1]; del args[i:i + 2]
    if not args:
        print("usage: make_benchmark.py <workspace> [--agent NAME] [--evals agent.json]", file=sys.stderr)
        sys.exit(2)
    ws = args[0]

    names = {}
    if evals_path:
        cfg = load(evals_path) or {}
        for c in cfg.get("cases", []):
            names[c["id"]] = c.get("name", f"case-{c['id']}")

    runs, rates, ids = [], {c: [] for c in CONFIGS}, set()
    for cfg in CONFIGS:
        for gp in sorted(glob.glob(os.path.join(ws, "eval-*", cfg, "grading.json"))):
            g = load(gp) or {}
            s = g.get("summary", {})
            base = os.path.basename(os.path.dirname(os.path.dirname(gp)))
            eid = int(base.split("-")[-1]) if base.split("-")[-1].isdigit() else base
            if isinstance(eid, int):
                ids.add(eid)
            pr = s.get("pass_rate", 0)
            rates[cfg].append(pr)
            runs.append({
                "eval_id": eid, "eval_name": names.get(eid, f"case-{eid}"),
                "configuration": cfg, "run_number": 1,
                "result": {"pass_rate": pr, "passed": s.get("passed", 0), "total": s.get("total", 0)},
                "expectations": g.get("expectations", []),
            })
    if not runs:
        sys.exit(1)

    def stat(v):
        return {"mean": statistics.mean(v) if v else 0,
                "stddev": statistics.pstdev(v) if len(v) > 1 else 0}

    rs = {c: {"pass_rate": stat(rates[c])} for c in CONFIGS}
    d = rs["agent"]["pass_rate"]["mean"] - rs["baseline"]["pass_rate"]["mean"]
    # viewer expects a with_skill/baseline pair; map agent->with_skill for the tab.
    rs["with_skill"] = rs.pop("agent")
    for r in runs:
        if r["configuration"] == "agent":
            r["configuration"] = "with_skill"
    rs["delta"] = {"pass_rate": f"{'+' if d >= 0 else ''}{round(d * 100)}%"}

    print(json.dumps({
        "metadata": {"skill_name": agent, "timestamp": datetime.date.today().isoformat(),
                     "evals_run": sorted(i for i in ids if isinstance(i, int)),
                     "runs_per_configuration": 1},
        "run_summary": rs, "runs": runs,
        "notes": [
            "Pass rate = fraction of structural assertions (grade.py) satisfied per run.",
            f"'with_skill' = the {agent} role spec injected; 'baseline' = same task, no spec.",
            "One run per configuration (stddev = 0); raise runs for variance.",
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
