#!/usr/bin/env python3
"""Build a benchmark.json for the eval-viewer's Benchmark tab from a workspace.

Scans <workspace>/eval-<id>/<config>/{grading.json,eval_metadata.json} (configs:
with_skill, baseline) and aggregates pass rates into the shape the viewer expects:
{metadata, run_summary:{with_skill,baseline,delta}, runs:[...], notes:[...]}.

Usage: python3 make_benchmark.py <workspace> [--skill NAME] [--evals evals.json]
Prints JSON to stdout. Emits nothing (exit 1) if no graded runs are found.
"""
import json, sys, glob, os, statistics, datetime

CONFIGS = ["with_skill", "baseline"]  # order defines column order in the viewer


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def main():
    args = sys.argv[1:]
    skill = "intake-brainstorm"
    evals_path = "evals.json"
    if "--skill" in args:
        i = args.index("--skill"); skill = args[i + 1]; del args[i:i + 2]
    if "--evals" in args:
        i = args.index("--evals"); evals_path = args[i + 1]; del args[i:i + 2]
    if not args:
        print("usage: make_benchmark.py <workspace> [--skill NAME] [--evals evals.json]", file=sys.stderr)
        sys.exit(2)
    ws = args[0]

    names = {}
    ev = load(evals_path)
    if ev:
        for e in ev.get("evals", []):
            names[e["id"]] = e.get("name", f"eval-{e['id']}")

    runs = []
    rates = {c: [] for c in CONFIGS}
    eval_ids = set()
    for cfg in CONFIGS:
        for grading_path in sorted(glob.glob(os.path.join(ws, "eval-*", cfg, "grading.json"))):
            run_dir = os.path.dirname(grading_path)
            grading = load(grading_path) or {}
            summary = grading.get("summary", {})
            meta = load(os.path.join(run_dir, "eval_metadata.json")) or {}
            eid = meta.get("eval_id")
            if eid is None:  # derive from .../eval-<id>/<cfg>/
                base = os.path.basename(os.path.dirname(run_dir))
                eid = int(base.split("-")[-1]) if base.split("-")[-1].isdigit() else base
            if isinstance(eid, int):
                eval_ids.add(eid)
            pr = summary.get("pass_rate", 0)
            rates[cfg].append(pr)
            runs.append({
                "eval_id": eid,
                "eval_name": names.get(eid, f"eval-{eid}"),
                "configuration": cfg,
                "run_number": 1,
                "result": {
                    "pass_rate": pr,
                    "passed": summary.get("passed", 0),
                    "total": summary.get("total", 0),
                },
                "expectations": grading.get("expectations", []),
            })

    if not runs:
        sys.exit(1)

    def stat(vals):
        return {"mean": statistics.mean(vals) if vals else 0,
                "stddev": statistics.pstdev(vals) if len(vals) > 1 else 0}

    run_summary = {c: {"pass_rate": stat(rates[c])} for c in CONFIGS}
    d = run_summary["with_skill"]["pass_rate"]["mean"] - run_summary["baseline"]["pass_rate"]["mean"]
    run_summary["delta"] = {"pass_rate": f"{'+' if d >= 0 else ''}{round(d * 100)}%"}

    out = {
        "metadata": {
            "skill_name": skill,
            "timestamp": datetime.date.today().isoformat(),
            "evals_run": sorted(i for i in eval_ids if isinstance(i, int)),
            "runs_per_configuration": 1,
        },
        "run_summary": run_summary,
        "runs": runs,
        "notes": [
            "Pass rate = fraction of structural assertions (assertions.py) satisfied per run.",
            "with_skill runs the hsb-teamwork:intake-brainstorm skill; baseline runs the same prompt with no skill.",
            "One run per configuration (stddev = 0); raise runs_per_configuration for variance.",
        ],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
