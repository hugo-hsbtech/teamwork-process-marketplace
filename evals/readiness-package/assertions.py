#!/usr/bin/env python3
"""Deterministic structural grader for a Readiness Package document.

Validates a produced readiness-document.md against the contract encoded in its own
section annotations (<!-- origination: id=...; blocks=...; min-confidence=...; kind=... -->).
No LLM required. Pairs with rubric.md (the qualitative LLM-graded layer).

Usage:  python3 assertions.py <path/to/readiness-document.md>
Exits 0 if all hard checks pass, 1 otherwise. Prints a JSON report.
"""
import re, sys, json

SENTINEL = "<!-- END OF DOCUMENT -->"
ANNOT = re.compile(r"<!--\s*origination:\s*(.*?)\s*-->")
HONEST = {"assumption", "discovery", "deferred"}
ORIGINS = {"inherited", "ai_drafted", "po_authored", "reused_from_kb"}
TRUNC = ["(unchanged)", "[continues]", "remaining sections omitted",
         "[fill]", "[placeholder]", "[Demand name]"]

def parse_annotation(s):
    d = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return d

# RP template uses `##` for every annotated section and `###` only for sub-parts,
# so split on level-2 headings only; sub-headings stay in their parent section body.
HEADING = re.compile(r"^##\s+(.*)")

def split_sections(text):
    lines = text.splitlines()
    secs, cur = [], None
    for ln in lines:
        m = HEADING.match(ln)
        if m:
            if cur: secs.append(cur)
            cur = [m.group(1).strip(), None, []]
        elif cur is not None:
            m = ANNOT.search(ln)
            if m and cur[1] is None:
                cur[1] = parse_annotation(m.group(1))
            cur[2].append(ln)
    if cur: secs.append(cur)
    return [(h, a, "\n".join(b)) for h, a, b in secs]

def conf_line(body):
    c = re.search(r"`?Confidence:`?\s*([0-9]{1,3}|__)", body)
    o = re.search(r"`?Origin:`?\s*([A-Za-z_]+|__)", body)
    disp = re.search(r"`?Disposition:`?\s*([A-Za-z_]+|__)", body)
    conf = c.group(1) if c else None
    return (None if conf in (None, "__") else int(conf)), \
           (o.group(1).lower() if o else None), \
           (disp.group(1).lower() if disp else None)

def grade(path):
    text = open(path, encoding="utf-8").read()
    checks = []
    def add(name, ok, detail=""): checks.append({"check": name, "ok": bool(ok), "detail": detail})

    last = [l for l in text.splitlines() if l.strip()]
    add("sentinel_present", bool(last) and last[-1].strip() == SENTINEL,
        "last line: " + (last[-1].strip() if last else "<empty>"))
    found = [m for m in TRUNC if m in text]
    add("no_truncation_markers", not found, "found: " + ", ".join(found) if found else "clean")

    secs = split_sections(text)
    annotated = [(h, a, b) for h, a, b in secs if a and a.get("id")]
    add("has_annotations", len(annotated) >= 10, f"{len(annotated)} annotated sections")

    blocking = [(h, a, b) for h, a, b in annotated
                if a.get("blocks") == "true" and a.get("kind") == "capture"]
    sat = 0
    for h, a, b in blocking:
        thr = int(a.get("min-confidence", "70"))
        conf, origin, disp = conf_line(b)
        ok = (disp in HONEST) or (conf is not None and conf >= thr)
        if ok: sat += 1
        add(f"blocking[{a['id']}]_satisfied", ok, f"conf={conf} thr={thr} disp={disp}")
    readiness = round(100 * sat / len(blocking)) if blocking else 0

    cap = [(h, a, b) for h, a, b in annotated if a.get("kind") in ("capture", "derived")]
    missing_conf = [a["id"] for h, a, b in cap
                    if a.get("kind") == "capture" and int(a.get("min-confidence", "0")) > 0
                    and "Confidence:" not in b]
    add("confidence_lines_present", not missing_conf,
        "missing on: " + ", ".join(missing_conf) if missing_conf else "all present")

    bad_origin = []
    for h, a, b in blocking:
        _, origin, _ = conf_line(b)
        if origin not in ORIGINS:
            bad_origin.append(f"{a['id']}={origin}")
    add("origin_present_valid", not bad_origin,
        "bad/missing: " + ", ".join(bad_origin) if bad_origin else "all valid")

    taref = [b for h, a, b in annotated if a.get("id") == "tech-assessment-ref"]
    if taref:
        t = taref[0].lower()
        _, _, disp = conf_line(taref[0])
        resolved = (disp in {"deferred", "decided"}) or ("not_requested" in t) \
                   or ("signed" in t) or ("assinado" in t)
        add("tech_assessment_ref_resolved", resolved, f"disposition={disp}")

    ok_all = all(c["ok"] for c in checks)
    return {"file": path, "pass": ok_all, "readiness_pct": readiness,
            "blocking_satisfied": f"{sat}/{len(blocking)}", "checks": checks}

def to_grading(rep):
    """Map the structural report onto the eval-viewer's grading.json shape:
    {summary:{pass_rate,passed,failed,total}, expectations:[{text,passed,evidence}]}.
    The viewer (evals/eval-viewer) renders this as the per-run "Grades" panel."""
    exps = [{"text": c["check"], "passed": c["ok"], "evidence": c["detail"]}
            for c in rep["checks"]]
    passed = sum(1 for e in exps if e["passed"])
    total = len(exps)
    return {
        "summary": {
            "pass_rate": (passed / total) if total else 0,
            "passed": passed,
            "failed": total - passed,
            "total": total,
        },
        "expectations": exps,
    }

if __name__ == "__main__":
    args = sys.argv[1:]
    grading_out = None
    if "--grading-json" in args:
        i = args.index("--grading-json")
        try:
            grading_out = args[i + 1]
        except IndexError:
            print("usage: assertions.py <readiness-document.md> [--grading-json <out.json>]"); sys.exit(2)
        del args[i:i + 2]
    if len(args) != 1:
        print("usage: assertions.py <readiness-document.md> [--grading-json <out.json>]"); sys.exit(2)
    rep = grade(args[0])
    if grading_out:
        with open(grading_out, "w", encoding="utf-8") as fh:
            json.dump(to_grading(rep), fh, indent=2, ensure_ascii=False)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    sys.exit(0 if rep["pass"] else 1)
