#!/usr/bin/env python3
"""Agnostic, config-driven structural grader for a *single agent* run.

This is the per-agent analogue of the skill-level `assertions.py`. Where that grades
a finished target-document, this grades **what one agent returned** when invoked in
isolation — the structured proposal/verdict it wrote to its return file (and, for the
single-writer boundary, which files it touched).

It is agnostic: the checks for a case are declared as a list of `assertions` in the
agent's `agent.json`, and this module is just a registry of assertion *types*. Adding
a new agent means writing fixtures + a few declared assertions, not new Python.

Assertion types (see each agent's agent.json):
  output_parses      the return file is present and valid (JSON, or non-empty text)
  required_fields    every item under <path> carries <fields>
  enum_field         <path>[].<field> is within <allowed>
  must_answer        a proposal for each of <question_ids> exists with a disposition in <allowed>
  no_fabrication     FAITHFULNESS: none of <question_ids> got a disposition in <forbidden>
                     (the agent did not invent an answer the sources don't support)
  grounded_source    FAITHFULNESS: every <disposition> proposal cites a source that
                     actually exists in the phase's sources (id/filename in sources-index)
  readonly_boundary  the read-only agent mutated no fixture file (only its return file)

Emits the eval-viewer's grading.json shape via --grading-json, like assertions.py.

Usage:
  grade.py <agent.json> <case_id> <return_file> [--phase-dir DIR]
           [--snapshot-before f.json --snapshot-after f.json] [--grading-json out]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agentlib  # noqa: E402


# --- return-file readers ------------------------------------------------------
def load_return(path):
    """Return (parsed, raw, kind). kind is 'json' | 'text' | 'missing'."""
    if not path or not os.path.isfile(path):
        return None, "", "missing"
    raw = open(path, encoding="utf-8").read()
    try:
        return json.loads(raw), raw, "json"
    except json.JSONDecodeError:
        return None, raw, "text"


def items_at(parsed, path):
    """Resolve a dotted list path like 'proposals' -> the list (or [])."""
    cur = parsed
    for part in (path or "").split(".") if path else []:
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return []
    return cur if isinstance(cur, list) else []


def find_proposals(parsed, qids):
    """Map question_id -> proposal dict, for the ids of interest (proposals list)."""
    out = {}
    for p in items_at(parsed, "proposals"):
        if isinstance(p, dict):
            qid = str(p.get("question_id", ""))
            if qid in qids:
                out[qid] = p
    return out


# --- assertion registry -------------------------------------------------------
def check(a, ctx):
    """Return (label, ok, evidence) for one declared assertion `a`."""
    t = a["type"]
    parsed, raw, kind = ctx["return"]

    if t == "output_parses":
        if kind == "missing":
            return ("output_parses", False, "no return file produced")
        if kind == "text":
            return ("output_parses", bool(raw.strip()), "non-empty text return" if raw.strip() else "empty")
        return ("output_parses", True, "valid JSON return")

    if t == "required_fields":
        path, fields = a["path"], a["fields"]
        bad = []
        for i, it in enumerate(items_at(parsed, path)):
            miss = [f for f in fields if not (isinstance(it, dict) and it.get(f) not in (None, ""))]
            if miss:
                bad.append(f"{path}[{i}] missing {miss}")
        return (f"required_fields:{path}", not bad,
                "all carry " + ",".join(fields) if not bad else "; ".join(bad))

    if t == "enum_field":
        path, field, allowed = a["path"], a["field"], set(a["allowed"])
        bad = [str(it.get(field)) for it in items_at(parsed, path)
               if isinstance(it, dict) and it.get(field) not in allowed]
        return (f"enum_field:{path}.{field}", not bad,
                f"all in {sorted(allowed)}" if not bad else f"out-of-enum: {bad}")

    if t == "must_answer":
        qids, allowed = set(map(str, a["question_ids"])), set(a["allowed"])
        found = find_proposals(parsed, qids)
        missing = [q for q in qids if q not in found or found[q].get("disposition") not in allowed]
        return ("must_answer:" + ",".join(sorted(qids)), not missing,
                f"answered {sorted(found)} (need disp∈{sorted(allowed)})"
                if not missing else f"not answered as required: {missing}")

    if t == "no_fabrication":  # FAITHFULNESS
        qids, forbidden = set(map(str, a["question_ids"])), set(a["forbidden"])
        found = find_proposals(parsed, qids)
        fabricated = [q for q, p in found.items() if p.get("disposition") in forbidden]
        return ("no_fabrication:" + ",".join(sorted(qids)), not fabricated,
                "no fabricated answer for unsupported question(s)"
                if not fabricated else f"FABRICATED (disp∈{sorted(forbidden)}) for: {fabricated}")

    if t == "grounded_source":  # FAITHFULNESS
        disp = a.get("disposition", "inferred")
        toks = ctx["source_tokens"]
        bad = []
        for p in items_at(parsed, "proposals"):
            if not isinstance(p, dict) or p.get("disposition") != disp:
                continue
            src = str(p.get("source", ""))
            if not toks:  # nothing to ground against (no sources fixture) -> can't fail it here
                continue
            if not any(tok in src for tok in toks):
                bad.append(f"{p.get('question_id')}: source={src!r} not in {sorted(toks)}")
        return (f"grounded_source:{disp}", not bad,
                "every cited source exists in the phase sources"
                if not bad else "; ".join(bad))

    if t == "readonly_boundary":
        before, after = ctx.get("snap_before"), ctx.get("snap_after")
        if before is None or after is None:
            return ("readonly_boundary", True, "skipped (no file snapshots — self-test)")
        allow = set(ctx.get("return_basenames", []))
        changed = [f for f in set(before) | set(after)
                   if before.get(f) != after.get(f) and os.path.basename(f) not in allow]
        return ("readonly_boundary", not changed,
                "no shared/fixture file mutated" if not changed else f"mutated: {changed}")

    return (f"unknown:{t}", False, "unknown assertion type")


def grade(agent_json, case_id, return_file, phase_dir=None,
          snap_before=None, snap_after=None):
    cfg = json.load(open(agent_json, encoding="utf-8"))
    case = next((c for c in cfg["cases"] if str(c["id"]) == str(case_id)), None)
    if case is None:
        raise SystemExit(f"no case {case_id} in {agent_json}")

    ctx = {
        "return": load_return(return_file),
        "source_tokens": agentlib.sources_tokens(phase_dir) if phase_dir else set(),
        "snap_before": load_snapshot(snap_before),
        "snap_after": load_snapshot(snap_after),
        "return_basenames": [os.path.basename(return_file)] if return_file else [],
    }
    checks = [check(a, ctx) for a in case.get("assertions", [])]
    exps = [{"text": lbl, "passed": ok, "evidence": ev} for lbl, ok, ev in checks]
    passed = sum(1 for e in exps if e["passed"])
    total = len(exps)
    return {
        "agent": cfg.get("agent"),
        "case": case.get("name", case_id),
        "summary": {"pass_rate": (passed / total) if total else 0,
                    "passed": passed, "failed": total - passed, "total": total},
        "expectations": exps,
        "pass": passed == total,
    }


def load_snapshot(path):
    if not path or not os.path.isfile(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--phase-dir", "--snapshot-before", "--snapshot-after", "--grading-json"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1]
            del args[i:i + 2]
    if len(args) != 3:
        print("usage: grade.py <agent.json> <case_id> <return_file> "
              "[--phase-dir D] [--snapshot-before f --snapshot-after f] [--grading-json out]")
        sys.exit(2)
    rep = grade(args[0], args[1], args[2],
                phase_dir=opts.get("--phase-dir"),
                snap_before=opts.get("--snapshot-before"),
                snap_after=opts.get("--snapshot-after"))
    if "--grading-json" in opts:
        with open(opts["--grading-json"], "w", encoding="utf-8") as fh:
            json.dump({"summary": rep["summary"], "expectations": rep["expectations"]},
                      fh, indent=2, ensure_ascii=False)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    sys.exit(0 if rep["pass"] else 1)


if __name__ == "__main__":
    main()
